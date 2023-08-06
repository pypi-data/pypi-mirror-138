import pytest

from ilp_keyboard_layout_optimization.data_aquisition.chars import Chars
from ilp_keyboard_layout_optimization.data_aquisition.positions import Positions
from ilp_keyboard_layout_optimization.ilp import KeyboardOptimization
from ilp_keyboard_layout_optimization.type_aliases import (
    Col,
    LinCosts,
    Mod,
    Pos,
    QuadCosts,
    Row,
    Side,
)


@pytest.fixture(scope="session")
def custom_quadratic_costs():
    def prepare_costs(
        optimization_problem: KeyboardOptimization,
    ) -> tuple[LinCosts, QuadCosts]:
        """Prepare the linear and quadratic costs for the provided assignment problem

        Parameters
        ----------
        optimization_problem : KeyboardOptimization
            The assignment problem to solve

        Returns
        -------
        tuple[LinCosts, QuadCosts]
            the costs corresponding to the assignment problem
        """
        _linear_costs = {}
        _quad_costs = {}
        for (char, pos) in optimization_problem.char_pos_assigns_keys:
            if (
                (char == "u" and pos == Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME))
            ):
                _linear_costs[char, pos] = 0.0
                continue
            _linear_costs[char, pos] = 1.0

        for (
            char,
            char_2,
            pos,
            pos_2,
        ) in optimization_problem.quad_char_pos_assigns_keys:
            if (
                (
                    char == "u"
                    and pos == Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME)
                    and char_2 == "i"
                    and pos_2 == Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME)
                )
                or (
                    char == "i"
                    and pos == Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME)
                    and char_2 == "a"
                    and pos_2 == Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME)
                )
                or (
                    char == "a"
                    and pos == Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME)
                    and char_2 == "e"
                    and pos_2 == Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME)
                )
            ):
                _quad_costs[char, char_2, pos, pos_2] = 0.0
                continue
            _quad_costs[char, char_2, pos, pos_2] = 1.0
        return _linear_costs, _quad_costs

    return prepare_costs


@pytest.fixture(scope="session")
def custom_linear_costs():
    def prepare_costs(
        optimization_problem: KeyboardOptimization,
    ) -> tuple[LinCosts, QuadCosts]:
        """Prepare the linear and quadratic costs for the provided assignment problem

        Parameters
        ----------
        optimization_problem : KeyboardOptimization
            The assignment problem to solve

        Returns
        -------
        tuple[LinCosts, QuadCosts]
            the costs corresponding to the assignment problem
        """
        _linear_costs = {}
        _quad_costs = {}
        for (char, pos) in optimization_problem.char_pos_assigns_keys:
            if (
                (char == "i" and pos == Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME))
                or (
                    char == "a"
                    and pos == Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME)
                )
                or (
                    char == "e" and pos == Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME)
                )
                or (
                    char == "n"
                    and pos == Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME)
                )
                or (
                    char == "r"
                    and pos == Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME)
                )
                or (
                    char == "t" and pos == Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.HOME)
                )
            ):
                _linear_costs[char, pos] = 0.0
                continue
            _linear_costs[char, pos] = 1.0

        for (
            char,
            char_2,
            pos,
            pos_2,
        ) in optimization_problem.quad_char_pos_assigns_keys:
            _quad_costs[char, char_2, pos, pos_2] = 0.0
        return _linear_costs, _quad_costs

    return prepare_costs


@pytest.fixture(scope="session")
def eight_custom_chars():
    return Chars("aeiunrtd")


@pytest.fixture(scope="session")
def four_custom_chars():
    return Chars("aeiu")


@pytest.fixture(scope="session")
def eight_custom_poss():
    return Positions(
        (
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME),
        )
    ).poss


@pytest.fixture(scope="session")
def four_custom_poss():
    return Positions(
        (
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME),
        )
    ).poss


@pytest.fixture(scope="session")
def custom_model(eight_custom_chars, eight_custom_poss):
    return KeyboardOptimization(eight_custom_chars, eight_custom_poss)


def test_optimization(custom_model, custom_linear_costs):
    linear_costs, quad_costs = custom_linear_costs(custom_model)
    custom_model.set_up_model(linear_costs, quad_costs)
    solution_str = custom_model.solve()
    assert f"('u', {Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME)}" in str(solution_str)
    assert f"('i', {Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME)}" in str(solution_str)
    assert f"('a', {Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME)}" in str(
        solution_str
    )
    assert f"('e', {Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME)}" in str(solution_str)
    assert f"('n', {Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME)}" in str(
        solution_str
    )
    assert f"('r', {Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME)}" in str(
        solution_str
    )
    assert f"('t', {Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.HOME)}" in str(solution_str)
    assert f"('d', {Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME)}" in str(
        solution_str
    )
    print(solution_str)
