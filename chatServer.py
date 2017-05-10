from twisted.internet.protocol import ClientFactory,Protocol, Factory
from twisted.internet import reactor
import time
from collections import deque
from chatFactory import *

reactor.listenTCP(8000, chatServerFactory())
reactor.run()
