from Chess3 import Chessboard, Coordinate, MovementUtils, MoveAction
from ChessboardUtils import MockBoard, MockPiece, ARMY_WHITE, ARMY_BLACK


def test_Chessboard_Field_linked():
    cb = Chessboard()
    for x in range(8):
        for y in range(8):
            assert cb is cb.get_field(Coordinate(x, y)).chessboard


def test_Chessboard_execute_move():
    cb = MockBoard((MockPiece, ARMY_WHITE, Coordinate(3, 5)), (MockPiece, ARMY_BLACK, Coordinate(2, 6)))
    white_piece = cb.get_piece(Coordinate(3, 5))
    black_piece = cb.get_piece(Coordinate(2, 6))
    move = MovementUtils.move_and_capture(Coordinate(3, 5), Coordinate(2, 6))
    cb.execute_move(move)
    assert white_piece.coord == Coordinate(2, 6)
    assert black_piece.field is None
    assert white_piece is cb.get_piece(Coordinate(2, 6))
    assert len(cb.black_army.pieces) == 0


def test_Chessboard_execute_move_swap_pieces():
    cb = MockBoard((MockPiece, ARMY_WHITE, Coordinate(3, 5)), (MockPiece, ARMY_BLACK, Coordinate(2, 6)))
    white_piece = cb.get_piece(Coordinate(3, 5))
    black_piece = cb.get_piece(Coordinate(2, 6))
    move = MovementUtils.move_from_to(Coordinate(3, 5), Coordinate(2, 6))
    move.movements.append(MoveAction(Coordinate(2, 6), Coordinate(3, 5)))
    cb.execute_move(move)
    assert white_piece.coord == Coordinate(2, 6)
    assert black_piece.coord == Coordinate(3, 5)
    assert white_piece is cb.get_piece(Coordinate(2, 6))
    assert black_piece is cb.get_piece(Coordinate(3, 5))


def test_Chessboard_execute_move_sideffect_move():
    cb = MockBoard((MockPiece, ARMY_WHITE, Coordinate(3, 5)), (MockPiece, ARMY_BLACK, Coordinate(2, 6)))
    white_piece = cb.get_piece(Coordinate(3, 5))
    black_piece = cb.get_piece(Coordinate(2, 6))
    move = MovementUtils.move_from_to(Coordinate(3, 5), Coordinate(2, 6))
    white_piece.movement_callback = lambda x: [MovementUtils.move_from_to(Coordinate(2, 6), Coordinate(2, 7))]
    cb.execute_move(move)
    assert white_piece is cb.get_piece(Coordinate(2, 6))
    assert black_piece is cb.get_piece(Coordinate(2, 7))


def test_Chessboard_execute_move_sideffect_capture():
    cb = MockBoard((MockPiece, ARMY_WHITE, Coordinate(3, 5)), (MockPiece, ARMY_BLACK, Coordinate(2, 6)), (MockPiece, ARMY_BLACK, Coordinate(2, 7)))
    white_piece = cb.get_piece(Coordinate(3, 5))
    black_piece1 = cb.get_piece(Coordinate(2, 6))
    black_piece2 = cb.get_piece(Coordinate(2, 7))
    move = MovementUtils.move_and_capture(Coordinate(3, 5), Coordinate(2, 6))
    black_piece1.capture_callback = lambda x: [MovementUtils.move_from_to(Coordinate(2, 7), Coordinate(2, 4))]
    cb.execute_move(move)
    assert white_piece is cb.get_piece(Coordinate(2, 6))
    assert black_piece2 is cb.get_piece(Coordinate(2, 4))
