class BotManager:
    admins = []
    name   = "BotManager"
    commands = ['join', 'part']

    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None):
        if not (bot and command and channel and arguments):
            return
        if nick not in self.admins:
            print(self.admins)
            bot.say(channel, "You're not allowed to execute this command")

        if   command == 'join':
            bot.join(arguments)
        elif command == 'part':
            bot.part(arguments)
        elif command == 'nick':
            bot.nickname = arguments

    def loadSettings(self, settings, bot):
        self.admins = settings.get('admins', '').split(',')
        bot.setNick(settings.get('nick', 'NircBot'))
        channels    = settings.get('channels', '').split(',')
        for channel in channels:
            bot.join(channel)
