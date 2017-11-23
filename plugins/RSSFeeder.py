import feedparser
import time
import threading

class RSSFeeder:
    name = "RSS"
    commands = ['rss']

    def __init__(self, **args):
        self.interval   = 15
        self.rssupdater = RSSUpdater()
        self.bot        = None
        self.channel    = "#news"

        self.read_defaults()
        thread = threading.Thread(target=self.monitor)
        thread.daemon = True
        thread.start()

    def read_defaults(self):
        for feed in [('AusCert',      'https://www.auscert.org.au/rss/bulletins/'),
                     ('CERT/CC',      'http://www.kb.cert.org/vulfeed'),
                     ('CERT-EU',      'https://cert.europa.eu/rss?type=category&id=VulnerabilitiesAll&language=all&duplicates=false'),
                     ('Exploit-DB',   'https://www.exploit-db.com/rss.xml'),
                     ('ICS-CERT',     'https://ics-cert.us-cert.gov/advisories/advisories.xml'),
                     ('JPCERT/CC',    'http://jvn.jp/en/rss/jvn.rdf'),
                     ('DoEnergy',     'https://energy.gov/articles/673/708757%2B708775/JC3%20Bulletin%20Archive?view=rss'),
                     ('JVN IPA',      'http://jvndb.jvn.jp/en/rss/jvndb_new.rdf'),
                     ('NIST',         'https://nvd.nist.gov/download/nvd-rss.xml'),
                     ('PacketStorm',  'https://rss.packetstormsecurity.com/files/'),
                     ('Scip',         'http://www.scip.ch/en/?rss.vuldb'),
                     ('SecuriTeam',   'http://www.securiteam.com/securiteam.rss'),
                     ('TippingPoint', 'http://feeds.feedburner.com/ZDI-Published-Advisories'),
                     ]:
            self.rssupdater.add_feed(feed[0], feed[1])

    def loadSettings(self, settings, bot=None):
        self.bot = bot
        self.bot.join(self.channel)

    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and command and arguments and channel and nick):
            pass

    def monitor(self):
        try:
            while True:
                for update in self.rssupdater.get_updates():
                    if self.bot:
                        self.bot.say(self.channel, "[%s] %s"%(update.feed_name, update.title))
                time.sleep(self.interval)
        except Exception as e:
            print(e)
            pass



class Feed:
    def __init__(self, name, url):
        self.name     = name
        self.url      = url
        self.etag     = None
        self.data     = None
        self.modified = None
        self.entries  = {}
        self.get_updates()

    def get_updates(self):
        d = feedparser.parse(self.url, etag=self.etag, modified=self.modified)
        if 'status' not in d or d.status != 304: # Not modified
            if 'etag' in d:
                self.etag = d.etag
            if 'modified' in d:
                self.modified = d.modified
            self.data = d.feed
            old          = self.entries
            self.entries = {x.id: x for x in d.entries if 'id' in x}
            new = [v for k,v in self.entries.items() if k not in old.keys()]
            return new
        return []


class RSSUpdater:
    feeds = {}
    def get_updates(self):
        updates = []
        for feed in self.feeds.values():
            feed_update = feed.get_updates()
            for x in feed_update:
                x['feed_name'] = feed.name
            updates.extend(feed_update)
        return updates

    def add_feed(self, name, url):
        self.feeds[name] = Feed(name, url)

    def del_feed(self, name):
        if name in self.feeds.keys():
            del self.feeds[name]
            return True
        return False
