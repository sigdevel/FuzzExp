"""
Serve web page and handle web sockets using Flask.
"""








import json
import time
import asyncio
import socket
import mimetypes
import threading
from urllib.parse import urlparse
from typing import Any, Dict, Union

import flask
from flask import Flask, request, current_app, url_for
from flask_sockets import Sockets

from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from ._app import manager
from ._session import get_page
from ._server import AbstractServer
from ._assetstore import assets
from ._clientcore import serializer
from ._flaskhelpers import register_blueprints, flexxBlueprint, flexxWS

from . import logger
from .. import config

app = Flask(__name__)



@app.route('/favicon.ico')
def favicon():
    return ''  


if app.debug:

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)

    @app.route("/site-map")
    def site_map():
        links = []
        for rule in current_app.url_map.iter_rules():
            
            
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        
        html = ["<h> URLs served by this server </h>", "<ul>"]
        for link in links:
            html.append(f'<li><a href="{link[0]}">{link[1]}</a></li>')
        html.append("</ul>")
        return '\n'.join(html)


@flexxWS.route('/ws/<path:path>')
def ws_handler(ws, path):
    
    wshandler = WSHandler(ws)

    async def flexx_msg_handler(ws, path): 
        wshandler.open(path)
        
    future = asyncio.run_coroutine_threadsafe(
        flexx_msg_handler(ws, path), loop=manager.loop
    )
    future.result()
    while not ws.closed:
        message = ws.receive()
        if message is None: 
            break
        manager.loop.call_soon_threadsafe(wshandler.on_message, message)
    manager.loop.call_soon_threadsafe(wshandler.ws_closed)


@flexxBlueprint.route('/', defaults={'path': ''})
@flexxBlueprint.route('/<path:path>')
def flexx_handler(path):
    
    "flexx/{path}"
    
    return MainHandler(flask.request).run()


IMPORT_TIME = time.time()


def is_main_thread():
    """ Get whether this is the main thread. """
    return isinstance(threading.current_thread(), threading._MainThread)


class FlaskServer(AbstractServer):
    """ Flexx Server implemented in Flask.
    """

    def __init__(self, *args, **kwargs):
        global app
        self._app = app
        self._server = None
        self._serving = None  
        
        super().__init__(*args, **kwargs) 

    def _open(self, host, port, **kwargs):
        
        
        
        
        if port:
            
            try:
                port = int(port)
            except ValueError:
                port = port_hash(port)
        else:
            
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            prefered_port = port_hash('Flexx')
            for i in range(8):
                port = prefered_port + i
                try:
                    a_socket.bind((host, port))
                except Exception:
                    continue
                a_socket.close()
                break
            else:
                raise RuntimeError("No port found to start flask")

        
        self._serving = (host, port)

        
        manager.loop = self._loop
        
        
        asyncio.run_coroutine_threadsafe(self._thread_switch(), self._loop)

    @staticmethod
    async def _thread_switch():
        """
        Python 3.8 is very unfrendly to thread as it does not leave any chances for 
        a Thread switch when no tasks are left to run. This function just let other
        Threads some time to run.
        """
        while True:
            time.sleep(0)
            await asyncio.sleep(1e-9)  

    def start(self):
        
        sockets = Sockets(app)
        register_blueprints(self._app, sockets)

        
        def RunServer():
            self._server = pywsgi.WSGIServer(
                self._serving, self._app, handler_class=WebSocketHandler
            )
            proto = self.protocol
            
            logger.info('Serving apps at %s://%s:%i/' % (proto, *self._serving))
            self._server.serve_forever()

        _thread = threading.Thread(target=RunServer)
        _thread.daemon = True  
        _thread.start()
        super().start()

    def start_serverless(self):
        super().start()

    def _close(self):
        self._server.stop()

    @property
    def app(self):
        """ The Flask Application object being used."""
        return self._app

    @property
    def server(self):
        """ The Flask HttpServer object being used."""
        return self._server

    @property
    def protocol(self):
        """ Get a string representing served protocol."""


        return 'http'


def port_hash(name):
    """ Given a string, returns a port number between 49152 and 65535

    This range (of 2**14 posibilities) is the range for dynamic and/or
    private ports (ephemeral ports) specified by iana.org. The algorithm
    is deterministic.
    """
    fac = 0xd2d84a61
    val = 0
    for c in name:
        val += (val >> 3) + (ord(c) * fac)
    val += (val >> 3) + (len(name) * fac)
    return 49152 + (val % 2 ** 14)


class RequestHandler:

    def __init__(self, request):
        self.request = request
        self.content = []
        self.values = {}
        
    def redirect(self, location):
        return flask.redirect(location)
    
    def write(self, string_or_bytes):
        self.content = string_or_bytes
    
    def send_error(self, error_no):
        return "Error", error_no
    
    def run(self):
        if self.request.method == 'GET':
            ret = self.get(request.path)
            if ret is not None:
                return ret
            else:
                return self.content, 200, self.values
    
    def get_argument(self, key, default):
        return self.request.values.get(key, default)
    
    def set_header(self, key, value):
        self.values[key] = value
        

class AppHandler(RequestHandler):
    """ Handler for http requests to get apps.
    """

    def get(self, full_path):

        logger.debug('Incoming request at %r' % full_path)

        ok_app_names = '__main__', '__default__', '__index__'
        parts = [p for p in full_path.split('/') if p]

        
        
        app_name = None
        path = '/'.join(parts)
        if parts:
            if path.lower() == 'flexx':  
                return self.redirect('/flexx/')
            if parts[0] in ok_app_names or manager.has_app_name(parts[0]):
                app_name = parts[0]
                path = '/'.join(parts[1:])

        
        
        
        "favicon.ico" that browsers request by default (
        if app_name is None:
            if len(parts) == 1 and '.' in full_path:
                return self.redirect('/flexx/data/' + full_path)
            
            app_name = '__main__'

        
        if app_name == '__main__':
            app_name = manager.has_app_name('__main__')
        elif '/' not in full_path:
            return self.redirect('/%s/' % app_name)  

        
        if not app_name:
            if not parts:
                app_name = '__index__'
            else:
                name = parts[0] if parts else '__main__'
                self.write('No app "%s" is currently hosted.' % name)

        
        
        
        
        
        if app_name == '__index__':
            return self._get_index(app_name, path)  
        else:
            return self._get_app(app_name, path)  

    def _get_index(self, app_name, path):
        if path:
            return self.redirect('/flexx/__index__')
        all_apps = ['<li><a href="%s/">%s</a></li>' % (name, name) for name in
                    manager.get_app_names()]
        the_list = '<ul>%s</ul>' % ''.join(all_apps) if all_apps else 'no apps'
        self.write('Index of available apps: ' + the_list)

    def _get_app(self, app_name, path):
        
        
        if path.startswith(('flexx/data/', 'flexx/assets/')):
            return self.redirect('/' + path)

        
        correct_app_name = manager.has_app_name(app_name)

        
        if not correct_app_name:
            self.write('No app "%s" is currently hosted.' % app_name)
        if correct_app_name != app_name:
            return self.redirect('/%s/%s' % (correct_app_name, path))

        
        session_id = self.get_argument('session_id', '')

        if session_id:
            
            session = manager.get_session_by_id(session_id)
            if session and session.status == session.STATUS.PENDING:
                self.write(get_page(session).encode())
            else:
                self.redirect('/%s/' % app_name)  
        else:

            
            async def run_in_flexx_loop(app_name, request):
                session = manager.create_session(app_name, request=request)
                return session

            future = asyncio.run_coroutine_threadsafe(
                run_in_flexx_loop(app_name, request=self.request), loop=manager.loop
            )
            session = future.result()
            self.write(get_page(session).encode())


class MainHandler(RequestHandler):
    """ Handler for assets, commands, etc. Basically, everything for
    which the path is clear.
    """

    def _guess_mime_type(self, fname):
        """ Set the mimetype if we can guess it from the filename.
        """
        guess = mimetypes.guess_type(fname)[0]
        if guess:
            self.set_header("Content-Type", guess)

    def get(self, full_path):

        logger.debug('Incoming request at %s' % full_path)

        
        
        parts = [p for p in full_path.split('/') if p][1:]
        if not parts:
            self.write('Root url for flexx, missing selector:' + 
                       'assets, assetview, data, info or cmd')
            return
        selector = parts[0]
        path = '/'.join(parts[1:])

        if selector in ('assets', 'assetview', 'data'):
            self._get_asset(selector, path)  
        elif selector == 'info':
            self._get_info(selector, path)
        elif selector == 'cmd':
            self._get_cmd(selector, path)  
        else:
            self.write('Invalid url path "%s".' % full_path)

    def _get_asset(self, selector, path):

        
        session_id, _, filename = path.partition('/')
        session_id = '' if session_id == 'shared' else session_id

        
        asset_provider = assets
        if session_id and selector != 'data':
            self.write('Only supports shared assets, not ' % filename)
        elif session_id:
            asset_provider = manager.get_session_by_id(session_id)

        
        if asset_provider is None:
            self.write('Invalid session %r' % session_id)
        if not filename:
            self.write('Root dir for %s/%s' % (selector, path))

        if selector == 'assets':

            
            if '.js:' in filename or '.css:' in filename or filename[0] == ':':
                fname, where = filename.split(':')[:2]
                return self.redirect('/flexx/assetview/%s/%s
                    (session_id or 'shared', fname.replace('/:', ':'), where))

            
            try:
                res = asset_provider.get_asset(filename)
            except KeyError:
                self.write('Could not load asset %r' % filename)
            else:
                self._guess_mime_type(filename)
                self.write(res.to_string())

        elif selector == 'assetview':

            
            try:
                res = asset_provider.get_asset(filename)
            except KeyError:
                self.write('Could not load asset %r' % filename)
            else:
                res = res.to_string()

            
            style = ('pre {display:block; width: 100%; padding:0; margin:0;} '
                    'a {text-decoration: none; color: 
                    ':target {background:
            lines = ['<html><head><style>%s</style></head><body>' % style]
            for i, line in enumerate(res.splitlines()):
                table = {ord('&'): '&amp;', ord('<'): '&lt;', ord('>'): '&gt;'}
                line = line.translate(table).replace('\t', '    ')
                lines.append('<pre id="L%i"><a href="">%s</a>  %s</pre>' % 
                    (i + 1, i + 1, str(i + 1).rjust(4).replace(' ', '&nbsp'), line))
            lines.append('</body></html>')
            self.write('\n'.join(lines))

        elif selector == 'data':
            

            
            res = asset_provider.get_data(filename)
            if res is None:
                return self.send_error(404)
            else:
                self._guess_mime_type(filename)  
                self.write(res)

        else:
            raise RuntimeError('Invalid asset type %r' % selector)

    def _get_info(self, selector, info):
        """ Provide some rudimentary information about the server.
        Note that this is publicly accesible.
        """
        runtime = time.time() - IMPORT_TIME
        napps = len(manager.get_app_names())
        nsessions = sum([len(manager.get_connections(x))
                         for x in manager.get_app_names()])

        info = []
        info.append('Runtime: %1.1f s' % runtime)
        info.append('Number of apps: %i' % napps)
        info.append('Number of sessions: %i' % nsessions)

        info = '\n'.join(['<li>%s</li>' % i for i in info])
        self.write('<ul>' + info + '</ul>')

    def _get_cmd(self, selector, path):
        """ Allow control of the server using http, but only from localhost!
        """
        if not self.request.host.startswith('localhost:'):
            self.write('403')
            return

        if not path:
            self.write('No command given')
        elif path == 'info':
            info = dict(address=self.application._flexx_serving,
                        app_names=manager.get_app_names(),
                        nsessions=sum([len(manager.get_connections(x))
                                        for x in manager.get_app_names()]),
                        )
            self.write(json.dumps(info))
        elif path == 'stop':
            asyncio.get_event_loop().stop()
            
            
            self.write("Stopping event loop.")
        else:
            self.write('unknown command %r' % path)


class MessageCounter:
    """ Simple class to count incoming messages and periodically log
    the number of messages per second.
    """

    def __init__(self):
        self._collect_interval = 0.2  
        self._notify_interval = 3.0  
        self._window_interval = 4.0  

        self._mps = [(time.time(), 0)]  
        self._collect_count = 0
        self._collect_stoptime = 0

        self._stop = False
        self._notify()

    def trigger(self):
        t = time.time()
        if t < self._collect_stoptime:
            self._collect_count += 1
        else:
            self._mps.append((self._collect_stoptime, self._collect_count))
            self._collect_count = 1
            self._collect_stoptime = t + self._collect_interval

    def _notify(self):
        mintime = time.time() - self._window_interval
        self._mps = [x for x in self._mps if x[0] > mintime]
        if self._mps:
            n = sum([x[1] for x in self._mps])
            T = self._mps[-1][0] - self._mps[0][0] + self._collect_interval
        else:
            n, T = 0, self._collect_interval
        logger.debug('Websocket messages per second: %1.1f' % (n / T))

        if not self._stop:
            loop = asyncio.get_event_loop()
            loop.call_later(self._notify_interval, self._notify)

    def stop(self):
        self._stop = True


class MyWebSocketHandler():
    """
    This class is designed to mimic the tornado WebSocketHandler to
    allow glue in code from WSHandler.
    """

    class Application:
        pass

    class IOLoop:

        def __init__(self, loop):
            self._loop = loop

        def spawn_callback(self, func, *args):
            self._loop.call_soon_threadsafe(func, *args)
    
    def __init__(self, ws):
        self._ws = ws
        self.application = MyWebSocketHandler.Application()
        self.application._io_loop = MyWebSocketHandler.IOLoop(manager.loop)
        self.cookies = {}

    def write_message(
        self, message: Union[bytes, str, Dict[str, Any]], binary: bool=False
    ):
        self._ws.send(message)
        
    def close(self, code: int=None, reason: str=None) -> None:
        if not self._ws.closed:
            self._ws.close(code, reason)

    def ws_closed(self):
        self.on_close()


class WSHandler(MyWebSocketHandler):
    """ Handler for websocket.
    """

    
    known_reasons = {1000: 'client done',
                     1001: 'client closed',
                     1002: 'protocol error',
                     1003: 'could not accept data',
                     }

    

    def open(self, path=None):
        """ Called when a new connection is made.
        """
        if not hasattr(self, 'close_code'):  
            self.close_code, self.close_reason = None, None

        self._session = None
        self._mps_counter = MessageCounter()

        if isinstance(path, bytes):
            path = path.decode()
        self.app_name = path.strip('/')

        logger.debug('New websocket connection %s' % path)
        if manager.has_app_name(self.app_name):
            self.application._io_loop.spawn_callback(self.pinger1)
        else:
            self.close(1003, "Could not associate socket with an app.")

    
    def on_message(self, message):
        """ Called when a new message is received from JS.

        This handles one message per event loop iteration.

        We now have a very basic protocol for receiving messages,
        we should at some point define a real formalized protocol.
        """
        self._mps_counter.trigger()

        try:
            command = serializer.decode(message)
        except Exception as err:
            err.skip_tb = 1
            logger.exception(err)

        self._pongtime = time.time()
        if self._session is None:
            if command[0] == 'HI_FLEXX':
                session_id = command[1]
                try:
                    self._session = manager.connect_client(self, self.app_name,
                                                           session_id,
                                                           cookies=self.cookies)
                except Exception as err:
                    self.close(1003, "Could not launch app: %r" % err)
                    raise
        else:
            try:
                self._session._receive_command(command)
            except Exception as err:
                err.skip_tb = 1
                logger.exception(err)

    def on_close(self):
        """ Called when the connection is closed.
        """
        self.close_code = code = self.close_code or 0
        reason = self.close_reason or self.known_reasons.get(code, '')
        logger.debug('Websocket closed: %s (%i)' % (reason, code))
        self._mps_counter.stop()
        if self._session is not None:
            manager.disconnect_client(self._session)
            self._session = None  

    def pinger1(self):
        """ Check for timeouts. This helps remove lingering false connections.

        This uses the websocket's native ping-ping mechanism. On the
        browser side, pongs work even if JS is busy. On the Python side
        we perform a check whether we were really waiting or whether Python
        was too busy to detect the pong.
        """
        self._pongtime = time.time()
        self._pingtime = pingtime = 0

        while self.close_code is None:
            dt = config.ws_timeout

            
            if pingtime <= self._pongtime:
                self.ping(b'x')
                pingtime = self._pingtime = time.time()
                iters_since_ping = 0

            

            
            iters_since_ping += 1
            if iters_since_ping < 5:
                pass  
            elif time.time() - self._pongtime > dt:
                
                
                logger.warning('Closing connection due to lack of pong')
                self.close(1000, 'Conection timed out (no pong).')
                return

    def on_pong(self, data):
        """ Implement the ws's on_pong() method. Called when our ping
        is returned by the browser.
        """
        self._pongtime = time.time()

    

    def write_command(self, cmd):
        assert isinstance(cmd, tuple) and len(cmd) >= 1
        bb = serializer.encode(cmd)
        try:
            self.write_message(bb, binary=True)
        except flask.Exception:  
            self.close(1000, 'closed by client')

    def close(self, *args):
        super().close(*args)

    def close_this(self):
        """ Call this to close the websocket
        """
        self.close(1000, 'closed by server')

    def check_origin(self, origin):
        """ Handle cross-domain access; override default same origin policy.
        """
        
        

        serving_host = self.request.headers.get("Host")
        serving_hostname, _, serving_port = serving_host.partition(':')
        connecting_host = urlparse(origin).netloc
        connecting_hostname, _, connecting_port = connecting_host.partition(':')

        serving_port = serving_port or '80'
        connecting_port = connecting_port or '80'

        if serving_hostname == 'localhost':
            return True  
        elif serving_host == connecting_host:
            return True  
        elif serving_hostname == '0.0.0.0' and serving_port == connecting_port:
            return True  
        elif connecting_host in config.host_whitelist:
            return True
        else:
            logger.warning('Connection refused from %s' % origin)
            return False
