from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass
from typing import Dict
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
@dataclass(frozen=True)
class Position:
    row: int
    col: int

    def __add__(self, other):
        dr, dc = other
        return Position(self.row+dr, self.col+dc)
    def is_valid(self) -> bool:
        return 0 <= self.row < 8 and 0 <= self.col < 8


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


class Piece:
    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.moved = False
    #todo подумать как можно реализовать методы get_posible_moves и can_move_to 1 -все возможные перемещения, 2 - на конкретную клетку
    # (какие атрибуты нужно передать функциям)

    def get_possible_moves(self, position, board):
        pass

    def can_move_to(self, position_from, position_to, board):
        if position_to in self.get_possible_moves(position_from, board):
            return True
        return False

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

    def get_possible_moves(self, position, board):
        """
        :param position: текущая позиция фигуры на доске
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
        new_row = position.row + direction
        if board.is_valid_position(new_row, position.colum) and not board.get_piece(new_row, position.colum):
            moves.add((new_row, position.colum))
        new_row_2 = position.row + direction * 2
        if position.row == start_row and not board.get_piece(new_row_2, position.colum):
            moves.add((new_row_2, position.colum))
        colum_left = position.colum - 1
        if board.is_valid_position(new_row, colum_left) and board.get_piece(new_row, colum_left):
            target_color = board.get_piece(new_row, colum_left).color
            if target_color != self.color:
                moves.add((new_row, colum_left))
        colum_right = position.colum + 1
        if board.is_valed_position(new_row, colum_right) and board.get_piece(new_row, colum_right):
            target_color = board.get_piece(new_row, colum_right).color
            if target_color != self.color:
                moves.add((new_row, colum_right))
        return moves

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.ROOK)

    def get_possible_moves(self, position, board):
        """
        :param position: текущая позиция фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for step in range(8):
                new_row, new_colum = position.row + dr, position.colum + dc * step
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
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.BISHOP)

    def get_possible_moves(self, position, board):
        """
        :param position: текущая позиция фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]
        for dr, dc in directions:
            for step in range(8):
                new_row, new_colum = position.row + dr, position.colum + dc * step
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
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.KNIGHT)

    def get_possible_moves(self, position, board):
        """
        :param position: текущая позиция фигуры
        :param board: доска
        :return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2),  (1, 2), (2, -1),  (2, 1)]
        for dr, dc in directions:
            new_row, new_colum = position.row + dr, position.colum + dc
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
class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.QUEEN)

    def get_possible_moves(self, from_position, board):
        """
        :param position: текущая позиция фигуры
        :param board: доска
        return moves: вовращает множество допустимых ходов
        """
        moves = set()
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            for step in range(8):
                position = position.row + dr * step, position.colum + dc * step
                if not board.is_valid_position(position):
                    break
                target = board.get_piece(position)
                if target is None:
                    moves.add((position))
                else:
                    if self.color != target.color:
                        moves.add((position))
                    break
            return moves

# ==============================================================
class King(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.KING)

    def get_possible_moves(self, from_pos: Position, board: 'Board') -> set[Position]:
        moves = set()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                to = from_pos + (dr, dc)
                if to.is_valid():
                    target = board.get_piece(to)
                    if target is None or target.color == self.color:
                        moves.add((to))


# Рокировка
        if not self.has_moved:
            # Короткая рокировка (0-0)
            rook_pos = Position(from_pos.row, 7)
            rook = board.get_piece(rook_pos)
            if (rook and rook.type == PieceType.ROOK and rook.color == self.color
                    and not rook.has_moved):
                # Проверяем, что между королём и ладьёй нет фигур
                if all(board.get_piece(Position(from_pos.row, c)) is None for c in (5, 6)):
                    # Король не должен быть под шахом, и не должен проходить через битое поле
                    if (not board.is_square_attacked(from_pos, self.color.opposite()) and
                            not board.is_square_attacked(Position(from_pos.row, 5), self.color.opposite()) and
                            not board.is_square_attacked(Position(from_pos.row, 6), self.color.opposite())):
                        moves.add(Position(from_pos.row, 6)) # Конечная позиция короля

            # Длинная рокировка (0-0-0)
            rook_pos2 = Position(from_pos.row, 0)
            rook2 = board.get_piece(rook_pos2)
            if (rook2 and rook2.type == PieceType.ROOK and rook2.color == self.color
                    and not rook2.has_moved):
                if all(board.get_piece(Position(from_pos.row, c)) is None for c in (1, 2, 3)):
                    if (not board.is_square_attacked(from_pos, self.color.opposite()) and
                            not board.is_square_attacked(Position(from_pos.row, 3), self.color.opposite()) and
                            not board.is_square_attacked(Position(from_pos.row, 2), self.color.opposite())):
                        moves.add(Position(from_pos.row, 2))


class Board:
    def __init__(self):
        self.width = 8
        self.height = 8
        self.pieces: Dict[Position, Piece] = {}
        self.board = [[None for i in range(self.width)] for j in range(self.height)]
        self.setup_board()



    def is_valid_position(self, row, colum):
        if row < 8 and row >= 0 and colum < 8 and colum >= 0:
            return True
        return False


    def setup_board(self):
        for col in range(self.width):
            self.pieces[Position(1, col)] = Pawn(Color.BLACK)
            self.pieces[Position(6, col)] = Pawn(Color.WHITE)

        back_row = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook ]
        for col, piece in enumerate(back_row):
            self.pieces[Position(0, col)] = piece(Color.BLACK)
            self.pieces[Position(7, col)] = piece(Color.WHITE)



    def get_piece(self, position):
        if self.is_valid_position(position):
            return self.pieces[position]
        return None

    def set_piece(self, position, piece):
        if piece is None:
            self.pieces.pop(position, None)
        else:
            self.pieces[position] = piece

    def find_king(self, color: Color) -> Optional[Position]:
        for pos, piece in self.pieces.items():
            if piece.type == PieceType.KING and piece.color == color:
                None


    def is_square_attacked(self, position: Position, color: Color) -> bool:
        for p, piece in self.pieces.items():
            if piece.color == by.color:
                if piece.can_move_to(p, pos, self):
                    return True
        return False


    def woud_leave_king_in_check(self, from_pos: Position, to_pos: Position) -> bool:
        piece = self.get_pieces(from_pos)
        if piece is None:
            return False


        captured = self.get_piece(to_pos)
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]

        king_pos = self.get_piece(piece.color)
        in_check = False
        if king_pos:
            in_check = self.is_square_attacked(king_pos, piece.color.oposite())


        if captured:
            self.piece[from_pos] = piece
            self.pieces[to_pos] = captured
        else:
            self.pieces[from_pos] = piece
            self.pieces[to_pos]

        return in_check

    def is_check(self, color: Color) -> bool:
        king_pos = self.get_piece(color)
        if king_pos is None:
            return False
        return self.is_square_attacked(king_pos, color.opposite())

    def is_checkmate(self, color: Color) -> bool:
        """Мат: король под шахом и нет легальных ходов."""
        if not self.is_check(color):
            return False
        return not self.has_legal_moves(color)

    def is_stalemate(self, color: Color) -> bool:
        """Пат: король не под шахом, но нет легальных ходов."""
        if self.is_check(color):
            return False
        return not self.has_legal_moves(color)

    def has_legal_moves(self, color: Color) -> bool:
        """Есть ли у игрока цвета color хотя бы один легальный ход."""
        for pos, piece in self.pieces.items():
            if piece.color == color:
                for to_pos in piece.get_possible_moves(pos, self):
                    if not self.would_leave_king_in_check(pos, to_pos):
                        return True
        return False


    def move_piece(self, from_pos: Position, to_pos: Position) -> bool:
        """Выполняет ход, если он легален. Возвращает True при успехе."""
        piece = self.get_piece(from_pos)
        if piece is None:
            return False

        # Проверяем, может ли фигура так сходить
        if not piece.can_move_to(from_pos, to_pos, self):
            return False

        # Проверяем, не останется ли король под шахом
        if self.would_leave_king_in_check(from_pos, to_pos):
            return False

        # Выполняем ход
        captured = self.get_piece(to_pos)
        self.pieces[to_pos] = piece
        del self.pieces[from_pos]
        piece.has_moved = True

        # Превращение пешки
        if piece.type == PieceType.PAWN:
            last_row = 0 if piece.color == Color.WHITE else 7
            if to_pos.row == last_row:
                # По умолчанию превращаем в ферзя
                self.pieces[to_pos] = Queen(piece.color)
        if piece.type == PieceType.KING:
            if from_pos == Position(7, 4) and to_pos == Position(7, 6):  # Белая короткая
                rook = self.get_piece(Position(7, 7))
                if rook:
                    self.pieces[Position(7, 5)] = rook
                    del self.pieces[Position(7, 7)]
                    rook.has_moved = True
            elif from_pos == Position(7, 4) and to_pos == Position(7, 2):  # Белая длинная
                rook = self.get_piece(Position(7, 0))
                if rook:
                    self.pieces[Position(7, 3)] = rook
                    del self.pieces[Position(7, 0)]
                    rook.has_moved = True
            elif from_pos == Position(0, 4) and to_pos == Position(0, 6):  # Чёрная короткая
                rook = self.get_piece(Position(0, 7))
                if rook:
                    self.pieces[Position(0, 5)] = rook
                    del self.pieces[Position(0, 7)]
                    rook.has_moved = True
            elif from_pos == Position(0, 4) and to_pos == Position(0, 2):  # Чёрная длинная
                rook = self.get_piece(Position(0, 0))
                if rook:
                    self.pieces[Position(0, 3)] = rook
                    del self.pieces[Position(0, 0)]
                    rook.has_moved = True

        return True

    def display(self):
        print("  a b c d e f g h")
        for row in range(8):
            print(f"{8 - row} ", end="")
            for col in range(8):
                pos = Position(row, col)
                piece = self.get_piece(pos)
                if piece:
                    print(str(piece), end=" ")
                else:
                    print(".git ", end="")
            print(f"{8 - row}")
        print("  a b c d e f g h")


#========= ИГРА ============
class Game:                                         #создание класса
    def __init__(self):
        self.board = Board()
        self.current_turn = Color.WHITE
        self.game_over = False
        self.winner = None
        self.move_history = []                      #указываем на прошлые объекты классов

    def parse_move(self, move_str: str) -> Tuple[Position, Position]:     #создаеам новую функцию
        if len(move_str) != 4:
            raise ValueError("Неверный формат хода. Используйте, например, 'e2e4'.")            #указываем пользователю на ошибку в ходе
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}                  #перевод колонок в числовые значения
        from_col = col_map[move_str[0].lower()]
        from_row = 8 - int(move_str[1])
        to_col = col_map[move_str[2].lower()]
        to_row = 8 - int(move_str[3])
        return Position(from_row, from_col), Position(to_row, to_col)           #возвращаем позицию

    def make_move(self, from_pos: Position, to_pos: Position) -> bool:              #создаем функцию
        if self.game_over:
            print("Игра уже окончена.")                #если игра окнчена то ходить нельзя
            return False

        piece = self.board.get_piece(from_pos)
        if piece is None:
            print("На начальной клетке нет фигуры.")
            return False                                        #проверка на тычек в пустую клетку

        if piece.color != self.current_turn:
            print(f"Сейчас ход {self.current_turn.value}.")
            return False                                            #-----------

        if self.board.move_piece(from_pos, to_pos):
            self.move_history.append((from_pos, to_pos))
            opponent = self.current_turn.opposite()
            if self.board.is_checkmate(opponent):
                self.game_over = True
                self.winner = self.current_turn
                print(f"Мат! Победили {self.winner.value}.")            #проверка на пат/мат
            elif self.board.is_stalemate(opponent):
                self.game_over = True
                self.winner = None
                print("Пат! Ничья.")
            else:
                # Переключение хода
                self.current_turn = opponent
                if self.board.is_check(opponent):
                    print(f"{opponent.value} под шахом!")
            return True
        else:
            print("Неверный ход.")
            return False
    def play(self):
        print("Добро пожаловать в шахматы!")
        print("Вводите ходы в формате 'e2e4' (с буквы на букву).")      #подготовка к старту игры
        print("Для выхода введите 'quit'.")
        self.board.display()

        while not self.game_over:
            move_str = input(f"\nХод {self.current_turn.value} (например, e2e4): ").strip()
            if move_str.lower() == 'quit':
                break
            try:
                from_pos, to_pos = self.parse_move(move_str)            #превращает текст в движение
                if self.make_move(from_pos, to_pos):
                    self.board.display()
            except ValueError as e:
                print(f"Ошибка: {e}")
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")           #ошибка/окончание игры

        print("Игра завершена.")












