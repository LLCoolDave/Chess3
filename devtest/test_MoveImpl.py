from Chess3.MoveImpl import Coordinate, MoveAction, Move


def test_Coordinate_equals():
    a = Coordinate(1, 2)
    b = Coordinate(1, 3)
    c = Coordinate(1, 2)

    assert a != b
    assert b != c
    assert a == c


def test_MoveAction_equals():
    a = Coordinate(1, 2)
    b = Coordinate(2, 2)
    c = Coordinate(2, 1)

    assert MoveAction(a, a) == MoveAction(a, a)
    assert MoveAction(a, b) == MoveAction(a, b)
    assert MoveAction(a, b) != MoveAction(b, a)
    assert MoveAction(a, b) != MoveAction(a, c)
    assert MoveAction(a, b) != MoveAction(c, b)


def test_Move_equals():
    a = Coordinate(1, 2)
    b = Coordinate(2, 2)
    c = Coordinate(2, 1)

    d = MoveAction(a, b)
    e = MoveAction(a, c)

    assert Move('blub', a, a, [], []) == Move('blub', a, a, [], [])
    assert Move('blub', a, a, [], []) == Move('blub', a, b, [], [])
    assert Move('blub', a, a, [], []) != Move('blub', a, a, [], [], False)
    assert Move('blub', a, a, [], []) != Move('blub', b, a, [], [])
    assert Move('blub', a, a, [], []) != Move('blub', a, a, [], [a])
    assert Move('blub', a, a, [], [a]) != Move('blub', a, a, [], [])
    assert Move('blub', a, a, [], [a, b]) != Move('blub', a, a, [], [b, a])
    assert Move('blub', a, a, [d], []) != Move('blub', a, a, [], [])
    assert Move('blub', a, a, [], []) != Move('blub', a, a, [d], [])
    assert Move('blub', a, a, [d, e], []) != Move('blub', a, a, [e, d], [])


def test_Coordinate_repr():
    assert str(Coordinate(0, 0)) == 'A1'
    assert str(Coordinate(7, 7)) == 'H8'
    assert Coordinate.from_string('A1') == Coordinate(0, 0)
    assert Coordinate.from_string('H8') == Coordinate(7, 7)
    assert Coordinate.from_string('B6') == Coordinate(5, 1)
    assert Coordinate.from_string('H1') == Coordinate(0, 7)
    assert Coordinate.from_string(str(Coordinate(4, 2))) == Coordinate(4, 2)
