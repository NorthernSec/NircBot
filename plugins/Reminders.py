import re
import threading
import time

from datetime import datetime, timedelta

class Reminders:
    name     = "Reminders"
    commands = ['remind']
    regex    = re.compile(r'((?P<days>\d+?)d)?((?P<hours>\d+?)h)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')

    def __init__(self, **args):
        self.reminders = []
        self.bot        = args.get('bot')
        thread = threading.Thread(target=self._reaper)
        thread.daemon = True
        thread.start()

    def _create_time_delta(self, timestring):
        parts = self.regex.match(timestring)
        if not parts: return
        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params)

    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and command and arguments and channel and nick):
            return

        if   command == 'remind':
            try:
                target, time, message = arguments.split(' ', 2)
            except:
                bot.say(channel, "syntax: remind <user> <time> <message>")
                return

            time = self._create_time_delta(time)
            if not time:
                bot.say(channel, "syntax example for time param: 7d3h2m5s")

            now      = datetime.now()
            deadline = now+time

            self.reminders.append((deadline, target, message))
            self.reminders.sort(key=lambda tup: tup[0])
            bot.say(channel, "Will remind %s in %s"%(target, time))

    def _reaper(self):
        while True:
            while True:
                try:
                    if len(self.reminders) > 0:
                        notice = self.reminders[0]
                        if notice[0] < datetime.now():
                            self.bot.notice(notice[1], "[NOTICE] %s"%notice[2])
                            print('noticing')
                            self.reminders.pop()
                    time.sleep(1)
                except Exception as e:
                    print(e)
