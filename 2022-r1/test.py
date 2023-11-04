from main import Case, cases_from_input, count_tree_neighbors, main, any_lonely_tree, solution
from io import StringIO


def sample_input1():
    return StringIO('''\
3
1 3
.^.
3 1
.
.
.
4 4
..^.
..^.
....
...^''')


def sample_input2():
    return StringIO('''\
3
1 3
.^.
3 1
.
#
#
4 4
..^.
.#^#
....
...^
''')


def test_get():
    case = Case(r=4, c=4, m=('.' '.' '^' '.'
                             '.' '.' '^' '.'
                             '.' '.' '.' '.'
                             '.' '.' '.' '^'))

    assert case.get(0, 0) == '.'
    assert case.get(0, 1) == '.'
    assert case.get(0, 2) == '^'
    assert case.get(0, 3) == '.'
    assert case.get(1, 0) == '.'
    assert case.get(1, 1) == '.'
    assert case.get(1, 2) == '^'
    assert case.get(1, 3) == '.'
    assert case.get(2, 0) == '.'
    assert case.get(2, 1) == '.'
    assert case.get(2, 2) == '.'
    assert case.get(2, 3) == '.'
    assert case.get(3, 0) == '.'
    assert case.get(3, 1) == '.'
    assert case.get(3, 2) == '.'
    assert case.get(3, 3) == '^'


def test_cases_from_input():
    _in = sample_input1()

    l = list(cases_from_input(_in))
    assert len(l) == 3
    assert l[0] == Case(r=1, c=3, m='.' '^' '.')
    assert l[1] == Case(r=3, c=1, m='.' '.' '.')
    assert l[2] == Case(r=4, c=4, m=('.' '.' '^' '.'
                                     '.' '.' '^' '.'
                                     '.' '.' '.' '.'
                                     '.' '.' '.' '^'))


def test_count_tree_neighbors():
    m = ('.' '^' '.'
         '.' '^' '^'
         '.' '.' '.')

    assert count_tree_neighbors(Case(m=m, r=3, c=3), 0, 0) == 1
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 0, 1) == 1
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 0, 2) == 2
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 1, 0) == 1
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 1, 1) == 2
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 1, 2) == 1
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 2, 0) == 0
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 2, 1) == 1
    assert count_tree_neighbors(Case(m=m, r=3, c=3), 2, 2) == 1


def test_mutate_start():
    m = ('.' '^' '.'
         '.' '^' '^'
         '.' '.' '.')
    mutated = Case(m=m, r=3, c=3).mutate(0, 0, '^')
    assert mutated.m == ('^' '^' '.'
                         '.' '^' '^'
                         '.' '.' '.')
    assert mutated.r == 3
    assert mutated.c == 3


def test_mutate_end():
    m = ('.^'
         '.^'
         '..')

    mutated = Case(m=m, r=3, c=2).mutate(2, 1, '^')

    assert mutated.m == ('.^'
                         '.^'
                         '.^')


def test_any_lonely_tree__single_row():
    assert any_lonely_tree(Case(m='.' '^' '.', r=1, c=3))


def test_any_lonely_tree__empty():
    assert not any_lonely_tree(Case(m='', r=0, c=0))


def test_any_lonely_tree__given_example():
    case = list(cases_from_input(sample_input1()))[-1]
    assert any_lonely_tree(case)


def no_lonely_tree__2x2():
    assert not any_lonely_tree(Case(m='^^'
                                      '^^', r=2, c=2))


def no_lonely_tree__2x3():
    assert not any_lonely_tree(Case(m='^^.'
                                      '^^.', r=2, c=3))


def test_solution__impossible_3x1():
    assert solution(Case(m='.^.', r=3, c=1)) is None


def test_solution__only_solution_2x2():
    s = solution(Case(m='.^'
                        '^.',
                      r=2, c=2))

    assert s == ('^^'
                 '^^')


def test_solution__empty_2x2():
    s = solution(Case(m='..'
                        '..',
                      r=2, c=2))

    assert s == ('..'
                 '..')


def test_solution_from_problem():
    _in = sample_input1()
    cases = list(cases_from_input(_in))
    case = cases[-1]
    s = solution(case)
    assert s is not None
    assert not any_lonely_tree(Case(r=case.r, c=case.c, m=s))


def test_solution_sample_input_with_rocks():
    _in = sample_input2()
    cases = list(cases_from_input(_in))
    case = cases[-1]
    s = solution(case)
    assert s is not None
    assert not any_lonely_tree(Case(r=case.r, c=case.c, m=s))
