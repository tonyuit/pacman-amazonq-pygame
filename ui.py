import pygame
import math

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class UI:
    def __init__(self, surface):
        """Initialize UI elements"""
        self.surface = surface
        self.width = surface.get_width()
        self.height = surface.get_height()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Try to load logo
        try:
            self.logo = pygame.image.load('assets/images/logo.png')
            self.logo = pygame.transform.scale(self.logo, (300, 100))
            self.has_logo = True
        except:
            self.has_logo = False
    
    def draw_text(self, text, font, color, x, y, align="center"):
        """Draw text with specified alignment"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.left = x
            text_rect.centery = y
        elif align == "right":
            text_rect.right = x
            text_rect.centery = y
        
        self.surface.blit(text_surface, text_rect)
        return text_rect
    
    def draw_menu(self):
        """Draw the main menu screen"""
        # Background
        self.surface.fill(BLACK)
        
        # Draw decorative elements
        for i in range(0, self.width, 30):
            pygame.draw.circle(self.surface, BLUE, (i, 20), 5)
            pygame.draw.circle(self.surface, BLUE, (i, self.height - 20), 5)
        
        for i in range(0, self.height, 30):
            pygame.draw.circle(self.surface, BLUE, (20, i), 5)
            pygame.draw.circle(self.surface, BLUE, (self.width - 20, i), 5)
        
        # Title
        y_pos = 100
        if self.has_logo:
            logo_rect = self.logo.get_rect(center=(self.width // 2, y_pos))
            self.surface.blit(self.logo, logo_rect)
            y_pos += 120
        else:
            self.draw_text("PAC-MAN", self.title_font, YELLOW, self.width // 2, y_pos)
            y_pos += 80
        
        # Draw Pac-Man and ghost
        pacman_radius = 30
        ghost_radius = 30
        
        # Pac-Man
        pygame.draw.arc(
            self.surface,
            YELLOW,
            pygame.Rect(
                self.width // 2 - 100 - pacman_radius,
                y_pos - pacman_radius,
                pacman_radius * 2,
                pacman_radius * 2
            ),
            math.radians(30),
            math.radians(330),
            pacman_radius
        )
        
        # Ghost
        ghost_x = self.width // 2 + 100
        ghost_y = y_pos
        
        pygame.draw.circle(
            self.surface,
            RED,
            (ghost_x, ghost_y - ghost_radius // 3),
            ghost_radius
        )
        
        pygame.draw.rect(
            self.surface,
            RED,
            pygame.Rect(
                ghost_x - ghost_radius,
                ghost_y - ghost_radius // 3,
                ghost_radius * 2,
                ghost_radius
            )
        )
        
        # Eyes
        pygame.draw.circle(self.surface, WHITE, (ghost_x - 10, ghost_y - 10), 8)
        pygame.draw.circle(self.surface, WHITE, (ghost_x + 10, ghost_y - 10), 8)
        pygame.draw.circle(self.surface, BLACK, (ghost_x - 7, ghost_y - 10), 4)
        pygame.draw.circle(self.surface, BLACK, (ghost_x + 13, ghost_y - 10), 4)
        
        y_pos += 100
        
        # Menu options
        self.draw_text("Press ENTER to Start", self.medium_font, WHITE, self.width // 2, y_pos)
        y_pos += 50
        self.draw_text("Use Arrow Keys to Move", self.small_font, WHITE, self.width // 2, y_pos)
        y_pos += 30
        self.draw_text("ESC to Pause", self.small_font, WHITE, self.width // 2, y_pos)
        
        # Credits
        self.draw_text("© 2025 Pac-Man Clone", self.small_font, WHITE, self.width // 2, self.height - 30)
    
    def draw_game_ui(self, score, lives, level):
        """Draw the in-game UI elements"""
        # Score
        self.draw_text(f"SCORE: {score}", self.medium_font, WHITE, 10, 20, "left")
        
        # Level
        self.draw_text(f"LEVEL: {level}", self.medium_font, WHITE, self.width - 10, 20, "right")
        
        # Lives
        life_x = 10
        life_y = self.height - 30
        self.draw_text("LIVES:", self.small_font, WHITE, life_x, life_y, "left")
        life_x += 70
        
        for i in range(lives):
            pygame.draw.circle(self.surface, YELLOW, (life_x + i * 30, life_y), 10)
    
    def draw_pause_screen(self):
        """Draw the pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.surface.blit(overlay, (0, 0))
        
        # Pause text
        self.draw_text("PAUSED", self.large_font, WHITE, self.width // 2, self.height // 2 - 40)
        self.draw_text("Press ESC to Resume", self.medium_font, WHITE, self.width // 2, self.height // 2 + 20)
        self.draw_text("Press ENTER to Restart", self.small_font, WHITE, self.width // 2, self.height // 2 + 60)
    
    def draw_game_over(self, score):
        """Draw the game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.surface.blit(overlay, (0, 0))
        
        # Game over text
        self.draw_text("GAME OVER", self.large_font, RED, self.width // 2, self.height // 2 - 60)
        self.draw_text(f"FINAL SCORE: {score}", self.medium_font, WHITE, self.width // 2, self.height // 2)
        self.draw_text("Press ENTER to Play Again", self.medium_font, WHITE, self.width // 2, self.height // 2 + 60)
    
    def draw_win_screen(self, score):
        """Draw the win screen"""
        # Semi-transparent overlay with animated colors
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Create a pulsating color effect
        pulse = (pygame.time.get_ticks() % 2000) / 2000.0
        if pulse < 0.5:
            alpha = int(128 + 127 * (pulse * 2))
        else:
            alpha = int(255 - 127 * ((pulse - 0.5) * 2))
        
        overlay.fill((0, 0, 100, alpha))
        self.surface.blit(overlay, (0, 0))
        
        # Win text
        self.draw_text("YOU WIN!", self.large_font, YELLOW, self.width // 2, self.height // 2 - 60)
        self.draw_text(f"FINAL SCORE: {score}", self.medium_font, WHITE, self.width // 2, self.height // 2)
        self.draw_text("Press ENTER to Play Again", self.medium_font, WHITE, self.width // 2, self.height // 2 + 60)
