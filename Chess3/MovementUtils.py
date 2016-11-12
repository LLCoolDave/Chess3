from .MoveImpl import Coordinate, MoveAction, Move


def move_from_to(origin, target, name=None):
    return Move('move' if name is None else name, origin, target, [MoveAction(origin, target)], [])


def move_and_capture(origin, target, name=None):
    return Move('move' if name is None else name, origin, target, [MoveAction(origin, target)], [target])


def get_relative_coord(origin, row_delta, column_delta):
    try:
        return Coordinate(origin.row + row_delta, origin.column + column_delta)
    except ArithmeticError:
        return None


def get_deltas(origin, target):
    return target.row - origin.row, target.column - origin.column


def possible_knight_moves(origin):
    ret = []
    for row_delta, column_delta in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
        target = get_relative_coord(origin, row_delta, column_delta)
        if target is not None:
            ret.append(target)
    return ret


def move_until_obstructed(piece, row_delta, column_delta, may_capture=True):
    ret = []

    # check for degenerate case
    if row_delta == 0 and column_delta == 0:
        return ret

    origin = piece.coord
    cb = piece.chessboard
    target = get_relative_coord(origin, row_delta, column_delta)
    while target is not None:
        if cb.get_field(target).is_empty():
            ret.append(move_from_to(origin, target))
            target = get_relative_coord(target, row_delta, column_delta)
        elif may_capture and cb.get_field(target).has_enemy(piece) and cb.get_piece(target).is_capturable(piece):
            ret.append(move_and_capture(origin, target))
            target = None
        else:
            target = None

    return ret


def multimove_until_obstructed(piece, deltas, may_capture=True):
    ret = []
    for row_delta, column_delta in set(deltas):
        ret.extend(move_until_obstructed(piece, row_delta, column_delta, may_capture))
    return ret


def possible_king_moves(origin):
    ret = []
    for row_delta, column_delta in [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]:
        target = get_relative_coord(origin, row_delta, column_delta)
        if target is not None:
            ret.append(target)
    return ret
