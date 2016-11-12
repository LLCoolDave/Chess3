from ChessboardUtils import MockBoard, MockPiece, MockArmy, ARMY_WHITE, ARMY_BLACK
from Chess3 import Coordinate


def test_deep_copy_empty_board():
    cb = MockBoard()
    copy = cb.deep_copy()
    assert isinstance(copy.black_army, MockArmy)
    assert isinstance(copy.white_army, MockArmy)


def test_deep_copy_pieces():
    cb = MockBoard((MockPiece, ARMY_WHITE, Coordinate(3, 5)), (MockPiece, ARMY_BLACK, Coordinate(2, 6)))
    cb.get_piece(Coordinate(2, 6)).king = True
    copy = cb.deep_copy()
    assert copy.get_piece(Coordinate(3, 5)) is not None
    assert copy.get_piece(Coordinate(2, 6)) is not None
    assert copy.get_piece(Coordinate(3, 5)).color == ARMY_WHITE
    assert copy.get_piece(Coordinate(2, 6)).color == ARMY_BLACK
    assert copy.get_piece(Coordinate(2, 6)).coord == Coordinate(2, 6)
    assert not copy.get_field(Coordinate(2, 6)).is_empty()
    assert copy.get_piece(Coordinate(2, 6)).is_king()
    assert copy.black_army.pieces == [copy.get_piece(Coordinate(2, 6))]
    assert copy.black_army.kings == [copy.get_piece(Coordinate(2, 6))]
