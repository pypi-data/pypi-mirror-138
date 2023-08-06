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
from ilp_keyboard_layout_optimization.ilp import KeyboardOptimization
from ilp_keyboard_layout_optimization.type_aliases import LinCosts, QuadCosts


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
    for (char, pos) in optimization_problem.char_key_assigns_keys:
        if (
            (char == "u" and pos == "left_pinky_home")
            or (char == "n" and pos == "right_index_home")
            or (char == "r" and pos == "right_middle_home")
            or (char == "t" and pos == "right_ring_home")
            or (char == "d" and pos == "right_pinky_home")
        ):
            _linear_costs[char, pos] = 0.0
            continue
        _linear_costs[char, pos] = 1.0

    for (char, char_2, pos, pos_2) in optimization_problem.quad_char_key_assigns_keys:
        if (
            (
                char == "u"
                and pos == "left_pinky_home"
                and char_2 == "i"
                and pos_2 == "left_middle_home"
            )
            or (
                char == "i"
                and pos == "left_middle_home"
                and char_2 == "a"
                and pos_2 == "left_index_home"
            )
            or (
                char == "a"
                and pos == "left_index_home"
                and char_2 == "e"
                and pos_2 == "left_ring_home"
            )
        ):
            _quad_costs[char, char_2, pos, pos_2] = 0.0
            continue
        _quad_costs[char, char_2, pos, pos_2] = 1.0
    return _linear_costs, _quad_costs


if __name__ == "__main__":
    test_chars = Chars(("a", "e", "i", "u", "n", "r", "t", "d"))
    test_poss = (
        "left_pinky_home",
        "left_ring_home",
        "left_middle_home",
        "left_index_home",
        "right_index_home",
        "right_middle_home",
        "right_ring_home",
        "right_pinky_home",
    )
    optimization_model = KeyboardOptimization(test_chars, test_poss)
    linear_costs, quad_costs = prepare_costs(optimization_model)
    optimization_model.set_up_model(linear_costs, quad_costs)
    optimization_model.solve()
