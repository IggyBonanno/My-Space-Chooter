import pygame
import os
import time
import random
pygame.font.init()
 
# Initialize Pygame
pygame.init()
 
WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(" Moj Spejs Chooter")
 
# Load images
RED_SPACE_SHIP =  pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP =  pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP =  pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
 
# Player  ship
YELLOW_SPACE_SHIP =  pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
 
# lasers
RED_LASER = pygame.image.load(os.path.join("assets","pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets","pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","pixel_laser_yellow.png"))
 
# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
 
class Laser:
    def __init__(self,  x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
   
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
 
    def move(self, vel):
        self.y += vel
 
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
   
    def collision(self, obj): #
        return collide(self, obj)
 
   


 
class Ship:
    COOLDOWN = 30
   
    def __init__(self, x, y, color=None, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0
       
        # Choose ship image based on color
        if color == 'red':
            self.ship_img = RED_SPACE_SHIP
        elif color == 'green':
            self.ship_img = GREEN_SPACE_SHIP
        elif color == 'blue':
            self.ship_img = BLUE_SPACE_SHIP
        else:
            self.ship_img = YELLOW_SPACE_SHIP
 
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
 
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
 
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
     
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
 
   
   
    def get_width(self):
        return self.ship_img.get_width() # using inside enemy ships constraint for screen movement
   
    def get_height(self):
        return self.ship_img.get_height()
 
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) # pixelperfect collision- hitbox pixel telly you  where pixels are and arent
        self.max_health = health # start with
 
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
 
class Enemy(Ship):
    COLOR_MAP = {
               "red": (RED_SPACE_SHIP, RED_LASER),
               "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
               "green": (GREEN_SPACE_SHIP, GREEN_LASER)
               }
   
    def __init__(self, x, y, color, health=100):
        super().__init__(x,y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
 
   
    def move(self, vel):
        self.y += vel
 
def collide(obj1, obj2): # defining collide with obj not hitbox
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y -obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None



 
def main():
    run = True
    FPS = 60
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("sans-serif", 50)
    lost_font = pygame.font.SysFont("sans-serif", 70)
 
    enemies = [] # storing in blank list where all enemies are
    wave_length = 5 #every new level generate batch of new enemies
    enemy_vel = 1
   
    player_vel = 5
    laser_vel = 5
 
    player = Player(200,400)
 
    lost = False
    lost_count = 0
 
    clock = pygame.time.Clock()
 
    def redraw_window():
        WIN.blit(BG, (0,0))
        # Draw text
        lives_label = main_font.render(f"Životi:{lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level:{level}", 1, (255,255,255))
 
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10 ))
 
        for enemy in enemies: # if in same position player is on top of enemy
            enemy.draw(WIN)
 
        player.draw(WIN)
 
        if lost:
            lost_label = lost_font.render("IZGUBILI STE!:-(", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 200)) # centering gave over on screen
           
 
        pygame.display.update()
   
    while run:
        clock.tick(FPS)
        redraw_window()
 
        if lives <= 0 or player.health <= 0:    # check if you have lost
            lost = True
            lost_count += 1
 
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue                      
 
        if len(enemies) == 0:                         # when no enemie on screen advance 1 level
            level +=1
            wave_length += 5                          # increase amount of enemies by 5
            for i in range(wave_length):               # creating the enemies
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"])) # Random pick of enemy ship color
                enemies.append(enemy)                   # appending enemies to enemy list
               
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
 
               
 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]and player.x - player_vel > 0: # Left
            player.x -= player_vel
        if keys[pygame.K_d]and player.x + player_vel + 100 < WIDTH:  # Right # 100 ogranicuje movement up,down,left,right
            player.x += player_vel
        if keys[pygame.K_w]and player.y - player_vel > 0: # Up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + 100 < HEIGHT: # Down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot
 
        for enemy in enemies[:]: # [:] copy of list so it doesent modify list
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if enemy.y + enemy.get_height() > HEIGHT: # checking for  position of enemies
                lives -= 1
                enemies.remove(enemy) # removing enemies when hit
 
        player.move_lasers(-laser_vel, enemies)
 
       
    # Quit Pygame
    pygame.quit()
 
if __name__ == '__main__':
    main()

 