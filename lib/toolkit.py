def nsplit(data, parts, sepparator=' \t'):
    if len(sepparator) >= 2:
        changelist = sepparator[1:]
        sepparator = sepparator[0]
        for ch in changelist:
            data = data.replace(ch, sepparator)
    data = data.split(sepparator, parts-1)
    data.extend([None]*(parts-len(data)))
    return data


def user_split(user):
    try:
        nick,   rest = user.split('!', 1)
        ident , host = rest.split('@', 1)
    except:
        nick  = user
        ident = None
        host  = None
    return (nick, ident, host)
