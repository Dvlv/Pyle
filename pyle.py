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
  #remove prev selectors with equal or more indents
    my_spaces = num_of_spaces(prev_selectors[-1][0])
    for old_select in prev_selectors[:-1]:
        if num_of_spaces(old_select[0]) >= my_spaces:
            prev_selectors.remove(old_select)

    #now fix double nesting
    prev_spaces = 999999999999 #will break if using over this many spaces. If you are, learn to style better
    for selector in reversed(prev_selectors):
        my_spaces = num_of_spaces(selector[0])
        if my_spaces < prev_spaces:
            prev_spaces = my_spaces
        else:
            prev_selectors.remove(selector)
         #   print(my_spaces < prev_spaces)

    #print selector chain
    selector_string = ''
    for selector in prev_selectors:
        if selector[0].strip().startswith('.') or selector[0].strip().startswith('#') or selector[0].strip().startswith(':'):
            selector_string += selector[0].strip()
        else:
            selector_string = selector_string + ' ' + selector[0].strip()
    selector_string = selector_string.strip()
    selector_string += ' { \n'

    #print style chain
    corrected_styles = []
    for style in prev_styles:
        halves = re.search(STYLE_REGEX, style)
        if halves.group(0) is not None:
            secondHalf = style[len(halves.group(0)):]
            firstHalf = '  ' + halves.group(0).strip()
            corrected_styles.append(firstHalf + ': ' + secondHalf)

    style_string = ''.join(corrected_styles)
    end_string = '} \n'

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
#                    print('i am ' + line + ' before me was a ' + str(prev_line) + ' and my prev selects are ' + str(prev_selectors))
                    if (prev_line == 'style' or prev_line == 'blank') and len(prev_selectors) > 0:
                        write_css_dec(prev_selectors, prev_styles)
                        prev_styles = []
                    selector_string = line[:-2]
                    prev_selectors.append([selector_string, num_of_spaces(line)])
                    prev_line = 'selector'
                elif line == '\n':
                    write_css_dec(prev_selectors, prev_styles)
                    prev_selectors = []
                    prev_styles = []
                    prev_line = 'blank'
                else:
                    prev_styles.append(line)
                    prev_line = 'style'

    return prev_selectors, prev_styles



prev_selectors, prev_styles = compile(sys.argv[1])
if prev_selectors and prev_styles:
    if not prev_styles[-1].endswith('\n'):
        prev_styles[-1] = prev_styles[-1] + '\n'
    write_css_dec(prev_selectors, prev_styles)
CSS_FILE.close()
