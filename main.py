# Author: Christian Castro (Github: gvmmybear)
# Date of Last Modification: 01/11/2022
# Description: After creating a Hasami Shogi Board game for a class project, I decided
#   that I wanted to create a chess program, as it is a game I am more acquainted with.
#   This program is still currently in progress, as there are some missing functionality
#   to this program (i.e. such as no castling, or checkmate verification as of yet).

import copy
import pygame
pygame.init()

# Some constants for the pygame window
width, height = 640, 640
fps = 50
white = (255, 255, 255)
blue = (0, 0, 110)
rows, cols = 8, 8
size = width // cols
window = pygame.display.set_mode((width, height))
resize = 40

# Images for chess pieces
# pygame.transform.scale(pygame.image.load("sprites/Sand.png"), (SCALE, SCALE))
white_king = pygame.transform.scale(pygame.image.load('pieces/white_king.png'), (resize, resize))
white_queen = pygame.transform.scale(pygame.image.load('pieces/white_queen.png'), (resize, resize))
white_rook = pygame.transform.scale(pygame.image.load('pieces/white_rook.png'), (resize, resize))
white_bishop = pygame.transform.scale(pygame.image.load('pieces/white_bishop.png'), (resize, resize))
white_knight = pygame.transform.scale(pygame.image.load('pieces/white_knight.png'), (resize, resize))
white_pawn = pygame.transform.scale(pygame.image.load('pieces/white_pawn.png'), (resize, resize))
black_king = pygame.transform.scale(pygame.image.load('pieces/black_king.png'), (resize, resize))
black_queen = pygame.transform.scale(pygame.image.load('pieces/black_queen.png'), (resize, resize))
black_rook = pygame.transform.scale(pygame.image.load('pieces/black_rook.png'), (resize, resize))
black_bishop = pygame.transform.scale(pygame.image.load('pieces/black_bishop.png'), (resize, resize))
black_knight = pygame.transform.scale(pygame.image.load('pieces/black_knight.png'), (resize, resize))
black_pawn = pygame.transform.scale(pygame.image.load('pieces/black_pawn.png'), (resize, resize))


class Pieces:
    """
    Class Pieces is a generalized class representing chess piece objects.
    Each Piece object is stored as a square occupant data member for class Square().
    ----------------------------------
    Each Square() object will then be appended to a list in class Board(). When
    referring to row or col, these are the indices of the Square() object that will
    hold the Piece() object as a square occupant.
    """
    def __init__(self, row, col, color):
        """
        Constructor method for class Pieces.
        ------------------------------------
        :param row: row is the row index at which the piece object is located at.
            (Must be passed as an integer)
        :param col: col is the column index at which the piece object is located at.
            (Must be passed as an integer)
        :param color: Piece color, is either "B" for black or "W" for white.
        """
        self._is_captured = False
        self._row = row
        self._col = col
        self._x = 0
        self._y = 0
        self._color = color
        self._moves = []
        self._letter = ""
        self._has_moved = None
        self.calculate_location()

    def get_row(self):
        """This piece class method returns the row index for the piece."""
        return self._row

    def get_col(self):
        """This piece class method returns the column index for the piece."""
        return self._col

    def get_x(self):
        """This class method returns the x coordinate for which the piece image/object
        will be projected onto the pygame window."""
        return self._x

    def get_y(self):
        """This class method returns the y coordinate for which the piece image/object
        will be projected onto the pygame window."""
        return self._y

    def get_color(self):
        """This class method returns the piece color of the object."""
        return self._color

    def set_row(self, row):
        """This class method sets the row index for the piece object"""
        self._row = row

    def set_col(self, col):
        """This class method sets the column index for the piece object."""
        self._col = col

    def set_x(self, x_value):
        """This class method sets the x coordinate for which the piece image/object
        will be projected onto the pygame window."""
        self._x = x_value

    def set_y(self, y_value):
        """This class method sets the y coordinate for which the piece image/object
        will be projected onto the pygame window."""
        self._y = y_value

    def get_moves(self):
        """This class method returns a list of moves as board indices
        i.e. example: moves = [[row_1, col_1], [row_2, col_2],...]"""
        return self._moves

    def clear_moves(self):
        """This class method clears the list of moves for the piece object."""
        self._moves = []

    def add_move(self, row, col):
        """This class method appends a list of board indices to self._moves"""
        self._moves.append([row, col])

    def remove_move(self, coord):
        self._moves.remove(coord)

    def get_letter(self):
        """This class method returns the piece letter for the object. I.e. for a King
        piece object, the letter is "K", for Queen it's "Q", Knight is "N" """
        return self._letter

    def get_has_moved(self):
        """This class method returns the data member self._has_moved. This is
        used for verifying if the player can conduct a castle move. """
        return self._has_moved

    def set_has_moved(self):
        self._has_moved = True

    def calculate_location(self):
        """This class method calculates the (x,y) coordinates for which the piece image will
        be blit onto the pygame window. These coordinates are in opposite order from the row
        and column values."""
        self._x = self._col * 80 + 20
        self._y = self._row * 80 + 20


class King(Pieces):
    """
    Class King represents a King piece object. Inherits attributes from parent class Pieces.
    """
    def __init__(self, row, col, color):
        """
        Constructor Method for Class King.
        ------------------------------------
        :param row: row index for King object
        :param col: column index for king object
        :param color: color of the King piece. Either "B" or "W".
        """
        super().__init__(row, col, color)
        self._in_check = False
        self._has_moved = False
        self._letter = "K"


class Queen(Pieces):
    """
    Class Queen represents a Queen piece object. Inherits attributes from parent class Pieces.
    """
    def __init__(self, row, col, color):
        """
        Constructor Method for Class Queen.
        ------------------------------------
        :param row: row index for the queen object.
        :param col: column index for the queen object.
        :param color: color of the Queen piece. Either "B" or "W".
        """
        super().__init__(row, col, color)
        self._letter = "Q"


class Pawn(Pieces):
    """
    Class Pawn represents a Pawn piece object. Inherits attributes from parent class Pieces.
    """
    def __init__(self, row, col, color):
        """
        Constructor Method for Class Pawn.
        ------------------------------------
        :param row: row index
        :param col: column index
        :param color: color of the Pawn piece. Either "B" or "W".
        """
        super().__init__(row, col, color)
        self._pawn_range = 2

    def get_pawn_range(self):
        """This Pawn class method returns the self._pawn_range. This attribute
        is used for a pawn's initial move (which can be 1 or 2 squares forward
        by game rules). It should be set once a pawn has executed its first move."""
        return self._pawn_range

    def set_pawn_range(self):
        """This Pawn class method sets the self._pawn_range to 1. This limits a
        pawn's future possible moves to only 1 square forward."""
        self._pawn_range = 1


class Knight(Pieces):
    """
    Class Knight represents a Knight piece object. Inherits attributes from parent class Pieces.
    """
    def __init__(self, row, col, color):
        """
        Constructor method for Class Knight. Inherits attributes from Parent class Pieces.
        ------------------------------------
        :param row: row index location
        :param col: column index location
        :param color: color of the Knight piece. Either "B" or "W".
        """
        super().__init__(row, col, color)
        self._letter = "N"


class Bishop(Pieces):
    """
    Class Bishop represents a Bishop piece object. Inherits attributes from parent class Pieces.
    """
    def __init__(self, row, col, color):
        """
        Constructor method for Class Bishop. Inherits attributes from Parent class Pieces.
        ------------------------------------
        :param row: row index location
        :param col: column index location
        :param color: color of the Bishop piece. Either "B" or "W".
        """
        super().__init__(row, col, color)
        self._letter = "B"


class Rook(Pieces):
    """
    Class Rook represents a Rook piece object. Inherits attributes from parent class Pieces.
    """
    def __init__(self, row, col, color):
        """
        Constructor method for class Rook. Inherits attributes from Parent class Pieces.
        :param row: row index
        :param col: column index
        :param color: color of the Bishop piece. Either "B" or "W".
        """
        super().__init__(row, col, color)
        self._has_moved = False     # needed for castle rule
        self._letter = "R"


class Square:
    """
    Class Square represents a Square object. A traditional chess board should contain
    an 8x8 2-Dimensional matrix containing 64 square objects.
    """
    def __init__(self, row, col, occupant, square_color):
        """
        Constructor method for Class Square.
        ------------------------------------
        :param row: row index for the square object.
        :param col: column index for the square object.
        :param occupant: contains either the Piece() object
            or a None value if empty.
        :param square_color: color of the Square. Either "B" or "W".
        """
        self._color = square_color
        self._occupant = occupant
        self._row = row
        self._col = col
        self._coordinates = [self._row, self._col]

    def get_square_color(self):
        """This class method returns the self._color or the square's
        color as represented by either "B" or "W" for Black or White."""
        return self._color

    def get_occupant(self):
        """This class method returns the occupant located in the square
        object. It will return the Piece() object or a None value if empty."""
        return self._occupant

    def set_occupant(self, piece):
        """This class method sets the square occupant."""
        self._occupant = piece

    def get_coordinates(self):
        """This method returns the [row, col] values for the square object.
        These values refer to the Square() objects location on the Board() object."""
        return self._coordinates


class Board:
    """
    ====================================
    Class Board represents a Board object as described in a traditional chess board
    setup. In addition to the physical representation of a chess board (i.e. an 8x8
    board containing alternating black and white squares), this class also contains
    much of the functionality behind this program. Methods in this class are
    responsible for actions such as determining check/checkmate, as well as scanning
    the Board() for possible legal moves.
    ====================================
    """
    def __init__(self):
        """
        Constructor Method for Class Board().
        ------------------------------------
        This method takes no parameters.
        """
        self._board = []
        self._simulator = None
        self._white_covered_squares = []
        self._black_covered_squares = []
        self._white_king_loc = None
        self._black_king_loc = None
        self._white_king_in_check = False
        self._black_king_in_check = False
        self._active_p = "W"
        self._inactive_p = "B"
        self._checkmate = False
        self._stalemate = False

    def get_checkmate_bool(self):
        """This class method returns a boolean value for the
        attribute self._checkmate."""
        return self._checkmate

    def set_simulation(self):
        """This method creates a deepcopy of the list containing the square
        objects. It essentially saves a copy of the current board/pieces
        setup."""
        self._simulator = copy.deepcopy(self._board)

    def reset_simulation(self):
        """This class method restores the saved copy of the board and piece setup."""
        self._board = copy.deepcopy(self._simulator)

    def get_active_p(self):
        """This class method returns the active player."""
        return self._active_p

    def get_inactive_p(self):
        """This class method returns the inactive player, i.e. if white to move,
        then black is the inactive player and vice versa."""
        return self._inactive_p

    def set_active_p(self):
        """This class method sets the active player by switching "W" for "B" or
        "B" for "W". It essentially just switches the players turns."""
        temp = self.get_active_p()
        if temp == "W":
            self._active_p = "B"
            self._inactive_p = "W"
        elif temp == "B":
            self._active_p = "W"
            self._inactive_p = "B"

    def get_king_check_status(self, color):
        """
        This class method gets the check status for a king.
        :param color: String, either "B" or "W"
        :return: boolean value. True if the king is in check
            and False if not.
        """
        if color == "W":
            self.get_w_king_check_status()
        elif color == "B":
            self.get_b_king_check_status()

    def get_b_king_check_status(self):
        # This method may be unnecessary
        # Marked for possible removal
        return self._black_king_in_check

    def get_w_king_check_status(self):
        # This method may be unnecessary
        # Marked for possible removal
        return self._white_king_in_check

    def set_king_location(self, coordinates, color):
        """This method returns the coordinates for a King() piece.
        This is kept track of by the Board() object for actions
        such as determining check/checkmate."""
        if color == "W":
            self.set_w_king_location(coordinates)
        elif color == "B":
            self.set_b_king_location(coordinates)

    def get_w_king_location(self):
        """This method returns the white king piece location."""
        return self._white_king_loc

    def get_b_king_location(self):
        """This method returns the black king piece location."""
        return self._black_king_loc

    def set_w_king_location(self, coordinates):
        """This method is used to set the white king location.
        Note: this method is not used for setting a King() to a
        specific Square(), it is only to keep track of where the
        King() is location in the self._board list."""
        self._white_king_loc = coordinates

    def set_b_king_location(self, coordinates):
        """This method is used to set the black king location.
        Note: this method is not used for setting a King() to a
        specific Square(), it is only to keep track of where the
        King() is location in the self._board list."""
        self._black_king_loc = coordinates

    def add_covered_squares(self, row, col, color):
        """
        ------------------------------------
        This method adds Square coordinates for Squares which are
        "controlled" by possible piece moves. This is important for
        determining which pieces a King can capture and which squares
        are allowed for movement, as to not put the King in check.
        ------------------------------------
        :param row: must be passed as an integer.
        :param col: must be passed as an integer.
        :param color: passed as string: either "B" or "W" value.
        :return: None
        """
        coord = [row, col]
        white_moves = coord in self.get_white_covered_squares()
        black_moves = coord in self.get_black_covered_squares()

        if color == "W" and white_moves is False:
            self._white_covered_squares.append(coord)
        elif color == "B" and black_moves is False:
            self._black_covered_squares.append(coord)

    def get_white_covered_squares(self):
        """This method returns a list of white controlled squares."""
        return self._white_covered_squares

    def get_black_covered_squares(self):
        """This method returns a list of black controlled squares."""
        return self._black_covered_squares

    def reset_covered_squares(self, color):
        """
        ------------------------------------
        This method clears the list containing the controlled squares
        for a particular color.
        ------------------------------------
        :param color: "B" or "W", passed as string.
        :return: None
        """
        if color == "W":
            self._white_covered_squares = []
        elif color == "B":
            self._black_covered_squares = []

    def get_board(self):
        """This method returns the self._board list."""
        return self._board

    def make_move(self, start, end, simulation=False):
        """
        ------------------------------------
        This Board() Class method is the primary method used for
        conducting a piece move. This method is also used for
        simulating possible piece moves for determining if a player
        in check has any legal possible moves remaining (ie a move
        that will take its King() out of the current check).

        ------------------------------------

        :param start: starting coordinates of the piece being moved.
                Can be passed as either a list value [row, col]
                containing two integer values (which references the
                self._board indices of the starting location) or as
                a tuple (x, y) containing the x, y coordinates as
                found on the window drawn by the pygame module.

        :param end: ending coordinates of the piece being moved.
                Values are passed the same as the start parameter.

        :param simulation: a boolean value. This should be set to
                False when actually conducting a piece move in the
                game, else simulation is set to True if we are using
                this method to iterate on possible moves for when
                determining checkmate.

        :return: True if the piece move meets game rule requirements.
                 returns False or None, otherwise.
        """

        # if-else statements below are used for determining the type
        #   of coordinates being passed to this function. I.e. either
        #   [row, col] where row, col are integers, or (x, y), where
        #   x, y are the pixel coordinates (also integers, just a much
        #   larger value) on the pygame window.
        if simulation is False:
            start = list(start)
            end = list(end)
            start_col, start_row = start[0] // 80, start[1] // 80
            end_col, end_row = end[0] // 80, end[1] // 80
        else:
            start_row, start_col = start[0], start[1]
            end_row, end_col = end[0], end[1]
        # ---------------

        # try/except below is used to save the possible square occupant
        #   located at the destination (end parameter) coordinates, in
        #   case the desired move violates a game rule. This is so we can
        #   "reset" the piece which was located to the move prior to
        #   setting the square occupant.
        try:
            save_square = self._board[end_row][end_col].get_occupant()
        except AttributeError:
            save_square = None
        # ---------------

        # Below is the start of main branch for executing a piece movement.
        #   The initial if statement ensures that we do not conduct a piece
        #   movement to the same square as the starting coordinates.
        #   I.e. start != end.
        if start_row != end_row or start_col != end_col:
            try:
                # Using try/except to initialize some values for verification.
                #   (If square occupant is None, then we can't call subsequent
                #   methods such as get_color())
                piece = self._board[start_row][start_col].get_occupant()
                piece_color = piece.get_color()
                moves = piece.get_moves()
                destination = [end_row, end_col]

                # Verification that the piece being moved meets conditions:
                #   -The active player is moving their own piece.
                #   -The destination square is in the calculated allowed moves list.
                #   -The make_move() method is being run as a simulation.
                if (destination in moves and piece_color == self.get_active_p()) or simulation is True:
                    letter = piece.get_letter()
                    move_status = piece.get_has_moved()

                    # Below is a special branch for King moves/castling
                    if letter == "K":
                        if move_status is False:

                            # White King Castling
                            if piece.get_color() == "W":
                                if destination == [7, 6]:
                                    self.castle_king_side(piece.get_color())
                                    self.set_king_location([7, 6], piece.get_color())
                                    piece.set_has_moved()
                                elif destination == [7, 2]:
                                    self.castle_queen_side(piece.get_color())
                                    self.set_king_location([7, 2], piece.get_color())
                                    piece.set_has_moved()

                            # Black King Castling
                            elif piece.get_color() == "B":
                                if destination == [0, 6]:
                                    self.castle_king_side(piece.get_color())
                                    self.set_king_location([0, 6], piece.get_color())
                                    piece.set_has_moved()
                                elif destination == [0, 2]:
                                    self.castle_queen_side(piece.get_color())
                                    self.set_king_location([0, 2], piece.get_color())
                                    piece.set_has_moved()
                        self.set_king_location([end_row, end_col], piece.get_color())

                    # The piece being moved is now reassigned to the destination coordinates.
                    #   The starting square is also set to None occupant (or empty square).
                    piece.set_row(end_row)
                    piece.set_col(end_col)
                    piece.calculate_location()
                    self._board[end_row][end_col].set_occupant(piece)
                    self._board[start_row][start_col].set_occupant(None)
                    # ---------------

                    # Next, we verify that the conducted piece movement has not placed the
                    #   active player's King in check (a violation of game rules).
                    #   If check is True, then we 'reset' the starting and ending squares
                    #   with the original occupants.
                    active_p_king_check = self.scan_for_king_check(self.get_active_p())
                    if active_p_king_check is True:

                        # Updates the King location in the Board() object if illegal move
                        #   must be reversed.
                        if piece.get_letter() == "K":
                            self.set_king_location([start_row, start_col], piece.get_color())
                            # self.scan_for_king_check(self.get_active_p())

                        # Below we reset the starting/ending squares with the original
                        #   occupant values.
                        self._board[start_row][start_col].set_occupant(piece)
                        piece.set_row(start_row)
                        piece.set_col(start_col)
                        piece.calculate_location()
                        self._board[end_row][end_col].set_occupant(save_square)
                        save_square.set_row(end_row)
                        save_square.set_col(end_col)
                        save_square.calculate_location()
                        # ---------------

                        return False

                    # else: the move conducted does not put the active player's King in
                    #   check, then  we can check some additional conditions, depending
                    #   on the type of piece being moved.
                    else:
                        # Sets pawn range so the moved pawn can only move 1 square at a
                        #   time, after it's initial move.
                        if piece.get_letter() == "":
                            piece.set_pawn_range()

                        # Additionally, if the moved piece is the King or Rook type, their
                        #   has_moved value must be set to True for the castling rule.
                        elif piece.get_letter() == "K" or piece.get_letter() == "R":
                            piece.set_has_moved()

                            # I believe this is a redundant and unnecessary check since we have also
                            #   have an identical set_king_location in above branch for King moves.
                            #   (or vice versa, the above set_king_location on line 566 may be unnecessary)
                            if piece.get_letter() == "K":
                                self.set_king_location(destination, piece.get_color())

                        # finally, we check if the active player's piece movement has put their opponent in
                        #   check. If check is True for the inactive player, then we also call an additional
                        #   class method to determine if this check has placed the inactive player's king
                        #   in checkmate.
                        if self.scan_for_king_check(self.get_inactive_p()) is True and simulation is False:
                            if self.scan_for_checkmate(self.get_inactive_p()) is True:
                                print("CHECKMATE!!!")

                        self.set_active_p()
                        return True

                    # possibly might need a return False somewhere around here so we have only
                    # False and True return values as this function has been returning None
                    # values for checkmate verification (which is should not be returning
                    # None, but it currently works in spite of that).
            except AttributeError:
                pass
        else:
            return False

    def scan_for_checkmate(self, color):
        """
        ------------------------------------
        This Board() Class method is used to determine if the King of the
        color parameter has been checkmated.
        ------------------------------------
        :param color: string type, should be either "B" or "W"
        :return: returns True if the player of the color param. has no
                remaining moves which take its king out of check. False
                if there is a possible move that removes the king check.
        """

        # Creates deepcopy of the board, along with all the square() and piece() objects.
        self.set_simulation()
        bool_values = []

        # First we iterate through each square on the board.
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                # ---------------
                try:
                    player_color = self._board[row][col].get_occupant().get_color()
                    occupant = self._board[row][col].get_occupant()

                    # Next, if the current square iteration contains a Piece()
                    #   then all the possible moves are then scanned for the piece.
                    if player_color == color and occupant is not None:
                        piece_moves = self.scan_for_moves(row, col)

                        # Then we iterate through all possible moves for the currently
                        #   analyzed piece. For each possible move, we append the return
                        #   value from the make_move() method and check if the bool_values
                        #   list contains a True. If we obtain a True return then we know
                        #   that there is at least 1 possible move that will take the player
                        #   out of check, thus it is not checkmate and we return False.
                        for each in piece_moves:
                            if self.get_active_p() != color:
                                self.set_active_p()
                            bool_values.append(self.make_move([row, col], each, simulation=True))
                            self.make_move(each, [row, col], simulation=True)

                            if True in bool_values:
                                self.reset_simulation()
                                self.set_active_p()
                                return False

                except AttributeError:
                    continue

        self.reset_simulation()
        self.set_active_p()
        self._checkmate = True
        return True

    def scan_all_piece_moves(self, color):
        """
        ------------------------------------
        This Board() Class method scans for all piece moves for a player color and
        appends these coordinates to a list. This method is used to determine which
        board squares the player controls. This will also include squares that are
        occupied by a piece if that Square() in the capture range of a Piece().
        ------------------------------------
        :param color: string type, represents player's color as "B" or "W"
        :return: the list containing all the piece moves for the color param.
        """

        # Iterates through each square on the board and scans for moves
        #   if the Square() contains a Piece() occupant.
        self.reset_covered_squares(color)
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                try:
                    self.scan_for_moves(row, col, scan_for_piece=False)
                except AttributeError:
                    continue

        if color == "W":
            return self.get_white_covered_squares()
        elif color == "B":
            return self.get_black_covered_squares()

    def scan_for_king_check(self, color):
        """
        ------------------------------------
        This Board() Class method scans the board to determine if the color param
        King is in check. I.e. if the King is found on one of the Squares()
        controlled by the opponent, then the King is in check.
        ------------------------------------
        :param color:
        :return:
        """
        self.reset_covered_squares(self.get_active_p())
        self.scan_all_piece_moves(self.get_active_p())
        self.reset_covered_squares(self.get_inactive_p())
        self.scan_all_piece_moves(self.get_inactive_p())

        if color == "B":
            b_king = self.get_b_king_location()
            white_controlled_squares = self.get_white_covered_squares()

            if b_king in white_controlled_squares:
                self._black_king_in_check = True
                print("BLACK KING IN CHECK!!!")
                return True
            else:
                self._black_king_in_check = False
                return False

        elif color == "W":
            w_king = self.get_w_king_location()
            black_controlled_squares = self.get_black_covered_squares()

            if w_king in black_controlled_squares:
                self._white_king_in_check = True
                print("WHITE KING IN CHECK!!!")
                return True
            else:
                self._white_king_in_check = False
                return False
        else:
            return False

    def castle_king_side(self, color):
        """
        ------------------------------------
        This Board() class method conducts the King side Castle.
        ------------------------------------
        :param color: string type passed as either "B" or "W"
        :return: None
        """

        # Below are two if statements that check for the color param.
        #   If this method is called, it simply checks the color param
        #   that was entered and conducts the King side castle with the
        #   hardcoded square reassignments within the if/elif blocks.
        if color == "W":

            # Changes Piece() attributes for King and Rook objects.
            king_side_rook = self._board[7][7].get_occupant()
            king = self._board[7][4].get_occupant()
            king_side_rook.set_has_moved()
            king_side_rook.set_row(7)
            king_side_rook.set_col(5)
            king_side_rook.calculate_location()
            king.set_has_moved()
            king.set_row(7)
            king.set_col(6)
            king.calculate_location()

            # Changes Board() attributes
            self._board[7][5].set_occupant(king_side_rook)
            self._board[7][6].set_occupant(king)
            self._board[7][4].set_occupant(None)
            self._board[7][7].set_occupant(None)

        elif color == "B":
            # Changes Piece() attributes for King and Rook objects.
            king_side_rook = self._board[0][7].get_occupant()
            king = self._board[0][4].get_occupant()
            king_side_rook.set_has_moved()
            king_side_rook.set_row(0)
            king_side_rook.set_col(5)
            king_side_rook.calculate_location()
            king.set_has_moved()
            king.set_row(0)
            king.set_col(6)
            king.calculate_location()

            # Changes Board() attributes
            self._board[0][5].set_occupant(king_side_rook)
            self._board[0][6].set_occupant(king)
            self._board[0][4].set_occupant(None)
            self._board[0][7].set_occupant(None)

    def castle_queen_side(self, color):
        """
        ------------------------------------
        This Board() class method conducts the Queen side Castle.
        ------------------------------------
        :param color: string type passed as either "B" or "W"
        :return: None
        """

        # This method is similar to the castle_king_side() method as each square
        #   reassignment is simply just hardcoded if this method is called.
        if color == "W":
            # Changes Piece() attributes for King and Rook objects.
            queen_side_rook = self._board[7][0].get_occupant()
            king = self._board[7][4].get_occupant()
            queen_side_rook.set_has_moved()
            queen_side_rook.set_row(7)
            queen_side_rook.set_col(3)
            queen_side_rook.calculate_location()
            king.set_has_moved()
            king.set_row(7)
            king.set_col(2)
            king.calculate_location()

            # Changes Board() attributes
            self._board[7][3].set_occupant(queen_side_rook)
            self._board[7][2].set_occupant(king)
            self._board[7][4].set_occupant(None)
            self._board[7][0].set_occupant(None)

        elif color == "B":
            # Changes Piece() attributes for King and Rook objects.
            queen_side_rook = self._board[0][0].get_occupant()
            king = self._board[0][4].get_occupant()
            queen_side_rook.set_has_moved()
            queen_side_rook.set_row(0)
            queen_side_rook.set_col(3)
            queen_side_rook.calculate_location()
            king.set_has_moved()
            king.set_row(0)
            king.set_col(2)
            king.calculate_location()

            # Changes Board() attributes
            self._board[0][3].set_occupant(queen_side_rook)
            self._board[0][2].set_occupant(king)
            self._board[0][4].set_occupant(None)
            self._board[0][0].set_occupant(None)

    def scan_for_moves(self, row, col, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method scans for legal piece moves.
        ------------------------------------
        :param row: starting row index (must be passed as an integer).
        :param col: starting column index (must be passed as an integer).
        :param scan_for_piece: if True we append to that Piece()
                object's moves list, else if False, we append to
                the Board() objects lists for player controlled
                squares.
        :return: the moves list from the Piece() object.
        """

        piece = self._board[row][col].get_occupant()
        piece.clear_moves()

        # SCANS FOR ROOK MOVES
        if piece.get_letter() == "R":
            self.scan_on_column(row, col, piece, scan_for_piece=scan_for_piece)
            self.scan_on_column(row, col, piece, direction=-1, scan_for_piece=scan_for_piece)
            self.scan_on_row(row, col, piece, scan_for_piece=scan_for_piece)
            self.scan_on_row(row, col, piece, direction=-1, scan_for_piece=scan_for_piece)

        # SCANS FOR BISHOP MOVES
        elif piece.get_letter() == "B":
            self.scan_on_diagonal(row, col, piece, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, row_dir=-1, col_dir=-1, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, row_dir=-1, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, col_dir=-1, scan_for_piece=scan_for_piece)

        # SCANS FOR QUEEN'S MOVES
        elif piece.get_letter() == "Q":
            self.scan_on_column(row, col, piece, scan_for_piece=scan_for_piece)
            self.scan_on_column(row, col, piece, direction=-1, scan_for_piece=scan_for_piece)
            self.scan_on_row(row, col, piece, scan_for_piece=scan_for_piece)
            self.scan_on_row(row, col, piece, direction=-1, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, row_dir=-1, col_dir=-1, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, row_dir=-1, scan_for_piece=scan_for_piece)
            self.scan_on_diagonal(row, col, piece, col_dir=-1, scan_for_piece=scan_for_piece)

        # SCANS FOR PAWN MOVES
        elif piece.get_letter() == "":
            if piece.get_color() == "B":
                self.scan_for_pawn(row, col, piece, scan_for_piece=scan_for_piece)
            elif piece.get_color() == "W":
                self.scan_for_pawn(row, col, piece, y_dir=-1, scan_for_piece=scan_for_piece)

        # SCANS FOR KNIGHT MOVES
        elif piece.get_letter() == "N":
            self.scan_for_knight(row, col, piece, scan_for_piece=scan_for_piece)

        # SCANS FOR KING MOVES
        elif piece.get_letter() == "K":
            self.scan_for_king(row, col, piece, scan_for_piece=scan_for_piece)

        # print(piece.get_moves())
        return piece.get_moves()

    def scan_for_king(self, row, col, piece, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method is used to scan for possible King moves.
        ------------------------------------
        :param row: starting row index (must be passed as an integer).
        :param col: starting column index (must be passed as an integer).
        :param piece: the Piece() object for which we are scanning moves.
        :param scan_for_piece: if True we append to that Piece()
                object's moves list, else if False, we append to
                the Board() objects lists for player controlled
                squares.
        :return: None
        """

        # The maximum number of possible moves at any given time for a King
        #   piece will not exceed 8 (not counting King/Queen side castles).
        #   In addition, since these possible moves do not seem to have any
        #   kind of iterative pattern (at least from what I can tell), these
        #   indices are first calculated below and placed within a possible
        #   moves list.
        row_pos_1, col_pos_1 = row + 1, col + 1
        row_neg_1, col_neg_1 = row - 1, col - 1

        moves = \
            [
                [row_pos_1, col_pos_1], [row, col_pos_1], [row_neg_1, col_pos_1],
                [row_neg_1, col], [row_neg_1, col_neg_1], [row, col_neg_1],
                [row_pos_1, col_neg_1], [row_pos_1, col]
            ]
        # ---------------

        # Next, we iterate through each of the possible squares, checking to
        #   see if conditions are met so that the king can legally move to
        #   the square.
        for index in range(len(moves)):
            try:
                x = moves[index][0]
                y = moves[index][1]
                next_square = self._board[x][y]

                # Checks the square and executes if the current square iteration
                #   contains no pieces.
                if next_square.get_occupant() is None:

                    # Below, the if/elif statements check if we are to append the
                    #   move to the Piece() object or the Board() object.
                    #   There is also an identical check in the subsequent elif
                    #   block below.
                    if scan_for_piece is True and 0 <= x <= 7 and 0 <= y <= 7:
                        piece.add_move(x, y)
                    elif scan_for_piece is False and 0 <= x <= 7 and 0 <= y <= 7:
                        self.add_covered_squares(x, y, piece.get_color())

                # Checks the square and executes if current iteration contains the
                #   opposite piece color.
                elif next_square.get_occupant().get_color() != piece.get_color():
                    if scan_for_piece is True and 0 <= x <= 7 and 0 <= y <= 7:
                        piece.add_move(x, y)
                    elif scan_for_piece is False and 0 <= x <= 7 and 0 <= y <= 7:
                        self.add_covered_squares(x, y, piece.get_color())

                # An additional if block is used for when we are scanning for player controlled squares.
                #   I.e., these squares can contain a players own color pieces.
                if next_square.get_occupant().get_color() == piece.get_color() and scan_for_piece is False:
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        self.add_covered_squares(x, y, piece.get_color())

            except AttributeError:
                continue
            except IndexError:
                continue
        # ---------------

        # Lastly, some additional helper functions are called
        #   if the King has not conducted a move. If determined
        #   that we can castle on 1 or both sides, then those
        #   moves are also appended to the King()'s moves list.
        if piece.get_has_moved() is False:
            self.check_king_side_castle(piece)
            self.check_queen_side_castle(piece)

    def check_king_side_castle(self, piece):
        """
        ------------------------------------
        This Board() class method checks if a player can castle King side.
        ------------------------------------
        :param piece: King() object
        :return: None
        """
        try:
            # If statement if checking king side castle for white king
            if piece.get_color() == "W":
                letter = self._board[7][7].get_occupant().get_letter()
                move_status = self._board[7][7].get_occupant().get_has_moved()

                # Next, we need to check the Rook for its move status.
                if letter == "R" and move_status is False:
                    square_1 = self._board[7][5].get_occupant()
                    square_2 = self._board[7][6].get_occupant()

                    # Also checks that the squares between the king side
                    #   rook and king are empty. Similarly there are
                    #   identical checks for the black king in the elif
                    #   block below, however the indices reference the
                    #   coordinates for the black pieces.
                    if square_1 is None and square_2 is None:
                        piece.add_move(7, 6)

            # elif statement if checking castle for black king.
            elif piece.get_color() == "B":
                letter = self._board[0][7].get_occupant().get_letter()
                move_status = self._board[0][7].get_occupant().get_has_moved()

                if letter == "R" and move_status is False:
                    square_1 = self._board[0][5].get_occupant()
                    square_2 = self._board[0][6].get_occupant()

                    if square_1 is None and square_2 is None:
                        piece.add_move(0, 6)

        except AttributeError:
            return

    def check_queen_side_castle(self, piece):
        """
        ------------------------------------
        This Board() class method checks if a player can castle King side.
        ------------------------------------
        :param piece: King() object
        :return: None
        """

        # The logical outline for this method is basically identical to the
        #   check_for_king_side_castle() method, with the exception that we
        #   must check that the 3 squares between King and Rook are empty.
        #   The Rook coordinates as well as the King, are also different, as
        #   they correspond to the Queen side instead of the king side.
        try:
            if piece.get_color() == "W":
                letter = self._board[7][0].get_occupant().get_letter()
                move_status = self._board[7][0].get_occupant().get_has_moved()

                if letter == "R" and move_status is False:
                    square_1 = self._board[7][1].get_occupant()
                    square_2 = self._board[7][2].get_occupant()
                    square_3 = self._board[7][3].get_occupant()

                    if square_1 is None and square_2 is None and square_3 is None:
                        piece.add_move(7, 2)

            elif piece.get_color() == "B":
                letter = self._board[0][0].get_occupant().get_letter()
                move_status = self._board[0][0].get_occupant().get_has_moved()

                if letter == "R" and move_status is False:
                    square_1 = self._board[0][1].get_occupant()
                    square_2 = self._board[0][2].get_occupant()
                    square_3 = self._board[0][3].get_occupant()

                    if square_1 is None and square_2 is None and square_3 is None:
                        piece.add_move(0, 2)

        except AttributeError:
            return

    def scan_on_column(self, row, col, piece, direction=1, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method scans for possible moves along a column.
        ------------------------------------
        :param row: starting row index
        :param col: starting column index
        :param piece: piece object
        :param direction: set to either -1 or 1
        :param scan_for_piece: True or False
        :return: None
        """
        # Default is set to iterate in the down direction, i.e. direction=1.
        # To scan up a column (from white perspective), direction should be set to -1

        status = True
        row = row + direction

        while status and 0 <= row <= 7:
            try:
                next_square = self._board[row][col]

                # Checks the next square in iteration and adds to moves if
                #   the square is empty.
                if next_square.get_occupant() is None:
                    if scan_for_piece is True:
                        piece.add_move(row, col)
                    elif scan_for_piece is False and 0 <= row <= 7 and 0 <= col <= 7:
                        self.add_covered_squares(row, col, piece.get_color())

                # If the next square contains an occupant but it is an opponent's piece
                #   then we add as a last possible move in that direction and terminate
                #   the while loop.
                elif next_square.get_occupant().get_color() != piece.get_color():
                    if scan_for_piece is True:
                        piece.add_move(row, col)
                    elif scan_for_piece is False and 0 <= row <= 7 and 0 <= col <= 7:
                        self.add_covered_squares(row, col, piece.get_color())

                    status = False

                elif next_square.get_occupant().get_color() == piece.get_color() and scan_for_piece is False:
                    self.add_covered_squares(row, col, piece.get_color())
                    status = False
                else:
                    status = False

                row = row + direction

            except AttributeError:
                status = False
            except IndexError:
                status = False

    def scan_on_row(self, row, col, piece, direction=1, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method scans for possible piece moves along a row.
        ------------------------------------
        :param row: starting row index
        :param col: starting column index
        :param piece: The Piece object.
        :param direction: set to either -1 or 1.
        :param scan_for_piece: set to ether True or False.
        :return: None
        """
        # Default direction is set to direction=1, this will iterate on squares
        #   towards the right side of the board.
        # If direction=-1, then we can also iterate on squares towards the left
        #   of the starting row, col indices.

        status = True
        col = col + direction

        while status and 0 <= col <= 7:
            try:
                next_square = self._board[row][col]

                if next_square.get_occupant() is None:
                    if scan_for_piece is True:
                        piece.add_move(row, col)
                    elif scan_for_piece is False and 0 <= row <= 7 and 0 <= col <= 7:
                        self.add_covered_squares(row, col, piece.get_color())

                elif next_square.get_occupant().get_color() != piece.get_color():
                    if scan_for_piece is True:
                        piece.add_move(row, col)
                    elif scan_for_piece is False and 0 <= row <= 7 and 0 <= col <= 7:
                        self.add_covered_squares(row, col, piece.get_color())

                    status = False

                elif next_square.get_occupant().get_color() == piece.get_color() and scan_for_piece is False:
                    self.add_covered_squares(row, col, piece.get_color())
                    status = False
                else:
                    status = False

                col = col + direction

            except AttributeError:
                status = False
            except IndexError:
                status = False

    def scan_for_knight(self, row, col, piece, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method scans possible moves for a Knight piece object.
        ------------------------------------
        :param row: starting row index
        :param col: starting column index
        :param piece: Knight piece object.
        :param scan_for_piece: set to either True of False
        :return: None
        """

        # Similarly to a King Piece, a Knight will have a max of 8 possible moves
        #   in the best case scenario, and in addition, due to the mechanics of
        #   Knight movements, each of these are simply hardcoded and appended to
        #   a list of possible moves. Each possible move is then analyzed and
        #   added to the Knight object's moves list if applicable.
        x_pos_2, y_pos_2 = col + 2, row + 2
        x_neg_2, y_neg_2 = col - 2, row - 2
        x_pos_1, y_pos_1 = col + 1, row + 1
        x_neg_1, y_neg_1 = col - 1, row - 1

        moves = \
            [
                [y_pos_1, x_pos_2], [y_neg_1, x_pos_2],
                [y_pos_2, x_pos_1], [y_pos_2, x_neg_1],
                [y_pos_1, x_neg_2], [y_neg_1, x_neg_2],
                [y_neg_2, x_pos_1], [y_neg_2, x_neg_1]
            ]

        for index in range(len(moves)):
            try:
                x = moves[index][0]
                y = moves[index][1]
                next_square = self._board[x][y]

                if next_square.get_occupant() is None:
                    if scan_for_piece is True and 0 <= x <= 7 and 0 <= y <= 7:
                        piece.add_move(x, y)
                    elif scan_for_piece is False and 0 <= x <= 7 and 0 <= y <= 7:
                        self.add_covered_squares(x, y, piece.get_color())

                elif next_square.get_occupant().get_color() != piece.get_color():
                    if scan_for_piece is True and 0 <= x <= 7 and 0 <= y <= 7:
                        piece.add_move(x, y)
                    elif scan_for_piece is False and 0 <= x <= 7 and 0 <= y <= 7:
                        self.add_covered_squares(x, y, piece.get_color())

                elif next_square.get_occupant().get_color() == piece.get_color() and scan_for_piece is False:
                    if 0 <= x <= 7 and 0 <= y <= 7:
                        self.add_covered_squares(x, y, piece.get_color())

            except AttributeError:
                continue
            except IndexError:
                continue

    def scan_on_diagonal(self, row, col, piece, row_dir=1, col_dir=1, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method scans along a diagonal path to check for possible moves.
        ------------------------------------
        :param row: starting row index
        :param col: starting column index
        :param piece: The Piece object.
        :param row_dir: set to either -1 or 1.
        :param col_dir: set to either -1 or 1.
        :param scan_for_piece: set to ether True or False.
        :return: None
        """
        # Similarly to the scanning methods for rows and columns, we can set our directional
        #   parameters to scan towards the desired corner of the board.
        #   Default (row_dir=1, col_dir=1) will iterate towards the bottom right corner of
        #   the playing board.
        #   Setting both to -1 (row_dir=-1, col_dir=-1) will iterate towards the top left.
        #   (row_dir=-1, col_dir=1): iterates towards the top right corner.
        #   (row_dir=1, col_dir=-1): iterates towards the bottom left corner.

        # The logic below is essentially the same layout as the scanning methods for rows and cols
        #   but instead of only changing a row or col on each iteration, both the row and col are
        #   changed so we can iterate and scan along a diagonal path.
        status = True
        col = col + col_dir
        row = row + row_dir

        while status and 0 <= col <= 7 and 0 <= row <= 7:
            try:
                next_square = self._board[row][col]

                if next_square.get_occupant() is None:
                    if scan_for_piece is True:
                        piece.add_move(row, col)
                    elif scan_for_piece is False and 0 <= row <= 7 and 0 <= col <= 7:
                        self.add_covered_squares(row, col, piece.get_color())

                elif next_square.get_occupant().get_color() != piece.get_color():
                    if scan_for_piece is True:
                        piece.add_move(row, col)

                    elif scan_for_piece is False and 0 <= row <= 7 and 0 <= col <= 7:
                        self.add_covered_squares(row, col, piece.get_color())

                    status = False

                elif next_square.get_occupant().get_color() == piece.get_color() and scan_for_piece is False:
                    self.add_covered_squares(row, col, piece.get_color())
                    status = False
                else:
                    status = False

                col = col + col_dir
                row = row + row_dir

            except AttributeError:
                status = False
            except IndexError:
                status = False

    def scan_for_pawn(self, row, col, piece, y_dir=1, scan_for_piece=True):
        """
        ------------------------------------
        This Board() class method scans for possible Pawn() piece moves.
        ------------------------------------
        :param row: starting row index
        :param col: starting column index
        :param piece: The Pawn() object.
        :param y_dir: set to either -1 or 1.
        :param scan_for_piece: set to ether True or False.
        :return: None
        """
        y = row + y_dir
        x_neg = col - 1
        x_pos = col + 1

        pawn_moves = piece.get_pawn_range()
        status = True

        # Depending on the Pawn() object's pawn range attribute, we scan
        #   either 1 or 2 squares forward (from player's perspective) for
        #   possible movement.
        while status and pawn_moves > 0:
            try:
                row = row + y_dir
                next_square = self._board[row][col]

                if next_square.get_occupant() is None:
                    piece.add_move(row, col)
                    pawn_moves -= 1

                elif next_square.get_occupant() is not None:
                    status = False

            except IndexError:
                status = False
            except AttributeError:
                status = False

            # Checks for diagonal capture for Pawn Pieces
            for square in range(2):
                try:
                    next_square_neg = self._board[y][x_neg]
                except IndexError:
                    next_square_neg = None

                try:
                    next_square_pos = self._board[y][x_pos]
                except IndexError:
                    next_square_pos = None

                try:
                    if square == 0:
                        if next_square_neg.get_occupant().get_color() != piece.get_color():
                            if scan_for_piece is True:
                                piece.add_move(y, x_neg)
                            else:
                                self.add_covered_squares(y, x_neg, piece.get_color())

                    if square == 1:
                        if next_square_pos.get_occupant().get_color() != piece.get_color():
                            if scan_for_piece is True:
                                piece.add_move(y, x_pos)
                            else:
                                self.add_covered_squares(y, x_pos, piece.get_color())

                except AttributeError:
                    continue

    def generate_board(self):
        """
        ------------------------------------
        This Board() class method is used to generate a new board as a list.
        Arguments: None
        ------------------------------------
        """

        # Creates an 8x8 list containing Square() objects which will
        #   either have a "B" for black square or "W" for white color
        #   in an alternating pattern, as found on a traditional chess
        #   playing board.
        for row in range(8):
            new_row = []
            for column in range(8):
                if row % 2 != 0:
                    if column % 2 != 0:
                        new_row.append(Square(row, column, None, "W"))
                    else:
                        new_row.append(Square(row, column, None, "B"))

                elif row % 2 == 0:
                    if column % 2 != 0:
                        new_row.append(Square(row, column, None, "B"))
                    else:
                        new_row.append(Square(row, column, None, "W"))

            self._board.append(new_row)
        self.set_board_pieces()

    def set_board_pieces(self):
        """
        ------------------------------------
        This Board() class method is used to initialize all Piece() objects
        as well as set them in their appropriate starting positions as Square()
        occupants. Takes no arguments
        ------------------------------------
        """
        # Each piece is initialized and set to the appropriate
        #   starting row, col values.

        # Piece() setup for Black
        for y in range(8):
            self._board[1][y].set_occupant(Pawn(1, y, "B"))
        self._board[0][0].set_occupant(Rook(0, 0, "B"))
        self._board[0][7].set_occupant(Rook(0, 7, "B"))
        self._board[0][1].set_occupant(Knight(0, 1, "B"))
        self._board[0][6].set_occupant(Knight(0, 6, "B"))
        self._board[0][3].set_occupant(Queen(0, 3, "B"))
        self._board[0][4].set_occupant(King(0, 4, "B"))
        self._board[0][2].set_occupant(Bishop(0, 2, "B"))
        self._board[0][5].set_occupant(Bishop(0, 5, "B"))
        self.set_b_king_location([0, 4])

        # Piece() setup for White
        for y in range(8):
            self._board[6][y].set_occupant(Pawn(6, y, "W"))
        self._board[7][0].set_occupant(Rook(7, 0, "W"))
        self._board[7][7].set_occupant(Rook(7, 7, "W"))
        self._board[7][1].set_occupant(Knight(7, 1, "W"))
        self._board[7][6].set_occupant(Knight(7, 6, "W"))
        self._board[7][3].set_occupant(Queen(7, 3, "W"))
        self._board[7][4].set_occupant(King(7, 4, "W"))
        self._board[7][2].set_occupant(Bishop(7, 2, "W"))
        self._board[7][5].set_occupant(Bishop(7, 5, "W"))
        self.set_w_king_location([7, 4])

    def print_board(self):
        """
        This class method is used to print the self._board list to terminal.
        It has no functionality in the execution of the program, but it was
        used while creating this program.
        """
        print(len(self._board))
        for index in range(len(self._board)):
            for i in range(len(self._board[index])):
                print(self._board[index][i].get_occupant())

    def draw_board(self, win):
        """
        ------------------------------------
        This Board() class method is used to draw a blue and white checkered board
        using the Pygame module.
        ------------------------------------
        :param win: the window we will draw the checkered pattern onto.
        :returns None
        """

        pygame.display.set_caption("Chess by Chris")
        win.fill(blue)

        for row in range(rows):
            for col in range(row % 2, rows, 2):
                pygame.draw.rect(win, white, (row * size, col * size, size, size))

    def draw_pieces(self, win):
        """
        ------------------------------------
        This Board() class method draws each Piece() object onto the Pygame window.
        ------------------------------------
        :param win: the window we will draw the the Pieces onto.
        :returns None
        """

        # Below, we iterate over each Square() object, and if the Square contains
        #   a Piece() object, then we get that piece's translated (x, y) coordinates
        #   so we can draw the appropriate piece at the corresponding (x, y) onto the
        #   generated pygame window.
        for row in range(8):
            for col in range(8):
                try:
                    piece = self._board[row][col].get_occupant()
                    player_color = piece.get_color()
                    piece_type = piece.get_letter()

                    if player_color == "B" and piece_type == "K":
                        win.blit(black_king, (piece.get_x(), piece.get_y()))
                    elif player_color == "B" and piece_type == "Q":
                        win.blit(black_queen, (piece.get_x(), piece.get_y()))
                    elif player_color == "B" and piece_type == "R":
                        win.blit(black_rook, (piece.get_x(), piece.get_y()))
                    elif player_color == "B" and piece_type == "B":
                        win.blit(black_bishop, (piece.get_x(), piece.get_y()))
                    elif player_color == "B" and piece_type == "N":
                        win.blit(black_knight, (piece.get_x(), piece.get_y()))
                    elif player_color == "B" and piece_type == "":
                        win.blit(black_pawn, (piece.get_x(), piece.get_y()))
                    elif player_color == "W" and piece_type == "K":
                        win.blit(white_king, (piece.get_x(), piece.get_y()))
                    elif player_color == "W" and piece_type == "Q":
                        win.blit(white_queen, (piece.get_x(), piece.get_y()))
                    elif player_color == "W" and piece_type == "R":
                        win.blit(white_rook, (piece.get_x(), piece.get_y()))
                    elif player_color == "W" and piece_type == "B":
                        win.blit(white_bishop, (piece.get_x(), piece.get_y()))
                    elif player_color == "W" and piece_type == "N":
                        win.blit(white_knight, (piece.get_x(), piece.get_y()))
                    elif player_color == "W" and piece_type == "":
                        win.blit(white_pawn, (piece.get_x(), piece.get_y()))

                except AttributeError:
                    continue

    def draw_piece_moves(self, win, mouse_coord):
        """
        ------------------------------------
        This Board() class method draws each Piece() object's possible moves
        onto the Pygame window as medium sized red dots.
        ------------------------------------
        :param win: the window we will draw the possible moves onto.
        :param mouse_coord: these are obtained in main() with pygame.MOUSEBUTTONDOWN
                as a tuple containing (x, y).
        :returns None
        """
        try:
            # First, we need to translate the pygame coordinates to list indices
            mouse_coord = list(mouse_coord)
            col = (mouse_coord[0] // 80)
            row = (mouse_coord[1] // 80)

            # Then using the indices, we get the occupant at the location and
            #   scan for all possible moves for the corresponding piece.
            piece = self._board[row][col].get_occupant()
            self.scan_for_moves(row, col)
            moves = piece.get_moves()

            # Next, we iterate through the list of possible moves, and draw them
            #   out as medium-sized red dots on squares which the piece object
            #   can potentially move to.
            for square in range(len(moves)):
                draw_on_board_y = (moves[square][0]) * 80 + 40
                draw_on_board_x = (moves[square][1]) * 80 + 40
                pygame.draw.circle(win, (255, 0, 0), (draw_on_board_x, draw_on_board_y), 10)

        except AttributeError:
            return
        except IndexError:
            return


class ChessGame:
    """
    Class ChessGame object is a class that represents a chess game.
    """
    def __init__(self):
        """
        Constructor method for class ChessGame.
        """

        # Note: There are some redundant class attributes as some of
        #   them also are attributes of class Board(). Some were
        #   initially intended to have purpose/functionality in class
        #   ChessGame, however I had to move several to Board() to get
        #   certain things working properly. I may remove some of these
        #   at a later time to clean up some of the extra code.
        self._player_turn = "W"
        self._inactive_p = "B"
        self._game_state = True
        self._board = Board()
        self._board.generate_board()
        self._white_check = False
        self._black_check = False
        self._move_num = 1
        self._moves = []

    def record_move(self, start, destination):
        """
        This method will be used to record each players move using
        traditional chess move notation.
        :param start:
        :param destination:
        :return:
        """
        pass

    def make_move(self, start, destination):
        """
        This class method is used to conduct a Piece move.
        :param start: starting pygame coordinates
        :param destination: destination pygame coordinates.
        :return: None
        """
        # There is not much functionality to this class's method
        #   since it calls on the Board() method to conduction
        #   the actual piece movement. To see how a piece move
        #   is conducted, please look at Class Board().
        if self._board.make_move(start, destination) is True:
            self.set_player_turn()

    def set_check(self, color):
        """
        This class method sets the check attribute to True if
        player king is in check.
        :param color: player's color, either "B" or "W". Passed as string.
        :return: None
        """
        if color == "W":
            self._white_check = True
        elif color == "B":
            self._black_check = True

    def draw_squares(self, win):
        """
        This class method draws a checkered board pattern onto the pygame window.
        Note: Please see draw_board() method in Class Board() for more detail on
            functionality.
        :param win: the pygame window to draw onto.
        :return: None
        """
        self._board.draw_board(win)

    def draw_pieces(self, win):
        """
        This class method is used to draw each of the remaining pieces onto
        the pygame window.
        Note: Please see draw_pieces() method in Class Board() for more detail on
            functionality.
        :param win:
        :return:
        """
        self._board.draw_pieces(win)

    def draw_moves(self, win, mouse_coord):
        """
        This class method draws a Piece's possible moves onto the pygame window.
        Note: Please see draw_piece_moves() method in Class Board() for more detail on
            functionality if desired or needed.
        :param win: the pygame window
        :param mouse_coord: starting square coordinates where mouse was clicked.
        :return: None
        """

        # This first try/except clause was added due to the program randomly
        #   crashing when attempting to click on a square. There did not seem
        #   to be a particular reason as to why this was the case, but since
        #   the addition of the try/except, there has been no subsequent
        #   TypeErrors that have been raised.
        try:
            square = list(mouse_coord)
            start_col, start_row = square[0] // 80, square[1] // 80

            # This second try/except ensures (hopefully) that the program does
            #   not crash if the user selects/clicks on an empty square.
            try:
                piece_color = self._board.get_board()[start_row][start_col].get_occupant().get_color()
                if piece_color == self.get_player_turn():
                    self._board.draw_piece_moves(win, mouse_coord)
                else:
                    return

            except AttributeError:
                return
            except IndexError:
                return

        except TypeError:
            pass

    def get_player_turn(self):
        """
        This class method is used to return the currently active player.
        :return: self._player_turn (the active player)
        """
        return self._player_turn

    def get_game_state(self):
        """
        This class method is used to get the current game state.
        :return: self._game_state (either a True or False value)
        """
        self._game_state = not (self._board.get_checkmate_bool())
        return self._game_state

    def set_player_turn(self):
        """
        This class method sets the active player attribute self._player_turn.
        :return: None
        """
        temp = self.get_player_turn()
        if temp == "W":
            self._inactive_p = "W"
            self._player_turn = "B"
        elif temp == "B":
            self._inactive_p = "B"
            self._player_turn = "W"
        self._move_num += 0.5

    def set_game_state(self, bool_value):
        """
        This class method sets the game state
        :param bool_value: either True or False.
        :return: None
        """
        self._game_state = bool_value

    def print_code_board(self):
        """
        This class method is used to print a Board() object's
        list to terminal using method print_board() from class
        Board().
        :return: None
        """
        self._board.print_board()


def main():

    game = ChessGame()

    clock = pygame.time.Clock()
    game.draw_squares(window)
    game.draw_pieces(window)

    mouse_start_pos = 0
    mouse_end_pos = 0
    pygame.display.update()
    run = True
    while run:
        clock.tick(fps)
        pygame.time.delay(100)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if game.get_game_state() is False:
                print('GAME OVER')
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_start_pos = pygame.mouse.get_pos()
                # print(mouse_start_pos)
                pygame.display.update()

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                game.draw_moves(window, mouse_start_pos)
                pygame.display.update()

            elif pygame.mouse.get_pressed(num_buttons=3)[0] is False:
                game.draw_squares(window)
                game.draw_pieces(window)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_end_pos = pygame.mouse.get_pos()
                game.make_move(mouse_start_pos, mouse_end_pos)
                game.draw_squares(window)
                game.draw_pieces(window)
                pygame.display.update()
                # print(mouse_end_pos)

    pygame.quit()


if __name__ == "__main__":
    main()
