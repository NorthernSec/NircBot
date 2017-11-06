import urllib.request, urllib.parse
import json
import html.parser


class Google:
    url  = "https://www.googleapis.com/customsearch/v1?key=%s&cx=017576662512468239146:omuauf_lfve&q=%s"
    api  = ""
    name = "Google"
    commands = ['google', 'g']
    h = html.parser.HTMLParser()

    def __init__(self, **args):
        pass

    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and command and arguments and channel and nick):
            return
        req = urllib.request.Request(self.url%(self.api, urllib.parse.quote(arguments)))
        data = urllib.request.urlopen(req).read()
        data = json.loads(str(data,encoding='utf-8'))

        items = []
        for item in data['items'][slice(0,3)]:
            items.append("%s - %s"%(item['title'], item['link']))
        if(len(items)>0):
            bot.say(channel, " | ".join(items))
        else:
            bot.say(channel, "No results.")


    def loadSettings(self, settings, **args):
        self.api = settings['api']
