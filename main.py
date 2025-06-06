import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 30
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pac-Man')
clock = pygame.time.Clock()

# Import game components
from map import Map
from pacman import PacMan
from ghost import Ghost
from ui import UI

class Game:
    def __init__(self):
        self.running = True
        self.state = "MENU"  # MENU, PLAYING, PAUSED, GAME_OVER, WIN
        self.score = 0
        self.lives = 3
        self.level = 1
        self.ui = UI(screen)
        self.reset_game()
        
        # Try to load sounds
        try:
            self.chomp_sound = pygame.mixer.Sound('assets/sounds/chomp.wav')
            self.death_sound = pygame.mixer.Sound('assets/sounds/death.wav')
            self.eat_ghost_sound = pygame.mixer.Sound('assets/sounds/eat_ghost.wav')
            self.power_pellet_sound = pygame.mixer.Sound('assets/sounds/power_pellet.wav')
            self.has_sounds = True
        except:
            self.has_sounds = False
    
    def reset_game(self):
        """Reset the game state for a new game"""
        self.score = 0
        self.lives = 3
        self.level = 1
        self.map = Map(CELL_SIZE)
        self.pacman = PacMan(self.map.pacman_start_pos, CELL_SIZE)
        
        # Create ghosts with different colors and behaviors
        self.ghosts = []
        ghost_colors = [RED, (255, 192, 203), (0, 255, 255), (255, 165, 0)]  # Red, Pink, Cyan, Orange
        ghost_personalities = ["chase", "ambush", "random", "patrol"]
        
        for i, (color, personality) in enumerate(zip(ghost_colors, ghost_personalities)):
            start_pos = self.map.ghost_start_pos[min(i, len(self.map.ghost_start_pos)-1)]
            self.ghosts.append(Ghost(start_pos, CELL_SIZE, color, personality))
        
        self.power_mode = False
        self.power_timer = 0
        self.total_pellets = self.map.count_pellets()
        self.collected_pellets = 0
    
    def handle_events(self):
        """Process game events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.state == "PLAYING":
                        self.state = "PAUSED"
                    elif self.state == "PAUSED":
                        self.state = "PLAYING"
                
                if event.key == K_RETURN:
                    if self.state == "MENU":
                        self.state = "PLAYING"
                    elif self.state == "GAME_OVER" or self.state == "WIN":
                        self.reset_game()
                        self.state = "PLAYING"
                
                # Handle Pac-Man movement
                if self.state == "PLAYING":
                    if event.key == K_UP:
                        self.pacman.change_direction("UP")
                    elif event.key == K_DOWN:
                        self.pacman.change_direction("DOWN")
                    elif event.key == K_LEFT:
                        self.pacman.change_direction("LEFT")
                    elif event.key == K_RIGHT:
                        self.pacman.change_direction("RIGHT")
    
    def update(self):
        """Update game state"""
        if self.state != "PLAYING":
            return
        
        # Update Pac-Man
        self.pacman.update(self.map)
        
        # Check for pellet collection
        pellet_type = self.map.check_pellet_collision(self.pacman.rect.center)
        if pellet_type == 1:  # Regular pellet
            self.score += 10
            self.collected_pellets += 1
            if self.has_sounds:
                self.chomp_sound.play()
        elif pellet_type == 2:  # Power pellet
            self.score += 50
            self.collected_pellets += 1
            self.power_mode = True
            self.power_timer = FPS * 10  # 10 seconds of power mode
            
            # Make all ghosts frightened
            for ghost in self.ghosts:
                ghost.frightened = True
            
            if self.has_sounds:
                self.power_pellet_sound.play()
        
        # Update power mode timer
        if self.power_mode:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_mode = False
                for ghost in self.ghosts:
                    ghost.frightened = False
        
        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.map, self.pacman, self.power_mode)
            
            # Check for ghost collision
            if self.pacman.rect.colliderect(ghost.rect):
                if self.power_mode and ghost.frightened:
                    # Eat the ghost
                    ghost.reset(self.map.ghost_start_pos[0])
                    ghost.frightened = False
                    self.score += 200
                    if self.has_sounds:
                        self.eat_ghost_sound.play()
                else:
                    # Lose a life
                    self.lives -= 1
                    if self.has_sounds:
                        self.death_sound.play()
                    
                    if self.lives <= 0:
                        self.state = "GAME_OVER"
                    else:
                        # Reset positions
                        self.pacman.reset(self.map.pacman_start_pos)
                        for i, ghost in enumerate(self.ghosts):
                            pos = self.map.ghost_start_pos[min(i, len(self.map.ghost_start_pos)-1)]
                            ghost.reset(pos)
        
        # Check win condition
        if self.collected_pellets >= self.total_pellets:
            self.state = "WIN"
    
    def draw(self):
        """Draw the game elements"""
        screen.fill(BLACK)
        
        if self.state == "MENU":
            self.ui.draw_menu()
        elif self.state == "PLAYING" or self.state == "PAUSED":
            # Draw map
            self.map.draw(screen)
            
            # Draw Pac-Man
            self.pacman.draw(screen)
            
            # Draw ghosts
            for ghost in self.ghosts:
                ghost.draw(screen)
            
            # Draw UI elements
            self.ui.draw_game_ui(self.score, self.lives, self.level)
            
            if self.state == "PAUSED":
                self.ui.draw_pause_screen()
        elif self.state == "GAME_OVER":
            self.ui.draw_game_over(self.score)
        elif self.state == "WIN":
            self.ui.draw_win_screen(self.score)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
