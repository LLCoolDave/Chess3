import pytest
from collections import Counter

from Chess3 import MovementUtils, Coordinate
from ChessboardUtils import MockBoard, MockPiece, ARMY_WHITE, ARMY_BLACK


@pytest.mark.parametrize(['origin', 'row_delta', 'column_delta', 'expected'], [
    (Coordinate(3, 3), 0, 0, Coordinate(3, 3)),
    (Coordinate(3, 3), 1, 0, Coordinate(4, 3)),
    (Coordinate(3, 3), -1, 0, Coordinate(2, 3)),
    (Coordinate(3, 3), 0, 1, Coordinate(3, 4)),
    (Coordinate(3, 3), 0, -1, Coordinate(3, 2)),
    (Coordinate(3, 3), 1, 1, Coordinate(4, 4)),
    (Coordinate(0, 0), -1, 0, None),
    (Coordinate(0, 0), 0, -1, None),
    (Coordinate(0, 0), -1, -1, None),
    (Coordinate(7, 7), 1, 0, None),
    (Coordinate(7, 7), 0, 1, None),
    (Coordinate(7, 7), 1, 1, None),
])
def test_MovementUtils_get_relative_coord(origin, row_delta, column_delta, expected):
    assert MovementUtils.get_relative_coord(origin, row_delta, column_delta) == expected


@pytest.mark.parametrize(['origin', 'target', 'expected'], [
    (Coordinate(3, 3), Coordinate(3, 3), (0, 0)),
    (Coordinate(3, 3), Coordinate(4, 3), (1, 0)),
    (Coordinate(3, 3), Coordinate(2, 3), (-1, 0)),
    (Coordinate(3, 3), Coordinate(3, 4), (0, 1)),
    (Coordinate(3, 3), Coordinate(3, 2), (0, -1)),
    (Coordinate(3, 3), Coordinate(4, 4), (1, 1)),
    (Coordinate(2, 3), Coordinate(3, 3), (1, 0)),
    (Coordinate(4, 3), Coordinate(3, 3), (-1, 0)),
    (Coordinate(3, 2), Coordinate(3, 3), (0, 1)),
    (Coordinate(3, 4), Coordinate(3, 3), (0, -1)),
    (Coordinate(2, 2), Coordinate(3, 3), (1, 1)),
])
def test_MovementUtils_get_deltas(origin, target, expected):
    assert MovementUtils.get_deltas(origin, target) == expected


@pytest.mark.parametrize(['origin', 'expected'], [
    (Coordinate.from_string('C3'), ['A2', 'A4', 'B1', 'B5', 'D1', 'D5', 'E2', 'E4']),
    (Coordinate.from_string('A1'), ['B3', 'C2']),
    (Coordinate.from_string('H8'), ['G6', 'F7']),
])
def test_MovementUtils_possible_knight_moves(origin, expected):
    assert Counter(MovementUtils.possible_knight_moves(origin)) == Counter(map(Coordinate.from_string, expected))


@pytest.mark.parametrize(['origin', 'pieces', 'row_delta', 'column_delta', 'may_capture', 'expected'], [
    ('D3', ((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')),), 0, 0, True, []),
    ('D3', ((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')),), -1, 0, True, [MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('D2')),
                                                                                   MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('D1'))]),
    ('D3', ((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')),), 1, 1, True, [MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('E4')),
                                                                                  MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('F5')),
                                                                                  MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('G6')),
                                                                                  MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('H7'))]),
    ('D3', ((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')),
            (MockPiece, ARMY_WHITE, Coordinate.from_string('G6')),), 1, 1, True, [MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('E4')),
                                                                                  MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('F5'))]),
    ('D3', ((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')),
            (MockPiece, ARMY_BLACK, Coordinate.from_string('G6')),), 1, 1, False, [MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('E4')),
                                                                                   MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('F5'))]),
    ('D3', ((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')),
            (MockPiece, ARMY_BLACK, Coordinate.from_string('G6')),), 1, 1, True, [MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('E4')),
                                                                                  MovementUtils.move_from_to(Coordinate.from_string('D3'), Coordinate.from_string('F5')),
                                                                                  MovementUtils.move_and_capture(Coordinate.from_string('D3'), Coordinate.from_string('G6'))]),
])
def test_MovementUtils_move_until_obstructed(origin, pieces, row_delta, column_delta, may_capture, expected):
    cb = MockBoard(*pieces)
    piece = cb.get_piece(Coordinate.from_string(origin))
    assert Counter(MovementUtils.move_until_obstructed(piece, row_delta, column_delta, may_capture)) == Counter(expected)


def test_MovementUtils_multimove_until_obstructed():
    cb = MockBoard((MockPiece, ARMY_WHITE, Coordinate.from_string('D3')))
    piece = cb.get_piece(Coordinate.from_string('D3'))
    assert Counter(MovementUtils.multimove_until_obstructed(piece, [(1, 1)])) == Counter(MovementUtils.multimove_until_obstructed(piece, [(1, 1), (1, 1)]))


@pytest.mark.parametrize(['origin', 'expected'], [
    (Coordinate.from_string('C3'), ['B2', 'B3', 'B4', 'C2', 'C4', 'D2', 'D3', 'D4']),
    (Coordinate.from_string('A1'), ['A2', 'B1', 'B2']),
    (Coordinate.from_string('H8'), ['G7', 'G8', 'H7']),
])
def test_MovementUtils_possible_king_moves(origin, expected):
    assert Counter(MovementUtils.possible_king_moves(origin)) == Counter(map(Coordinate.from_string, expected))


def test_MovementUtils_move_from_to_name():
    assert MovementUtils.move_from_to(Coordinate(1, 1), Coordinate(3, 3)).name == 'move'
    assert MovementUtils.move_from_to(Coordinate(1, 1), Coordinate(3, 3), 'blub').name == 'blub'


def test_MovementUtils_move_and_capture_name():
    assert MovementUtils.move_and_capture(Coordinate(1, 1), Coordinate(3, 3)).name == 'move'
    assert MovementUtils.move_and_capture(Coordinate(1, 1), Coordinate(3, 3), 'blub').name == 'blub'