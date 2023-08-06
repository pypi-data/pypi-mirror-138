# From `man cowsay`:
#
# There are several provided modes which change the appearance of the cow
# depending on its particular emotional/physical state.   The  -b  option
# initiates  Borg  mode;  -d  causes  the  cow to appear dead; -g invokes
# greedy mode; -p causes a state of paranoia to come  over  the  cow;  -s
# makes  the  cow  appear thoroughly stoned; -t yields a tired cow; -w is
# somewhat the opposite of -t, and initiates wired mode; -y brings on the
# cow's youthful appearance.

DEFAULT_EYES = 'oo'
DEFAULT_TONGUE = '  '

modes = {
    'borg':{
        'eyes': '==',
        'tongue': '  ',
    },
    'dead': {
        'eyes': 'xx',
        'tongue': 'U ',
    },
    'greedy': {
        'eyes': '@@',
        'tongue': '  ',
    },
    'paranoid': {
        'eyes': '@@',
        'tongue': '  ',
    },
    'stoned': {
        'eyes': 'xx',
        'tongue': '  ',
    },
    'tired': {
        'eyes': '--',
        'tongue': '  ',
    },
    'wired': {
        'eyes': '@@',
        'tongue': '  ',
    },
    'youthful': {
        'eyes': 'oo',
        'tongue': '  ',
    },
}

def getFace(mode=None, **options):
    e = options.get('e') if options.get('e') else None
    T = options.get('T') if options.get('T') else None
    if mode: 
        return modes[mode]
    else: 
        eyes = e if e else DEFAULT_EYES
        tongue = T if T else DEFAULT_TONGUE
        return eyes, tongue
        """return {
        'eyes': e if e else DEFAULT_EYES,
        'tongue': T if T else DEFAULT_TONGUE,
    }"""
