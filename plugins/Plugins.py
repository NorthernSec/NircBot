import os

class Plugins:
    name     = "Plugins"
    commands = ['list', 'load', 'unload']

    def __init__(self, **args):
        pass


    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and channel and command):
            return
        if   command == 'list':
            commands = bot.plugManager.hooks['commands']
            commands = [(c, commands[c].name) for c in sorted(commands.keys())]
            commands = [('Command', 'Plugin'), ('-----', '-----')] + commands
            maxlen   = max([len(x[0]) for x in commands])
            for c in commands:
                command = c[0]+' '*(maxlen-len(c[0]))
                bot.say(channel, "%s - %s"%(command, c[1]))

        elif command == 'load':
            try:
                name, settings = arguments.split(' ', 1)
                mode = 'load'
            except:
                name, mode, settings = arguments, 'default', None
            path = 'plugins/%s'%os.path.basename(name)
            try:
                bot.plugManager.load_plugin(path, mode, settings)
                bot.say(channel, 'Plugin loaded')
            except:
                bot.say(channel, 'Could not load plugin')

        elif command == 'unload':
            try:
                bot.plugManager.unload_plugin(arguments)
                bot.say(channel, "Plugin unloaded")
            except Exception as e:
                print(e)
                bot.say(channel, "Could not unload plugin")
