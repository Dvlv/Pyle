import pytest
from pyle import pyle

def test_is_selector():
    assert(pyle.is_selector('love:\n') == True)
    assert(pyle.is_selector('love\n') == False)
    assert(pyle.is_selector('border: 1px solid grey') == False)

def test_is_comment():
    assert(pyle.is_comment('; comment') == True)
    assert(pyle.is_comment(': not comment') == False)
    assert(pyle.is_comment('# not comment') == False)

def test_num_of_spaces():
    assert(pyle.num_of_spaces('    four') == 4)
    assert(pyle.num_of_spaces('  ') == 2)
    assert(pyle.num_of_spaces('  tw     o') == 2)

def test_build_tree_no_nest():
    sel_list = list(reversed([[0,'body'], [2,'div'], [4,'span']]))
    expected = {'body': {'div': {'span': {}}}}
    fail = {
        'body': {},
        'div': {},
        'span': {}
    }
    assert(pyle.build_tree(sel_list) == expected)
    assert(pyle.build_tree(sel_list) != fail)

def test_build_tree_nest():
    sel_list = list(reversed([[0, 'body'], [2, 'div'], [2, 'span'], [4, 'label'], [6, 'tr'], [6, 'td']]))
    expected = {
        'body': {
            'div': {
                'label': {
                    'tr': {},
                    'td': {}
                }
            },
            'span': {
                'label': {
                    'tr': {},
                    'td': {}
                }
            }
        }
    }

    fail = {'body': {}, 'div': {}, 'span': {}, 'label': {}, 'tr': {}, 'td': {}}

    assert(pyle.build_tree(sel_list) == expected)
    assert(pyle.build_tree(sel_list) != fail)

def test_selector_list_from_tree_no_nest():
    tree = {'body': {'div': {'span':{}}}}
    assert(pyle.selector_list_from_tree(tree) == [('body', 'div', 'span')])

def test_selector_list_from_tree_nest():
    tree = {
        'body': {
            'div': {
                'label': {
                    'tr': {},
                    'td': {}
                }
            },
            'span': {
                'label': {
                    'tr': {},
                    'td': {}
                }
            }
        }
    }
    expected = [
        ('body', 'div', 'label', 'tr'),
        ('body', 'div', 'label', 'td'),
        ('body', 'span', 'label', 'tr'),
        ('body', 'span', 'label', 'td')
    ]

    fail = [('body', 'span', 'label', 'tr'),
            ('body', 'div', 'label', 'td'),
            ('body', 'span', 'label', 'tr'),
            ('body', 'span', 'label', 'td')
    ]

    actual = pyle.selector_list_from_tree(tree)
    assert(sorted(actual) == sorted(expected))
    assert(sorted(actual) != sorted(fail))

def test_create_selector_string_no_nest():
    prev_selectors = ['html', '  body', '    div', '      label']
    actual = pyle.create_selector_string(prev_selectors, 0)
    expected = ('html body div label {\n', False)

    assert (actual == expected)

def test_create_selector_string_nest():
    prev_selectors = ['html', '  body', '    div,', '    span', '      label']
    actual = pyle.create_selector_string(prev_selectors, 0)
    expected = ('html body div label, \nhtml body span label {\n', False)

    assert (actual == expected)
