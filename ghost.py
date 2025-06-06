import pygame
import random
import math

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Ghost:
    def __init__(self, start_pos, cell_size, color, personality):
        """Initialize a ghost with starting position and behavior type"""
        self.cell_size = cell_size
        self.radius = int(cell_size * 0.4)
        self.x, self.y = start_pos
        self.color = color
        self.personality = personality  # chase, ambush, random, patrol
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.speed = 1.5
        self.frightened = False
        self.frightened_timer = 0
        self.animation_frame = 0
        self.animation_speed = 0.2
        
        # Create rect for collision detection
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
        
        # Try to load ghost sprites
        try:
            self.sprite = pygame.image.load('assets/images/ghost.png')
            self.sprite = pygame.transform.scale(self.sprite, (self.radius * 2, self.radius * 2))
            self.frightened_sprite = pygame.image.load('assets/images/frightened_ghost.png')
            self.frightened_sprite = pygame.transform.scale(
                self.frightened_sprite, (self.radius * 2, self.radius * 2)
            )
            self.has_sprites = True
        except:
            self.has_sprites = False
    
    def update(self, game_map, pacman, power_mode):
        """Update ghost position and behavior"""
        # Update frightened state
        if power_mode and not self.frightened:
            self.frightened = True
            # Reverse direction when becoming frightened
            self.reverse_direction()
        elif not power_mode:
            self.frightened = False
        
        # Decide movement direction
        if self.frightened:
            self.move_frightened(game_map)
        else:
            self.move_normal(game_map, pacman)
        
        # Update animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2:
            self.animation_frame = 0
    
    def move_normal(self, game_map, pacman):
        """Move ghost based on its personality and Pac-Man's position"""
        # Get current grid position
        grid_x = self.x // self.cell_size
        grid_y = self.y // self.cell_size
        
        # Check if we're at a grid intersection (center of a cell)
        at_intersection = (
            abs(self.x - (grid_x * self.cell_size + self.cell_size // 2)) < self.speed and
            abs(self.y - (grid_y * self.cell_size + self.cell_size // 2)) < self.speed
        )
        
        if at_intersection:
            # Snap to grid center
            self.x = grid_x * self.cell_size + self.cell_size // 2
            self.y = grid_y * self.cell_size + self.cell_size // 2
            
            # Get valid directions (excluding the opposite of current direction)
            valid_directions = game_map.get_valid_directions((self.x, self.y))
            opposite_direction = self.get_opposite_direction(self.direction)
            if opposite_direction in valid_directions and len(valid_directions) > 1:
                valid_directions.remove(opposite_direction)
            
            if valid_directions:
                if self.personality == "chase":
                    # Chase Pac-Man directly
                    self.direction = self.get_direction_towards_target(
                        (self.x, self.y), (pacman.x, pacman.y), valid_directions
                    )
                elif self.personality == "ambush":
                    # Try to predict where Pac-Man is going
                    target_x = pacman.x + pacman.get_direction_vector(pacman.direction)[0] * 4 * self.cell_size
                    target_y = pacman.y + pacman.get_direction_vector(pacman.direction)[1] * 4 * self.cell_size
                    self.direction = self.get_direction_towards_target(
                        (self.x, self.y), (target_x, target_y), valid_directions
                    )
                elif self.personality == "random":
                    # Move randomly
                    self.direction = random.choice(valid_directions)
                elif self.personality == "patrol":
                    # Patrol between corners
                    corners = [
                        (self.cell_size * 1.5, self.cell_size * 1.5),
                        (self.cell_size * (game_map.width - 1.5), self.cell_size * 1.5),
                        (self.cell_size * 1.5, self.cell_size * (game_map.height - 1.5)),
                        (self.cell_size * (game_map.width - 1.5), self.cell_size * (game_map.height - 1.5))
                    ]
                    
                    # Find the nearest corner that's not too close
                    target = None
                    min_dist = float('inf')
                    for corner in corners:
                        dist = math.sqrt((self.x - corner[0])**2 + (self.y - corner[1])**2)
                        if dist < min_dist and dist > self.cell_size * 3:
                            min_dist = dist
                            target = corner
                    
                    # If no good corner found, chase Pac-Man
                    if target is None:
                        target = (pacman.x, pacman.y)
                    
                    self.direction = self.get_direction_towards_target(
                        (self.x, self.y), target, valid_directions
                    )
        
        # Move in the current direction
        dx, dy = self.get_direction_vector(self.direction)
        self.x += dx * self.speed
        self.y += dy * self.speed
        
        # Update rect position
        self.rect.center = (self.x, self.y)
    
    def move_frightened(self, game_map):
        """Move ghost in frightened mode (random movement)"""
        # Get current grid position
        grid_x = self.x // self.cell_size
        grid_y = self.y // self.cell_size
        
        # Check if we're at a grid intersection
        at_intersection = (
            abs(self.x - (grid_x * self.cell_size + self.cell_size // 2)) < self.speed and
            abs(self.y - (grid_y * self.cell_size + self.cell_size // 2)) < self.speed
        )
        
        if at_intersection:
            # Snap to grid center
            self.x = grid_x * self.cell_size + self.cell_size // 2
            self.y = grid_y * self.cell_size + self.cell_size // 2
            
            # Get valid directions (excluding the opposite of current direction)
            valid_directions = game_map.get_valid_directions((self.x, self.y))
            opposite_direction = self.get_opposite_direction(self.direction)
            if opposite_direction in valid_directions and len(valid_directions) > 1:
                valid_directions.remove(opposite_direction)
            
            if valid_directions:
                self.direction = random.choice(valid_directions)
        
        # Move in the current direction at reduced speed
        dx, dy = self.get_direction_vector(self.direction)
        self.x += dx * (self.speed * 0.5)  # Slower when frightened
        self.y += dy * (self.speed * 0.5)
        
        # Update rect position
        self.rect.center = (self.x, self.y)
    
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
    
    def get_opposite_direction(self, direction):
        """Get the opposite of a direction"""
        if direction == "UP":
            return "DOWN"
        elif direction == "DOWN":
            return "UP"
        elif direction == "LEFT":
            return "RIGHT"
        elif direction == "RIGHT":
            return "LEFT"
        return direction
    
    def reverse_direction(self):
        """Reverse the current direction"""
        self.direction = self.get_opposite_direction(self.direction)
    
    def get_direction_towards_target(self, current_pos, target_pos, valid_directions):
        """Get the best direction to move towards a target"""
        best_direction = None
        min_distance = float('inf')
        
        for direction in valid_directions:
            # Calculate new position if we move in this direction
            dx, dy = self.get_direction_vector(direction)
            new_x = current_pos[0] + dx * self.cell_size
            new_y = current_pos[1] + dy * self.cell_size
            
            # Calculate distance to target from this new position
            distance = math.sqrt((new_x - target_pos[0])**2 + (new_y - target_pos[1])**2)
            
            if distance < min_distance:
                min_distance = distance
                best_direction = direction
        
        return best_direction if best_direction else random.choice(valid_directions)
    
    def reset(self, start_pos):
        """Reset ghost to starting position"""
        self.x, self.y = start_pos
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.frightened = False
        self.rect.center = (self.x, self.y)
    
    def draw(self, surface):
        """Draw the ghost on the screen"""
        if self.has_sprites:
            # Draw sprite based on state
            sprite = self.frightened_sprite if self.frightened else self.sprite
            sprite_rect = sprite.get_rect(center=(self.x, self.y))
            
            # Tint the sprite with the ghost's color if not frightened
            if not self.frightened:
                tinted_sprite = sprite.copy()
                tinted_sprite.fill(self.color, special_flags=pygame.BLEND_MULT)
                surface.blit(tinted_sprite, sprite_rect)
            else:
                # Blinking effect when frightened mode is about to end
                if self.frightened_timer < 3 * 60 and self.frightened_timer % 30 > 15:
                    surface.blit(sprite, sprite_rect)
                else:
                    surface.blit(sprite, sprite_rect)
        else:
            # Draw ghost as a simple shape
            ghost_color = BLUE if self.frightened else self.color
            
            # Draw ghost body (circle with rectangular bottom)
            pygame.draw.circle(
                surface,
                ghost_color,
                (self.x, self.y - self.radius // 3),
                self.radius
            )
            
            pygame.draw.rect(
                surface,
                ghost_color,
                pygame.Rect(
                    self.x - self.radius,
                    self.y - self.radius // 3,
                    self.radius * 2,
                    self.radius
                )
            )
            
            # Draw "skirt" at bottom
            wave_height = self.radius // 3
            for i in range(3):
                pygame.draw.rect(
                    surface,
                    ghost_color,
                    pygame.Rect(
                        self.x - self.radius + i * (self.radius * 2) // 3,
                        self.y + self.radius * 2 // 3 - wave_height,
                        (self.radius * 2) // 3,
                        wave_height
                    )
                )
            
            # Draw eyes
            eye_radius = self.radius // 3
            eye_offset = self.radius // 2
            
            # Eye whites
            pygame.draw.circle(
                surface,
                WHITE,
                (self.x - eye_offset, self.y - self.radius // 3),
                eye_radius
            )
            pygame.draw.circle(
                surface,
                WHITE,
                (self.x + eye_offset, self.y - self.radius // 3),
                eye_radius
            )
            
            # Eye pupils (look in movement direction)
            pupil_offset = eye_radius // 2
            dx, dy = self.get_direction_vector(self.direction)
            
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                (self.x - eye_offset + dx * pupil_offset, self.y - self.radius // 3 + dy * pupil_offset),
                eye_radius // 2
            )
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                (self.x + eye_offset + dx * pupil_offset, self.y - self.radius // 3 + dy * pupil_offset),
                eye_radius // 2
            )
