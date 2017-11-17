class TextOperations:
    name     = "TextOperations"
    commands = ['say', 'reverse', 'upper', 'lower', 'capitalize']
    def __init__(self, **args):
        pass

    def command(self, bot=None, command=None, arguments=None, nick=None,
                      channel=None, ident=None, host=None, **args):
        if not (bot and arguments):
            return
        if   command == 'say':         return arguments
        elif command == 'reverse':     return arguments[::-1]
        elif command == 'upper':       return arguments.upper()
        elif command == 'lower':       return arguments.lower()
        elif command == 'capitalize':  return arguments.capitalize()