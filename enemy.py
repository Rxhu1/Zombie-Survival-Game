import pygame
from settings import *
from entity import Entity
from support import *

class Enemy(Entity):
    '''
    This is the enemy class. This is what each object of this class will be based off of
    and is an inherited class from the superior class entity. The superior class holds attributes
    and methods that are shared between both the enemy and player classes.
    '''
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,add_exp,add_energy):
        '''
        These are the attributes for the enemy class containing all of the data from the monster data dictionary.
        It also includes the status, timer variables, and sound effect directories as attributes to be used within
        the different methods.
        '''
        super().__init__(groups)
        self.sprite_type = 'enemy'

        #graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        #movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.energy = monster_info['energy']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        #player interaction
        self.can_attack = True
        self.attack_time = 0
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp
        self.add_energy = add_energy

        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

        #sounds
        self.death_sound = pygame.mixer.Sound('sprites2/5 - level graphics/audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('sprites2/5 - level graphics/audio/hit.wav')
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])
        self.death_sound.set_volume(0.05)
        self.hit_sound.set_volume(0.05)
        self.attack_sound.set_volume(0.05)
    
    def import_graphics(self,name):
        '''
        This method is used to display the graphics for the enemies along side their animations.
        This make use of an imported method 'import_folder' from another file. It involves the
        manipulation of my file names with the names of the enemies so that the file directory
        changes in response to the name of the enemy passed in as an argument when this method
        is called.
        '''
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'sprites2/5 - level graphics/graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)
    
    def get_player_distance_direction(self,player):
        '''
        This method works out both the distance and direction of that the enemy
        can take to get to the user. This involves using the verctor2 class in pygame
        to gather the coordinations of the center of the enemy and the player and use
        this to work out the distance (pythagoras theorem). This creates the displacement
        between the two. It then uses the normalize subroutine to find the direction the enemy
        needs to take to reach the player.
        '''
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec  = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return(distance,direction)

    def get_status(self,player):
        '''
        This method finds the distance the anamy moves to check if they are moving
        as well as checking if their status is attacking, moving or idle. Here, this
        method will switch between the three status states depending on the validity 
        of certain conditions.
        '''
        distance = self.get_player_distance_direction(player)[0]

        #conditions to allow the enemies to attack move etc
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self,player):
        '''
        This method checks for the status of the enemy and performs relating actions.
        For example, this method will play the attack sound effect, damage to the player
        and the timer for each atttack. This only occurs if their status is attack. If
        their status is move, they will move towords the player. If neither of these occur,
        their direction will be set to their current position might makes it seem like they are not moving.
        '''
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2() #when they stop moving after player gets far
    
    def animate(self):
        '''
        This is the animate method. This is responsible for playing the correct animations
        during an enemies status. In addition, this method also includes the implementation for
        flickering the enemy when they take damage by manipulating their asset alpha values.
        '''
        animation = self.animations[self.status]

        #looping the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            #attack delay timer for enemy
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center) #displays enemy in the right position

        if not self.vulnerable:
            #flicker
            #toggle between 0 and 255
            alpha = self.damage_wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(225)

    def cooldowns(self):
        '''
        This method includes the implementation of the different cooldowns used within the
        enemy class. This includes the cooldown between attacks by the enemy and the cooldowns
        that they are invulnerable for.
        '''
        #timer between attacks
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            #uses pygames inbuilt ticks
            #sets duration for cooldown
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        '''
        This method is used to reduce the health of the enemy if they are attacked
        by the player by either a weapon or magic. It also controls some variables
        used for cooldowns as well as sound effects.
        '''
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            else:
                #magic damage
                self.health -= player.get_full_magic_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    
    def check_death(self):
        '''
        This method includes the following methods needing to be called once an enemy dies.
        This will be constantly checked in an update function.
        '''
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,self.monster_name)
            self.add_exp(self.exp)
            self.death_sound.play()
            self.add_energy(self.energy)

    def knockback(self):
        '''
        This method applies a knockback to the enemy when they get attacked
        by the player. They will move in the negative direction to where they
        were going. Each enemy has their own resisitance value which means
        larger enemies such as the gorilla will be knockbacked less than a
        zombie.
        '''
        #applies once enemy is attacked
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self): #general update
        '''
        This update method performs what the name suggests, running all of the methods
        which will need to be called every single tick that the program is running (when
        not paused). This update method is called in the level run method.
        '''
        self.knockback()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self,player): #update for enemy
        '''
        This is another update method which is more specific towords
        the enemy. This includes fewer methods which are called.
        '''
        self.get_status(player)
        self.actions(player)