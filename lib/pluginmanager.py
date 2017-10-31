import importlib
import logging

from lib.toolkit import nsplit, user_split

class PluginManager():
    def __init__(self, bot):
        self.bot = bot
        self.plugins  = {}
        self.hooks = {'user_join':      [],
                      'user_part':      [],
                      'user_quit':      [],
                      'user_message':   [],
                      'user_action':    [],
                      'user_notice':    [],
                      'user_nick':      [],
                      'user_kick':      [],
                      'user_privmsg':   [],

                      'bot_join':       [],
                      'bot_part':       [],
                      'bot_connect':    [],
                      'bot_disconnect': [],
                      'bot_message':    [],
                      'bot_action':     [],
                      'bot_notice':     [],
                      'bot_nick':       [],
                      'bot_kick':       [],
                      'bot_privmsg':    [],

                      'command':        {},
                      'mode_change':    [],
                      'topic_change':   []}
        logging.debug("PluginManager created")

    def load_plugin(self, path, mode, settings):
        try:
            logging.debug("Loading plugin %s"%path)
            if mode.lower() not in ['load', 'default']:
                return
            # import plugin and make it into an object
            i = importlib.import_module(path.replace('/', '.'))
            plugin = getattr(i, path.split('/')[-1])()
            if mode.lower() == 'load':
                if not hasattr(plugin, 'loadSettings:'):
                    logging.info("%s takes no settings"%path)
                else:
                    plugin.loadSettings(settings)
                    logging.debug("%s loaded settings %s"%(path, settings))
            self.plugins[plugin.name] = plugin
            for hook in [k for k in self.hooks.keys() if k != 'command']:
                if hasattr(plugin, hook):
                    self.hooks[hook].append(plugin)
            if hasattr(plugin, 'command') and hasattr(plugin, 'commands'):
                for command in getattr(plugin, 'commands'):
                    current = self.hooks['command'].get(command)
                    if current:
                        logging.warning("Command `%s` is already loaded by %s. Conflicting with %s"%(command, current.name, plugin.name))
                    else:
                        self.hooks['command'][command] = plugin

            logging.info("Plugin %s loaded"%plugin.name)
        except Exception as e:
            print(e)
            logging.warning("Could not load %s"%path)


    def unload_plugin(self, name):
        try:
            plugin = self.plugins[name]
            for hook in self.hooks.keys():
                self.hooks[hook] = [h for h in self.hooks[hook] if h.name != name]
            for command, plugin in self.hooks['command'].items():
                if name == plugin.name:
                    del self.hooks['command'][command]
            if hasattr(plugin, "unload"):
                plugin.unload()
            del self.plugins[name]
            logging.info("Plugin %s unloaded"%name)
        except:
            logging.warning("Could not unload plugin %s"%name)


    def load_plugins(self):
        conffile = "./etc/plugins.txt"
        try:
            logging.debug("Reading config file %s"%conffile)
            data = open(conffile, 'r').read()
        except:
            logging.error("Could not read plugin conf file!")
            return
        data = [nsplit(x, 3) for x in data.splitlines() if not x.startswith("#")]
        for path, mode, settings in [x for x in data if x[1] ]:
            self.load_plugin(path, mode, settings)

    def perform(self, action, msg, user, channel, **args):
        nick, ident, host = user_split(user)

        for plugin in self.hooks.get(action, []):
            try:
                f = getattr(plugin, action)
                f(self.bot, msg, nick, channel, ident, host, **args)
            except:
                self.bot.msg("Pluggin %s encountered an error!"%plugin.name)

    def exec_if_command(self, command, args, user, channel):
        try:
            nick, ident, host = user_split(user)
            logging.debug("Parsing command %s"%command)
            plug = self.hooks['command'].get(command)
            if plug:
                logging.debug("Performing command %s (plugin %s)"%(command, plug.name))
                plug.command(bot=self.bot, command=command, arguments=args,
                             nick=nick, channel=channel, ident=ident, host=host)
        except:
            self.bot.msg(channel, "An error happened trying to perform this command")
