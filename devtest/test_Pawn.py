from ChessboardUtils import MockBoard, ARMY_WHITE, ARMY_BLACK, MockPiece
from Chess3 import Coordinate, MovementUtils, Move, MoveAction
from Chess3.Pieces.PawnImpl import Pawn
from collections import Counter


# white movement

def test_Pawn_movement_white_empty_board():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3), 'double move')])


def test_Pawn_movement_white_empty_board_moved():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    pawn.unmoved = False
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3))])


def test_Pawn_movement_white_obstructed_firendly_direct():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_WHITE, Coordinate(4, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([])


def test_Pawn_movement_white_obstructed_enemy_direct():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(4, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([])


def test_Pawn_movement_white_obstructed_firendly_distant():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_WHITE, Coordinate(5, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3))])


def test_Pawn_movement_white_obstructed_enemy_distant():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(5, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3))])


def test_Pawn_movement_white_end_of_board():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(7, 3)))
    pawn = cb.get_piece(Coordinate(7, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([])


def test_Pawn_movement_white_side_of_board():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 0)), (Pawn, ARMY_WHITE, Coordinate(3, 7)))
    pawn1 = cb.get_piece(Coordinate(3, 0))
    pawn2 = cb.get_piece(Coordinate(3, 7))
    assert Counter(pawn1.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 0), Coordinate(4, 0)),
                                                               MovementUtils.move_from_to(Coordinate(3, 0), Coordinate(5, 0), 'double move')])
    assert Counter(pawn2.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 7), Coordinate(4, 7)),
                                                               MovementUtils.move_from_to(Coordinate(3, 7), Coordinate(5, 7), 'double move')])


def test_Pawn_movement_white_cant_capture_friendly():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_WHITE, Coordinate(4, 4)), (MockPiece, ARMY_WHITE, Coordinate(4, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3), 'double move')])


def test_Pawn_movement_white_capture_enemy():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(4, 4)), (MockPiece, ARMY_BLACK, Coordinate(4, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3), 'double move'),
                                                              MovementUtils.move_and_capture(Coordinate(3, 3), Coordinate(4, 4)),
                                                              MovementUtils.move_and_capture(Coordinate(3, 3), Coordinate(4, 2))])


def test_Pawn_movement_white_capture_enemy_pawn_en_passant():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (Pawn, ARMY_BLACK, Coordinate(3, 4)), (Pawn, ARMY_BLACK, Coordinate(3, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    enemypawn1 = cb.get_piece(Coordinate(3, 2))
    enemypawn2 = cb.get_piece(Coordinate(3, 4))
    enemypawn1.en_passant = True
    enemypawn2.en_passant = True
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3), 'double move'),
                                                              Move('en passant', Coordinate(3, 3), Coordinate(4, 2), [MoveAction(Coordinate(3, 3), Coordinate(4, 2))], [Coordinate(3, 2)]),
                                                              Move('en passant', Coordinate(3, 3), Coordinate(4, 4), [MoveAction(Coordinate(3, 3), Coordinate(4, 4))], [Coordinate(3, 4)])])


def test_Pawn_movement_white_cannot_capture_friendly_pawn_en_passant():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (Pawn, ARMY_WHITE, Coordinate(3, 4)), (Pawn, ARMY_WHITE, Coordinate(3, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    enemypawn1 = cb.get_piece(Coordinate(3, 2))
    enemypawn2 = cb.get_piece(Coordinate(3, 4))
    enemypawn1.en_passant = True
    enemypawn2.en_passant = True
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3), 'double move')])


def test_Pawn_movement_white_cannot_capture_enemy_non_pawn_en_passant():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(3, 4)), (MockPiece, ARMY_BLACK, Coordinate(3, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    enemypawn1 = cb.get_piece(Coordinate(3, 2))
    enemypawn2 = cb.get_piece(Coordinate(3, 4))
    enemypawn1.en_passant = True
    enemypawn2.en_passant = True
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3), 'double move')])
    
# black movement

def test_Pawn_movement_black_empty_board():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(1, 3), 'double move')])


def test_Pawn_movement_black_empty_board_moved():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    pawn.unmoved = False
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3))])


def test_Pawn_movement_black_obstructed_firendly_direct():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(2, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([])


def test_Pawn_movement_black_obstructed_enemy_direct():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_WHITE, Coordinate(2, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([])


def test_Pawn_movement_black_obstructed_firendly_distant():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(1, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3))])


def test_Pawn_movement_black_obstructed_enemy_distant():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_WHITE, Coordinate(1, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3))])


def test_Pawn_movement_black_end_of_board():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(0, 3)))
    pawn = cb.get_piece(Coordinate(0, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([])


def test_Pawn_movement_black_side_of_board():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 0)), (Pawn, ARMY_BLACK, Coordinate(3, 7)))
    pawn1 = cb.get_piece(Coordinate(3, 0))
    pawn2 = cb.get_piece(Coordinate(3, 7))
    assert Counter(pawn1.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 0), Coordinate(2, 0)),
                                                               MovementUtils.move_from_to(Coordinate(3, 0), Coordinate(1, 0), 'double move')])
    assert Counter(pawn2.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 7), Coordinate(2, 7)),
                                                               MovementUtils.move_from_to(Coordinate(3, 7), Coordinate(1, 7), 'double move')])


def test_Pawn_movement_black_cant_capture_friendly():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(2, 4)), (MockPiece, ARMY_BLACK, Coordinate(2, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(1, 3), 'double move')])


def test_Pawn_movement_black_capture_enemy():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_WHITE, Coordinate(2, 4)), (MockPiece, ARMY_WHITE, Coordinate(2, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(1, 3), 'double move'),
                                                              MovementUtils.move_and_capture(Coordinate(3, 3), Coordinate(2, 4)),
                                                              MovementUtils.move_and_capture(Coordinate(3, 3), Coordinate(2, 2))])


def test_Pawn_movement_black_capture_enemy_pawn_en_passant():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (Pawn, ARMY_WHITE, Coordinate(3, 4)), (Pawn, ARMY_WHITE, Coordinate(3, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    enemypawn1 = cb.get_piece(Coordinate(3, 2))
    enemypawn2 = cb.get_piece(Coordinate(3, 4))
    enemypawn1.en_passant = True
    enemypawn2.en_passant = True
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(1, 3), 'double move'),
                                                              Move('en passant', Coordinate(3, 3), Coordinate(2, 2), [MoveAction(Coordinate(3, 3), Coordinate(2, 2))], [Coordinate(3, 2)]),
                                                              Move('en passant', Coordinate(3, 3), Coordinate(2, 4), [MoveAction(Coordinate(3, 3), Coordinate(2, 4))], [Coordinate(3, 4)])])


def test_Pawn_movement_black_cannot_capture_friendly_pawn_en_passant():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (Pawn, ARMY_BLACK, Coordinate(3, 4)), (Pawn, ARMY_BLACK, Coordinate(3, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    enemypawn1 = cb.get_piece(Coordinate(3, 2))
    enemypawn2 = cb.get_piece(Coordinate(3, 4))
    enemypawn1.en_passant = True
    enemypawn2.en_passant = True
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(1, 3), 'double move')])


def test_Pawn_movement_black_cannot_capture_enemy_non_pawn_en_passant():
    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(3, 3)), (MockPiece, ARMY_BLACK, Coordinate(3, 4)), (MockPiece, ARMY_BLACK, Coordinate(3, 2)))
    pawn = cb.get_piece(Coordinate(3, 3))
    enemypawn1 = cb.get_piece(Coordinate(3, 2))
    enemypawn2 = cb.get_piece(Coordinate(3, 4))
    enemypawn1.en_passant = True
    enemypawn2.en_passant = True
    assert Counter(pawn.get_all_possible_moves()) == Counter([MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(2, 3)),
                                                              MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(1, 3), 'double move')])


# general stuff

def test_Pawn_sets_en_passant_flag_correctly():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(3, 3)))
    pawn = cb.get_piece(Coordinate(3, 3))
    assert not pawn.en_passant
    pawn.move_executed(MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3)))
    assert not pawn.en_passant
    pawn.move_executed(MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3)))
    assert not pawn.en_passant
    dbmove = MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(5, 3))
    dbmove.name = 'double move'
    pawn.move_executed(dbmove)
    assert pawn.en_passant
    pawn.advance_tick()
    assert not pawn.en_passant
    dbmove = MovementUtils.move_from_to(Coordinate(3, 3), Coordinate(4, 3))
    dbmove.name = 'double move'
    pawn.move_executed(dbmove)
    assert pawn.en_passant


# test promotion
def test_Pawn_offers_promotion_empty_board():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(6, 3)))
    pawn = cb.get_piece(Coordinate(6, 3))
    pawn.army.promotions = {'promote to MockPiece': MockPiece}
    assert len(pawn.get_all_possible_moves()) == 2
    pawn.army.promotions['promote to MockPiece 2'] = MockPiece
    assert len(pawn.get_all_possible_moves()) == 3

    cb = MockBoard((Pawn, ARMY_BLACK, Coordinate(1, 3)))
    pawn = cb.get_piece(Coordinate(1, 3))
    pawn.army.promotions = {'promote to MockPiece': MockPiece}
    assert len(pawn.get_all_possible_moves()) == 2
    pawn.army.promotions['promote to MockPiece 2'] = MockPiece
    assert len(pawn.get_all_possible_moves()) == 3


def test_Pawn_offers_promotion_capture():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(6, 3)), (MockPiece, ARMY_BLACK, Coordinate(7, 4)))
    pawn = cb.get_piece(Coordinate(6, 3))
    pawn.army.promotions = {'promote to MockPiece': MockPiece}
    assert len(pawn.get_all_possible_moves()) == 4
    pawn.army.promotions['promote to MockPiece 2'] = MockPiece
    assert len(pawn.get_all_possible_moves()) == 6


# test promotion
def test_Pawn_promotion_empty_board():
    cb = MockBoard((Pawn, ARMY_WHITE, Coordinate(6, 3)))
    pawn = cb.get_piece(Coordinate(6, 3))
    pawn.army.promotions = {'promote to MockPiece': MockPiece}
    promotionmove = [move for move in pawn.get_all_possible_moves() if move.name == 'promote to MockPiece'][0]
    cb.execute_move(promotionmove)
    assert pawn.field is None
    assert cb.get_piece(Coordinate(6, 3)) is None
    newpiece = cb.get_piece(Coordinate(7, 3))
    assert newpiece is not None
    assert isinstance(newpiece, MockPiece)
