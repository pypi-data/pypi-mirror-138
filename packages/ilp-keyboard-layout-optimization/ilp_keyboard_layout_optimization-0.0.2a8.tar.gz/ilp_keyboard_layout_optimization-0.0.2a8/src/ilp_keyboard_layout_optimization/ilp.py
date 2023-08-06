"""The actual implementation of the quadratic optimization problem."""
from itertools import chain, permutations, product
from typing import Iterable

from pyscipopt import Model, quicksum

from .data_aquisition.chars import Chars
from .type_aliases import (
    CharPosPair,
    CharPosQuadruple,
    LinCosts,
    LinVars,
    PosTuple,
    QuadCosts,
    QuadVars,
)


class KeyboardOptimization:
    """Instances of this class represent instances of the keyboard layout QAP

    The IP variant of an optimization of character to key assignments can be modeled
    as a so-called quadratic assignment problem (QAP). The task is to assign a set of
    characters to a set of keys on a keyboard. The way in which they should be
    arranged has to meet certain criteria such as for instance: characters that are
    often typed after one another should not be assigned to positions, that are supposed
    to be pressed by the same finger.

    Parameters
    ----------
    chars : CharTuple
        the (special) characters to be assign
    poss: PosTuple
        the positions to which we want to assign the (special) characters
    """

    chars: Chars
    poss: PosTuple

    def __init__(self, chars: Chars, poss: PosTuple):
        assert len(chars.monos) == len(poss)
        self.chars = chars
        self.poss = poss
        self.char_pos_assigns: LinVars = {}
        self.quad_char_pos_assigns: QuadVars = {}
        self.char_pos_costs: LinCosts = {}
        self.quad_char_pos_costs: QuadCosts = {}
        self.model: Model = Model("Keyboard Layout Optimization")

    def set_up_model(self, char_key_costs: LinCosts, quad_char_key_costs: QuadCosts):
        """Set up all the variables and initialize the costs for the SCIP model"""
        for (char, key) in self.char_key_assigns_keys:
            self.char_pos_assigns[char, key] = self.model.addVar(
                name=f"{key}={char}", vtype="B"
            )
        for (char, char_2, key, key_2) in self.quad_char_key_assigns_keys:
            self.quad_char_pos_assigns[char, char_2, key, key_2] = self.model.addVar(
                name=f"{key}={char}_and_{key_2}={char_2}", vtype="C", lb=0, ub=1
            )
        assert len(quad_char_key_costs) == len(self.quad_char_pos_assigns)
        assert len(char_key_costs) == len(self.char_pos_assigns)
        self.char_pos_costs = char_key_costs
        self.quad_char_pos_costs = quad_char_key_costs

        constr = {}
        for char in self.chars.monos:
            self.model.addCons(
                quicksum(self.char_pos_assigns[char, key] for key in self.poss) == 1,
                f"AllCharacterAssignedOnce({char})",
            )
            for (key, key_2) in self.key_pairs:
                self.model.addCons(
                    quicksum(
                        self.quad_char_pos_assigns[char, char_2, key, key_2]
                        for char_2 in self.chars.monos
                        if char_2 != char
                    )
                    <= self.char_pos_assigns[char, key],
                    f"QuadCharacterAssignedLEQThanPosition({char},{key},{key_2})",
                )
                self.model.addCons(
                    quicksum(
                        self.quad_char_pos_assigns[char_2, char, key_2, key]
                        for char_2 in self.chars.monos
                        if char_2 != char
                    )
                    <= self.char_pos_assigns[char, key],
                    f"QuadCharacterAssignedLEQThanSecondPosition({char},{key_2},{key})",
                )
            for char_2 in self.chars.monos:
                for key in self.poss:
                    if char_2 != char:
                        self.model.addCons(
                            quicksum(
                                self.quad_char_pos_assigns[char, char_2, key, key_2]
                                for key_2 in self.poss
                                if key_2 != key
                            )
                            <= self.char_pos_assigns[char, key],
                            f"QuadCharacterAssignedLEQThanCharacter({char},{char_2},"
                            f"{key})",
                        )
                        self.model.addCons(
                            quicksum(
                                self.quad_char_pos_assigns[char_2, char, key_2, key]
                                for key_2 in self.poss
                                if key_2 != key
                            )
                            <= self.char_pos_assigns[char, key],
                            f"QuadCharacterAssignedLEQThanSecondCharacter({char_2},"
                            f"{char},{key})",
                        )

        for (char, char_2, key, key_2) in self.quad_char_key_assigns_keys:
            self.model.addCons(
                self.char_pos_assigns[char, key] + self.char_pos_assigns[char_2, key_2]
                <= 1 + self.quad_char_pos_assigns[char, char_2, key, key_2],
                f"IntegrableQuadAssign({char},{key_2},{key})",
            )

        for key in self.poss:
            constr[key] = self.model.addCons(
                quicksum(self.char_pos_assigns[char, key] for char in self.chars.monos)
                == 1,
                f"AllPositionsAssignedOnce({key})",
            )

        self.model.setObjective(
            quicksum(
                costs * assigns
                for (costs, assigns) in zip(
                    self.char_pos_costs.values(), self.char_pos_assigns.values()
                )
            )
            + quicksum(
                costs * assigns
                for (costs, assigns) in zip(
                    self.quad_char_pos_costs.values(),
                    self.quad_char_pos_assigns.values(),
                )
            ),
            "minimize",
        )

    def solve(self, visualize: bool = True):
        """Actually solve the optimization problem

        Parameters
        ----------
        visualize : bool, optional
            If True (default), the result will be shown after finishing
        """
        self.model.optimize()
        if visualize:
            self.visualize_solution()

    def visualize_solution(self):
        """Rudimentary visualize the optimization result on the console"""
        solution_assignments = []
        for (char, key) in self.char_key_assigns_keys:
            print(
                f"({char}, {key}): "
                f"{self.model.getVal(self.char_pos_assigns[char, key])}, "
                f"cost: {self.char_pos_costs[char, key]}"
            )
            if self.model.getVal(self.char_pos_assigns[char, key]) == 1:
                solution_assignments.append((char, key))

        assert "('u', 'left_pinky_home')" in str(solution_assignments)
        # assert "('a', 'left_middle_home')" in str(solution_assignments)
        # assert "('e', 'left_index_home')" in str(solution_assignments)
        # assert "('i', 'left_ring_home')" in str(solution_assignments)
        assert "('a', 'left_index_home')" in str(solution_assignments)
        assert "('e', 'left_ring_home')" in str(solution_assignments)
        assert "('i', 'left_middle_home')" in str(solution_assignments)
        assert "('n', 'right_index_home')" in str(solution_assignments)
        assert "('r', 'right_middle_home')" in str(solution_assignments)
        assert "('t', 'right_ring_home')" in str(solution_assignments)
        assert "('d', 'right_pinky_home')" in str(solution_assignments)

        print(f"{str(solution_assignments)}")

    @property
    def char_key_assigns_keys(self) -> Iterable[CharPosPair]:
        """An iterator for the pairs of (special) characters and corresponding keys"""
        return product(self.chars.monos, self.poss)

    @property
    def quad_char_key_assigns_keys(self) -> Iterable[CharPosQuadruple]:
        """An iterator for quadruples of character pairs and corresponding key pairs"""
        flattened_tuple_of_quads = chain.from_iterable(
            chain.from_iterable(
                product(permutations(self.chars.monos, 2), permutations(self.poss, 2))
            )
        )
        iter_of_quads = (iter(flattened_tuple_of_quads),) * 4
        return zip(*iter_of_quads)

    @property
    def key_pairs(self) -> Iterable:
        """An iterator for all pairs of keys that are possible"""
        return permutations(self.poss, 2)
