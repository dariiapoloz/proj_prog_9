class CheckersLogic:
    def __init__(self):
        self.SIZE = 8
        self.turn = 'w'
        self.selected = None
        self.board = [[None] * 8 for _ in range(8)]
        self._board_setup()
        self.must_continue = False
        self.winner = None

    def _board_setup(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.board[row][col] = 'b'
                    elif row > 4:
                        self.board[row][col] = 'w'

    def click(self, row2, col2):
        if self.selected:
            row1, col1 = self.selected
            piece = self.board[row1][col1]

            if self.move(row1, col1, row2, col2, piece):
                if not self.must_continue:
                    self.selected = None
                return True
            if not self.must_continue:      
                self.selected = None
            return True

        if self.board[row2][col2] and self.board[row2][col2].lower() == self.turn:
            self.selected = (row2, col2)
            return True

        return False

    def move(self, row1, col1, row2, col2, piece):
        if piece is None:
            return False
        
        dir_row = row2 - row1
        dir_col = col2 - col1
        direction = -1 if piece.lower() == 'w' else 1
        
        if not (0 <= row1 < self.SIZE and 0 <= col1 < self.SIZE):
            return False

        if not (0 <= row2 < self.SIZE and 0 <= col2 < self.SIZE):
            return False

        if abs(dir_col) == 1 and self.board[row2][col2] is None:
            if dir_row == direction or piece.isupper():
                self._move_piece(row1, col1, row2, col2, piece)
                self.must_continue = False
                self._switch_turn()
                self.check_winner()
                return True

        if abs(dir_col) == 2 and abs(dir_row) == 2 and self.board[row2][col2] is None:
            mid_row, mid_col = row1 + dir_row // 2, col1 + dir_col // 2
            opponent = self.board[mid_row][mid_col]

            if opponent and opponent.lower() != piece.lower():
                if dir_row == 2 * direction or piece.isupper():
                    self.board[mid_row][mid_col] = None
                    self._move_piece(row1, col1, row2, col2, piece)

                    if self._can_capture(row2, col2):
                        self.selected = (row2, col2)
                        self.must_continue = True
                        return True
                    self.must_continue = False
                    self._switch_turn()
                    self.check_winner()
                    return True
                    
        return False

    def _move_piece(self, row1, col1, row2, col2, piece):
        self.board[row1][col1] = None

        if (piece == 'w' and row2 == 0) or (piece == 'b' and row2 == 7):
            piece = piece.upper()
        self.board[row2][col2] = piece

    def _can_capture(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return False

        directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)] 

        for dir_row, dir_col in directions:
            new_row, new_col = row + dir_row, col + dir_col
            if 0 <= new_row < self.SIZE and 0 <= new_col < self.SIZE:
                if self.board[new_row][new_col] is None:
                    mid_row, mid_col = row + dir_row // 2, col + dir_col // 2
                    opponent = self.board[mid_row][mid_col]

                    if opponent and opponent.lower() != piece.lower():
                        if piece.isupper():
                            return True
                        direction = -1 if piece == 'w' else 1
                        if dir_row == 2 * direction:
                            return True
        return False
    
    def check_winner(self):
        white_exists = False
        black_exists = False

        for row in range(self.SIZE):
            for col in range(self.SIZE):
                piece = self.board[row][col]
                if piece:
                    if piece.lower() == 'w':
                        white_exists = True
                    elif piece.lower() == 'b':
                        black_exists = True

        if not white_exists:
            self.winner = 'Black'
        elif not black_exists:
            self.winner = 'White'
            
    def _switch_turn(self):
        self.turn = 'b' if self.turn == 'w' else 'w' 
        self.check_winner()
