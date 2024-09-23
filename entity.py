import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    '''
    This is the entity class, the parent class to both the player and
    enemy classes. This class contains attributes and methods that will
    be shared between both of these classes.
    '''
    def __init__(self,groups):
        '''
        These are the attributes for the entity class. This includes attributes
        to do with animation, direction, boolean attributes and the status. These
        are used within the methods in the entity class.
        '''
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.circle_collision = False
        #self.movement_position = pygame.math.Vector2()
        self.status = 'down'
    
    def move(self,speed):
        '''
        This is the move method which controls the movement of the hitboxes.
        This is done via the manipulation of the x and y coordinates. This
        also uses the collision method to check for either a horizontal or
        vertical collision to determine how the x and y values change.
        '''
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #self.movement_position = pygame.math.Vector2()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
        #self.rect.center += self.direction * speed

    def collision(self,direction):
        '''
        This is the collision method. This checks what the direction is first
        before determining if there is a obstacle colliding with the hitbox of
        the entity. This will apply to both the enemy and the player. If there is
        a collision, it will reset the x or y value to its prior value before collision.
        '''
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    #self.status = 'collided'
                    self.circle_collision = True
                    if self.direction.x > 0: #moving to the right
                        self.hitbox.right = sprite.hitbox.left #return the right of entity to left of collision object.
                        
                    if self.direction.x < 0: #moving to the left
                        self.hitbox.left = sprite.hitbox.right
                        
                elif not sprite.hitbox.colliderect(self.hitbox):
                    self.circle_collision = False
                #elif self.movement_position[0] != pygame.math.Vector2()[0]:
                    #self.circle_collision = False

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.circle_collision = True
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                        
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom
                        
                #elif self.movement_position[1] != pygame.math.Vector2()[1]:
                    #self.circle_collision = False
                #else:
                    #self.circle_collision = False
                        
        #if not sprite.hitbox.colliderect(self.hitbox):
        #            self.circle_collision = False
    
    def damage_wave_value(self):
        '''
        This is the method which controls the flickering of the enemy
        and the player, using a sin curve to change the value, which will
        be used as the alpha value to flicker the entity. This is for when
        the entity is damaged.
        '''
        value = sin(pygame.time.get_ticks() * 0.1)
        if value >= 0:
            return 255
        else:
            return 0
    
    def start_wave_value(self):
        '''
        This is the method which controls the flickering of the player,
        using a sin curve to change the value, which will be used as the
        alpha value to flicker the player. This is for when the player is
        spawning in, in line with the audio to show the player spawning in.
        '''
        value = sin(pygame.time.get_ticks() * 10)
        if value >= 0:
            return 255
        else:
            return 0