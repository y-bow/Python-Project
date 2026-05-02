import pygame
import chess
import os
import time
import sys

class ChessGame:
    def __init__(self):
        pygame.init()
        
        # Auto Fullscreen Detection
        info = pygame.display.Info()
        self.screen_w = info.current_w
        self.screen_h = info.current_h
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h), pygame.FULLSCREEN)
        pygame.display.set_caption("Chess Pro - Fullscreen Mode")
        
        # Dynamic Scaling
        self.panel_h = self.screen_h // 12
        available_board_h = self.screen_h - (2 * self.panel_h)
        self.sq_size = min(self.screen_w, available_board_h) // 8
        
        self.board_w = self.sq_size * 8
        self.board_h = self.sq_size * 8
        self.offset_x = (self.screen_w - self.board_w) // 2
        self.offset_y = (self.screen_h - self.board_h) // 2
        
        # Colors - Premium Palette
        self.WHITE_SQ = (240, 240, 220)
        self.DARK_SQ = (120, 150, 80)
        self.BG_COLOR = (25, 25, 25)
        self.TEXT_COLOR = (255, 255, 255)
        self.TIMER_BG = (15, 15, 15)
        self.HIGHLIGHT_COLOR = (255, 255, 0, 120)
        
        self.board = chess.Board()
        self.images = {}
        self.load_images()
        self.selected_sq = None
        self.legal_moves = []
        self.game_over = False
        
        # Timer settings (10 minutes each)
        self.white_time = 600.0
        self.black_time = 600.0
        self.last_tick = pygame.time.get_ticks()
        
        # Fonts
        self.font_size = self.panel_h // 2
        self.font = pygame.font.SysFont("Segoe UI", self.font_size, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", self.font_size // 2)

    def load_images(self):
        piece_map = {
            'k': '01_black_king.png', 'q': '02_black_queen.png', 'r': '03_black_rook.png',
            'b': '04_black_bishop.png', 'n': '05_black_knight.png', 'p': '06_black_pawn.png',
            'K': '07_white_king.png', 'Q': '08_white_queen.png', 'R': '09_white_rook.png',
            'B': '10_white_bishop.png', 'N': '11_white_knight.png', 'P': '12_white_pawn.png'
        }
        path = "static/images/pieces"
        for p, file in piece_map.items():
            try:
                img = pygame.image.load(os.path.join(path, file)).convert_alpha()
                self.images[p] = pygame.transform.scale(img, (self.sq_size, self.sq_size))
            except Exception as e:
                print(f"Error loading {file}: {e}")
                surf = pygame.Surface((self.sq_size, self.sq_size))
                surf.fill((255, 0, 0))
                self.images[p] = surf

    def format_time(self, seconds):
        if seconds < 0: seconds = 0
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins:02d}:{secs:02d}"

    def draw_panels(self):
        # Full Screen Background
        self.screen.fill(self.BG_COLOR)
        
        # Top Panel (Black Info)
        pygame.draw.rect(self.screen, self.TIMER_BG, (0, 0, self.screen_w, self.panel_h))
        black_timer = self.format_time(self.black_time)
        text = self.font.render(f"Black: {black_timer}", True, (200, 200, 200))
        self.screen.blit(text, (self.offset_x, (self.panel_h - text.get_height()) // 2))
        
        # Bottom Panel (White Info)
        pygame.draw.rect(self.screen, self.TIMER_BG, (0, self.screen_h - self.panel_h, self.screen_w, self.panel_h))
        white_timer = self.format_time(self.white_time)
        text = self.font.render(f"White: {white_timer}", True, (255, 255, 255))
        self.screen.blit(text, (self.offset_x, self.screen_h - self.panel_h + (self.panel_h - text.get_height()) // 2))

        # Instructions
        instr = self.small_font.render("Press 'R' to Reset | 'ESC' to Exit", True, (120, 120, 120))
        self.screen.blit(instr, (self.screen_w - instr.get_width() - self.offset_x, self.screen_h - self.panel_h + (self.panel_h - instr.get_height()) // 2))

    def draw_board(self):
        # Draw board border/shadow
        pygame.draw.rect(self.screen, (10, 10, 10), (self.offset_x - 5, self.offset_y - 5, self.board_w + 10, self.board_h + 10))
        
        for r in range(8):
            for c in range(8):
                color = self.WHITE_SQ if (r + c) % 2 == 0 else self.DARK_SQ
                pygame.draw.rect(self.screen, color, (self.offset_x + c*self.sq_size, self.offset_y + r*self.sq_size, self.sq_size, self.sq_size))

        if self.selected_sq is not None:
            r, c = 7 - (self.selected_sq // 8), self.selected_sq % 8
            s = pygame.Surface((self.sq_size, self.sq_size), pygame.SRCALPHA)
            s.fill(self.HIGHLIGHT_COLOR)
            self.screen.blit(s, (self.offset_x + c*self.sq_size, self.offset_y + r*self.sq_size))

    def draw_pieces(self):
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                r, c = 7 - (sq // 8), sq % 8
                self.screen.blit(self.images[piece.symbol()], (self.offset_x + c*self.sq_size, self.offset_y + r*self.sq_size))

    def draw_moves(self):
        for move in self.legal_moves:
            sq = move.to_square
            r, c = 7 - (sq // 8), sq % 8
            circle_surf = pygame.Surface((self.sq_size, self.sq_size), pygame.SRCALPHA)
            pygame.draw.circle(circle_surf, (0, 0, 0, 60), (self.sq_size//2, self.sq_size//2), self.sq_size // 6)
            self.screen.blit(circle_surf, (self.offset_x + c*self.sq_size, self.offset_y + r*self.sq_size))

    def draw_status(self):
        if self.game_over or self.white_time <= 0 or self.black_time <= 0:
            msg_font = pygame.font.SysFont("Segoe UI", self.sq_size, bold=True)
            msg = "Game Over!"
            if self.board.is_checkmate(): msg = "Checkmate!"
            elif self.board.is_stalemate(): msg = "Stalemate!"
            elif self.white_time <= 0: msg = "Black Wins on Time!"
            elif self.black_time <= 0: msg = "White Wins on Time!"
            
            # Modal Background
            overlay = pygame.Surface((self.screen_w, self.screen_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            
            text = msg_font.render(msg, True, (255, 255, 255))
            rect = text.get_rect(center=(self.screen_w//2, self.screen_h//2))
            self.screen.blit(text, rect)
            
            sub = self.small_font.render("Press 'R' to Restart", True, (200, 200, 200))
            sub_rect = sub.get_rect(center=(self.screen_w//2, self.screen_h//2 + self.sq_size))
            self.screen.blit(sub, sub_rect)
            self.game_over = True

    def update_timers(self):
        if self.game_over: return
        now = pygame.time.get_ticks()
        delta = (now - self.last_tick) / 1000.0
        self.last_tick = now
        if self.board.turn == chess.WHITE: self.white_time -= delta
        else: self.black_time -= delta

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.update_timers()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    if event.key == pygame.K_r:
                        self.board = chess.Board()
                        self.selected_sq = None; self.legal_moves = []
                        self.white_time = 600.0; self.black_time = 600.0
                        self.game_over = False
                        self.last_tick = pygame.time.get_ticks()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    # Check if click is within board
                    if (self.offset_x <= pos[0] < self.offset_x + self.board_w and 
                        self.offset_y <= pos[1] < self.offset_y + self.board_h):
                        c = (pos[0] - self.offset_x) // self.sq_size
                        r = (pos[1] - self.offset_y) // self.sq_size
                        sq = (7 - r) * 8 + c
                        
                        move = next((m for m in self.legal_moves if m.to_square == sq), None)
                        if move:
                            # Auto-promotion
                            if self.board.piece_at(move.from_square).piece_type == chess.PAWN:
                                if (self.board.turn == chess.WHITE and sq >= 56) or (self.board.turn == chess.BLACK and sq <= 7):
                                    move.promotion = chess.QUEEN
                            self.board.push(move)
                            self.selected_sq = None; self.legal_moves = []
                            self.last_tick = pygame.time.get_ticks()
                        else:
                            piece = self.board.piece_at(sq)
                            if piece and piece.color == self.board.turn:
                                self.selected_sq = sq
                                self.legal_moves = [m for m in self.board.legal_moves if m.from_square == sq]
                            else:
                                self.selected_sq = None; self.legal_moves = []

            self.draw_panels()
            self.draw_board()
            self.draw_pieces()
            self.draw_moves()
            self.draw_status()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = ChessGame()
    game.run()
