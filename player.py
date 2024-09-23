import pygame
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
    '''
    This is the player class which is inherited from the superior class 'entity'.
    It includes all of the relevant attributes and methods needed for the player
    to move around the map and play the game. It uses some methods shared with the 
    enemy as they work the same from the parent class.
    '''
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
        '''
        These are the attributes related to the player such as their asset, hitbox, cooldowns,
        flicker, as well as a large quantity of stats and sound effects.
        '''
        super().__init__(groups)
        self.image = pygame.image.load('sprites2/5 - level graphics/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-6,HITBOX_OFFSET['player'])

        #graphics setup
        self.import_player_assets()

        #flicker timer
        self.start_flicker = True
        self.flicker_switch = False
        self.flicker_cooldown = 1425
        self.flicker_time = None

        #movement
        self.attacking = False #Required for the attack timer
        self.attack_cooldown = 400 #Required for the attack timer
        self.attack_time = None #Required for the attack timer
        self.obstacle_sprites = obstacle_sprites

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0 #number to change between weapons
        self.weapon = list(weapon_data.keys())[self.weapon_index] #gets a key from the weapon data
        self.can_switch_weapon = True #Required for the weapon timer
        self.weapon_switch_time = None #Required for the weapon timer
        self.switch_duration_cooldown = 200 #Required for the weapon timer

        #magic
        self.create_magic = create_magic
        self.magic_index = 0 #number to change between weapons
        self.magic = list(magic_data.keys())[self.magic_index] #gets a key from the magic data
        self.can_switch_magic = True
        self.magic_switch_time = None

        #circle positions
        self.circle_pos_x = 1200
        self.circle_pos_y = 105
        self.proportion_x = MINIMAP_WIDTH / WIDTH
        self.proportion_y = MINIMAP_HEIGHT / HEIGHT

        #stats
        self.stats = {'health': 150,'energy': 60,'attack': 10,'magic': 4,'speed': 5}
        self.health = self.stats['health']
        self.energy = self.stats['energy'] * 0.8
        self.exp = 0
        self.speed = self.stats['speed']

        #death
        self.death = False

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #import sounds
        self.weapon_attack_sound = pygame.mixer.Sound('sprites2/5 - level graphics/audio/sword.wav')
        self.weapon_attack_sound.set_volume(0.05)
    
    def import_player_assets(self):
        '''
        This method is the foundation for importing files from their directories
        and using them to set up animations that will be used in other methods.
        '''
        character_path = '../NEA/sprites2/5 - level graphics/graphics/player/'
        self.animations = {'up': [],'down': [],'left': [],'right': [],
            'right_idle': [],'left_idle': [], 'up_idle': [],'down_idle': [],
            'right_attack': [],'left_attack': [],'up_attack': [],'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        
    #player movement
    def input(self):
        '''
        This method checks the input of the player to see which direction they want to move in and
        changes the status accordingly as well as the x and y of the player, letting them move. It
        also changes the coordinates of the player dot for the minimap. It checks for the inputs for
        changing weapons or magic and performs the following action aswell as checking if the user
        is trying to attack with either their weapon directly or from a range with their magic.
        '''
        if not self.attacking:    
            keys = pygame.key.get_pressed()

            #movement input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
                #self.collision('verticle')
                #if self.status != 'collided':
                if self.circle_collision == False:
                    self.circle_pos_y += self.direction.y * self.proportion_y
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
                #self.collision('verticle')
                #if self.status != 'collided':
                if self.circle_collision == False:
                    self.circle_pos_y += self.direction.y * self.proportion_y
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
                #self.collision('horizontal')
                #if self.status != 'collided':
                if self.circle_collision == False:
                    self.circle_pos_x += self.direction.x * self.proportion_x
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
                #self.collision('horizontal')
                #if self.status != 'collided':
                if self.circle_collision == False:
                    self.circle_pos_x += self.direction.x * self.proportion_x
            else:
                self.direction.x = 0

            #attack input
            if keys[pygame.K_f] or pygame.mouse.get_pressed()[0]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()
                
            #magic input
            if keys[pygame.K_c]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style,strength,cost)
            
            #weapon swap
            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                
                self.weapon = list(weapon_data.keys())[self.weapon_index]
            
            #magic swap
            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()
                
                if self.magic_index < len(list(magic_data.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0
                
                self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        '''
        This method is really important for other methods as it determines the status
        of the player via the direction they are facing in aswell as checking if they
        are attack or idle by being still.
        '''
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'
        
        #attacking status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'

        elif 'attack' in self.status:
            self.status = self.status.replace('_attack','')

    def cooldowns(self):
        '''
        This method has the implementation for all of the cooldowns used in the player class.
        This includes attacking , weapon and magic swap, vulnerability, and flickering cooldowns.
        '''
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()
        
        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True
        
        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

        if self.flicker_switch:
            if current_time - self.flicker_time >= self.flicker_cooldown:
                self.flicker_switch = False
                self.start_flicker = False

    def animate(self):
        '''
        This is the animate method which makes use of the status of the player
        to determine the aniamtion that should be played. In addition, the flickering
        of the player implementation is here, only once the player takes damage, using
        the manipulation of the asset alpha values.
        '''
        animation = self.animations[self.status]

        #loop the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        #flicker
        if not self.vulnerable:
            #toggle between 0 and 255
            alpha = self.damage_wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(225)

        #if self.start_flicker:
        #    self.flicker_switch = True
        #    self.flicker_time = pygame.time.get_ticks()
        #    alpha = self.wave_value()
        #    self.image.set_alpha(alpha)
        #    if not self.flicker_switch:
        #        self.start_flicker = False

    def check_death(self):
        '''
        This method quite litterally checks if the player is dead and
        if so, will change the death attribute to true.
        '''
        if self.health <= 0:
            self.death = True

    def get_full_weapon_damage(self):
        '''
        This method gets the damage of the weapon in use as well as the
        base damage of the player to get a total damage being returned
        which will be used in other methods.
        '''
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        '''
        This method gets the damage of the magic spell in use as well
        as the base damage of the player to get a total damage being
        returned which will be used in other methods.
        '''
        base_damage = self.stats['magic']
        spell_damage = magic_data[self.magic]['strength']
        return base_damage + spell_damage

    def energy_recovery(self):
        '''
        This is the method which allows the energy of the player to slowly increment
        every tick until it matches the stat of the energy for the player which
        is full.
        '''
        if self.energy < self.stats['energy']:
            self.energy += 0.02
        else:
            self.energy = self.stats['energy']

    def update(self):
        '''
        This is the update method for the player class. This calls all
        of the relevant methods in the player class that need to be called
        each tick. This was made to aid with the modularity of the program.
        '''
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.energy_recovery()
        self.check_death()