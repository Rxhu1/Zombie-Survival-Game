import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from pause import Pause



class Level:
    def __init__(self):
        '''
        Attributes of the level class. In this case, there will be a lot of attributes
        as they will used throughout a lot of methods. This is one of the longest files.
        For any external classes being used, these are instantiated here.
        '''
        #to grap the display surface
        self.display_surface = pygame.display.get_surface()
        self.minimap = pygame.image.load('sprites2/5 - level graphics/graphics/tilemap/ground3.png').convert()
        
        #Group of Sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        #user interface
        self.ui = UI()
        self.pause = Pause()
        self.deathstate = True
        self.death_paused = False
        self.state = True
        self.state_timer = 0
        self.state_cooldown = 400
        self.game_paused = False
        self.circle_state = True
        self.circle_timer = 0
        self.circle_cooldown = 1
        self.death_music = False

        #sounds
        self.you_died = pygame.mixer.Sound('sprites2/5 - level graphics/audio/you_died.wav')
        self.you_died.set_volume(0.5)

        #circle positions
        #self.circle_pos_x = self.player.circle_pos_x
        #self.circle_pos_y = self.player.circle_pos_y

        #particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        '''
        This method is called once and creates the map. It involves defining all of the csv layouts
        for each type of asset into a dictionary. It replaces the numbers in the csv file with the
        respective style to be drawn. This is done using the Tile class. It is in this class that
        all of enemies and the player are instatiated in their positions on the map.
        '''
        layouts = {
            'boundary': import_csv_layout('sprites2/5 - level graphics/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('sprites2/5 - level graphics/map/map_Grass.csv'),
            'object': import_csv_layout('sprites2/5 - level graphics/map/map_Objects.csv'),
            'entities': import_csv_layout('sprites2/5 - level graphics/map/map_Entities.csv')
        }
        graphics = {
            'grass': import_folder('sprites2/5 - level graphics/graphics/grass'),
            'objects': import_folder('sprites2/5 - level graphics/graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    #to get x and y values via the tilesize
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites],'invisible') #Only needs to be collidable
                        if style == 'grass':
                            #grass tile
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',random_grass_image) #Needs to be both visible and collidable

                        if style == 'object':
                            #object tile
                            surf= graphics['objects'][int(col)] #the column is used as an index
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

                        if style == 'entities':
                            #enemy
                            if col == '394':
                                self.player = Player((x,y),[self.visible_sprites],self.obstacle_sprites,self.create_attack,self.destroy_attack,self.create_magic)
                            else:
                                if col == '390': monster_name = 'grassrot'
                                elif col == '391': monster_name = 'tear'
                                elif col == '392': monster_name = 'gorilla'
                                else: monster_name = 'zombie'
                                Enemy(monster_name,(x,y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,self.damage_player,
                                      self.trigger_death_particles,self.add_exp,self.add_energy)

    def create_attack(self):
        '''
        This method is quite obvious where I create the different weapons on screen to attack the sprites
        in the attack sprites group.
        '''
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites])

    def create_magic(self,style,strength,cost):
        '''
        This is where I call either the heal or flame methods of the player class
        depending on the style that is currently equipped.
        '''
        if style == 'heal':
            self.magic_player.heal(self.player,strength,cost,[self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player,cost,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        '''
        This is used to delete the sprite from the groups it is associated with.
        This is done when the attribute current_attack is true.
        '''
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        '''
        This subroutine is constantly run to check for the collision of attack sprites and
        attackable sprites. For example, if there is collision between the two, with the target being grass,
        the related grass particles.
        '''
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                #checking collision of all attack and attackable sprites
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75)
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset,[self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player,attack_sprite.sprite_type)

    def damage_player(self,amount,attack_type):
        '''
        This method reduces the health of the player if they arent invulnerable.
        The player is invulnerable between hits to make the experience more 
        enjoyable. The hurt_time attribute was used to create the timer between hits
        for the time of invulnerability
        '''
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(attack_type,self.player.rect.center,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        '''
        particles are played after death, using the particle type
        and position which is passed in as an argument.
        '''
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def play_music(self,mp3_file):
        '''
        This is the music player. This is used to player to longer audio tracks.
        The following methods, load the file, set the volume and play the song
        whilst looping it indefinetly till the song changes.
        '''
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(loops=-1)

    def add_exp(self,amount):
        '''
        This method is created to add to the exp of the player.
        This will be added as an argument to the enemy when it is created.
        It will add the amount specified by the enemy type and its data for exp.
        '''
        self.player.exp += amount

    def add_energy(self,amount):
        '''
        This is very similar to the add_exp method, but instead just adds
        to the level of energy that the player has. Similarly, it uses the amount specified
        in the enemy dictionary. This is unique depending on the enemy that is killed. A 
        stronger enemy will give the player more energy for killing them compared to a simple enemy.
        '''
        self.player.energy += amount

    def toggle_menu(self):
        '''
        This method is used to toggle between being paused and unpaused. It
        achieves this by using 'not' to switch the boolean value held in 
        game_pause. In this same method, I used this boolean variable to 
        pause and unpause the music. This way, the music does not keep playing
        when the game is paused. It also does not restart the song when you unpause.
        '''
    
        self.game_paused = not self.game_paused

        if self.game_paused:
            pygame.mixer.music.pause()
        elif not self.game_paused:
            pygame.mixer.music.unpause()

    def toggle_death(self):
        '''
        Similar to my pause method, this will be used for the player dies.
        This is used to switch to the death gamestate
        '''
        self.death_paused = not self.death_paused

    def level_cooldown(self):
        '''
        This method looks after all of my cooldowns in my level class.
        This will control the timer between being able to switch between 
        playing and pause gamestates without being able to 'spam' between them.
        Similarly, I have this for the state of my circle so that is only drawn when the
        variable is false.
        '''
        current_time = pygame.time.get_ticks()

        if not self.state:
            if current_time - self.state_timer >= self.state_cooldown:
                self.state = True

        if not self.circle_state:
            if current_time - self.circle_timer >= self.circle_cooldown:
                self.circle_state = True

    def run(self):
        '''
        This is the run function in my level class. This run function is constantly called throughout the lifetime
        of the program for every tick. I have separated this using selective statements which allowed me to choose what
        is run depending on the gamestate. For example, I have all of the draw methods at the top so that they always
        constantly run no matter the gamestate. This is the same with any cooldown functions which need to be called
        to constantly check if the cooldown has expired after each tick. I then separatly add the update functions to the
        end via the else statement. This means if the user has not entered any of the other gamestates, the updates will proceed
        as normal. When the game is paused, that boolean variable becomes true and the follow code is run whilst the update functions
        are not run which makes it seem like the game is paused. Similarly, I did the same with the circle state for the minimap and the
        death gamestate.
        '''
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        self.display_surface.blit(self.minimap,(1074,14))
        self.level_cooldown()
        if self.circle_state:
            pygame.draw.circle(self.display_surface,(57,255,20),(self.player.circle_pos_x,self.player.circle_pos_y), 3)
            self.circle_state = False
            self.circle_timer = pygame.time.get_ticks()

        if self.game_paused:
            #display pause sign
            #self.pause_cooldown()
            surf = self.pause.blur_surf()
            self.display_surface.blit(surf,(0,0))
            self.pause.draw_pause()

        elif self.death_paused:
            surf = self.pause.blur_surf()
            self.display_surface.blit(surf,(0,0))
            self.pause.draw_death()
            self.death_music = True
            #self.play_music('sprites2/5 - level graphics/audio/soulofcinder.ogg')
            
            

        else: #run the game
            #need to update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            


class YSortCameraGroup(pygame.sprite.Group):
    '''
    This class was created to centre the camera around the player at all times no matter where
    they move. In addition, I created a custom draw method, to draw sprites on the map. In this
    same custom draw method, I have added offsets to the x and y coordinates. This way, it feels
    slightly less ridged. This also includes the enemy update method.
    '''
    def __init__(self):
        '''
        These are the attributes for this 'ysortcameragroup' class which include general variables
        such as the screen size, the display surface, as well as the offset that will be used. IT also
        contains the file used for the floor and its respective vector.
        '''
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2(100,200)

        #ground creation
        self.floor_surf = pygame.image.load('sprites2/5 - level graphics/graphics/tilemap/ground2.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self,player):
        '''
        This is the custom draw method which focuses on adding the offset to the camera when it is
        centred around the player as well as drawing assets onto the map.
        '''
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawing the floor + offset
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

    def enemy_update(self,player):
        '''
        This method is for updating the enemy constantly which can be called within the
        level run method.
        '''
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for sprite in enemy_sprites:
            sprite.enemy_update(player)