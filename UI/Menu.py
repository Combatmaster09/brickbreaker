import pygame
import globals

class Menu:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.screen = game_instance.screen
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Button dimensions and positions
        button_width = 200
        button_height = 60
        self.screen_center_x = self.screen.get_width() // 2
        self.screen_center_y = self.screen.get_height() // 2
        
        # Play button
        self.play_button_rect = pygame.Rect(
            self.screen_center_x - button_width // 2,
            self.screen_center_y - 20,
            button_width, 
            button_height
        )
        
        # Exit button
        self.exit_button_rect = pygame.Rect(
            self.screen_center_x - button_width // 2,
            self.screen_center_y + 60,
            button_width, 
            button_height
        )
        
        # Paddle selection buttons
        selection_width = 250
        selection_height = 40
        
        # Velocity paddle button
        self.velocity_button_rect = pygame.Rect(
            self.screen_center_x - selection_width // 2,
            self.screen_center_y - 100,
            selection_width,
            selection_height
        )
        
        # Acceleration paddle button
        self.accel_button_rect = pygame.Rect(
            self.screen_center_x - selection_width // 2,
            self.screen_center_y - 140,
            selection_width,
            selection_height
        )
        
        # Game state
        self.active = True
        self.show_main_menu = True
        self.show_game_over = False
        
    def draw_main_menu(self):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title_text = self.font_large.render("BRICK BREAKER", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_center_x, self.screen_center_y - 250))
        self.screen.blit(title_text, title_rect)
        
        # Draw paddle selection text
        paddle_text = self.font_medium.render("SELECT PADDLE TYPE:", True, (255, 255, 255))
        paddle_rect = paddle_text.get_rect(center=(self.screen_center_x, self.screen_center_y - 180))
        self.screen.blit(paddle_text, paddle_rect)
        
        # Draw velocity paddle button
        # Highlight the currently selected paddle type
        velocity_color = (0, 150, 200) if globals.paddle_type == "VelocityPaddle" else (50, 50, 150)
        pygame.draw.rect(self.screen, velocity_color, self.velocity_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.velocity_button_rect, 2)
        
        velocity_text = self.font_small.render("Velocity Paddle", True, (255, 255, 255))
        velocity_text_rect = velocity_text.get_rect(center=self.velocity_button_rect.center)
        self.screen.blit(velocity_text, velocity_text_rect)
        
        # Draw acceleration paddle button
        accel_color = (0, 150, 200) if globals.paddle_type == "AccelerationPaddle" else (50, 50, 150)
        pygame.draw.rect(self.screen, accel_color, self.accel_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.accel_button_rect, 2)
        
        accel_text = self.font_small.render("Acceleration Paddle", True, (255, 255, 255))
        accel_text_rect = accel_text.get_rect(center=self.accel_button_rect.center)
        self.screen.blit(accel_text, accel_text_rect)
        
        # Draw play button
        pygame.draw.rect(self.screen, (50, 150, 50), self.play_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.play_button_rect, 2)
        
        play_text = self.font_medium.render("PLAY", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=self.play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)
        
        # Draw exit button
        pygame.draw.rect(self.screen, (150, 50, 50), self.exit_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.exit_button_rect, 2)
        
        exit_text = self.font_medium.render("EXIT", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text, exit_text_rect)
        
    def draw_game_over(self, score):
        # Fill background
        self.screen.fill((0, 0, 0))
        
        # Draw game over title
        title_text = self.font_large.render("GAME OVER", True, (255, 50, 50))
        title_rect = title_text.get_rect(center=(self.screen_center_x, self.screen_center_y - 150))
        self.screen.blit(title_text, title_rect)
        
        # Draw final score
        score_text = self.font_medium.render(f"Final Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_center_x, self.screen_center_y - 70))
        self.screen.blit(score_text, score_rect)
        
        # Draw play again button (reuse play button position)
        pygame.draw.rect(self.screen, (50, 150, 50), self.play_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.play_button_rect, 2)
        
        play_text = self.font_medium.render("PLAY AGAIN", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=self.play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)
        
        # Draw exit button
        pygame.draw.rect(self.screen, (150, 50, 50), self.exit_button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), self.exit_button_rect, 2)
        
        exit_text = self.font_medium.render("EXIT", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text, exit_text_rect)
    
    def handle_events(self):
        """Handle menu events, returns True if game should start, False if exit"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.game = False
                pygame.quit()
                return False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check for button clicks
                if self.play_button_rect.collidepoint(mouse_pos):
                    self.active = False
                    self.show_main_menu = False
                    self.show_game_over = False
                    return True
                    
                if self.exit_button_rect.collidepoint(mouse_pos):
                    globals.game = False
                    pygame.quit()
                    return False
                    
                # Handle paddle selection button clicks
                if self.show_main_menu:
                    if self.velocity_button_rect.collidepoint(mouse_pos):
                        globals.paddle_type = "VelocityPaddle"
                    elif self.accel_button_rect.collidepoint(mouse_pos):
                        globals.paddle_type = "AccelerationPaddle"
        
        return None  # No definitive action taken
    
    def run_menu_loop(self):
        """Run the menu loop until a definitive choice is made"""
        clock = pygame.time.Clock()
        
        while self.active and globals.game:
            clock.tick(60)
            result = self.handle_events()
            
            if result is not None:
                return result
                
            if self.show_main_menu:
                self.draw_main_menu()
            elif self.show_game_over:
                self.draw_game_over(globals.score)
                
            pygame.display.flip()
        
        return True  # Default to starting the game