ANSI_COLOR = {
    'FATAL': '\033[31m',
    'ERROR': '\033[91m',
    'WARN': '\033[93m',
    'INFO': '\033[96m',
    'DEBUG': '\033[90m',
    'TRACE': '\033[92m',
    'BOLD': '\033[1m',
    'ENDL': '\033[0m',
}


class _Debug(object):
    @staticmethod
    def debug(level, message):
        if level in ANSI_COLOR:
            print(''.join([
                ANSI_COLOR[level],
                ANSI_COLOR['BOLD'],
                '[',
                level,
                '] ',
                ANSI_COLOR['ENDL'],
                ANSI_COLOR[level],
                message,
                ANSI_COLOR['ENDL']
            ]))
        else:
            print(message)
