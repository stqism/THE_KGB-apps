import urllib2

#Update schema
__url__ = "https://raw.githubusercontent.com/KittyHawkIrc/modules/production/" + __name__ + ".py"
__version__ = 1.0

req = urllib2.Request('https://raw.githubusercontent.com/KittyHawkIrc/FPS-verified/master/users.txt')



def declare():
    return {"overkill": "userjoin"}

def callback(self):

    if self.channel == '#fatpeoplesuck':

        fd = urllib2.urlopen(req)
        isverified = eval(fd.read())
        fd.close()

        u = self.user.split('!',1)[0].lower()
        if u in isverified:
            self.msg('ChanServ', 'voice %s %s' % (self.channel, u))
        elif u+'_' in isverified:
            self.msg('Chanserv', 'voice %s %s' % (self.channel, u+'_'))
