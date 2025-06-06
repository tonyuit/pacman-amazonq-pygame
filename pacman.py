import pygame
import math

# Colors
YELLOW = (255, 255, 0)

class PacMan:
    def __init__(self, start_pos, cell_size):
        """Initialize Pac-Man with starting position and properties"""
        self.cell_size = cell_size
        self.radius = int(cell_size * 0.4)
        self.x, self.y = start_pos
        self.direction = "RIGHT"  # Initial direction
        self.next_direction = None  # Direction to change to when possible
        self.speed = 2
        self.animation_timer = 0
        self.mouth_angle = 45  # Mouth opening angle in degrees
        self.mouth_direction = 1  # 1 for opening, -1 for closing
        
        # Create rect for collision detection
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        
        # Try to load Pac-Man sprites
        try:
            self.sprites = {
                "RIGHT": pygame.image.load('assets/images/pacman_right.png'),
                "LEFT": pygame.image.load('assets/images/pacman_left.png'),
                "UP": pygame.image.load('assets/images/pacman_up.png'),
                "DOWN": pygame.image.load('assets/images/pacman_down.png')
            }
            for direction, sprite in self.sprites.items():
                self.sprites[direction] = pygame.transform.scale(
                    sprite, (self.radius * 2, self.radius * 2)
                )
            self.has_sprites = True
        except:
            self.has_sprites = False
    
    def change_direction(self, new_direction):
        """Change Pac-Man's direction or queue it for the next valid position"""
        self.next_direction = new_direction
    
    def update(self, game_map):
        """Update Pac-Man's position and animation"""
        # Try to change to the queued direction if possible
        if self.next_direction:
            if self.can_move(self.next_direction, game_map):
                self.direction = self.next_direction
                self.next_direction = None
        
        # Move in the current direction if possible
        if self.can_move(self.direction, game_map):
            dx, dy = self.get_direction_vector(self.direction)
            self.x += dx * self.speed
            self.y += dy * self.speed
            
            # Update rect position
            self.rect.center = (self.x, self.y)
        
        # Update mouth animation
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.animation_timer = 0
            self.mouth_angle += 5 * self.mouth_direction
            
            if self.mouth_angle >= 45:
                self.mouth_direction = -1
            elif self.mouth_angle <= 0:
                self.mouth_direction = 1
    
    def can_move(self, direction, game_map):
        """Check if Pac-Man can move in the specified direction"""
        dx, dy = self.get_direction_vector(direction)
        
        # Calculate the position after movement
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Check if the new position would be inside a wall
        if game_map.is_wall((new_x, new_y)):
            return False
        
        return True
    
    def get_direction_vector(self, direction):
        """Convert direction string to movement vector"""
        if direction == "UP":
            return (0, -1)
        elif direction == "DOWN":
            return (0, 1)
        elif direction == "LEFT":
            return (-1, 0)
        elif direction == "RIGHT":
            return (1, 0)
        return (0, 0)
    
    def reset(self, start_pos):
        """Reset Pac-Man to starting position"""
        self.x, self.y = start_pos
        self.direction = "RIGHT"
        self.next_direction = None
        self.rect.center = (self.x, self.y)
    
    def draw(self, surface):
        """Draw Pac-Man on the screen"""
        if self.has_sprites:
            # Draw sprite based on direction
            sprite = self.sprites[self.direction]
            sprite_rect = sprite.get_rect(center=(self.x, self.y))
            surface.blit(sprite, sprite_rect)
        else:
            # Draw Pac-Man as a circle with a mouth
            # Calculate mouth angles based on direction
            if self.direction == "RIGHT":
                start_angle = self.mouth_angle / 2
                end_angle = 360 - self.mouth_angle / 2
            elif self.direction == "LEFT":
                start_angle = 180 - self.mouth_angle / 2
                end_angle = 180 + self.mouth_angle / 2
            elif self.direction == "UP":
                start_angle = 270 - self.mouth_angle / 2
                end_angle = 270 + self.mouth_angle / 2
            elif self.direction == "DOWN":
                start_angle = 90 - self.mouth_angle / 2
                end_angle = 90 + self.mouth_angle / 2
            
            # Draw Pac-Man body
            pygame.draw.arc(
                surface,
                YELLOW,
                pygame.Rect(
                    self.x - self.radius,
                    self.y - self.radius,
                    self.radius * 2,
                    self.radius * 2
                ),
                math.radians(start_angle),
                math.radians(end_angle),
                self.radius
            )
            
            # Draw the center line to complete the circle
            if self.mouth_angle < 45:  # Only draw the line if mouth is not fully open
                if self.direction == "RIGHT":
                    end_pos = (self.x, self.y - self.radius * math.sin(math.radians(self.mouth_angle / 2)))
                    start_pos = (self.x, self.y + self.radius * math.sin(math.radians(self.mouth_angle / 2)))
                elif self.direction == "LEFT":
                    end_pos = (self.x, self.y - self.radius * math.sin(math.radians(self.mouth_angle / 2)))
                    start_pos = (self.x, self.y + self.radius * math.sin(math.radians(self.mouth_angle / 2)))
                elif self.direction == "UP":
                    end_pos = (self.x - self.radius * math.sin(math.radians(self.mouth_angle / 2)), self.y)
                    start_pos = (self.x + self.radius * math.sin(math.radians(self.mouth_angle / 2)), self.y)
                elif self.direction == "DOWN":
                    end_pos = (self.x - self.radius * math.sin(math.radians(self.mouth_angle / 2)), self.y)
                    start_pos = (self.x + self.radius * math.sin(math.radians(self.mouth_angle / 2)), self.y)
                
                pygame.draw.line(surface, YELLOW, start_pos, end_pos, 2)
