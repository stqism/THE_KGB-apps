import urllib2
pimpdb = {}
pimpToChandb = {}

def declare():
    return {"pimp": "privmsg"}

def callback(self, type, isop, command="", msg="", user="", channel="", mode=""):
    u = user.lower().split('!')[0]
    global pimpdb
    if channel.startswith('#'):

        chan = channel.lower()

        var = msg.lower().split()

        try:
            target = var[1]
        except:
            target = u

        try:
            com = var[2]
        except:
            com = 'get'

        if chan not in pimpdb:
            pimpdb[chan] = {}

        if u == target and com != 'get':
            self.msg(chan, "%s: Y'all can't pimp yourself, ma nigga" % (u))
            return

        if com == '+1':
            addPoints(chan, u, target, 1)
        elif com == '-1':
            addPoints(chan, u, target, 1)
        elif com == 'get':
            try:
                pimp = pimpdb[chan][target]
                if pimp > 0:
                    self.msg(channel, "that nigga got %s pimp points up in this bitch" % (pimp))
                else:
                    self.msg(channel, "that nigga got %s bitch points" % (pimp))
            except:
                pimp = 5
                self.msg(channel, "that nigga got 5 pimp points up in this bitch")
            for k,v in pimpToChandb.items():
                if v:
                    self.msg(k, "%s <%s> %s[%s]'s checked %s[%s]'s points" % (time.time(),chan,u,pimpdb[c][u],target,pimpdb[c][target])
        else:
            self.msg(channel, "%s: Nigga, you really think you that og, just giving out more points like that?" % (u))

    elif isop: #format as pimp [command] [channel] [target] [value]
        var = msg.lower().split()
        com = var[1]

        try:
            chan = var[2]
            target = var[3]
        except:
            if not (com == 'load' or com == 'dump' or com == 'inflate' or com == 'addtoall'):
                return

        try:
            val = var[4]
        except:
            val = 5

        if com == 'set':
            try:
                pimpdb[chan][target] = int(val)
                self.msg(u, "%s's score in %s is now set to %s" % (target, chan, val))
            except:
                self.msg(u, "%s doesn't exist in %s" % (target, chan))
        
        elif com == 'add':
            try:
                pimpdb[chan][target] += val
                self.msg(u, "%s's score in %s is now set to %s" % (target, chan, val))
            except:
                self.msg("Doesn't %s exist in %s" % (target, chan))
        
        elif com == 'remove':
            if target in pimpdb[chan]:
                pimpdb[chan].pop(target)
                self.msg(u, "%s is now removed from that channel's list" % (target))
            else:
                self.msg(u, "%s is not in that channel's list")
        
        elif com == 'new':
            if chan not in pimpdb:
                pimpdb[chan] = {}
            if target not in pimpdb[chan]:
                pimpdb[chan][target] = int(val)
                self.msg(u, "%s is now added to the channel with %s points" % (target, val))
            else:
                self.msg(u, "%s is already in the channel with %s points, please remove them before adding them again" % (target, val))
        
        elif com == 'dump':
            self.msg(u, str(pimpdb))
            
        elif com == 'load':
            req = urllib2.Request(msg.lower().split('load')[1])
            fd = urllib2.urlopen(req)
            pimpdb = eval(fd.read())
            fd.close()
            
        elif com == 'inflate': #target == value to multiply by
            for k, v in pimpdb[chan].items():
                if v > 0:
                    pimpdb[chan][k] *= int(target)
                else:
                    pimpdb[chan][k] /= int(target)
        
        elif com == 'addtoall': #target == value to add to each user
            for k,v in pimpdb[chan].items():
                pimpdb[chan][k] += int(target)
        
        elif com == 'pimptochannel': #target == "on", otherwise assumed "off"
            if target == "on":
                pimpToChandb[chan] = True
            else:
                pimpToChandb[chan] = False
        else:
            self.msg(u, "unavailable")

#c = channel
#u = user giving/taking points
#t = target who's points are being modified
#p = points being taken/removed
def addPoints(c, u, t, p):
    global pimpdb
    ts = time.time()
    up = 0
    tp = 0
    
    assert p = 1 or p = -1
    
    if u not in pimpdb[c]:
        pimpdb[c][u] = 4
        for k,v in pimpToChandb.items():
            if v:
                self.msg(k, "%s <%s> %s added to db with %s points" % (ts,c,t,pimpdb[c][u])
    elif pimpdb[c][u] > 0:
        pimpdb[c][u] = int(pimpdb[c][u]) - 1
    else:
        self.msg(channel, "%s: You ain't got no pimp points" % (u))
        for k,v in pimpToChandb.items():
            if v:
                self.msg(k, "%s <%s> %s[%s]'s attempted to change %s[%s]'s points by %s" % (ts,c,u,pimpdb[c][u],t,pimpdb[c][t],p)
        return
    
    try: #modifies users points
        pimpdb[c][t] += p
    except:
        pimpdb[c][t] = 5 + p
        for k,v in pimpToChandb.items():
            if v:
                self.msg(k, "%s <%s> %s added to db with %s points" % (ts,c,t,pimpdb[c][t]-p)
    
    for k,v in pimpToChandb.items():
        if v:
            self.msg(k, "%s <%s> %s[%s]'s changes %s[%s]'s points by %s" % (ts,c,u,pimpdb[c][u]-p,t,pimpdb[c][t]-p,p)
