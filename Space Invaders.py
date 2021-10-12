import random
import math
import time
import arcade


class Lives(arcade.sprite):
    def __init__(self):
        super().__init__('')




class Enemy(arcade.Sprite):
    def __init__(self, w, h):
        super().__init__(":resources:images/space_shooter/playerShip2_orange.png")
        self.speed = 4 
        self.center_x= random.randint(0, w)
        self.center_y= h
        self.angle = 180
        self.width = 48
        self.height = 48
    def move(self):
        self.center_y -= self.speed
        

class Bullet(arcade.Sprite):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.speed = 8
        self.angle = host.angle
        self.center_x = host.center_x
        self.center_y = host.center_y
    
    def move(self):
        angle_rad = math.radians(self.angle)
        self.center_x -= self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)



class SpaceCraft(arcade.Sprite):
    def __init__(self, w):
        super().__init__(":resources:images/space_shooter/playerShip1_green.png")
        self.width = 48
        self.height = 48
        self.center_x = w//2
        self.center_y = 48
        self.angle = 0
        self.change_angle = 0
        self.bullet_list = []

    
    def rotate(self):
        self.angle += 4*(self.change_angle)
    def fire(self):
        self.bullet_list.append(Bullet(self)) 

class Game(arcade.Window):
    def __init__(self):
        self.w = 800
        self.h = 600
        super().__init__(width=self.w, height=self.h, title='Silver space craft')
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.me = SpaceCraft(self.w)
        self.enemy_list = []
        self.start_time = time.time()
        # Pre-load the animation frames. We don't do this in the __init__
        # of the explosion sprite because it
        # takes too long and would cause the game to pause.
        self.explosion_texture_list = []

        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"

        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)

        # Load sounds. Sounds from kenney.nl
    

    
    


    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h, self.background_image)
        self.me.draw()
        for i in range(len(self.me.bullet_list)):
            self.me.bullet_list[i].draw()
        for i in range(len(self.enemy_list)):
            self.enemy_list[i].draw()
            
            
            
    
    def on_update(self, delta_time):
        print(len(self.enemy_list), len(self.me.bullet_list))
        self.end_time = time.time()

        if self.end_time-self.start_time >random.randint(4,6):
            self.enemy_list.append(Enemy(self.w, self.h))
            self.start_time = time.time()
            
        for i in range(len(self.me.bullet_list)):
            self.me.bullet_list[i].move()

        for i in range(len(self.enemy_list)):
            self.enemy_list[i].move()
        
        self.me.rotate()
        
        try:    
            for i in range(len(self.me.bullet_list)):
                for j in range(len(self.enemy_list)):

                    if arcade.check_for_collision(self.me.bullet_list[i], self.enemy_list[j]):
                        del self.me.bullet_list[i]
                        
                        
                        del self.enemy_list[j]
                        break
                    else:
                        pass
        except:
            pass    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.RIGHT:
            self.me.change_angle=-1
        elif key == arcade.key.LEFT:
            self.me.change_angle=1
        elif key == arcade.key.SPACE:
            self.me.fire()
    def on_key_release(self, key, modifiers):

        if key == arcade.key.RIGHT:
            self.me.change_angle=0
        elif key == arcade.key.LEFT:
            self.me.change_angle=0
        
    

game = Game()
arcade.run()