import globals
from Models.Brick import Brick
from pygame.math import Vector2
from utils import load_sprite
import random
from LevelDesigns import LEVEL_DESIGNS

class LevelManager:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.current_level = 1
        self.levels_data = self._generate_levels_data(10)  # Pre-generate 10 levels

    def load_custom_level(self, level_number):
        """Load a custom-designed level"""
        if level_number <= len(LEVEL_DESIGNS):
            level_design = LEVEL_DESIGNS[level_number - 1]
        else:
            # If requesting a level beyond the designed ones,
            # use the last level or generate a procedural one
            if LEVEL_DESIGNS:
                level_design = LEVEL_DESIGNS[-1]
            else:
                # Fallback to procedural generation
                return self.load_level(level_number)
        
        # Update global level
        globals.level = level_number
        self.current_level = level_number
        
        # Clear existing bricks
        self.game_instance.game_objects = [obj for obj in self.game_instance.game_objects 
                                        if not isinstance(obj, Brick)]
        
        # Create bricks based on the level design
        bricks = self._create_from_design(level_design)
        
        # Add bricks to game objects
        for brick in bricks:
            self.game_instance.game_objects.append(brick)
        
        return True

    def _create_from_design(self, level_design):
        """Create brick formation from a level design"""
        bricks = []
        
        # Set up brick dimensions explicitly
        brick_width, brick_height = globals.BRICK_SIZE
        
        # Add padding between bricks
        horizontal_padding = 5
        vertical_padding = 5
        
        # Calculate total width needed for bricks
        num_cols = max(len(row) for row in level_design)
        total_width = num_cols * (brick_width + horizontal_padding) - horizontal_padding
        
        # Calculate starting position to center the brick formation
        screen_width = self.game_instance.screen.get_width()
        start_x = (screen_width - total_width) // 2
        start_y = 80  # Start further from the top for better visibility
        
        # Create the bricks based on the design
        for row_idx, row in enumerate(level_design):
            for col_idx, char in enumerate(row):
                if char == ' ':
                    continue  # No brick here
                    
                # Calculate exact position for each brick
                x = start_x + col_idx * (brick_width + horizontal_padding) + brick_width / 2
                y = start_y + row_idx * (brick_height + vertical_padding) + brick_height / 2
                
                # Determine brick health and powerup based on character
                powerup_type = None
                powerup_chance = 0.2  # Default chance
                
                if char in '23456789':
                    health = int(char)
                elif char == '#':
                    health = 1
                elif char == 'E':  # Expand paddle powerup
                    health = 1
                    powerup_type = "expand"
                    powerup_chance = 1.0  # 100% chance
                elif char == 'S':  # Shrink paddle powerup
                    health = 1
                    powerup_type = "shrink"
                    powerup_chance = 1.0
                elif char == 'M':  # Multiball powerup
                    health = 1
                    powerup_type = "multiball"
                    powerup_chance = 1.0
                elif char == 'L':  # Slow ball powerup
                    health = 1
                    powerup_type = "slowball"
                    powerup_chance = 1.0
                elif char == 'F':  # Fast ball powerup
                    health = 1
                    powerup_type = "fastball"
                    powerup_chance = 1.0
                elif char == '+':  # Extra life powerup
                    health = 1
                    powerup_type = "extralife"
                    powerup_chance = 1.0
                else:
                    continue  # Unknown character
                
                # Create the brick with precise positioning and powerup information
                brick = Brick(Vector2(x, y), load_sprite("brick"), health, powerup_chance, powerup_type)
                
                # Adjust the sprite size to match the desired brick size
                if brick.sprite.get_width() != brick_width or brick.sprite.get_height() != brick_height:
                    import pygame
                    brick.sprite = pygame.transform.scale(brick.sprite, (brick_width, brick_height))
                    # Update radius for collision detection
                    brick.radius = max(brick_width, brick_height) / 2
                
                bricks.append(brick)
        
        return bricks
    
    def _generate_levels_data(self, num_levels):
        """Generate data for multiple levels with increasing difficulty"""
        levels = []
        
        for level in range(1, num_levels + 1):
            level_data = {
                "rows": min(3 + level // 2, 10),  # Increase rows as level increases (max 10)
                "cols": min(5 + level // 3, 15),  # Increase columns as level increases (max 15)
                "brick_health": 1 + level // 3,  # Increase brick health every 3 levels
                "ball_speed": 5 + level * 0.5,  # Gradually increase ball speed
                "special_bricks": level // 2,  # Add special bricks in higher levels
            }
            levels.append(level_data)
        
        return levels
    
    def load_level(self, level_number):
        """Load a specific level"""
        if level_number > len(self.levels_data):
            # If we've gone beyond pre-generated levels, create a harder one
            level_data = self._generate_level_data(level_number)
        else:
            level_data = self.levels_data[level_number - 1]
        
        # Update global level
        globals.level = level_number
        self.current_level = level_number
        
        # Clear existing bricks
        self.game_instance.game_objects = [obj for obj in self.game_instance.game_objects if not isinstance(obj, Brick)]
        
        # Create new bricks based on level data
        bricks = self._create_level_bricks(level_data)
        
        # Add bricks to game objects
        for brick in bricks:
            self.game_instance.game_objects.append(brick)
        
        # Update ball speed
        for ball in [obj for obj in self.game_instance.game_objects if hasattr(obj, "VELOCITY")]:
            ball.VELOCITY = level_data["ball_speed"]
            
        return True
    
    def _create_level_bricks(self, level_data):
        """Create brick formation based on level data"""
        bricks = []
        rows = level_data["rows"]
        cols = level_data["cols"]
        
        # Calculate available space
        screen_width = self.game_instance.screen.get_width()
        
        # Set up brick dimensions
        if isinstance(globals.BRICK_SIZE, tuple):
            brick_width, brick_height = globals.BRICK_SIZE
        else:
            brick_width, brick_height = 50, 20
        
        # Add padding between bricks
        padding = 5
        
        # Calculate total width needed for bricks
        total_width = cols * (brick_width + padding) - padding
        
        # Calculate starting x position to center the brick formation
        start_x = (screen_width - total_width) // 2
        start_y = 50  # Start from the top with some margin
        
        # Create the grid of bricks
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (brick_width + padding)
                y = start_y + row * (brick_height + padding)
                
                # Determine brick health
                if random.random() < 0.2:  # 20% chance for a stronger brick
                    health = level_data["brick_health"] + 1
                else:
                    health = level_data["brick_health"]
                
                # Create the brick
                brick = Brick(Vector2(x, y), load_sprite("brick"), health)
                bricks.append(brick)
                
        return bricks
        
    def check_level_complete(self):
        """Check if the current level is complete (all bricks destroyed)"""
        # Get all active bricks from game instance
        bricks = [obj for obj in self.game_instance.game_objects 
                if isinstance(obj, Brick) and not obj.destroyed]
        
        # If no bricks left, level is complete
        if not bricks:
            # Move to next level
            next_level = self.current_level + 1
            success = self.load_custom_level(next_level)
            
            if success:
                # Update global level
                globals.level = next_level
                self.current_level = next_level
                
                # Reset ball position
                for obj in self.game_instance.game_objects:
                    if hasattr(obj, 'attached_to_paddle'):
                        obj.attached_to_paddle = True
                        obj.velocity = Vector2(0, 0)
                        # Position ball above paddle
                        if hasattr(obj, 'paddle') and obj.paddle:
                            obj.position.x = obj.paddle.position.x
                            obj.position.y = obj.paddle.position.y - obj.paddle.radius - obj.radius
                
                return True
        
        return False