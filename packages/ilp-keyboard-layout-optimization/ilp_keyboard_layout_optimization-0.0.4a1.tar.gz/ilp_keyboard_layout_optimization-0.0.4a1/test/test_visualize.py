from hypothesis import given
from hypothesis.strategies import characters as chrs

from ilp_keyboard_layout_optimization.type_aliases import Col, Mod, Pos, Row, Side
from ilp_keyboard_layout_optimization.visualize import make_layer_strs


def test_make_layer_strs_function():
    assert make_layer_strs


def test_make_layer_strs_len():
    assert len(make_layer_strs({})) == 3023


def test_make_layer_strs_all_modifiers_there():
    layout_string = make_layer_strs({})
    for mod in Mod:
        if mod.name == "NONE":
            assert "UNMODIFIED" in layout_string
        else:
            assert mod.name in layout_string
    print(layout_string)


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_unmodified_upper(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.UPPER): char0,
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.UPPER): char1,
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.UPPER): char2,
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.UPPER): char3,
            Pos(Side.LEFT, Mod.NONE, Col.INNERMOST, Row.UPPER): char4,
            Pos(Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.UPPER): char5,
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.UPPER): char6,
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.UPPER): char7,
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.UPPER): char8,
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.UPPER): char9,
        },
    )
    assert (
        f"|  ⇥  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|  ←  |" in layout_string
    )


@given(
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
)
def test_make_layer_strs_with_unmodified_home(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9, char10
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME): char0,
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME): char1,
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME): char2,
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME): char3,
            Pos(Side.LEFT, Mod.NONE, Col.INNERMOST, Row.HOME): char4,
            Pos(Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.HOME): char5,
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME): char6,
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME): char7,
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.HOME): char8,
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME): char9,
            Pos(Side.RIGHT, Mod.NONE, Col.OUTERMOST, Row.HOME): char10,
        },
    )
    assert (
        f"|  ⎈  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|  {char10}  |" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_unmodified_lower(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.LOWER): char0,
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.LOWER): char1,
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.LOWER): char2,
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.LOWER): char3,
            Pos(Side.LEFT, Mod.NONE, Col.INNERMOST, Row.LOWER): char4,
            Pos(Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.LOWER): char5,
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.LOWER): char6,
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.LOWER): char7,
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.LOWER): char8,
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.LOWER): char9,
        },
    )
    assert (
        f"|  ⇧  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        "|  ⇧  |" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_shifted_upper(
    char_1, char_2, char_3, char_4, char_5, char_6, char_7, char_8, char_9, char_0
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.SHIFT, Col.PINKY, Row.UPPER): char_1,
            Pos(Side.LEFT, Mod.SHIFT, Col.RING, Row.UPPER): char_2,
            Pos(Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.UPPER): char_3,
            Pos(Side.LEFT, Mod.SHIFT, Col.INDEX, Row.UPPER): char_4,
            Pos(Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.UPPER): char_5,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.UPPER): char_6,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.UPPER): char_7,
            Pos(Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.UPPER): char_8,
            Pos(Side.RIGHT, Mod.SHIFT, Col.RING, Row.UPPER): char_9,
            Pos(Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.UPPER): char_0,
        },
    )
    assert (
        f"|  ⇥  |  {char_1}  |  {char_2}  |  {char_3}  |  {char_4}  |  {char_5}  "
        f"|     |  {char_6}  |  {char_7}  |  {char_8}  |  {char_9}  |  {char_0}  "
        f"|  ←  |" in layout_string
    )


@given(
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
)
def test_make_layer_strs_with_shifted_home(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9, char10
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.SHIFT, Col.PINKY, Row.HOME): char0,
            Pos(Side.LEFT, Mod.SHIFT, Col.RING, Row.HOME): char1,
            Pos(Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.HOME): char2,
            Pos(Side.LEFT, Mod.SHIFT, Col.INDEX, Row.HOME): char3,
            Pos(Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.HOME): char4,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.HOME): char5,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.HOME): char6,
            Pos(Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.HOME): char7,
            Pos(Side.RIGHT, Mod.SHIFT, Col.RING, Row.HOME): char8,
            Pos(Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.HOME): char9,
            Pos(Side.RIGHT, Mod.SHIFT, Col.OUTERMOST, Row.HOME): char10,
        },
    )
    assert (
        f"|  ⎈  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|  {char10}  |" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_shifted_lower(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.SHIFT, Col.PINKY, Row.LOWER): char0,
            Pos(Side.LEFT, Mod.SHIFT, Col.RING, Row.LOWER): char1,
            Pos(Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.LOWER): char2,
            Pos(Side.LEFT, Mod.SHIFT, Col.INDEX, Row.LOWER): char3,
            Pos(Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.LOWER): char4,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.LOWER): char5,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.LOWER): char6,
            Pos(Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.LOWER): char7,
            Pos(Side.RIGHT, Mod.SHIFT, Col.RING, Row.LOWER): char8,
            Pos(Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.LOWER): char9,
        },
    )
    assert (
        f"|  ⇧  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        "|  ⇧  |" in layout_string
    )


@given(
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
)
def test_make_layer_strs_with_lower_home(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9, char10
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.LOWER, Col.PINKY, Row.HOME): char0,
            Pos(Side.LEFT, Mod.LOWER, Col.RING, Row.HOME): char1,
            Pos(Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.HOME): char2,
            Pos(Side.LEFT, Mod.LOWER, Col.INDEX, Row.HOME): char3,
            Pos(Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.HOME): char4,
            Pos(Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.HOME): char5,
            Pos(Side.RIGHT, Mod.LOWER, Col.INDEX, Row.HOME): char6,
            Pos(Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.HOME): char7,
            Pos(Side.RIGHT, Mod.LOWER, Col.RING, Row.HOME): char8,
            Pos(Side.RIGHT, Mod.LOWER, Col.PINKY, Row.HOME): char9,
            Pos(Side.RIGHT, Mod.LOWER, Col.OUTERMOST, Row.HOME): char10,
        },
    )
    assert (
        f"|  ⇕  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|  {char10}  |" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_lower_lower(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.LOWER, Col.PINKY, Row.LOWER): char0,
            Pos(Side.LEFT, Mod.LOWER, Col.RING, Row.LOWER): char1,
            Pos(Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.LOWER): char2,
            Pos(Side.LEFT, Mod.LOWER, Col.INDEX, Row.LOWER): char3,
            Pos(Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.LOWER): char4,
            Pos(Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.LOWER): char5,
            Pos(Side.RIGHT, Mod.LOWER, Col.INDEX, Row.LOWER): char6,
            Pos(Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.LOWER): char7,
            Pos(Side.RIGHT, Mod.LOWER, Col.RING, Row.LOWER): char8,
            Pos(Side.RIGHT, Mod.LOWER, Col.PINKY, Row.LOWER): char9,
        },
    )
    assert (
        f"|  ⎇  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        "|AltGr|" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_upper_upper(
    char_1, char_2, char_3, char_4, char_5, char_6, char_7, char_8, char_9, char_0
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.UPPER, Col.PINKY, Row.UPPER): char_1,
            Pos(Side.LEFT, Mod.UPPER, Col.RING, Row.UPPER): char_2,
            Pos(Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.UPPER): char_3,
            Pos(Side.LEFT, Mod.UPPER, Col.INDEX, Row.UPPER): char_4,
            Pos(Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.UPPER): char_5,
            Pos(Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.UPPER): char_6,
            Pos(Side.RIGHT, Mod.UPPER, Col.INDEX, Row.UPPER): char_7,
            Pos(Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.UPPER): char_8,
            Pos(Side.RIGHT, Mod.UPPER, Col.RING, Row.UPPER): char_9,
            Pos(Side.RIGHT, Mod.UPPER, Col.PINKY, Row.UPPER): char_0,
        },
    )
    assert (
        f"|  ⇥  |  {char_1}  |  {char_2}  |  {char_3}  |  {char_4}  |  {char_5}  "
        f"|     |  {char_6}  |  {char_7}  |  {char_8}  |  {char_9}  |  {char_0}  "
        f"|  ⌦  |" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_upper_home(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    assert (
        f"|  ⎈  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|  ⇕  |"
        in make_layer_strs(
            {
                Pos(Side.LEFT, Mod.UPPER, Col.PINKY, Row.HOME): char0,
                Pos(Side.LEFT, Mod.UPPER, Col.RING, Row.HOME): char1,
                Pos(Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.HOME): char2,
                Pos(Side.LEFT, Mod.UPPER, Col.INDEX, Row.HOME): char3,
                Pos(Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.HOME): char4,
                Pos(Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.HOME): char5,
                Pos(Side.RIGHT, Mod.UPPER, Col.INDEX, Row.HOME): char6,
                Pos(Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.HOME): char7,
                Pos(Side.RIGHT, Mod.UPPER, Col.RING, Row.HOME): char8,
                Pos(Side.RIGHT, Mod.UPPER, Col.PINKY, Row.HOME): char9,
            },
        )
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_upper_lower(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    assert (
        f"|  ⇧  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        "|AltGr|"
        in make_layer_strs(
            {
                Pos(Side.LEFT, Mod.UPPER, Col.PINKY, Row.LOWER): char0,
                Pos(Side.LEFT, Mod.UPPER, Col.RING, Row.LOWER): char1,
                Pos(Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.LOWER): char2,
                Pos(Side.LEFT, Mod.UPPER, Col.INDEX, Row.LOWER): char3,
                Pos(Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.LOWER): char4,
                Pos(Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.LOWER): char5,
                Pos(Side.RIGHT, Mod.UPPER, Col.INDEX, Row.LOWER): char6,
                Pos(Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.LOWER): char7,
                Pos(Side.RIGHT, Mod.UPPER, Col.RING, Row.LOWER): char8,
                Pos(Side.RIGHT, Mod.UPPER, Col.PINKY, Row.LOWER): char9,
            },
        )
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_nav_upper(
    char_1, char_2, char_3, char_4, char_5, char_6, char_7, char_8, char_9, char_0
):
    layout_string = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.NAV, Col.PINKY, Row.UPPER): char_1,
            Pos(Side.LEFT, Mod.NAV, Col.RING, Row.UPPER): char_2,
            Pos(Side.LEFT, Mod.NAV, Col.MIDDLE, Row.UPPER): char_3,
            Pos(Side.LEFT, Mod.NAV, Col.INDEX, Row.UPPER): char_4,
            Pos(Side.LEFT, Mod.NAV, Col.INNERMOST, Row.UPPER): char_5,
            Pos(Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.UPPER): char_6,
            Pos(Side.RIGHT, Mod.NAV, Col.INDEX, Row.UPPER): char_7,
            Pos(Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.UPPER): char_8,
            Pos(Side.RIGHT, Mod.NAV, Col.RING, Row.UPPER): char_9,
            Pos(Side.RIGHT, Mod.NAV, Col.PINKY, Row.UPPER): char_0,
        },
    )
    assert (
        f"|  ⇥  |  {char_1}  |  {char_2}  |  {char_3}  |  {char_4}  |  {char_5}  "
        f"|     |  {char_6}  |  {char_7}  |  {char_8}  |  {char_9}  |  {char_0}  "
        f"|  ←  |" in layout_string
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_nav_home(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    assert (
        f"|     |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|     |"
        in make_layer_strs(
            {
                Pos(Side.LEFT, Mod.NAV, Col.PINKY, Row.HOME): char0,
                Pos(Side.LEFT, Mod.NAV, Col.RING, Row.HOME): char1,
                Pos(Side.LEFT, Mod.NAV, Col.MIDDLE, Row.HOME): char2,
                Pos(Side.LEFT, Mod.NAV, Col.INDEX, Row.HOME): char3,
                Pos(Side.LEFT, Mod.NAV, Col.INNERMOST, Row.HOME): char4,
                Pos(Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.HOME): char5,
                Pos(Side.RIGHT, Mod.NAV, Col.INDEX, Row.HOME): char6,
                Pos(Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.HOME): char7,
                Pos(Side.RIGHT, Mod.NAV, Col.RING, Row.HOME): char8,
                Pos(Side.RIGHT, Mod.NAV, Col.PINKY, Row.HOME): char9,
            },
        )
    )


@given(chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs(), chrs())
def test_make_layer_strs_with_nav_lower(
    char0, char1, char2, char3, char4, char5, char6, char7, char8, char9
):
    assert (
        f"|  ⇧  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        "|  ⇧  |"
        in make_layer_strs(
            {
                Pos(Side.LEFT, Mod.NAV, Col.PINKY, Row.LOWER): char0,
                Pos(Side.LEFT, Mod.NAV, Col.RING, Row.LOWER): char1,
                Pos(Side.LEFT, Mod.NAV, Col.MIDDLE, Row.LOWER): char2,
                Pos(Side.LEFT, Mod.NAV, Col.INDEX, Row.LOWER): char3,
                Pos(Side.LEFT, Mod.NAV, Col.INNERMOST, Row.LOWER): char4,
                Pos(Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.LOWER): char5,
                Pos(Side.RIGHT, Mod.NAV, Col.INDEX, Row.LOWER): char6,
                Pos(Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.LOWER): char7,
                Pos(Side.RIGHT, Mod.NAV, Col.RING, Row.LOWER): char8,
                Pos(Side.RIGHT, Mod.NAV, Col.PINKY, Row.LOWER): char9,
            },
        )
    )


@given(
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
    chrs(),
)
def test_make_layer_strs_with_all_positions_set_manually_randomly(
    char0,
    char1,
    char2,
    char3,
    char4,
    char5,
    char6,
    char7,
    char8,
    char9,
    char10,
    char11,
    char12,
    char13,
    char14,
    char15,
    char16,
    char17,
    char18,
    char19,
    char110,
    char20,
    char21,
    char22,
    char23,
    char24,
    char25,
    char26,
    char27,
    char28,
    char29,
    char_31,
    char_32,
    char_33,
    char_34,
    char_35,
    char_36,
    char_37,
    char_38,
    char_39,
    char_30,
    char40,
    char41,
    char42,
    char43,
    char44,
    char45,
    char46,
    char47,
    char48,
    char49,
    char410,
    char50,
    char51,
    char52,
    char53,
    char54,
    char55,
    char56,
    char57,
    char58,
    char59,
    char60,
    char61,
    char62,
    char63,
    char64,
    char65,
    char66,
    char67,
    char68,
    char69,
    char610,
    char70,
    char71,
    char72,
    char73,
    char74,
    char75,
    char76,
    char77,
    char78,
    char79,
    char8_1,
    char8_2,
    char8_3,
    char8_4,
    char8_5,
    char8_6,
    char8_7,
    char8_8,
    char8_9,
    char8_0,
    char90,
    char91,
    char92,
    char93,
    char94,
    char95,
    char96,
    char97,
    char98,
    char99,
    char100,
    char101,
    char102,
    char103,
    char104,
    char105,
    char106,
    char107,
    char108,
    char109,
    char11_1,
    char11_2,
    char11_3,
    char11_4,
    char11_5,
    char11_6,
    char11_7,
    char11_8,
    char11_9,
    char11_0,
    char120,
    char121,
    char122,
    char123,
    char124,
    char125,
    char126,
    char127,
    char128,
    char129,
    char130,
    char131,
    char132,
    char133,
    char134,
    char135,
    char136,
    char137,
    char138,
    char139,
):
    layout = make_layer_strs(
        {
            Pos(Side.LEFT, Mod.NAV, Col.PINKY, Row.LOWER): char130,
            Pos(Side.LEFT, Mod.NAV, Col.RING, Row.LOWER): char131,
            Pos(Side.LEFT, Mod.NAV, Col.MIDDLE, Row.LOWER): char132,
            Pos(Side.LEFT, Mod.NAV, Col.INDEX, Row.LOWER): char133,
            Pos(Side.LEFT, Mod.NAV, Col.INNERMOST, Row.LOWER): char134,
            Pos(Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.LOWER): char135,
            Pos(Side.RIGHT, Mod.NAV, Col.INDEX, Row.LOWER): char136,
            Pos(Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.LOWER): char137,
            Pos(Side.RIGHT, Mod.NAV, Col.RING, Row.LOWER): char138,
            Pos(Side.RIGHT, Mod.NAV, Col.PINKY, Row.LOWER): char139,
            Pos(Side.LEFT, Mod.LOWER, Col.PINKY, Row.HOME): char60,
            Pos(Side.LEFT, Mod.LOWER, Col.RING, Row.HOME): char61,
            Pos(Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.HOME): char62,
            Pos(Side.LEFT, Mod.LOWER, Col.INDEX, Row.HOME): char63,
            Pos(Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.HOME): char64,
            Pos(Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.HOME): char65,
            Pos(Side.RIGHT, Mod.LOWER, Col.INDEX, Row.HOME): char66,
            Pos(Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.HOME): char67,
            Pos(Side.RIGHT, Mod.LOWER, Col.RING, Row.HOME): char68,
            Pos(Side.RIGHT, Mod.LOWER, Col.PINKY, Row.HOME): char69,
            Pos(Side.RIGHT, Mod.LOWER, Col.OUTERMOST, Row.HOME): char610,
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.UPPER): char0,
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.UPPER): char1,
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.UPPER): char2,
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.UPPER): char3,
            Pos(Side.LEFT, Mod.NONE, Col.INNERMOST, Row.UPPER): char4,
            Pos(Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.UPPER): char5,
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.UPPER): char6,
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.UPPER): char7,
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.UPPER): char8,
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.UPPER): char9,
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.HOME): char10,
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.HOME): char11,
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.HOME): char12,
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.HOME): char13,
            Pos(Side.LEFT, Mod.NONE, Col.INNERMOST, Row.HOME): char14,
            Pos(Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.HOME): char15,
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.HOME): char16,
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.HOME): char17,
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.HOME): char18,
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.HOME): char19,
            Pos(Side.LEFT, Mod.NAV, Col.PINKY, Row.HOME): char120,
            Pos(Side.LEFT, Mod.NAV, Col.RING, Row.HOME): char121,
            Pos(Side.LEFT, Mod.NAV, Col.MIDDLE, Row.HOME): char122,
            Pos(Side.LEFT, Mod.NAV, Col.INDEX, Row.HOME): char123,
            Pos(Side.LEFT, Mod.NAV, Col.INNERMOST, Row.HOME): char124,
            Pos(Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.HOME): char125,
            Pos(Side.RIGHT, Mod.NAV, Col.INDEX, Row.HOME): char126,
            Pos(Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.HOME): char127,
            Pos(Side.RIGHT, Mod.NAV, Col.RING, Row.HOME): char128,
            Pos(Side.RIGHT, Mod.NAV, Col.PINKY, Row.HOME): char129,
            Pos(Side.LEFT, Mod.NAV, Col.PINKY, Row.UPPER): char11_1,
            Pos(Side.LEFT, Mod.NAV, Col.RING, Row.UPPER): char11_2,
            Pos(Side.LEFT, Mod.NAV, Col.MIDDLE, Row.UPPER): char11_3,
            Pos(Side.LEFT, Mod.NAV, Col.INDEX, Row.UPPER): char11_4,
            Pos(Side.LEFT, Mod.NAV, Col.INNERMOST, Row.UPPER): char11_5,
            Pos(Side.RIGHT, Mod.NAV, Col.INNERMOST, Row.UPPER): char11_6,
            Pos(Side.RIGHT, Mod.NAV, Col.INDEX, Row.UPPER): char11_7,
            Pos(Side.RIGHT, Mod.NAV, Col.MIDDLE, Row.UPPER): char11_8,
            Pos(Side.RIGHT, Mod.NAV, Col.RING, Row.UPPER): char11_9,
            Pos(Side.RIGHT, Mod.NAV, Col.PINKY, Row.UPPER): char11_0,
            Pos(Side.RIGHT, Mod.NONE, Col.OUTERMOST, Row.HOME): char110,
            Pos(Side.LEFT, Mod.NONE, Col.PINKY, Row.LOWER): char20,
            Pos(Side.LEFT, Mod.NONE, Col.RING, Row.LOWER): char21,
            Pos(Side.LEFT, Mod.NONE, Col.MIDDLE, Row.LOWER): char22,
            Pos(Side.LEFT, Mod.NONE, Col.INDEX, Row.LOWER): char23,
            Pos(Side.LEFT, Mod.NONE, Col.INNERMOST, Row.LOWER): char24,
            Pos(Side.RIGHT, Mod.NONE, Col.INNERMOST, Row.LOWER): char25,
            Pos(Side.RIGHT, Mod.NONE, Col.INDEX, Row.LOWER): char26,
            Pos(Side.RIGHT, Mod.NONE, Col.MIDDLE, Row.LOWER): char27,
            Pos(Side.RIGHT, Mod.NONE, Col.RING, Row.LOWER): char28,
            Pos(Side.RIGHT, Mod.NONE, Col.PINKY, Row.LOWER): char29,
            Pos(Side.LEFT, Mod.UPPER, Col.PINKY, Row.LOWER): char100,
            Pos(Side.LEFT, Mod.UPPER, Col.RING, Row.LOWER): char101,
            Pos(Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.LOWER): char102,
            Pos(Side.LEFT, Mod.UPPER, Col.INDEX, Row.LOWER): char103,
            Pos(Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.LOWER): char104,
            Pos(Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.LOWER): char105,
            Pos(Side.RIGHT, Mod.UPPER, Col.INDEX, Row.LOWER): char106,
            Pos(Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.LOWER): char107,
            Pos(Side.RIGHT, Mod.UPPER, Col.RING, Row.LOWER): char108,
            Pos(Side.RIGHT, Mod.UPPER, Col.PINKY, Row.LOWER): char109,
            Pos(Side.LEFT, Mod.UPPER, Col.PINKY, Row.HOME): char90,
            Pos(Side.LEFT, Mod.UPPER, Col.RING, Row.HOME): char91,
            Pos(Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.HOME): char92,
            Pos(Side.LEFT, Mod.UPPER, Col.INDEX, Row.HOME): char93,
            Pos(Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.HOME): char94,
            Pos(Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.HOME): char95,
            Pos(Side.RIGHT, Mod.UPPER, Col.INDEX, Row.HOME): char96,
            Pos(Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.HOME): char97,
            Pos(Side.RIGHT, Mod.UPPER, Col.RING, Row.HOME): char98,
            Pos(Side.RIGHT, Mod.UPPER, Col.PINKY, Row.HOME): char99,
            Pos(Side.LEFT, Mod.UPPER, Col.PINKY, Row.UPPER): char8_1,
            Pos(Side.LEFT, Mod.UPPER, Col.RING, Row.UPPER): char8_2,
            Pos(Side.LEFT, Mod.UPPER, Col.MIDDLE, Row.UPPER): char8_3,
            Pos(Side.LEFT, Mod.UPPER, Col.INDEX, Row.UPPER): char8_4,
            Pos(Side.LEFT, Mod.UPPER, Col.INNERMOST, Row.UPPER): char8_5,
            Pos(Side.RIGHT, Mod.UPPER, Col.INNERMOST, Row.UPPER): char8_6,
            Pos(Side.RIGHT, Mod.UPPER, Col.INDEX, Row.UPPER): char8_7,
            Pos(Side.RIGHT, Mod.UPPER, Col.MIDDLE, Row.UPPER): char8_8,
            Pos(Side.RIGHT, Mod.UPPER, Col.RING, Row.UPPER): char8_9,
            Pos(Side.RIGHT, Mod.UPPER, Col.PINKY, Row.UPPER): char8_0,
            Pos(Side.LEFT, Mod.LOWER, Col.PINKY, Row.LOWER): char70,
            Pos(Side.LEFT, Mod.LOWER, Col.RING, Row.LOWER): char71,
            Pos(Side.LEFT, Mod.LOWER, Col.MIDDLE, Row.LOWER): char72,
            Pos(Side.LEFT, Mod.LOWER, Col.INDEX, Row.LOWER): char73,
            Pos(Side.LEFT, Mod.LOWER, Col.INNERMOST, Row.LOWER): char74,
            Pos(Side.RIGHT, Mod.LOWER, Col.INNERMOST, Row.LOWER): char75,
            Pos(Side.RIGHT, Mod.LOWER, Col.INDEX, Row.LOWER): char76,
            Pos(Side.RIGHT, Mod.LOWER, Col.MIDDLE, Row.LOWER): char77,
            Pos(Side.RIGHT, Mod.LOWER, Col.RING, Row.LOWER): char78,
            Pos(Side.RIGHT, Mod.LOWER, Col.PINKY, Row.LOWER): char79,
            Pos(Side.LEFT, Mod.SHIFT, Col.PINKY, Row.UPPER): char_31,
            Pos(Side.LEFT, Mod.SHIFT, Col.RING, Row.UPPER): char_32,
            Pos(Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.UPPER): char_33,
            Pos(Side.LEFT, Mod.SHIFT, Col.INDEX, Row.UPPER): char_34,
            Pos(Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.UPPER): char_35,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.UPPER): char_36,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.UPPER): char_37,
            Pos(Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.UPPER): char_38,
            Pos(Side.RIGHT, Mod.SHIFT, Col.RING, Row.UPPER): char_39,
            Pos(Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.UPPER): char_30,
            Pos(Side.LEFT, Mod.SHIFT, Col.PINKY, Row.HOME): char40,
            Pos(Side.LEFT, Mod.SHIFT, Col.RING, Row.HOME): char41,
            Pos(Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.HOME): char42,
            Pos(Side.LEFT, Mod.SHIFT, Col.INDEX, Row.HOME): char43,
            Pos(Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.HOME): char44,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.HOME): char45,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.HOME): char46,
            Pos(Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.HOME): char47,
            Pos(Side.RIGHT, Mod.SHIFT, Col.RING, Row.HOME): char48,
            Pos(Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.HOME): char49,
            Pos(Side.RIGHT, Mod.SHIFT, Col.OUTERMOST, Row.HOME): char410,
            Pos(Side.LEFT, Mod.SHIFT, Col.PINKY, Row.LOWER): char50,
            Pos(Side.LEFT, Mod.SHIFT, Col.RING, Row.LOWER): char51,
            Pos(Side.LEFT, Mod.SHIFT, Col.MIDDLE, Row.LOWER): char52,
            Pos(Side.LEFT, Mod.SHIFT, Col.INDEX, Row.LOWER): char53,
            Pos(Side.LEFT, Mod.SHIFT, Col.INNERMOST, Row.LOWER): char54,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INNERMOST, Row.LOWER): char55,
            Pos(Side.RIGHT, Mod.SHIFT, Col.INDEX, Row.LOWER): char56,
            Pos(Side.RIGHT, Mod.SHIFT, Col.MIDDLE, Row.LOWER): char57,
            Pos(Side.RIGHT, Mod.SHIFT, Col.RING, Row.LOWER): char58,
            Pos(Side.RIGHT, Mod.SHIFT, Col.PINKY, Row.LOWER): char59,
        },
    )
    assert (
        "\n    "
        "UNMODIFIED:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  |  {char0}  |  {char1}  |  {char2}  |  {char3}  |  {char4}  "
        f"|     |  {char5}  |  {char6}  |  {char7}  |  {char8}  |  {char9}  "
        f"|  ←  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎈  |  {char10}  |  {char11}  |  {char12}  |  {char13}  |  {char14}  "
        f"|     |  {char15}  |  {char16}  |  {char17}  |  {char18}  |  {char19}  "
        f"|  {char110}  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  |  {char20}  |  {char21}  |  {char22}  |  {char23}  |  {char24}  "
        f"|     |  {char25}  |  {char26}  |  {char27}  |  {char28}  |  {char29}  "
        "|  ⇧  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "SHIFT:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  |  {char_31}  |  {char_32}  |  {char_33}  |  {char_34}  |  {char_35}  "
        f"|     |  {char_36}  |  {char_37}  |  {char_38}  |  {char_39}  |  {char_30}  "
        f"|  ←  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎈  |  {char40}  |  {char41}  |  {char42}  |  {char43}  |  {char44}  "
        f"|     |  {char45}  |  {char46}  |  {char47}  |  {char48}  |  {char49}  "
        f"|  {char410}  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  |  {char50}  |  {char51}  |  {char52}  |  {char53}  |  {char54}  "
        f"|     |  {char55}  |  {char56}  |  {char57}  |  {char58}  |  {char59}  "
        "|  ⇧  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "LOWER:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        "| F1  | F2  | F3  | F4  | F5  | F6  |     | F7  | F8  | F9  | F10 | F11 "
        "| F12 |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇕  |  {char60}  |  {char61}  |  {char62}  |  {char63}  |  {char64}  "
        f"|     |  {char65}  |  {char66}  |  {char67}  |  {char68}  |  {char69}  "
        f"|  {char610}  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎇  |  {char70}  |  {char71}  |  {char72}  |  {char73}  |  {char74}  "
        f"|     |  {char75}  |  {char76}  |  {char77}  |  {char78}  |  {char79}  "
        "|AltGr|\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "UPPER:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  |  {char8_1}  |  {char8_2}  |  {char8_3}  |  {char8_4}  |  {char8_5}  "
        f"|     |  {char8_6}  |  {char8_7}  |  {char8_8}  |  {char8_9}  |  {char8_0}  "
        f"|  ⌦  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⎈  |  {char90}  |  {char91}  |  {char92}  |  {char93}  |  {char94}  "
        f"|     |  {char95}  |  {char96}  |  {char97}  |  {char98}  |  {char99}  "
        f"|  ⇕  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  |  {char100}  |  {char101}  |  {char102}  |  {char103}  |  {char104}  "
        f"|     |  {char105}  |  {char106}  |  {char107}  |  {char108}  |  {char109}  "
        "|AltGr|\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    \n    "
        "NAV:\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇥  |  {char11_1}  |  {char11_2}  |  {char11_3}  |  {char11_4}  "
        f"|  {char11_5}  |     |  {char11_6}  |  {char11_7}  |  {char11_8}  "
        f"|  {char11_9}  |  {char11_0}  |  ←  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|     |  {char120}  |  {char121}  |  {char122}  |  {char123}  |  {char124}  "
        f"|     |  {char125}  |  {char126}  |  {char127}  |  {char128}  |  {char129}  "
        f"|     |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        f"|  ⇧  |  {char130}  |  {char131}  |  {char132}  |  {char133}  |  {char134}  "
        f"|     |  {char135}  |  {char136}  |  {char137}  |  {char138}  |  {char139}  "
        "|  ⇧  |\n    "
        f"-------------------------------------     "
        f"-------------------------------------\n    "
        in layout
    )
