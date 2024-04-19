class ChessboardReader:
    def read_chessboard(self, input_text):
        chessboard = {}
        rows = input_text.strip().split('\n')
        for row in rows:
            piece, col, row = row.split()
            chessboard[(ord(col) - ord('a') + 1),int(row)] = piece
        return chessboard

    def read_chessboard_from_file(self, file_path):
        with open(file_path, 'r') as file:
            input_text = file.read()
        return self.read_chessboard(input_text)

class Chessboard:
    def __init__(self, chessList=None, parent=None, moves=None, rank=None):
        self.board = {} if chessList is None else chessList
        self.parent = parent
        self.moves = moves
        if rank is not None:
            self.rank = rank
        else:
            self.rank = self._ranking(self.board)

    def __lt__(self, other):
        # Define a comparision for the queue
        return self.rank > other.rank

    def add(self, key, value):
        self.board[key] = value

    def _ranking(self, chessboard):
        scores = {
            "queen": 6,
            "rook": 5,
            "bishop": 4,
            "knight": 3,
            "king": 2,
            "pawn": 1
        }
        totalScore = 0
        pieceCount = len(chessboard)

        if self.parent is None:
            for chess in chessboard:
                for other_chess in chessboard:
                    if self.can_capture(chess, other_chess):
                        totalScore += scores[self.board[chess]]
        else:
            old_items = set(self.parent.board.items())
            new_items = set(self.board.items())

            added_items = new_items - old_items
            removed_items = old_items - new_items
            added_values = {key: value for key, value in added_items}
            removed_values = {key: value for key, value in removed_items}
            for chess in added_values:
                for other_chess in chessboard:
                    if self.can_capture(chess, other_chess):
                        totalScore += scores[self.board[chess]]
            for chess in removed_values:
                for other_chess in chessboard:
                    if self.can_capture(chess, other_chess):
                        totalScore -= scores[self.board[chess]]

        return (totalScore, -pieceCount)

    def can_capture(self, this, other):
        if (this[0] == other[0] and this[1] == other[1]):
            return False
        piece_type = self.board[this]
        if piece_type == "pawn":
            return self._pawn_capture(this, other)
        elif piece_type == "knight":
            return self._knight_capture(this, other)
        elif piece_type == "bishop":
            return self._bishop_capture(this, other)
        elif piece_type == "rook":
            return self._rook_capture(this, other)
        elif piece_type == "queen":
            return self._queen_capture(this, other)
        elif piece_type == "king":
            return self._king_capture(this, other)

    def _pawn_capture(self, this, other):
        # pawn can only move upward and eat diagonally
        # Assuming pawns move upwards
        return (abs(this[0] - other[0]) == 1 and other[1] - this[1] == 1)

    def _knight_capture(self, this, other):
        # kngiht moves in an L shape, to the x or y direction
        dx = abs(this[0] - other[0])
        dy = abs(this[1] - other[1])
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)

    def _bishop_capture(self, this, other):
        # bishop move diangoally
        return self._check_diagonal(this, other)

    def _rook_capture(self, this, other):
        # rook capture horizontally or vertically
        return self._check_vertical(this, other)

    def _queen_capture(self, this, other):
        # queen combine the move of rook and bishop
        if self._check_diagonal(this, other):
            return True
        if self._check_vertical(this, other):
            return True
        return False

    def _king_capture(self, this, other):
        # king capture one cell around him
        return abs(this[0] - other[0]) <= 1 and abs(this[1] - other[1]) <= 1

    def _check_diagonal(self, this, other):
        if abs(this[0] - other[0]) == abs(this[1] - other[1]):
            dx = other[0] - this[0]
            dy = other[1] - this[1]

            # Calculate the step sizes for x and y
            step_x = 1 if dx > 0 else -1
            step_y = 1 if dy > 0 else -1

            # Start from the square after (this[0], this[1])
            x = this[0] + step_x
            y = this[1] + step_y

            # Check squares along the diagonal until reaching (other[0], other[1])
            while (x, y) != (other[0], other[1]):
                # If there's a piece at any square along the diagonal, return True
                if (x,y) in self.board:
                    return False
                # Move to the next square along the diagonal
                x += step_x
                y += step_y
            return True
        return False

    def _check_vertical(self, this, other):
        if this[0] == other[0]:  # Vertical movement
            step_x = 0
            step_y = 1 if other[1] > this[1] else -1
        elif this[1] == other[1]:  # Horizontal movement
            step_x = 1 if other[0] > this[0] else -1
            step_y = 0
        else:
            # Invalid movement for a rook
            return False

        # Start from the square after (this[0], this[1])
        x = this[0] + step_x
        y = this[1] + step_y

        # Check squares along the path until reaching (other[0], other[1])
        while (x, y) != (other[0], other[1]):
            # If there's a piece at any square along the path, return False
            if (x,y) in self.board:
                return False
            # Move to the next square along the path
            x += step_x
            y += step_y

        # If no piece was found between (this[0], this[1]) and (other[0], other[1]), return True
        return True

