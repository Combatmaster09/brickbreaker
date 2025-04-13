import pygame
import pygame.mixer
import globals
from pygame.math import Vector2
from Models.AccelerationPaddle import acceleration_paddle
from Models.Ball import Ball
from Models.VelocityPaddle import velocity_paddle
from Models.Brick import Brick
from UI.ScoreManager import ScoreManager
from LevelManager import LevelManager

class brickbreaker:
    _instance = None
    @staticmethod
    def get_instance():
        return brickbreaker._instance
    #This class manages overall game state and acts as the main loop for the game
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Brick Breaker")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.restart_game = False
        
        # Set this instance as the singleton instance
        brickbreaker._instance = self
        
        # Initialize game objects right away
        self.game_objects = []
        self._initialize_game_objects()
        
        # Initialize level manager after game objects
        from LevelManager import LevelManager
        self.level_manager = LevelManager(self)
        
        # Initialize score manager
        from UI.ScoreManager import ScoreManager
        self.score_manager = ScoreManager()


        
    def _init_pygame(self):
        """This function initializes the pygame library and sets the game window caption"""
        pygame.init()
        pygame.display.set_caption("Brick Breaker")
     
    def main_loop(self):
        """This function is the main game loop that handles user input, 
        game logic processing, and rendering"""
        while globals.game:
            self.clock.tick(60)
            self._handle_input()
            
            # If game flag is turned off, exit the loop immediately
            if not globals.game:
                break
                
            self._process_game_logic()
            self._draw()
            
            if self.restart_game:
                self.reset_game()
                self.restart_game = False
                
                
    def _init_pygame(self):
        """This function initializes the pygame library and sets the game window caption"""
        pygame.init()
        pygame.display.set_caption("Brick Breaker")
        
    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.game = False
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Launch the ball when space is pressed
                    if hasattr(self, 'ball') and self.ball.attached_to_paddle:
                        self.ball.launch()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            globals.game = False
            pygame.quit()
            return
            
        # Handle paddle movement with A and D keys
        if globals.game and hasattr(self, 'paddle'):
            direction = "none"
            if keys[pygame.K_a]:  # A key for left
                direction = "left"
            elif keys[pygame.K_d]:  # D key for right
                direction = "right"
            
            self.paddle.direction = direction
                
        
    def _process_game_logic(self):
        self.score_manager.update()
        if self.level_manager.check_level_complete():
            # Apply bonuses for completing a level
            globals.score += 100 * globals.level
        for game_object in self._get_game_objects():
            # Check what parameters the move method accepts
            if hasattr(game_object, 'direction') and hasattr(game_object, 'move'):
                # For paddles that accept direction and surface
                game_object.move(direction=game_object.direction, surface=self.screen)
            elif hasattr(game_object, 'move'):
                # For other objects with move method
                try:
                    # First try with surface
                    game_object.move(self.screen)
                except TypeError:
                    # If that fails, try without parameters
                    game_object.move()

        
    def _draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        self.score_manager.draw(self.screen)
        
        pygame.display.flip()
    
    def _get_game_objects(self):
        """Returns a list of all game objects that need to be updated each frame"""
        # Initialize game objects if they don't exist yet
        if not hasattr(self, 'initialized_objects'):
            self._initialize_game_objects()
        
        # Return only active game objects (filtering out destroyed bricks)
        return [obj for obj in self.game_objects if not (isinstance(obj, Brick) and obj.destroyed)]

    def _initialize_game_objects(self):
        """Initialize all game objects - separating initialization logic for better OOP"""
        self.game_objects = []
        # Create paddle
        self._create_paddle()
        # Create ball
        self._create_ball()
        # Create bricks
        self._create_bricks()
        # Mark objects as initialized
        self.initialized_objects = True

    def _create_paddle(self):
        """Create the appropriate paddle based on game settings"""
        paddle_position = Vector2(self.screen.get_width() / 2, self.screen.get_height() - 50)
        
        # Create the appropriate paddle type
        if globals.paddle_type == "AccelerationPaddle":
            self.paddle = acceleration_paddle(paddle_position, self._create_ball_callback)
        else:
            self.paddle = velocity_paddle(paddle_position, self._create_ball_callback)
            
        self.game_objects.append(self.paddle)

    def _create_ball(self):
        """Create the ball object"""
        ball_position = Vector2(self.screen.get_width() / 2, self.screen.get_height() - 100)
        self.ball = Ball(ball_position, self._create_ball_callback, self.paddle)
        self.ball.velocity = Vector2(3, -3)  # Set initial velocity
        self.game_objects.append(self.ball)

    def _create_bricks(self):
        """Create the brick formation using the level manager"""
        # Use the level manager to create bricks for level 1
        if hasattr(self, 'level_manager'):
            self.level_manager.load_level(1)
        else:
            print("Level manager not initialized")

    def _create_ball_callback(self):
        """Callback function for creating new balls"""
        # This method would be called when a new ball needs to be created
        new_ball_position = Vector2(self.screen.get_width() / 2, self.screen.get_height() - 100)
        new_ball = Ball(new_ball_position, self._create_ball_callback, self.paddle)
        new_ball.velocity = Vector2(3, -3)
        self.game_objects.append(new_ball)
        return new_ball
    
    def reset_game(self):
        # Clear existing game objects
        if hasattr(self, 'game_objects'):
            delattr(self, 'game_objects')
        # Next time _get_game_objects is called, it will reinitialize everything
    
    def handle_ball_lost(self):
        game_over = self.score_manager.reduce_life()
        if game_over:
            self.restart_game = True
        else:
            # Create a new ball attached to the paddle
            self._create_ball()