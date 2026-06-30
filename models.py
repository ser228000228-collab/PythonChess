from abc import ABC, abstractmethod
from enum import Enum
"""
файл доски для шахмат
размер доски 8 x 8, по горизонтали цифры от 1 до 8, по вертикали буквы от a до h
"""
class ChessDesk:
    def __init__(self, name = "Chess_desk", size = 8, horizontal = "abcdefgh", vertical = "12345678", colors = None):
        self.name = name
        self.size = size
        self.horizontal = horizontal
        self.vertical = vertical
        self.colors = colors

cd1 = ChessDesk(name = "вася")
cd2 = ChessDesk()
print(cd1.name)
print(cd2.name)
#====================================

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

#однострочный retern используется когда есть всего 2 варианта значений на возврат
    def opposite(self):
        return Color.BLACK if self == Color.WHITE else Color.WHITE
#а второй тип когда вариантов возврощаемого ответа больше двух
#    def opposite(self):
#        if self == Color.BLACK:
#            return Color.WHITE
#        else:
#            return Color.BLACK

#третий тип когда не наривться первый
#    def opposite(self):
#        if self == Color.BLACK:
#            return Color.WHITE
#        return Color.BLACK

class PieceType(Enum):
    PAWN = "пешка"
    ROOK = "ладья"
    BISHOP = "слон"
    KING = "король"
    KNIGHT = "конь"
    QUEEN = "королева"


class Piece(ABC):
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.moved = False
    #todo подумать как можно реализовать методы get_posible_moves и can_move_to 1 -все возможные перемещения, 2 - на конкретную клетку
    # (какие атрибуты нужно передать функциям)

    @abstractmethod
    def get_possible_moves(self, row, colum, board):
        pass

    @abstractmethod
    def can_move_to(self, row_from, colum_from, row_to, colum_to, board):
        pass

    def __repr__(self):
        symbols = {
            (Color.WHITE, PieceType.KING): "♔",
            (Color.WHITE, PieceType.QUEEN): "♕",
            (Color.WHITE, PieceType.ROOK): "♖",
            (Color.WHITE, PieceType.BISHOP): "♗",
            (Color.WHITE, PieceType.KNIGHT): "♘",
            (Color.WHITE, PieceType.PAWN): "♙",
            (Color.BLACK, PieceType.KING): "♚",
            (Color.BLACK, PieceType.QUEEN): "♛",
            (Color.BLACK, PieceType.ROOK): "♜",
            (Color.BLACK, PieceType.BISHOP): "♝",
            (Color.BLACK, PieceType.KNIGHT): "♞",
            (Color.BLACK, PieceType.PAWN): "♟",
        }
        return symbols.get((self.color, self.type), "?")

#ToDo попробовать реализовать пешку

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.PAWN)

    def get_possible_moves(self, row, colum, board):
        """
        :param row: текущий ряд фигуры
        :param colum: текущая колонка фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        if self.color == Color.WHITE:
            direction = 1           #направление
            start_row = 1           #начальный ряд
        else:
            direction = -1
            start_row = 6
        new_row = row + direction
        if board.is_valid_position(new_row, colum) and not board.get_piece(new_row, colum):
            moves.add((new_row, colum))
        new_row_2 = row + direction * 2
        if row == start_row and not board.get_piece(new_row_2, colum):
            moves.add((new_row_2, colum))
        colum_left = colum - 1
        if board.is_valid_position(new_row, colum_left) and board.get_piece(new_row, colum_left):
            target_color = board.get_piece(new_row, colum_left).color
            if target_color != self.color:
                moves.add((new_row, colum_left))
        colum_right = colum + 1
        if board.is_valed_position(new_row, colum_right) and board.get_piece(new_row, colum_right):
            target_color = board.get_piece(new_row, colum_right).color
            if target_color != self.color:
                moves.add((new_row, colum_right))
        return moves


class Board:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.board = [[None for i in range(self.width)] for j in range(self.height)]
        self.setup_board()


    def is_valid_position(self, row, colum):
        if row < 8 and row >= 0 and colum < 8 and colum >= 0:
            return True
        return False

    def setup_board(self):
        pass

    def get_piece(self, row, colum):
        if self.is_valid_position(row, colum):
            return self.board[row][colum]
        return None

    def set_piece(self, row, colum, piece):
        pass

#============================================
class ROOK(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.ROOK)

    def get_possible_moves(self, row, colum, board):
        """
        :param row: текущий ряд фигуры
        :param colum: текущая колонка фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for step in range(8):
                new_row, new_colum = row + dr, colum + dc * step
                if not board.is_valid_position(new_row, new_colum):
                    break
                target = board.get_piece(new_row, new_colum)
                if target is None:
                    moves.add((new_row, new_colum))
                else:
                    if self.color == target.color:
                        moves.add((new_row, new_colum))
        return moves


#==============================================================
class BISHOP(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.BISHOP)

    def get_possible_moves(self, row, colum, board):
        """
        :param row: текущий ряд фигуры
        :param colum: текущая колонка фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            for step in range(8):
                new_row, new_colum = row + dr, colum + dc * step
                if not board.is_valid_position(new_row, new_colum):
                    break
                target = board.get_piece(new_row, new_colum)
                if target is None:
                    moves.add((new_row, new_colum))
                else:
                    if self.color == target.color:
                        moves.add((new_row, new_colum))
        return moves






    # ==============================================================  Домашняя работа
class KNIGHT(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.KNIGHT)

    def get_possible_moves(self, row, colum, board):
        """
        :param row: текущий ряд фигуры
        :param colum: текущая колонка фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2),  (1, 2), (2, -1),  (2, 1)]
        for dr, dc in directions:
            new_row, new_colum = row + dr, colum + dc
            if not board.is_valid_position(new_row, new_colum):
                continue
            target = board.get_piece(new_row, new_colum)
            if target is None:
                moves.add((new_row, new_colum))
            else:
                if self.color != target.color:
                    moves.add((new_row, new_colum))
        return moves

# ==============================================================
class QUEEN(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.QUEEN)

    def get_possible_moves(self, row, colum, board):
        """
        :param row: текущий ряд фигуры
        :param colum: текущая колонка фигуры
        :param board: доска
        return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for step in range(8):
                new_row, new_colum = row + dr * step, colum + dc * step
                if not board.is_valid_position(new_row, new_colum):
                    break
                target = board.get_piece(new_row, new_colum)
                if target is None:
                    moves.add((new_row, new_colum))
                else:
                    if self.color != target.color:
                        moves.add((new_row, new_colum))
                    break
            return moves

# ==============================================================
class KING(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.KING)

    def get_possible_moves(self, row, colum, board):
        """
        :param row: текущий ряд фигуры
        :enemy_color: цвет противника 
        :param colum: текущая колонка фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            new_row, new_colum = row + dr, colum + dc
            if not board.is_valid_position(new_row, new_colum):
                break
            target = board.get_piece(new_row, new_colum)
            if target is None:
                moves.add((new_row, new_colum))
            else:
                if self.color != target.color:
                    moves.add((new_row, new_colum))
        return moves


#===========================================
    def check(self, row, colum, board, enemy_color):
        mate = 0
        if enemy_color != self.color:
            target = board.get_piece.KING(row, colum)
            print(self.color.KING, target("шах"))
            if self.color.KING == target:
                mate += 1
            print("победили", enemy_color)
#============================================
    def plaeer(self, color, row, colum, board):
        colum = int("введите номер колонки")
        row = int("введите номер ряда")









