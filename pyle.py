#!/usr/bin/env python3
import sys
import re
import argparse
import collections

COLON = ':\n'
COMMA = ',\n'
STYLE_REGEX = re.compile('\s*[\w\-]+\s')
SPACES_REGEX = re.compile('^\s*')

custom_vars = {}

def is_selector(line):
    return line.endswith(COLON) or line.endswith(COMMA)

def is_comment(line):
    return line.startswith(';')

def num_of_spaces(line):
    spaces = re.search(SPACES_REGEX, line)
    if spaces.group(0) is not None:
        num_spaces = len(spaces.group(0))
    else:
        num_spaces = 0

    return num_spaces

def create_selector_list(prev_selectors):
    hierarchy_list = [[num_of_spaces(prev_selector), prev_selector] for prev_selector in prev_selectors]
    hierarchy_list = sorted(hierarchy_list, key=lambda x: x[0])

    reversed_list = list(reversed(hierarchy_list))

    tree = build_tree(reversed_list)

    selector_list = selector_list_from_tree(tree)

    return selector_list


def build_tree(hierarchy):
    struct = {}
    current_index = hierarchy[0][0]
    prev_text = ''

    for item in hierarchy:
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

    return struct

def selector_list_from_tree(struct):

    def paths(tree, cur=()):
        if not tree:
            yield cur
        else:
            for n, s in tree.items():
                for path in paths(s, cur+(n,)):
                    yield path

    return list(paths(struct))


def create_selector_string(prev_selectors, minified):
    #remove prev selectors with more indents
    my_spaces = num_of_spaces(prev_selectors[-1])
    for index, old_select in enumerate(prev_selectors[:-1]):
        if num_of_spaces(old_select) >= my_spaces and not old_select.endswith(','):
            prev_selectors.remove(old_select)

    #now fix double nesting
    prev_spaces = 999999999999
    list_length = len(prev_selectors)
    for index, selector in enumerate(reversed(prev_selectors)):
        my_spaces = num_of_spaces(selector)
        offset = index + 1
        original_index = list_length - offset

        if my_spaces < prev_spaces:
            prev_spaces = my_spaces
        else:
            if not selector.endswith(','):
                del prev_selectors[original_index]

    selector_string = ''
    double_close = False

    prev_selectors_list = create_selector_list(prev_selectors)
    num_selector_strings = len(prev_selectors_list)

    for prev_selectors in prev_selectors_list:
        for selector in prev_selectors:
            if selector.endswith(','):
                selector = selector[:-1]

            if selector.strip().startswith('@media'):
                if double_close:
                    #already written media declaration, so indent and skip
                    selector_string = selector_string.replace ('\n', '\n  ')
                    continue
                my_spaces = num_of_spaces(selector)
                width = selector.strip().split()[1]
                if width == 'mobile':
                    if minified:
                        selector = '@media(max-width:420px)'
                    else:
                        selector = (' '*my_spaces) + '@media (max-width: 420px)'
                elif width == 'tablet':
                    if minified:
                        selector = '@media(max-width:800px)'
                    else:
                        selector = (' '*my_spaces) + '@media (max-width: 800px)'
                elif width.isdigit():
                    if minified:
                        selector = '@media(max-width:' + width + 'px)'
                    else:
                        selector = (' '*my_spaces) + '@media (max-width: ' + width + 'px)'
                if minified:
                    selector_string = selector.strip() + '{' + selector_string.strip()
                else:
                    if num_selector_strings > 1:
                        selector_string = selector.strip() + ' {\n' + selector_string
                    else:
                        selector_string = selector.strip() + ' {\n  ' + selector_string
                double_close = True
            elif selector.strip().startswith('&') or selector.strip().startswith(':'):
                noAmp = selector.strip().replace('&','')
                selector_string += noAmp
            else:
                if not selector_string or selector_string[-1] == '\n':
                    selector_string = selector_string + selector.strip()
                else:
                    selector_string = selector_string + ' ' + selector.strip()
        if num_selector_strings > 1:
            if minified:
                selector_string = selector_string.strip() + ','
            else:
                selector_string = selector_string.strip() + ', \n'

    if num_selector_strings > 1:
        if minified:
            selector_string = selector_string.strip()[:-1] + '{'
        else:
            selector_string = selector_string.strip()[:-1] + ' {\n'
    else:
        if minified:
            selector_string += '{'
        else:
            selector_string = selector_string + ' {\n'

    return selector_string, double_close
        #return selector_string, double_close


def write_css_dec(prev_selectors, prev_styles, CSS_FILE, minified):

    selector_string, double_close = create_selector_string(prev_selectors, minified)

    #print style chain
    corrected_styles = []
    for style in prev_styles:
        halves = re.match(STYLE_REGEX, style)
        if halves is not None:
            style_value = style[len(halves.group(0)):-1]
            if style_value in custom_vars:
                style_value = custom_vars[style_value]
            if minified:
                style_type = halves.group(0).strip()
            else:
                style_type = '  ' + halves.group(0).strip()
            if double_close and not minified:
                style_type = '  ' + style_type
            if minified:
                corrected_styles.append(style_type + ':' + style_value + ';')
            else:
                corrected_styles.append(style_type + ': ' + style_value + ';\n')

    style_string = ''.join(corrected_styles)
    if minified:
        end_string = '}'
    else:
        end_string = '}\n'
    if double_close:
        if minified:
            end_string = '}' + end_string
        else:
            end_string = '  }\n' + end_string

    CSS_FILE.write(selector_string + style_string + end_string)

def compile(filename, CSS_FILE, minified):
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

            if is_comment(line):
                # dont need to put these in the css i don't imagine
                continue

            if is_selector(line):
#                    print('i am ' + line + ' before me was a ' + str(prev_line) + ' and my prev selects are ' + str(prev_selectors))
                if (prev_line == 'style' or prev_line == 'blank') and len(prev_selectors) > 0:
                    write_css_dec(prev_selectors, prev_styles, CSS_FILE, minified)
                    prev_styles = []
                #keep comma, strip newline and colon
                if line.endswith(COMMA):
                    selector_string = line[:-1]
                else:
                    selector_string = line[:-2]
                prev_selectors.append(selector_string)
                prev_line = 'selector'
            elif line == '\n':
                write_css_dec(prev_selectors, prev_styles, CSS_FILE, minified)
                prev_selectors = []
                prev_styles = []
                prev_line = 'blank'
            else:
                prev_styles.append(line)
                prev_line = 'style'

    if prev_selectors and prev_styles:
        if not prev_styles[-1].endswith('\n'):
            prev_styles[-1] = prev_styles[-1] + '\n'
        write_css_dec(prev_selectors, prev_styles, CSS_FILE, minified)

def parse_main(main_file):
    global custom_vars

    with open(main_file, 'r') as mf:
        for index, line in enumerate(mf, start=1):
            if line.startswith('def'):
                var_pieces = line.split()
                if len(var_pieces) == 3:
                    custom_vars['@' + str(var_pieces[1])] = str(var_pieces[2])
                else:
                    if len(var_pieces) > 1:
                        var_name = var_pieces[1]
                        print('variable "{}" declared incorrectly, please use "def varname value"'.format(var_name))
                    else:
                        print('skipping empty def on line {}, please remove'.format(index))
            elif line.startswith('@import'):
                yield line.split()[1]

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--main_file', help='Your main file which imports your individual styling files (default main.pyle)', type=str, default="main.pyle")
    parser.add_argument('-c', '--css_file', help='The name of the css file to write to (default style.css)', type=str, default="style.css")
    parser.add_argument('-m', '--minified', help='create minified file', type=bool, default=False)
    args = parser.parse_args()

    return args

def main():
    args = handle_args()

    CSS_FILE = open(args.css_file, 'w')

    for pyle_file in parse_main(args.main_file):
        compile(pyle_file, CSS_FILE, args.minified)

    CSS_FILE.close()

if __name__ == '__main__':
    main()
