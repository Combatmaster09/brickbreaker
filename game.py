import pygame
import pygame.mixer
import globals
from pygame.math import Vector2
from Models.AccelerationPaddle import acceleration_paddle
from Models.Ball import Ball
from Models.VelocityPaddle import velocity_paddle
from Models.Brick import Brick
from UI.ScoreManager import ScoreManager
from UI.Menu import Menu  # Import the Menu class
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
        self.game_running = False  # Track if actual gameplay is running
        
        # Set this instance as the singleton instance
        brickbreaker._instance = self
        
        # Initialize game objects list (but don't create objects yet)
        self.game_objects = []
        
        # Initialize score manager
        from UI.ScoreManager import ScoreManager
        self.score_manager = ScoreManager()
        
        # Initialize menu system
        self.menu = Menu(self)
        
        # Initialize level manager
        from LevelManager import LevelManager
        self.level_manager = LevelManager(self)
        
        # Initialize game objects (but don't show them until game starts)
        self._initialize_game_objects()
        
    def _init_pygame(self):
        """This function initializes the pygame library and sets the game window caption"""
        pygame.init()
        pygame.display.set_caption("Brick Breaker")
     
    def main_loop(self):
        """This function is the main game loop that handles user input, 
        game logic processing, and rendering"""
        
        # Start with the main menu
        self.game_running = False
        self.menu.active = True
        self.menu.show_main_menu = True
        self.menu.show_game_over = False
        
        start_game = self.menu.run_menu_loop()
        
        if start_game:
            self.game_running = True
        
        while globals.game:
            self.clock.tick(60)
            
            if not self.game_running:
                # Show appropriate menu
                if self.restart_game:
                    self.menu.active = True
                    self.menu.show_main_menu = False
                    self.menu.show_game_over = True
                    
                    # Reset restart flag
                    self.restart_game = False
                    
                    # Run menu loop
                    if self.menu.run_menu_loop():
                        self.reset_game()
                        self.game_running = True
                    
                continue  # Skip to next frame if not in gameplay mode
            
            self._handle_input()
            
            # If game flag is turned off, exit the loop immediately
            if not globals.game:
                break
                
            self._process_game_logic()
            self._draw()
            
            if self.restart_game:
                self.game_running = False
                
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
            
            # Handle powerup effect timers
            elif event.type >= pygame.USEREVENT + 1 and event.type <= pygame.USEREVENT + 4:
                # Reset effects
                if event.type == pygame.USEREVENT + 1:  # Expand paddle timeout
                    self._reset_paddle_size()
                elif event.type == pygame.USEREVENT + 2:  # Shrink paddle timeout
                    self._reset_paddle_size()
                elif event.type == pygame.USEREVENT + 3:  # Slow ball timeout
                    self._reset_ball_speed()
                elif event.type == pygame.USEREVENT + 4:  # Fast ball timeout
                    self._reset_ball_speed()
        
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
        
        # Process game objects
        for game_object in self._get_game_objects():
            # Move objects appropriately
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
        
        # Check for powerup collection
        from Models.Powerup import Powerup
        powerups_to_remove = []
        
        for game_object in self._get_game_objects():
            if isinstance(game_object, Powerup) and game_object.active:
                # Check if powerup collides with paddle
                if hasattr(self, 'paddle') and game_object.collides_with(self.paddle):
                    # Apply powerup effect
                    game_object.apply_effect(self)
                    powerups_to_remove.append(game_object)
                    # Play collection sound if available
                    try:
                        powerup_sound = load_sound("powerup_collect")
                        powerup_sound.play()
                    except:
                        pass
                
                # Remove powerups that fall off screen
                elif not game_object.active:
                    powerups_to_remove.append(game_object)
        
        # Remove collected/fallen powerups
        for powerup in powerups_to_remove:
            if powerup in self.game_objects:
                self.game_objects.remove(powerup)

    def handle_ball_lost(self):
        """Handle when a ball falls off the bottom of the screen"""
        # Reduce lives if score manager exists
        game_over = False
        if hasattr(self, 'score_manager'):
            game_over = self.score_manager.reduce_life()
        
        if game_over:
            # Game over - trigger the game over menu
            self.restart_game = True
        else:
            # Find the ball that needs to be reset (should be only one that's active)
            ball_to_reset = None
            for obj in self.game_objects:
                if isinstance(obj, Ball) and not obj.attached_to_paddle:
                    ball_to_reset = obj
                    break
                    
            # If we found an active ball, reset it to the paddle
            if ball_to_reset and hasattr(ball_to_reset, 'paddle') and ball_to_reset.paddle:
                ball_to_reset.attached_to_paddle = True
                ball_to_reset.velocity = Vector2(0, 0)
                ball_to_reset.position.x = ball_to_reset.paddle.position.x
                ball_to_reset.position.y = ball_to_reset.paddle.position.y - ball_to_reset.paddle.radius - ball_to_reset.radius
            
    def _draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        self.score_manager.draw(self.screen)
        
        pygame.display.flip()
    
    def _get_game_objects(self):
        """Returns a list of all game objects that need to be updated each frame"""
        # Make sure game_objects exists
        if not hasattr(self, 'game_objects') or self.game_objects is None:
            self.game_objects = []
            self._initialize_game_objects()
        
        # Return only active game objects (filtering out destroyed bricks)
        return [obj for obj in self.game_objects if not (isinstance(obj, Brick) and hasattr(obj, 'destroyed') and obj.destroyed)]

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
        if hasattr(self, 'level_manager'):
            # Use custom level designs instead of procedural generation
            self.level_manager.load_custom_level(1)
        else:
            print("Level manager not initialized")

    def _create_ball_callback(self):
        """Callback function for creating new balls"""
        # Check if we already have an active ball
        existing_balls = [obj for obj in self.game_objects if isinstance(obj, Ball)]
        if existing_balls:
            # We already have at least one ball, no need to create another
            return existing_balls[0]
            
        # Only create a new ball if none exist
        new_ball_position = Vector2(self.screen.get_width() / 2, self.screen.get_height() - 100)
        new_ball = Ball(new_ball_position, self._create_ball_callback, self.paddle)
        new_ball.velocity = Vector2(3, -3)
        self.game_objects.append(new_ball)
        return new_ball
    
    def reset_game(self):
        # Clear existing game objects
        if hasattr(self, 'game_objects'):
            # Remove all balls from game objects
            self.game_objects = [obj for obj in self.game_objects if not isinstance(obj, Ball)]
            
        # Reset score and lives
        if hasattr(self, 'score_manager'):
            self.score_manager.reset_score()
            self.score_manager.lives = 3
        
        # Reset level to 1
        globals.level = 1
        if hasattr(self, 'level_manager'):
            self.level_manager.current_level = 1
            self.level_manager.load_custom_level(1)
            
        # Re-initialize the game objects
        self._initialize_game_objects()
    
    def _reset_paddle_size(self):
        """Reset paddle to its original size"""
        if hasattr(self, 'paddle') and hasattr(self.paddle, 'sprite'):
            # Reset the paddle sprite to its original size
            paddle_position = self.paddle.position
            paddle_class = self.paddle.__class__
            
            # Create a new paddle of the same type with the default size
            if globals.paddle_type == "AccelerationPaddle":
                self.paddle = acceleration_paddle(paddle_position, self._create_ball_callback)
            else:
                self.paddle = velocity_paddle(paddle_position, self._create_ball_callback)
            
            # Update the paddle's radius to match the new sprite
            self.paddle.radius = self.paddle.sprite.get_width() / 2
            
            # Replace the old paddle in the game objects list
            for i, obj in enumerate(self.game_objects):
                if isinstance(obj, paddle_class):
                    self.game_objects[i] = self.paddle
                    break

    def _reset_ball_speed(self):
        """Reset all balls to normal speed"""
        from Models.Ball import Ball
        
        # Get the default ball speed from a new ball instance
        temp_ball = Ball(Vector2(0, 0), None, None)
        default_velocity = temp_ball.VELOCITY
        
        # Reset all existing balls to default speed
        for obj in self.game_objects:
            if isinstance(obj, Ball):
                obj.VELOCITY = default_velocity
                # Maintain direction but adjust speed
                if obj.velocity.length() > 0:
                    obj.velocity = obj.velocity.normalize() * default_velocity
        """Reset ball speed to normal"""
        # Get default ball speed for current level
        if hasattr(self, 'level_manager') and hasattr(self.level_manager, 'levels_data'):
            level_idx = min(self.level_manager.current_level - 1, len(self.level_manager.levels_data) - 1)
            default_speed = self.level_manager.levels_data[level_idx]["ball_speed"]
        else:
            default_speed = 5  # Default speed
        
        # Reset all balls to default speed
        for obj in self.game_objects:
            if hasattr(obj, 'VELOCITY') and hasattr(obj, 'velocity'):
                obj.VELOCITY = default_speed
                # Preserve direction but adjust speed
                if obj.velocity.length() > 0:
                    obj.velocity = obj.velocity.normalize() * obj.VELOCITY

    def _create_multiball(self):
        """Create a new ball specifically for multiball powerups"""
        from Models.Ball import Ball
        
        # Create a new ball at the paddle's position
        if hasattr(self, 'paddle'):
            ball_position = Vector2(self.paddle.position.x, self.paddle.position.y - self.paddle.radius - 5)
            new_ball = Ball(ball_position, self._create_ball_callback, self.paddle)
            
            # Give it a random direction but ensure it's going upward
            angle = random.uniform(-0.5, 0.5)  # Between -30 and 30 degrees
            new_ball.velocity = Vector2(angle, -1).normalize() * new_ball.VELOCITY
            new_ball.attached_to_paddle = False  # Not attached so it moves immediately
            
            self.game_objects.append(new_ball)
            return new_ball
        return None