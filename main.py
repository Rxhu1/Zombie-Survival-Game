import pygame, sys, os
from settings import *
from level import Level

#v.1.0.3

class Game:
    def __init__(self):  
        '''
        Attributes of the main game class. These will be used throughout the program.
        This mainly contains some boolean attributes, needed to run specific subroutines
        throughout this section of code.
        '''
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('Ruf Der Untoten')
        self.clock = pygame.time.Clock()
        self.startupimage1 = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/startup3.png')
        self.startupimage2 = pygame.image.load('sprites2/5 - level graphics/graphics/gamestates/startup2.png')
        self.level = Level()
        self.gameShowing = False
        self.audio_playing = False
        self.death_played = True
        self.death_effect = True
        self.run_game = True
        #self.state = True
        #self.minimap = pygame.image.load('sprites2/5 - level graphics/graphics/tilemap/ground3.png').convert()

        #sound
        #self.main_sound = pygame.mixer.Sound('sprites2/5 - level graphics/audio/tigertracks.mp3')
        #self.startup_sound = pygame.mixer.Sound('sprites2/5 - level graphics/audio/soon.mp3')
        #self.main_sound.set_volume(0.3)
        #self.startup_sound.set_volume(0.3)
        
    #def play_music(self,mp3_file):
     #   pygame.mixer.init()
      #  pygame.mixer.music.load(mp3_file)
       # pygame.mixer.music.set_volume(0.3)
        #pygame.mixer.music.play(loops=-1)

    '''
    This is the main run file is. This is where most of the important sections of the code lie,
    where I can make use of the event loop and switch between different gamestates.
    ''' 
    def run(self):
        imageTimer = 0
        self.level.play_music('sprites2/5 - level graphics/audio/zero.ogg')
        while self.run_game:
            '''
            Below is where I will make use of the event loop, which will let me check my user inputs,
            and call certain methods from other files which correspond to their input
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #Allows game to be closed
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN: #Checks for any user input
                    if event.key == pygame.K_SPACE: #Allows player to enter the playing gamestate when they press space
                        self.gameShowing = True
                        if not self.audio_playing:
                            self.level.play_music('sprites2/5 - level graphics/audio/tigertracks.mp3')
                            self.audio_playing = True
                if self.gameShowing and self.level.game_paused and self.level.state: #This section is for the button press with the mouse
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if pos[0] < 709 and pos[0] > 569: #These are the two x values that I need to check if the mouse click is within
                            if pos[1] < 424 and pos[1] > 335: #These are the two y values that I need to check if the mouse click is within
                                self.level.toggle_menu()
                                '''
                                These are the required variables needed to be stated in order
                                to make use of my cooldowns timer in my level file.
                                '''
                                self.level.state = False
                                self.level.state_timer = pygame.time.get_ticks()
                #if self.level.death_music and self.death_played:
                    #self.level.play_music('sprites2/5 - level graphics/audio/soulofcinder.ogg')
                    #self.death_played = False
                '''
                The set of code below will allow the user to restart the game,
                making use of the 'os' library.
                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.level.death_paused:
                        #self.run_game = False
                        print("Restart")
                        pygame.mouse.set_pos([1500,360])
                        os.execl(sys.executable, sys.executable, *sys.argv)
                        
                    
                        
            '''
            The following code is run when the game starts,
            including the run method in the level class
            '''
            if self.gameShowing:
                self.screen.fill(LAVA_COLOR)
                self.level.run()
                #pygame.mixer.music.stop()
                #self.play_music('sprites2/5 - level graphics/audio/tigertracks.mp3')
                #self.startup_sound.set_volume(0)
                #self.main_sound.play(loops = -1)
                #self.screen.blit(self.minimap,(1074,14))
                #pygame.draw.circle(self.screen,(57,255,20),(1200,105), 3)
                '''
                Below is the usage of the event loop to allow the user to
                pause and unpause the game as well as enter the death gamestate.
                '''
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.level.state:
                        self.level.toggle_menu()
                        self.level.state = False
                        self.level.state_timer = pygame.time.get_ticks()
                if self.level.player.death and self.level.deathstate:
                    self.level.toggle_death()
                    self.level.deathstate = False

                '''
                This set of code is to let the player flicker on screen as they are spawning
                alongside the music. This is done by manipulating the alpha value of the player
                which changes the transparency of the player.
                '''
                if self.level.player.start_flicker:
                    if not self.level.player.flicker_switch:
                        self.level.player.flicker_time = pygame.time.get_ticks()
                    self.level.player.flicker_switch = True
                    alpha = self.level.player.start_wave_value()
                    self.level.player.image.set_alpha(alpha)
                    #if not self.level.player.flicker_switch:
                        #self.level.player.start_flicker = False

                '''
                This determines what happens to the player when they die. Here, music will
                be played, the death screen will be shown, death effects will be drawn
                and boolean variables will be toggled to maintain this gamestate.
                '''  
                if self.level.death_music and self.death_played:
                    self.level.play_music('sprites2/5 - level graphics/audio/soulofcinder4.ogg')
                    pygame.mixer.music.set_volume(0.4)
                    self.level.you_died.play()
                    self.death_played = False

                if self.level.death_music and self.death_effect:
                    self.level.you_died.play()
                    self.death_effect = False

            else:
                '''
                This is where the startup gamestate occurs, where the screen will switch between these two images.
                It will have its own delay per image to really bring out the sense that the buttons in the controls
                are being pressed. The usage of the timer will be needed to make sure that the second image is only
                shown for 25 ticks whereas the main image is shown for a total of 65 ticks, before resetting the timer.
                '''
                #self.play_music('sprites2/5 - level graphics/audio/tigertracks.mp3')
                #self.startup_sound.play(loops = -1)
                #game.play_music('sprites2/5 - level graphics/audio/soon.ogg')
                if imageTimer > 25:
                    self.screen.blit(self.startupimage1, (0,0))
                    if imageTimer > 90:
                        imageTimer = 0
                else:
                    self.screen.blit(self.startupimage2, (0,0))
                #self.play_music('sprites2/5 - level graphics/audio/tigertracks.mp3')

            pygame.display.update() #update method for the display
            self.clock.tick(FPS)
            imageTimer += 1 #used for timer
            
'''
Below is where my main file starts running code from. This is where the game class is instantiated
and the run method is called.
'''
if __name__ == '__main__': #This calls the method 'run' in the game class at the start of the program.
    game = Game()
    restart = False
    #restart feature
    #while restart == False:
    game.run()
    #    game.level.death_paused = False
    #game.run_game = True









