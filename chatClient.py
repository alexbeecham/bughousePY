from twisted.internet.protocol import ClientFactory,Protocol, Factory
from twisted.internet import reactor
import time
from collections import deque
from chatFactory import *

'''Connect to server'''
factory = chatFactory()
reactor.connectTCP("localhost",8000,factory)
reactor.run()
