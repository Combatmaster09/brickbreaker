# In UI/ScoreManager.py
import pygame
import globals
from utils import print_text
import time  # Add this import

class ScoreManager:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.score_color = (255, 255, 255)
        self.high_score = 0
        self.lives = 3
        self.last_life_lost_time = 0  # Track when the last life was lost
        self.life_loss_cooldown = 1.0  # Cooldown in seconds
    
    def reduce_life(self):
        current_time = time.time()
        # Check if enough time has passed since the last life was lost
        if current_time - self.last_life_lost_time >= self.life_loss_cooldown:
            self.lives -= 1
            self.last_life_lost_time = current_time
            return self.lives <= 0  # Return True if game over
        return False  # Not enough time has passed, don't count as game over
        
    def update(self):
        # Update high score if current score is higher
        if globals.score > self.high_score:
            self.high_score = globals.score
    
    def draw(self, surface):
        # Draw score
        score_text = f"Score: {int(globals.score)}"
        level_text = f"Level: {globals.level}"
        lives_text = f"Lives: {self.lives}"
        high_score_text = f"High Score: {int(self.high_score)}"
        
        # Render score at top-left
        score_surface = self.font.render(score_text, True, self.score_color)
        surface.blit(score_surface, (20, 20))
        
        # Render level at top-center
        level_surface = self.font.render(level_text, True, self.score_color)
        level_rect = level_surface.get_rect(midtop=(surface.get_width() // 2, 20))
        surface.blit(level_surface, level_rect)
        
        # Render lives at top-right
        lives_surface = self.font.render(lives_text, True, self.score_color)
        lives_rect = lives_surface.get_rect(topright=(surface.get_width() - 20, 20))
        surface.blit(lives_surface, lives_rect)
        
        # Render high score at bottom-left
        high_score_surface = self.font.render(high_score_text, True, self.score_color)
        high_score_rect = high_score_surface.get_rect(bottomleft=(20, surface.get_height() - 20))
        surface.blit(high_score_surface, high_score_rect)
    
    def reset_score(self):
        globals.score = 0
    
    def reduce_life(self):
        self.lives -= 1
        return self.lives <= 0  # Return True if game over
    
    def add_life(self):
        """Add an extra life to the player"""
        self.lives += 1
        # Optionally play a sound or show an animation
        try:
            # If you have a sound for extra life
            extra_life_sound = load_sound("extra_life")
            extra_life_sound.play()
        except:
            pass