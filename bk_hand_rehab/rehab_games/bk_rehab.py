import pygame
import sys
from rehab_games.utils.constants import *
from rehab_games.homescreen import HomeScreen
from rehab_games.shapes_and_colors import ShapesAndColors
from rehab_games.eggs_and_milk import EggsAndMilk
from rehab_games.dino_run import DinoRun
from rehab_games.game_over import GameOver

# global pygame objects
class PyGameObject:
  def __init__(self, screen, clock, font, font_setting, music):
    self.screen = screen
    self.clock = clock
    self.font = font
    self.font_setting = font_setting
    self.music = music

# game setting
class GameSetting:
  def __init__(self):
    self.enable_music = True
    self.enable_Vie_language = False
      
  def set_music(self):
    self.enable_music = not self.enable_music
  
  def set_language(self):
    self.enable_Vie_language = not self.enable_Vie_language
  
  def is_music(self):
    return self.enable_music
  
  def is_Vietnamese(self):
    return self.enable_Vie_language
  
# main app
class BKRehab:
  def __init__(self):
    # init game
    pygame.mixer.init(44100, -16, 2, 2048)
    pygame.init()
    pygame.font.init()
    pygame.font.get_init()
    pygame.display.set_icon(pygame.image.load(ICON_PATH))
    pygame.display.set_caption("Video Games for Hand Rehabilitation")

    # pygame objects
    music = pygame.mixer.Sound(MUSIC)
    music.set_volume(0.5)

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.Font(FONT, 40)
    font_setting = pygame.font.Font(FONT, 30)

    # game objects and default game setting
    self.utils = PyGameObject(screen, clock, font, font_setting, music)
    self.setting = GameSetting()
    self.is_playing_music = False

    # state of the app
    self.state = 'home'
    self.prev_state = None
  
  # main loop of the app
  def start_app(self):
    while True:
      # music
      if self.setting.is_music():
        if not self.is_playing_music:
          self.utils.music.play(loops=-1)
        self.is_playing_music = True
      else:
        self.utils.music.stop()
        self.is_playing_music = False

      # continue to render the current window
      if self.state == self.prev_state:
        action = self.window.render()
        if action is not None:
          self.state = action
      # create new window
      else:
        if self.state == 'home':
          self.window = HomeScreen(self.utils, self.setting)
        elif self.state == 'game1':
          self.window = ShapesAndColors(self.utils, self.setting)
        elif self.state == 'game2':
          self.window = EggsAndMilk(self.utils, self.setting)
        elif self.state == 'game3':
          self.window = DinoRun(self.utils, self.setting)
        elif type(self.state) is tuple and self.state[0] == 'over':
          self.window = GameOver(self.utils, self.setting, self.prev_state, self.state[1])
          self.state = self.state[0]
        
        self.prev_state = self.state
      
        # render the window
        self.window.render()

      # listen to user event
      for event in pygame.event.get():
        # user press a key
        if event.type == pygame.KEYDOWN:
          action = self.window.process_key(event.key)
          if action is not None:
            self.state = action
        # user quit the game
        elif event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
      

      pygame.display.flip()
      # tick the clock
      self.utils.clock.tick(60)