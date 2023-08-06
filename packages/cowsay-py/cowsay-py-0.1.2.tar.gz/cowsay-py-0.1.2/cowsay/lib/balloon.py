from ..modules import stringWidth

SPEECH_DELIMITERS = {
  'first':  ['/', '\\'],
  'middle': ['|', '|'],
  'last':   ['\\', '/'],
  'only':   ['<', '>'],  
}

THOUGHT_DELIMITERS = {
  'first':  ['(', ')'],
  'middle': ['(', ')'],
  'last':   ['(', ')'],
  'only':   ['(', ')'],
}

def pad(text, length:int):
    listlen = length - stringWidth(text) + 1
    trailingSpaces = ' ' * listlen
    return text + trailingSpaces

def top(length):
    return f' {"_"*(length + 3)}'

def bottom(length):
    return ' ' + '_'*(length + 3)

def say(text, wrap):
  return format(text, wrap, SPEECH_DELIMITERS)

def think(text, wrap):
  return format(text, wrap, THOUGHT_DELIMITERS)

def split(text, wrap):
    #print(f"wrap: '{wrap}'")
    text = text.replace("/\r\n?|[\n\u2028\u2029]/g", '\n').replace("/^\uFEFF/", '').replace("/\t/g", '        ')
    lines = []

    if wrap:
        text = ' '.join(text.split("/\s+/"))
        start = 0
        while start < len(text):
            end = min(start + wrap, len(text))
            space = text.rfind(' ', 0, end)
            if end < len(text) and space > start:
                end = space
            lines.append(text[start:end])
            if space > start:
                start = end + 1
            else:
                start = end
                
    else:
        lines = text.split('\n')
    return lines


def format(text, wrap, delimiters):
    #print(wrap)
    lines = split(text, wrap) if wrap else [text]
    if len(lines) == 0:
        lines = ['']
    maxLength = max(map(stringWidth, lines))

    def mapfunc(line):
        i = lines.index(line)
        only = len(lines) if len(lines) == 1 else None
        first = True if i == 0 else None
        last = True if i == (len(lines)-1) else None
        _type = 'only' if only else 'first' if first else 'last' if last else 'middle'
        start, end = delimiters[_type]
        return f"{start} {pad(line, maxLength)} {end}"

    res1 = map(mapfunc, lines)
    res = list(res1)
    # print(f"list(res): '{res}'")
    balloon = [
        top(maxLength),
    ]
    for j in range(0, len(res)):
        balloon.append(res[j])
    balloon.append(bottom(maxLength))
    # print(balloon)
    return '\n'.join(balloon)