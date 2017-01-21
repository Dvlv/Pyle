class PyleTree():
    def __init__(self, value, children):
        self.value = value
        self.children = children

    {'0': {
        'A': {
            'B': {
                'C': {}
            }
        },
        'D': {
            'E': {},
            'F': {}
        }
    }}

j = [[0, 'html'], [2, 'body'], [4, 'div'], [4,'span'], [6, 'label'], [8, 'tr'], [8, 'th'], [8, 'td']]
j2 = list(reversed(j))
#print(list(j2))
struct = {}
current_index = j2[0][0]
prev_text = ''

for item in j2:
    index = item[0]
    text = item[1]

    if index < current_index:
        old_struct = struct.copy()
        struct = {}
        struct[text] = old_struct
    elif index == current_index and prev_text:
        struct[text] = struct[prev_text].copy()
    else:
        struct[text] = {}

    prev_text = text
    current_index = index

#print(struct)

s = {'html': {
        'body': {
            'div': {
                'label': {
                    'tr': {},
                    'td': {},
                    'th': {}
                }
            },
            'span': {
                'label': {
                    'tr': {},
                    'td': {},
                    'th': {}
                }
            }
        }
    }}

def paths(tree, cur=()):
    if not tree:
        yield cur
    else:
        for n, s in tree.items():
            for path in paths(s, cur+(n,)):
                yield path

print(list(paths(struct)))


