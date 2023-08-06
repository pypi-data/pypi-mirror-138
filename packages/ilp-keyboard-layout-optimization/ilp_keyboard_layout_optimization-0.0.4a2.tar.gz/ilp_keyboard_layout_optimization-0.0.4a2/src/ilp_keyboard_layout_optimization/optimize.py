"""This module provides the CLI for the application.

At the moment it is only possible to call it via:

$ pip install .
Processing /home/bjorn/code/ilp_keyboard_layout_optimization
  Installing build dependencies ... done
[...]
Successfully installed ilp-keyboard-layout-optimization-0.0.1
$ python -m ilp_keyboard_layout_optimization.optimize

We might add command line parameters at a later time. For now please edit the main
function at the very bottom of this file to change inputs.
"""
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
            or (char == "n" and pos == Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME))
            or (char == "r" and pos == Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME))
        ):
            _linear_costs[char, pos] = 0.0
            continue
        _linear_costs[char, pos] = 1.0

    for (char, char_2, pos, pos_2) in optimization_problem.quad_char_pos_assigns_keys:
        if (
            char == "u"
            and pos == Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME)
            and char_2 == "i"
            and pos_2 == Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME)
        ) or (
            char == "i"
            and pos == Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME)
            and char_2 == "a"
            and pos_2 == Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME)
        ):
            _quad_costs[char, char_2, pos, pos_2] = 0.0
            continue
        _quad_costs[char, char_2, pos, pos_2] = 1.0
    return _linear_costs, _quad_costs


if __name__ == "__main__":
    test_chars = Chars("uiaenr")
    test_poss = Positions(
        (
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME),
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME),
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME),
        )
    )
    optimization_model = KeyboardOptimization(test_chars, test_poss.poss)
    linear_costs, quad_costs = prepare_costs(optimization_model)
    optimization_model.set_up_model(linear_costs, quad_costs)
    print(optimization_model.solve())
