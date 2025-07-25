




















"""
ClusterShell inter-nodes communication module

This module contains the required material for nodes to communicate between each
others within the propagation tree. At the highest level, messages are instances
of several classes. They can be converted into XML to be sent over SSH links
through a Channel instance.

In the other side, XML is parsed and new message objects are instantiated.

Communication channels have been implemented as ClusterShell events handlers.
Whenever a message chunk is read, the data is given to a SAX XML parser, that
will use it to create corresponding messages instances as a messages factory.

As soon as an instance is ready, it is then passed to a recv() method in the
channel. The recv() method of the Channel class is a stub, that requires to be
implemented in subclass to process incoming messages. So is the start() method
too.

Subclassing the Channel class allows implementing whatever logic you want on the
top of a communication channel.
"""

try:
    import _pickle as cPickle
except ImportError:  
    import cPickle

import base64
import binascii
import logging
import os
import xml.sax

from xml.sax.handler import ContentHandler
from xml.sax.saxutils import XMLGenerator
from xml.sax import SAXParseException

from collections import deque

try:
    
    from cStringIO import StringIO as BytesIO
except ImportError:  
    from io import BytesIO

from ClusterShell import __version__
from ClusterShell.Event import EventHandler



ENCODING = 'utf-8'


DEFAULT_B64_LINE_LENGTH = 65536


class MessageProcessingError(Exception):
    """base exception raised when an error occurs while processing incoming or
    outgoing messages.
    """


class XMLReader(ContentHandler):
    """SAX handler for XML -> Messages instances conversion"""
    def __init__(self):
        """XMLReader initializer"""
        ContentHandler.__init__(self)
        self.msg_queue = deque()
        self.version = None
        
        self._draft = None
        self._sections_map = None

    def startElement(self, name, attrs):
        """read a starting xml tag"""
        if name == 'channel':
            self.version = attrs.get('version')
            self.msg_queue.appendleft(StartMessage())
        elif name == 'message':
            self._draft_new(attrs)
        else:
            raise MessageProcessingError('Invalid starting tag %s' % name)

    def endElement(self, name):
        """read an ending xml tag"""
        
        if name == 'message':
            self.msg_queue.appendleft(self._draft)
            self._draft = None
        elif name == 'channel':
            self.msg_queue.appendleft(EndMessage())

    def characters(self, content):
        """read content characters (always decoded string)"""
        if self._draft is not None:
            self._draft.data_update(content.encode(ENCODING))

    def msg_available(self):
        """return whether a message is available for delivery or not"""
        return len(self.msg_queue) > 0

    def pop_msg(self):
        """pop and return the oldest message queued"""
        if self.msg_available():
            return self.msg_queue.pop()

    def _draft_new(self, attributes):
        """start a new packet construction"""
        
        
        ctors_map = {
            ConfigurationMessage.ident: ConfigurationMessage,
            ControlMessage.ident: ControlMessage,
            ACKMessage.ident: ACKMessage,
            ErrorMessage.ident: ErrorMessage,
            StdOutMessage.ident: StdOutMessage,
            StdErrMessage.ident: StdErrMessage,
            RetcodeMessage.ident: RetcodeMessage,
            TimeoutMessage.ident: TimeoutMessage,
        }
        try:
            msg_type = attributes['type']
            
            ctor = ctors_map[msg_type]
        except KeyError:
            raise MessageProcessingError('Unknown message type')
        
        self._draft = ctor()
        self._draft.selfbuild(attributes)


class Channel(EventHandler):
    """Use this event handler to establish a communication channel between to
    hosts within the propagation tree.

    The endpoint's logic has to be implemented by subclassing the Channel class
    and overriding the start() and recv() methods.

    There is no default behavior for these methods apart raising a
    NotImplementedError.

    Usage:
      >> chan = MyChannel() 
      >> task = task_self()
      >> task.shell("uname -a", node="host2", handler=chan)
      >> task.resume()
    """

    
    SNAME_WRITER = 'ch-writer'
    SNAME_READER = 'ch-reader'
    SNAME_ERROR = 'ch-error'

    def __init__(self, initiator=False):
        """
        """
        EventHandler.__init__(self)

        self.worker = None

        
        self.opened = False
        self.setup = False
        
        
        
        self.initiator = initiator

        self._xml_reader = XMLReader()
        self._parser = xml.sax.make_parser(["IncrementalParser"])
        self._parser.setContentHandler(self._xml_reader)

        self.logger = logging.getLogger(__name__)

    def _init(self):
        """start xml document for communication"""
        XMLGenerator(self.worker, encoding=ENCODING).startDocument()

    def _open(self):
        """open a new communication channel from src to dst"""
        xmlgen = XMLGenerator(self.worker, encoding=ENCODING)
        xmlgen.startElement('channel', {'version': __version__})

    def _close(self):
        """close an already opened channel"""
        send_endtag = self.opened
        if send_endtag:
            XMLGenerator(self.worker, encoding=ENCODING).endElement('channel')
        self.worker.abort()
        self.opened = self.setup = False

    def ev_start(self, worker):
        """connection established. Open higher level channel"""
        self.worker = worker
        self.start()

    def ev_read(self, worker, node, sname, msg):
        """channel has data to read"""
        

        if sname == self.SNAME_ERROR:
            if self.initiator:
                self.recv(StdErrMessage(node, msg))
            
            
            return

        try:
            self._parser.feed(msg + b'\n')
        except SAXParseException as ex:
            self.logger.error("SAXParseException: %s: %s", ex.getMessage(), msg)
            
            if self.initiator:
                self.recv(StdErrMessage(node, ex.getMessage()))
            else:
                
                self.send(ErrorMessage('Parse error: %s' % ex.getMessage()))
            
            self._close()
            return
        except MessageProcessingError as ex:
            self.logger.error("MessageProcessingError: %s", ex)
            if self.initiator:
                self.recv(StdErrMessage(node, str(ex)))
            else:
                
                self.send(ErrorMessage(str(ex)))
            
            self._close()
            return

        
        while self._xml_reader.msg_available():
            msg = self._xml_reader.pop_msg()
            assert msg is not None
            self.recv(msg)

    def send(self, msg):
        """write an outgoing message as its XML representation"""
        "%s"', id(self.worker),
        
        self.worker.write(msg.xml() + b'\n', sname=self.SNAME_WRITER)

    def start(self):
        """initialization logic"""
        raise NotImplementedError('Abstract method: subclasses must implement')

    def recv(self, msg):
        """callback: process incoming message"""
        raise NotImplementedError('Abstract method: subclasses must implement')


class Message(object):
    """base message class"""
    _inst_counter = 0
    ident = 'GEN'
    has_payload = False

    def __init__(self):
        """
        """
        self.attr = {'type': str, 'msgid': int}
        self.type = self.__class__.ident
        self.msgid = Message._inst_counter
        self.data = None
        Message._inst_counter += 1

    def data_encode(self, inst):
        """serialize an instance and store the result"""
        
        
        
        encoded = base64.b64encode(cPickle.dumps(inst))

        
        
        "non-alphabet characters"
        
        line_length = int(os.environ.get('CLUSTERSHELL_GW_B64_LINE_LENGTH',
                                         DEFAULT_B64_LINE_LENGTH))
        self.data = b'\n'.join(encoded[pos:pos+line_length]
                               for pos in range(0, len(encoded), line_length))

    def data_decode(self):
        """deserialize a previously encoded instance and return it"""
        
        
        
        try:
            return cPickle.loads(base64.b64decode(self.data))
        except (EOFError, TypeError, cPickle.UnpicklingError, binascii.Error):
            
            raise MessageProcessingError('Message %s has an invalid payload'
                                         % self.ident)

    def data_update(self, raw):
        """append data to the instance (used for deserialization)"""
        if self.has_payload:
            if self.data is None:
                self.data = raw  
            else:
                self.data += raw
        else:
            
            raise MessageProcessingError('Got unexpected payload for Message %s'
                                         % self.ident)

    def selfbuild(self, attributes):
        """self construction from a table of attributes"""
        for k, fmt in self.attr.items():
            try:
                setattr(self, k, fmt(attributes[k]))
            except KeyError:
                raise MessageProcessingError(
                    'Invalid "message" attributes: missing key "%s"' % k)

    def __str__(self):
        """printable representation"""
        elts = ['%s: %s' % (k, str(self.__dict__[k])) for k in self.attr.keys()]
        attributes = ', '.join(elts)
        return "Message %s (%s)" % (self.type, attributes)

    def xml(self):
        """generate XML version of a configuration message"""
        out = BytesIO()
        generator = XMLGenerator(out, encoding=ENCODING)

        "stringify" entries for XML conversion
        state = {}
        for k in self.attr:
            state[k] = str(getattr(self, k))

        generator.startElement('message', state)
        if self.data:
            generator.characters(self.data)
        generator.endElement('message')
        xml_msg = out.getvalue()
        out.close()
        return xml_msg

class ConfigurationMessage(Message):
    """configuration propagation container"""
    ident = 'CFG'
    has_payload = True

    def __init__(self, gateway=''):
        """initialize with gateway node name"""
        Message.__init__(self)
        self.attr.update({'gateway': str})
        self.gateway = gateway

class RoutedMessageBase(Message):
    """abstract class for routed message (with worker source id)"""
    def __init__(self, srcid):
        Message.__init__(self)
        self.attr.update({'srcid': int})
        self.srcid = srcid

class ControlMessage(RoutedMessageBase):
    """action request"""
    ident = 'CTL'
    has_payload = True

    def __init__(self, srcid=0):
        """
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'action': str, 'target': str})
        self.action = ''
        self.target = ''

class ACKMessage(Message):
    """acknowledgement message"""
    ident = 'ACK'

    def __init__(self, ackid=0):
        """
        """
        Message.__init__(self)
        self.attr.update({'ack': int})
        self.ack = ackid

class ErrorMessage(Message):
    """error message"""
    ident = 'ERR'

    def __init__(self, err=''):
        """
        """
        Message.__init__(self)
        self.attr.update({'reason': str})
        self.reason = err

class StdOutMessage(RoutedMessageBase):
    """container message for standard output"""
    ident = 'OUT'
    has_payload = True

    def __init__(self, nodes='', output=None, srcid=0):
        """
        Initialized either with empty payload (to be loaded, already encoded),
        or with payload provided (via output to encode here).
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'nodes': str})
        self.nodes = nodes
        self.data = None 
        if output is not None:
            self.data_encode(output)

class StdErrMessage(StdOutMessage):
    """container message for stderr output"""
    ident = 'SER'

class RetcodeMessage(RoutedMessageBase):
    """container message for return code"""
    ident = 'RET'

    def __init__(self, nodes='', retcode=0, srcid=0):
        """
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'retcode': int, 'nodes': str})
        self.retcode = retcode
        self.nodes = nodes

class TimeoutMessage(RoutedMessageBase):
    """container message for timeout notification"""
    ident = 'TIM'

    def __init__(self, nodes='', srcid=0):
        """
        """
        RoutedMessageBase.__init__(self, srcid)
        self.attr.update({'nodes': str})
        self.nodes = nodes

class StartMessage(Message):
    """message indicating the start of a channel communication"""
    ident = 'CHA'

class EndMessage(Message):
    """end of channel message"""
    ident = 'END'
