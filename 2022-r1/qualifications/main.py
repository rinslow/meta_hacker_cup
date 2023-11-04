import dataclasses
from typing import Optional
import copy

import tqdm as tqdm

Matrix = str
TREE = '^'
EMPTY = '.'
ROCK = "#"

DIRECTIONS = ((0, -1), (0, 1), (-1, 0), (1, 0))  # delta_row, delta_column


@dataclasses.dataclass
class Case:
    r: int
    c: int
    m: Matrix  # matrix

    def get(self, r, c):
        return self.m[r * self.c + c]

    # Returns a new Case with a given value at the given row and column.
    def mutate(self, r: int, c: int, v: str) -> "Case":
        assert 0 <= r < self.r and 0 <= c < self.c, f"Row or column is out of the matrix bounds. r={r}, c={c}"
        assert len(v) == 1, f"New value must be a single character. v={v}"

        i = r * self.c + c
        m = self.m[:i] + v + self.m[i + 1:]
        return dataclasses.replace(self, m=m)

    def __repr__(self):
        return f"{self.__class__.__name__}(r={self.r!r}, c={self.c!r}, m={self.m!r})"

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c and self.m == other.m

    def __hash__(self):
        return hash((self.r, self.c, self.m))


def cases_from_input(_in):
    cases = _in.readline()
    for _ in range(int(cases)):
        r, c = map(int, _in.readline().split())
        m = ''
        for _ in range(r):
            _in_line = _in.readline().rstrip()  # remove \n
            m += _in_line
        yield Case(r, c, m)


def empty(case: Case, r: int, c: int) -> bool:
    return case.get(r, c) == EMPTY


def tree(case: Case, r: int, c: int) -> bool:
    return case.get(r, c) == TREE


def rock(case: Case, r: int, c: int) -> bool:
    return case.get(r, c) == ROCK


def neighbors(case: Case, r: int, c: int):
    for dr, dc in DIRECTIONS:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < case.r and 0 <= new_c < case.c:
            yield new_r, new_c


def count_tree_neighbors(case: Case, r: int, c: int) -> int:
    return sum(1 for n in neighbors(case, r, c) if tree(case, *n))


def is_lonely_tree(case: Case, r: int, c: int):
    return tree(case, r, c) and count_tree_neighbors(case, r, c) < 2


def cells_r_c(case: Case):
    for r in range(case.r):
        for c in range(case.c):
            yield r, c


def any_lonely_tree(case: Case):
    return any(is_lonely_tree(case, r, c) for r, c in cells_r_c(case))


def lonely_trees(case: Case):
    return ((r, c) for r, c in cells_r_c(case) if is_lonely_tree(case, r, c))


def mutate(case: Case, r: int, c: int, v: str) -> Case:
    i = r * case.r + c
    m = case.m[:i] + v + case.m[i + 1:]
    return dataclasses.replace(case, m=m)


def solution(case: Case) -> Optional[Matrix]:
    if not any_lonely_tree(case):
        return case.m  # Solution found

    candidate_frontier = [case]
    transposition_set = set()  # Prevent transposition-loops

    while candidate_frontier:
        candidate_case = candidate_frontier.pop()  # Heuristic function can be installed on a PQ here
        lonely_trees_in_candidate = list(lonely_trees(candidate_case))

        if not lonely_trees_in_candidate:
            return candidate_case.m  # Solution found!

        transposition_set.add(candidate_case.m)

        # Assertion: there is at least one lonely tree
        for r, c in lonely_trees_in_candidate:
            for nr, nc in neighbors(candidate_case, r, c):
                if tree(candidate_case, nr, nc):
                    continue  # Nothing to mutate

                new_case = candidate_case.mutate(nr, nc, TREE)

                if new_case.m in transposition_set:
                    continue

                if new_case not in candidate_frontier:
                    candidate_frontier.append(new_case)

    return None  # All candidates exhausted


def main(_in, _out):
    for i, case in tqdm.tqdm(list(enumerate(cases_from_input(_in)))):
        s = solution(case)
        print(f"{i} / 100")
        is_possible = s is not None
        possibility = "Impossible" if not is_possible else "Possible"
        _out.write(f"Case #{i + 1}: {possibility}\n")

        if is_possible:
            for r in range(case.r):
                _out.write(s[r * case.c:(r + 1) * case.c] + "\n")


if __name__ == '__main__':
    with open('../../input.txt', 'rt') as _in, open('../../output.txt', 'wt') as _out:
        main(_in=_in, _out=_out)
