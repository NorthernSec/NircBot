import logging

from twisted.internet import reactor

from lib.bot import BotFactory

hostname = '127.0.0.1'
port     = 6667
channel  = "#test"

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    f = BotFactory(channels=[channel])
    #reactor.connectSSL(hostname, port, f, ssl.ClientContextFactory())
    reactor.connectTCP(hostname, port, f)
    reactor.run()
