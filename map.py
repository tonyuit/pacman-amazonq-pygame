import pygame
import random

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

class Map:
    def __init__(self, cell_size):
        """Initialize the game map with walls, pellets, and starting positions"""
        self.cell_size = cell_size
        self.width = 20  # Map width in cells
        self.height = 15  # Map height in cells
        
        # Create the map layout
        # 0 = empty path, 1 = wall, 2 = pellet, 3 = power pellet, 4 = pacman start, 5 = ghost start
        self.layout = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 3, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 3, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1],
            [1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 0, 0, 0, 5, 5, 0, 0, 0, 1, 2, 1, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 5, 5, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [0, 0, 0, 1, 2, 1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0],
            [1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        
        # Find starting positions
        self.pacman_start_pos = self.find_position(4)
        self.ghost_start_pos = self.find_all_positions(5)
        
        # Create wall rects for collision detection
        self.walls = []
        self.pellets = []
        self.power_pellets = []
        
        for y in range(self.height):
            for x in range(self.width):
                cell_value = self.layout[y][x]
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                
                if cell_value == 1:  # Wall
                    self.walls.append(rect)
                elif cell_value == 2:  # Pellet
                    self.pellets.append(rect)
                elif cell_value == 3:  # Power Pellet
                    self.power_pellets.append(rect)
        
        # Try to load wall texture, otherwise use a simple blue rectangle
        try:
            self.wall_texture = pygame.image.load('assets/images/wall.png')
            self.wall_texture = pygame.transform.scale(self.wall_texture, (cell_size, cell_size))
            self.has_wall_texture = True
        except:
            self.has_wall_texture = False
    
    def find_position(self, value):
        """Find the first position of a specific value in the layout"""
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == value:
                    return (x * self.cell_size + self.cell_size // 2, 
                            y * self.cell_size + self.cell_size // 2)
        return (0, 0)  # Default if not found
    
    def find_all_positions(self, value):
        """Find all positions of a specific value in the layout"""
        positions = []
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] == value:
                    positions.append((x * self.cell_size + self.cell_size // 2, 
                                     y * self.cell_size + self.cell_size // 2))
        return positions
    
    def count_pellets(self):
        """Count the total number of pellets and power pellets"""
        return len(self.pellets) + len(self.power_pellets)
    
    def check_pellet_collision(self, position):
        """Check if Pac-Man collides with a pellet or power pellet"""
        x, y = position
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)
        
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            cell_value = self.layout[grid_y][grid_x]
            
            if cell_value == 2:  # Regular pellet
                self.layout[grid_y][grid_x] = 0
                # Remove the pellet from the list
                pellet_rect = pygame.Rect(grid_x * self.cell_size, grid_y * self.cell_size, 
                                         self.cell_size, self.cell_size)
                if pellet_rect in self.pellets:
                    self.pellets.remove(pellet_rect)
                return 1
            elif cell_value == 3:  # Power pellet
                self.layout[grid_y][grid_x] = 0
                # Remove the power pellet from the list
                power_pellet_rect = pygame.Rect(grid_x * self.cell_size, grid_y * self.cell_size, 
                                              self.cell_size, self.cell_size)
                if power_pellet_rect in self.power_pellets:
                    self.power_pellets.remove(power_pellet_rect)
                return 2
        
        return 0  # No pellet collision
    
    def is_wall(self, position):
        """Check if a position contains a wall"""
        x, y = position
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)
        
        if 0 <= grid_x < self.width and 0 <= grid_y < self.height:
            return self.layout[grid_y][grid_x] == 1
        
        return True  # Treat out of bounds as walls
    
    def get_valid_directions(self, position):
        """Get valid movement directions from a position"""
        x, y = position
        grid_x = int(x // self.cell_size)
        grid_y = int(y // self.cell_size)
        
        valid_directions = []
        directions = [("UP", (0, -1)), ("DOWN", (0, 1)), ("LEFT", (-1, 0)), ("RIGHT", (1, 0))]
        
        for direction, (dx, dy) in directions:
            new_x, new_y = grid_x + dx, grid_y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if self.layout[new_y][new_x] != 1:  # Not a wall
                    valid_directions.append(direction)
        
        return valid_directions
    
    def draw(self, surface):
        """Draw the map with walls and pellets"""
        # Draw walls
        for wall in self.walls:
            if self.has_wall_texture:
                surface.blit(self.wall_texture, wall)
            else:
                pygame.draw.rect(surface, BLUE, wall)
        
        # Draw pellets
        for pellet in self.pellets:
            pellet_rect = pygame.Rect(
                pellet.x + self.cell_size // 3,
                pellet.y + self.cell_size // 3,
                self.cell_size // 3,
                self.cell_size // 3
            )
            pygame.draw.ellipse(surface, WHITE, pellet_rect)
        
        # Draw power pellets (larger and pulsating)
        for power_pellet in self.power_pellets:
            # Create a pulsating effect
            size_mod = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0 * 0.2 + 0.6
            power_size = int(self.cell_size * size_mod)
            power_rect = pygame.Rect(
                power_pellet.x + (self.cell_size - power_size) // 2,
                power_pellet.y + (self.cell_size - power_size) // 2,
                power_size,
                power_size
            )
            pygame.draw.ellipse(surface, YELLOW, power_rect)
