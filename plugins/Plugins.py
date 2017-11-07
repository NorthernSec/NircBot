class Plugins:
    name     = "Plugins"
    commands = ['list']

    def __init__(self, **args):
        pass


    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and channel and command):
            return
        if command == 'list':
            commands = bot.plugManager.hooks['commands']
            commands = [(c, commands[c].name) for c in sorted(commands.keys())]
            commands = [('Command', 'Plugin'), ('-----', '-----')] + commands
            maxlen   = max([len(x[0]) for x in commands])
            for c in commands:
                command = c[0]+' '*(maxlen-len(c[0]))
                bot.say(channel, "%s - %s"%(command, c[1]))
