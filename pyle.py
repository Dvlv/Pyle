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

def write_css_dec(prev_selectors, prev_styles):
  #remove prev selectors with equal or more indents
    my_spaces = num_of_spaces(prev_selectors[-1][0])
    for old_select in prev_selectors[:-1]:
        if num_of_spaces(old_select[0]) >= my_spaces:
            prev_selectors.remove(old_select)

    #now fix double nesting
    prev_spaces = 999999999999
    for selector in reversed(prev_selectors):
        my_spaces = num_of_spaces(selector[0])
        if my_spaces < prev_spaces:
            prev_spaces = my_spaces
        else:
            prev_selectors.remove(selector)
         #   print(my_spaces < prev_spaces)

    #print selector chain
    selector_string = ''
    double_close = False
    for selector in prev_selectors:
        if selector[0].strip().startswith('@media'):
            my_spaces = num_of_spaces(selector[0])
            width = selector[0].strip().split()[1]
            if width == 'mobile':
                selector[0] = (' '*my_spaces) + '@media (max-width: 420px)'
            elif width == 'tablet':
                selector[0] = (' '*my_spaces) + '@media (max-width: 800px)'
            elif width.isdigit():
                selector[0] = (' '*my_spaces) + '@media (max-width: ' + width +'px)'
            selector_string = selector[0].strip() + ' {\n ' + selector_string
            double_close = True
        elif selector[0].strip().startswith('&') or selector[0].strip().startswith(':'):
            noAmp = selector[0].strip().replace('&','')
            selector_string += noAmp
        else:
            selector_string = selector_string + ' ' + selector[0].strip()
    selector_string = selector_string.strip()
    selector_string += ' { \n'

    #print style chain
    corrected_styles = []
    for style in prev_styles:
        halves = re.match(STYLE_REGEX, style)
        if halves is not None:
            style_value = style[len(halves.group(0)):-1]
            style_type = '  ' + halves.group(0).strip()
            if double_close:
                style_type = '  ' + style_type
            corrected_styles.append(style_type + ': ' + style_value + ';\n')

    style_string = ''.join(corrected_styles)
    end_string = '} \n'
    if double_close:
        end_string = '  }\n' + end_string

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

    if prev_selectors and prev_styles:
        if not prev_styles[-1].endswith('\n'):
            prev_styles[-1] = prev_styles[-1] + '\n'
        write_css_dec(prev_selectors, prev_styles)

def parse_main(main_file):
    with open(main_file, 'r') as mf:
        for line in mf:
            if line.startswith('@import'):
                yield line.split()[1]


for pyleFile in parse_main(sys.argv[1]):
    compile(pyleFile)

CSS_FILE.close()
