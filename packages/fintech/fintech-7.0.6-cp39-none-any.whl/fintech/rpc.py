#  Fintech RPC-Service
#
#  Copyright (c) 2014 joonis new media
#  Author: Thimo Kraemer <thimo.kraemer@joonis.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02110-1301, USA.

import datetime
import inspect
import logging
import ssl
import uuid
from argparse import ArgumentParser, ArgumentError, _AppendAction
from base64 import b64decode
from configparser import ConfigParser
from decimal import Decimal
from functools import partial
from hashlib import sha1, sha256
from threading import Lock
from xmlrpc.client import Marshaller, WRAPPERS
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
from socketserver import ThreadingMixIn  # , ForkingMixIn

import fintech

fintech._imported = False

logger = logging.getLogger('fintech.rpc')

##############################################################################
# Some patches of XML-RPC Marshaller

# Add date type dispatcher to the marshaller.
def _dump_date(self, value, write):
    value = (value.year, value.month, value.day, 0, 0, 0)
    self.dump_datetime(value, write)
Marshaller.dispatch[datetime.date] = _dump_date

# Add decimal type dispatcher to the marshaller.
def _dump_decimal(self, value, write):
    self.dump_double(float(value), write)
Marshaller.dispatch[Decimal] = _dump_decimal
    
# Return an empty string for None if allow_none is not set.
def _dump_nil(self, value, write):
    if self.allow_none:
        self.dump_nil(value, write)
    else:
        self.dump_unicode('', write)
Marshaller.dispatch[type(None)] = _dump_nil

# Modify the dispatcher for instances not to return attributes
# starting with an underscore.
def _dump_instance(self, value, write):
    # check for special wrappers
    if value.__class__ in WRAPPERS:
        # fallback to default behaviour
        self.dump_instance(value, write)
    else:
        # store instance attributes as a struct
        d = {}
        for name in dir(value):
            if name.startswith('_'):
                continue
            try:
                attr = getattr(value, name)
            except AttributeError:
                attr = None
            if not callable(attr):
                d[name] = attr
        self.dump_struct(d, write)

if '_arbitrary_instance' in Marshaller.dispatch:
    Marshaller.dispatch['_arbitrary_instance'] = _dump_instance
else:
    raise RuntimeError("don't know how to set instance dispatcher")

# fintech.sepa.Amount dispatcher
def _dump_amount(self, value, write):
    d = {'value': value.value, 'currency': value.currency}
    self.dump_struct(d, write)

##############################################################################


class AuthRequestHandler(SimpleXMLRPCRequestHandler):
    """SimpleXMLRPCRequestHandler with support for HTTPAuth"""
    
    def _dispatch(self, method, params):
        # Add user to params for kind of session handling.
        return self.server._dispatch(method, (self._user, params))
    
    def parse_request(self):
        self._user = None
        if not super().parse_request():
            return False
        # Check ip address
        ip_address = self.address_string()
        allowed_ips = self.server._allowed_ips
        if allowed_ips and ip_address not in allowed_ips:
            self.send_error(403, 'Forbidden')
            return False
        # Get user
        auth = self.headers.get('Authorization', '')
        auth_type, sep, auth_data = auth.partition(' ')
        if auth_type == 'Basic':
            user, sep, password = b64decode(auth_data).partition(b':')
            self._user = user.decode()
        # Check user
        if self.server._users:
            if not self._user:
                self.send_error(401, 'Basic authentication required')
                return False
            hash = self.server._users.get(self._user, '')
            if len(hash) == 40:
                # SHA1 for backwards compatibility
                pwd_hash = sha1(password).hexdigest()
                logger.warning(
                    'sha1 password hash for user "%s" '
                    'should be changed to sha256 hash'
                    % self._user)
            else:
                # SHA256
                pwd_hash = sha256(password).hexdigest()
            if not hash or hash.lower() != pwd_hash:
                self.send_error(401, 'Unknown user or invalid password')
                return False
        return True
    
    def log_message(self, format, *args):
        logger.info('request from %s %s %s',
                    self.address_string(),
                    self._user or '-', format % args)


class SecureXMLRPCServer(SimpleXMLRPCServer):
    """SimpleXMLRPCServer with support for SSL and HTTPAuth"""
    
    def __init__(self, addr, requestHandler=AuthRequestHandler,
                 logRequests=True, allow_none=False, encoding=None,
                 bind_and_activate=True, use_builtin_types=False,
                 users=None, allowed_ips=None, ssl_files=None):
        
        super().__init__(addr, requestHandler, logRequests, allow_none,
                         encoding, bind_and_activate=False,
                         use_builtin_types=use_builtin_types)
        self._users = users
        self._allowed_ips = allowed_ips
        if ssl_files:
            self.socket = ssl.wrap_socket(self.socket, ssl_files['key'],
                                          ssl_files['cert'], server_side=True,
                                          ssl_version=ssl.PROTOCOL_SSLv23)
        if bind_and_activate:
            self.server_bind()
            self.server_activate()


class ThreadedXMLRPCServer(ThreadingMixIn, SecureXMLRPCServer):
    """Multithreaded SecureXMLRPCServer"""
    pass


class FintechRPCService:
    """The fintech XML-RPC Service"""
    
    _NO_ARGS = []

    def __init__(self):
        self._modules = import_fintech()
        self._cache = {}
        self._lock = Lock()
    
    def _add_object(self, user, obj):
        """Add an object to the object table and return its id"""
        if not hasattr(obj, '_rpc_lock'):
            obj._rpc_lock = Lock()
        # Create a unique object id
        oid = '%s_%x_%s' % (obj.__class__.__name__, id(obj), uuid.uuid4().hex)
        objects = self._cache.setdefault(user, {})
        objects[oid] = obj
        return oid
    
    def purge(self, _user, oid=None):
        """Remove objects from the object table"""
        self._lock.acquire()
        count = 0
        try:
            if _user in self._cache:
                if oid:
                    # Just remove the specified objects
                    if isinstance(oid, str):
                        oid = [oid]
                    for id in oid:
                        try:
                            del self._cache[_user][id]
                        except KeyError:
                            continue
                        else:
                            count = count + 1
                else:
                    # Remove all objects of current user
                    count = len(self._cache[_user])
                    del self._cache[_user]
        finally:
            self._lock.release()
        logger.debug('removed %i objects from object table', count)
        return count

    def has_object(self, _user, oid):
        """Check if *oid* is an existing object id"""
        return oid in self._cache.get(_user, {})
    
    def version(self):
        """Return the version of the fintech package"""
        return fintech.__version__
    
    def echo(self, *args):
        """Just an echo method for testing purposes"""
        return args

    def _detect_object(self, kwargs):
        """Detect object from dictionary"""
        # Account
        # TODO: find a better way to identify an account structure
        if 'iban' in kwargs and 'name' in kwargs:
            cid = kwargs.pop('creditor_id', None)
            cuc = kwargs.pop('cbi_unique_code', None)
            mandate = kwargs.pop('mandate', None)
            uname = kwargs.pop('ultimate_name', None)
            account = sepa.Account(**kwargs)
            if cid or cuc:
                account.set_originator_id(cid, cuc)
            if mandate:
                mandate = self._prepare_args(mandate)
                account.set_mandate(**mandate)
            if uname:
                account.set_ultimate_name(uname)
            return account
        
        # BusinessTransactionFormat
        if 'service' in kwargs and 'msg_name' in kwargs:
            return ebics.BusinessTransactionFormat(**kwargs)
    
    def _prepare_args(self, value, user=None):
        """Convert type of arguments for further usage"""
        if isinstance(value, dict):
            obj = self._detect_object(value)
            if obj:
                return obj
            for k, v in value.items():
                value[k] = self._prepare_args(v, user)
        elif isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = self._prepare_args(v, user)
        elif isinstance(value, str) and value in self._cache.get(user, {}):
            value = self._cache[user][value]
        return value
    
    def _apply(self, obj, method, args, user=None):
        """Call a method of the specified object"""
        # Not all objects are thread-safe, so we have to block
        # simultaneous execution of the same object.
        lock = getattr(obj, '_rpc_lock', None)
        if lock:
            lock.acquire()
        try:
            attr = getattr(obj, method)
            if method.startswith('_'):
                raise Exception('method "%s" not supported' % method)
            if callable(attr):
                # Callable
                if obj != self:
                    args = self._prepare_args(args, user)
                elif '_user' in inspect.getargspec(attr).args:
                    attr = partial(attr, user)
                if isinstance(args, dict):
                    # structures are mapped by name
                    retval = attr(**args)
                elif isinstance(args, list):
                    # arrays are mapped by position
                    retval = attr(*args)
                else:
                    # single values are passed as first argument
                    retval = attr(args)
            elif args is self._NO_ARGS:
                # Get property
                retval = attr
            else:
                # Set property
                args = self._prepare_args(args, user)
                setattr(obj, method, args)
                retval = None
        finally:
            if lock:
                lock.release()
        return retval
    
    def _dispatch(self, method, params):
        """Main dispatch function called on each request"""
        try:
            # Extract the user that was added by AuthRequestHandler
            user, params = params
            user = user or ''
            logger.info('called method: %s', method)
            logger.debug('params: %s', params)
            # Deny access to methods starting with an underscore
            if method.startswith('_') or '._' in method:
                raise Exception('method "%s" not supported' % method)
            methods = method.split('.')
            root = methods.pop(0)
            if methods:
                obj = self._modules.get(root) or \
                    self._cache.get(user, {}).get(root)
                if obj is None:
                    raise Exception('module or object "%s" not found' % root)
                if len(params) > len(methods):
                    raise Exception('too many parameters')
                # Apply each method on the parent object
                for i, method in enumerate(methods):
                    try:
                        args = params[i]
                    except IndexError:
                        args = self._NO_ARGS
                    obj = self._apply(obj, method, args, user)
            else:
                obj = self._apply(self, root, list(params), user)
            if type(obj) in Marshaller.dispatch:
                return obj
            return self._add_object(user, obj)
        
        except Exception as err:
            logger.exception(str(err))
            raise


def import_fintech(reg_data=None):
    if not fintech._imported:
        if reg_data:
            fintech.register(*reg_data)
        global ebics, sepa, iban, swift, datev
        from fintech import ebics, sepa, iban, swift, datev
        fintech._imported = True
        Marshaller.dispatch[sepa.Amount] = _dump_amount
        Marshaller.dispatch[sepa.SEPATransaction] = _dump_instance
    return {
        'ebics': ebics,
        'sepa': sepa,
        'iban': iban,
        'swift': swift,
        'datev': datev,
    }

def run(address='localhost', port=8830, threaded=False,
        users=None, allowed_ips=None, ssl_files=None):
    # Create server
    if threaded:
        XMLRPCServer = ThreadedXMLRPCServer
    else:
        XMLRPCServer = SecureXMLRPCServer
    server = XMLRPCServer((address, port), allow_none=True,
                          use_builtin_types=True, users=users,
                          allowed_ips=allowed_ips, ssl_files=ssl_files)
    server.register_introspection_functions()
    server.register_multicall_functions()
    server.register_instance(FintechRPCService())
    # Run the server's main loop
    logger.info('listen on %s, port %i (SSL %s)', address,
                port, ssl_files and 'enabled' or 'disabled')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('quit')


class LoadConfigAction(_AppendAction):
    """Action loading configuration files"""
    
    def __call__(self, parser, namespace, values, option_string=None):
        super().__call__(parser, namespace, values, option_string)
        cfg = ConfigParser()
        if not cfg.read(values):
            raise ArgumentError(self, "file '%s' not found" % values)
        actions = parser._registries['action']
        for section in cfg.sections():
            prefix = '-'.join(section.lower().split()) + '-'
            if prefix == 'main-':
                prefix = ''
            for option in cfg.options(section):
                arg = '--' + prefix + '-'.join(option.lower().split())
                action = parser._option_string_actions.get(arg)
                if action:
                    if isinstance(action, (actions['store_true'], actions['store_false'])) \
                            and not cfg.getboolean(section, option):
                        continue
                    value = cfg.get(section, option)
                    conv = action.type or str
                    if isinstance(action, actions['append']):
                        for v in value.splitlines():
                            action(parser, namespace, conv(v), arg)
                    else:
                        action(parser, namespace, conv(value), arg)


def rpc_command_line(args=None):
    """
    RPC Command Line Interface
    """
    parser = ArgumentParser(description='Fintech RPC server')
    parser.add_argument('-c', '--config-file', metavar='FILE',
                        type=str, action=LoadConfigAction,
                        help='load specified configuration file')
    parser.add_argument('-b', '--bind-address', metavar='ADDRESS', default='localhost',
                        help='bind server to given address (default: localhost)')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=8830,
                        help='the port number to use (default: 8830)')
    parser.add_argument('-t', '--threaded', action='store_true',
                        help='create a threaded server')
    parser.add_argument('-f', '--log-file', metavar='FILE',
                        help='write log to specified file')
    levels = ['debug', 'info', 'warning', 'error', 'critical']
    parser.add_argument('-l', '--log-level', metavar='LEVEL', default='info',
                        choices=levels, help='log level (%s)' % ', '.join(levels))
    
    group = parser.add_argument_group('Authorization', 'User management options')
    group.add_argument('-a', '--auth-user', metavar='USER:HASH', action='append',
                       help='enable http basic auth and add the specified user')
    group.add_argument('-i', '--auth-address', metavar='ADDRESS', action='append',
                       help='allow access only for specified ip address')
    
    group = parser.add_argument_group('Secure Socket Layer', 'Options to enable SSL')
    group.add_argument('-K', '--ssl-key', metavar='FILE', help='path to ssl key file')
    group.add_argument('-C', '--ssl-cert', metavar='FILE', help='path to ssl cert file')
    
    group = parser.add_argument_group('License', 'Options to register a licensed version')
    group.add_argument('-n', '--license-name', metavar='NAME', help='name of licensee')
    group.add_argument('-k', '--license-key', metavar='KEYCODE', help='license key code')
    group.add_argument('-u', '--license-user', metavar='USERID', action='append',
                       help='EBICS user id (must be applied for each user id)')
    args = parser.parse_args(args)
    
    # Set up logging
    level = levels.index(args.log_level) * 10 + 10
    # Reset logging handlers (why is this required?)
    for handler in list(logging.root.handlers):
        logging.root.removeHandler(handler)
    # Apply basic config
    logging.basicConfig(filename=args.log_file, level=level,
                        format='[%(asctime)s] %(levelname)s - %(name)s: %(message)s')
    
    # Register fintech package and import modules
    import_fintech([args.license_name, args.license_key, args.license_user])
    # Prepare users
    users = {}
    if args.auth_user:
        for user in args.auth_user:
            name, hash = user.split(':')
            users[name] = hash
    # Prepare SSL
    ssl_files = {}
    if args.ssl_key and args.ssl_cert:
        ssl_files['key'] = args.ssl_key
        ssl_files['cert'] = args.ssl_cert
    # Start server
    run(args.bind_address, args.port, args.threaded,
        users, args.auth_address, ssl_files)


if __name__ == '__main__':
    rpc_command_line()
