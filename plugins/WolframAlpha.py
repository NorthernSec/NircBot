import urllib.request
import urllib.parse


class WolframAlpha():
    api = "http://api.wolframalpha.com/v2/query?input={}&appid={}"
    appId = ""
    name = "WolframAlpha"
    commands = ['w', 'wa']

    def _apiFetch(self, userInput):
        # args = urllib.parse.quote(userInput)
        apiRequest = urllib.request.Request(
            self.api.format(input, self.appId))
        try:
            apiResonse = urllib.request.urlopen(apiRequest).read()
        except urllib.error.URLError:
            return False
        else:
            return apiResonse

    def command(self, bot=None, command=None, arguments=None,
                nick=None, channel=None, ident=None, host=None):
        apiData = self._apiFetch(arguments)
        if(apiData):
            print("yes")
        else:
            print("API not available.")

    def loadSettings(self, settings, **args):
        self.api = settings['api']
