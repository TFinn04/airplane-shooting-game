import pygame
import os
import random
from constants import *
import time

class Boss:
    def __init__(self):
        # Initialize boss position at the middle top of the screen
        self.rect = pygame.Rect(
            (screen_width - boss_width) // 2, 
            -boss_height,  # Start just above the screen
            boss_width,
            boss_height
        )
        
        # Select a random folder for boss images
        self.boss_images_folder = random.choice([
            "Images/bosses/boss1/", 
            "Images/bosses/boss2/", 
            "Images/bosses/boss3/"
        ])
        
        self.boss_animation_frames = []

        # Load các frame animation của boss từ thư mục được chọn
        for filename in sorted(os.listdir(self.boss_images_folder)):  # Đảm bảo thứ tự sắp xếp
            if filename.endswith(".png"):
                boss_frame = pygame.image.load(os.path.join(self.boss_images_folder, filename)).convert_alpha()
                self.boss_animation_frames.append(boss_frame)
        self.boss_frame_counter = 0
        self.boss_animation_speed = 5
        self.current_boss_frame = 0
        
        self.health = boss_health
        self.direction = 1  # 1 for right, -1 for left
        self.bullets = []
        
        # Load animation frames for boss bullets
        self.bullet_frames = []
        self.bullet_anim_folder = "Images/enemy_bullet/"  # Path to bullet animation frames
        for filename in sorted(os.listdir(self.bullet_anim_folder)):  # Ensure sorted order
            if filename.endswith(".png"):
                bullet_frame = pygame.image.load(os.path.join(self.bullet_anim_folder, filename)).convert_alpha()
                self.bullet_frames.append(bullet_frame)
        self.current_bullet_frame = 0
        self.bullet_animation_speed = 10  # Speed of bullet animation
        self.bullet_frame_counter = 0
        
        self.last_shot_time = pygame.time.get_ticks()
        self.charging = False
        self.charge_start_time = 0
        self.beam_start_time = 0
        self.beam_active = False

    def move(self):
        # Existing move method for vertical movement
        target_y = -boss_height//3
        if self.rect.y < target_y:
            self.rect.y += boss_speed  # Move down
        else:
            self.rect.y = target_y  # Stop at middle top

    def attack1(self):
        # Horizontal movement for attack1
        if self.rect.x <= 0:
            self.direction = 1
        elif self.rect.x >= screen_width - self.rect.width:
            self.direction = -1
        
        self.rect.x += boss_speed * self.direction

        # Shooting mechanism with animation
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > 300:  # Fire every 0.3 seconds
            # Bullet from left wing
            self.bullets.append(pygame.Rect(self.rect.x + self.rect.x//6, self.rect.centery - self.rect.y, self.bullet_frames[0].get_width(), self.bullet_frames[0].get_height()))
            # Bullet from right wing
            self.bullets.append(pygame.Rect(self.rect.right- self.rect.x//6 - self.bullet_frames[0].get_width(), self.rect.centery - self.rect.y, self.bullet_frames[0].get_width(), self.bullet_frames[0].get_height()))
            self.last_shot_time = current_time
    
    def attack2(self):
        if not self.charging and not self.beam_active:
            self.charging = True
            self.charge_start_time = time.time()

    def update_attack2(self):
        if self.charging:
            if time.time() - self.charge_start_time >= 5:  # Charging duration
                self.charging = False
                self.beam_active = True
                self.beam_start_time = time.time()

        if self.beam_active:
            if time.time() - self.beam_start_time >= 5:  # Beam duration
                self.beam_active = False

    def reposition(self):
        if self.rect.x <= 0:
            self.direction = 1
        elif self.rect.x >= screen_width - self.rect.width:
            self.direction = -1
        
        if self.rect != pygame.Rect((screen_width - boss_width) // 2, self.rect.y, boss_width, boss_height):
            self.rect.x += boss_speed * self.direction

    def draw(self, screen):
        # Draw the boss animation frame
        self.boss_frame_counter += 1
        if self.boss_frame_counter >= self.boss_animation_speed:
            self.current_boss_frame = (self.current_boss_frame + 1) % len(self.boss_animation_frames)
            self.boss_frame_counter = 0

        screen.blit(self.boss_animation_frames[self.current_boss_frame], (self.rect.x, self.rect.y))

        # Draw bullets with animation
        for bullet in self.bullets:
            # Animate the bullets
            self.bullet_frame_counter += 1
            if self.bullet_frame_counter >= self.bullet_animation_speed:
                self.current_bullet_frame = (self.current_bullet_frame + 1) % len(self.bullet_frames)
                self.bullet_frame_counter = 0

            screen.blit(self.bullet_frames[self.current_bullet_frame], (bullet.x, bullet.y))
        
        if self.charging:
            elapsed_time = time.time() - self.charge_start_time
            frame_index = int(elapsed_time * 121) % 121
            charge_image_path = f"Images/charge/charge{frame_index + 1}.png"
            charge_image = pygame.image.load(charge_image_path).convert_alpha()
            charge_rect = charge_image.get_rect(center=(self.rect.centerx, self.rect.bottom + charge_size//2.5))
            screen.blit(charge_image, charge_rect)

        if self.beam_active:
            elapsed_time = time.time() - self.beam_start_time
            frame_index = int(elapsed_time * 18) % 12
            beam_image_path = f"Images/beam/beam{frame_index + 1}.png"
            beam_image = pygame.image.load(beam_image_path).convert_alpha()
            
            beam_rect = beam_image.get_rect(center=(self.rect.centerx, self.rect.bottom +beam_height//2.5))
            screen.blit(beam_image, beam_rect)

    def take_damage(self, damage):
        # Reduce health by damage amount
        self.health -= damage
        return self.health <= 0  # Returns True if health is depleted

    def update_bullets(self):
        # Update bullet positions
        for bullet in self.bullets:
            bullet.y += enemy_bullet_speed
        # Remove bullets that have left the screen
        self.bullets = [bullet for bullet in self.bullets if bullet.y < screen_height]