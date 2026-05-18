class CheckersLogic:
    def __init__(self):
        self.SIZE = 8
        self.turn = 'w'
        self.selected = None
        self.board = [[None] * 8 for _ in range(8)]
        self._board_setup()
        self.must_continue = False
        self.winner = None
        self.white_count = 12
        self.black_count = 12

    def _board_setup(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 != 0:
                    if row < 3:
                        self.board[row][col] = 'b' #black pieces on top
                    elif row > 4:
                        self.board[row][col] = 'w' #white pieces on bottom
                        
    def _in_bounds(self, row, col): #checks if coordinates are within the board
        return 0 <= row < self.SIZE and 0 <= col < self.SIZE
    
    def handle_click(self, row2, col2):
        if self.selected:
            row1, col1 = self.selected
            piece = self.board[row1][col1]

            if self.move(row1, col1, row2, col2, piece):
                if not self.must_continue:
                    self.selected = None
                return True
            if not self.must_continue: # clears selection if move failed      
                self.selected = None
            return True

        if self.board[row2][col2] and self.board[row2][col2].lower() == self.turn: # selects piece if it belongs to current player
            self.selected = (row2, col2)
            return True

        return False

    def move(self, row1, col1, row2, col2, piece):
        if piece is None:
            return False
        
        dir_row, dir_col = row2 - row1, col2 - col1 #direction 
        direction = -1 if piece.lower() == 'w' else 1

        if not self._in_bounds(row2, col2):# check if it's within bounds for both start and end positions
            return False

        if not self._in_bounds(row2, col2):
            return False

        if piece.isupper() and self.board[row2][col2] is None:

            if abs(dir_row) == abs(dir_col):# must move diagonally

                step_row = 1 if dir_row > 0 else -1
                step_col = 1 if dir_col > 0 else -1
                r = row1 + step_row
                c = col1 + step_col
                opponent_found = None

                while r != row2 and c != col2:
                    current = self.board[r][c]

                    if current:
                        if current.lower() == piece.lower():# own piece blocks movement
                            return False

                        if opponent_found:# cannot jump over 2 pieces
                            return False
                        opponent_found = (r, c)
                    r += step_row
                    c += step_col
                    
                if opponent_found:
                    opp_row, opp_col = opponent_found
                    self._capture_piece(opp_row, opp_col)
                    self._move_piece(row1, col1, row2, col2, piece)
                    return self._end_turn(row2, col2, capture_made=True)
                else:
                    self._move_piece(row1, col1, row2, col2, piece)
                    return self._end_turn(row2, col2, capture_made=False)

        if abs(dir_col) == 1 and self.board[row2][col2] is None:        # normal pieces move 1  square
            if dir_row == direction:
                self._move_piece(row1, col1, row2, col2, piece)
                return self._end_turn(row2, col2, capture_made=False)

        if abs(dir_col) == 2 and abs(dir_row) == 2 and self.board[row2][col2] is None: # capture move is 2 squares diagonally
            mid_row = row1 + dir_row // 2
            mid_col = col1 + dir_col // 2
            opponent = self.board[mid_row][mid_col]
            
            if opponent and opponent.lower() != piece.lower():
                if dir_row == 2 * direction:
                    self._capture_piece(mid_row, mid_col)
                    self._move_piece(row1, col1, row2, col2, piece)
                    return self._end_turn(row2, col2, capture_made=True)
        return False
    
    def _end_turn(self, row, col, capture_made):
        
        if capture_made and self._can_capture(row, col):
            self.selected = (row, col)
            self.must_continue = True
        else:
            self.must_continue = False
            self.turn = 'b' if self.turn == 'w' else 'w' 
            self.check_winner()
        return True

    def _move_piece(self, row1, col1, row2, col2, piece):
        self.board[row1][col1] = None

        if (piece == 'w' and row2 == 0) or (piece == 'b' and row2 == 7):
            piece = piece.upper()
        self.board[row2][col2] = piece

    def _can_capture(self, row, col):
        piece = self.board[row][col]
        if not piece:
            return False
        is_queen = piece.isupper()
        
        if is_queen:# Check queen captures
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                opponent_found = False
                while self._in_bounds(r, c):
                    current = self.board[r][c]
                    if current:  
                        if current.lower() == piece.lower() or opponent_found:
                            break
                        opponent_found = True
                    else:
                        if opponent_found:
                            return True
                    r += dr
                    c += dc
            return False
        
        direction = -1 if piece == 'w' else 1
        capture_moves = [(2 * direction, -2), (2 * direction, 2)] 

        for dir_row, dir_col in capture_moves:# Check  piece captures
            new_row, new_col = row + dir_row, col + dir_col
            if self._in_bounds(new_row, new_col) and self.board[new_row][new_col] is None:
                mid_row, mid_col = row + dir_row // 2, col + dir_col // 2
                opponent = self.board[mid_row][mid_col]
                if opponent and opponent.lower() != piece.lower():
                    return True
        return False
    
    def _capture_piece(self, row, col):
        captured = self.board[row][col]
        self.board[row][col] = None
        if captured.lower() == 'w':
            self.white_count -= 1
        else:
            self.black_count -= 1
            
    def check_winner(self):
        if self.white_count == 0:
            self.winner = 'Black'
        elif self.black_count == 0:
            self.winner = 'White'
