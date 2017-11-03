import logging

from twisted.internet        import protocol
from twisted.words.protocols import irc

from lib.pluginmanager       import PluginManager
from lib.toolkit             import nsplit

class Bot(irc.IRCClient):
    def __init__(self):
        self.trigger = '.'
        self.plugManager = PluginManager(self)
        logging.debug("Bot created")

    def signedOn(self):
        self.plugManager.load_plugins()

        for chan in self.factory.channels:
            logging.info("Joining %s"%chan)
            self.join(chan)

    def userJoined(self, user, channel):
        self.plugManager.perform('user_join', None, user, channel)

    def userLeft(self, user, channel):
        self.plugManager.perform('user_part', None, user, channel)

    def userQuit(self, user, message):
        self.plugManager.perform('user_quit', message, user, None)

    def privmsg(self, user, channel, message):
        if channel != self.nickname:
            if message.startswith(self.trigger):
                command, payload = nsplit(message[len(self.trigger):], 2)
                self.plugManager.exec_if_command(command, payload, user, channel)
            self.plugManager.perform('user_message', message, user, channel)
        else:
            command, payload = nsplit(message, 2)
            self.plugManager.exec_if_command(command, payload, user, channel)
            self.plugManager.perform('user_privmsg', message, user, channel)

    def action(self, user, channel, message):
        self.plugManager.perform('user_action', message, user, channel)

    def noticed(self, user, channel, message):
        if channel != self.irc.nick:
            channel = self.irc.channels.get(channel)
        self.plugManager.perform('user_notice', message, user, channel)

    def userRenamed(self, oldname, newname):
        self.plugManager.perform('user_nick', None, oldname, None,
                                  newname=newname)

    def useKicked(self, kickee, channel, kicker, message):
        self.plugManager.perform('user_notice', message, None, channel,
                                 kickee=kickee, kicker=kicker)

    def modeChanged(self, user, channel, isset, modes, args):
        modes = '+%s'%modes if isset else '-%s'%modes
        self.plugManager.perform('mode_change', modes, user, channel)



class BotFactory(protocol.ClientFactory):
    protocol = Bot

    def __init__(self, nick=None, channels=None):
        if not nick:      nick      = "NircBot"
        if not channels:  channels  = []

        self.nickname = nick
        self.channels = channels

    def clientConnectionLost(self, connector, reason):
        logging.warn("Lost connection to server. Reason: %s"%reason)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        logging.error("Could not connect to IRC server")
