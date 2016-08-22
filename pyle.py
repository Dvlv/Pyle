import sys
import re

COLON = ':\n'
CSS_FILE = open('style.css', 'w')
STYLE_REGEX = re.compile('\s*[\w\-]+\s')
SPACES_REGEX = re.compile('^\s*')

def is_selector(line):
    if line.endswith(COLON):
        return True
    else:
        return False

def num_of_spaces(line):
    spaces = re.search(SPACES_REGEX, line)
    if spaces.group(0) is not None:
        num_spaces = len(spaces.group(0))
    else:
        num_spaces = 0

    return num_spaces

def handle_selector_line():
    pass


def handle_style_line(line):
    pass


def end_selectors(num, num_tabs=None):
    pass

def write_css_dec(prev_selectors, prev_styles):
    selector_string = ''
    for selector in prev_selectors:
        if selector.startswith('.') or selector.startswith('#'):
            selector_string += selector
        else:
            selector_string = selector_string + ' ' + selector
    selector_string += ' { \n'

    style_string = '\n'.join(prev_styles)
    end_string = '\n } \n'

    CSS_FILE.write(selector_string + style_string + end_string)

def compile(filename):
    num_selectors = 0
    prev_line = None
    prev_spaces = 0
    first_line = True
    indent_width = 0
    prev_selectors = []
    prev_styles = []
    with open(filename, 'r') as open_file:
            for line in open_file:
                if not first_line and indent_width == 0:
                        indent_width = num_of_spaces(line)
                if first_line:
                    first_line = False

                if is_selector(line):
                    if (prev_line == 'style' or prev_line == 'blank') and len(prev_selectors) > 0:
                        write_css_dec(prev_selectors, prev_styles)
                        prev_styles = []
                    selector_string = line[:-2]
                    prev_selectors.append(selector_string)
                elif line == '\n':
                    write_css_dec(prev_selectors, prev_styles)
                    prev_selectors = []
                    prev_styles = []
                    prev_line = 'blank'
                else:
                    prev_styles.append(line)
                    prev_line = 'style'

    return num_selectors



num_selectors = compile(sys.argv[1])
if num_selectors > 0:
    CSS_FILE.write('\n')
    end_selectors(num_selectors)
CSS_FILE.close()
