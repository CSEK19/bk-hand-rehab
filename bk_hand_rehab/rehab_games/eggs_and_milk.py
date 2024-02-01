import pygame
import os
import random
from rehab_games.utils.constants import *
from rehab_games.utils.functions import *

class Object(pygame.sprite.Sprite):
  def __init__(self, moving_range, img, state):
    super(Object, self).__init__()
    # initial state
    self.img = img
    self.state = state
    # init coordinate
    self.x_center, self.y_center = random.choice(moving_range), 50

  def update_y(self, y_range):
    self.y_center += y_range


class Container(pygame.sprite.Sprite):
  def __init__(self, container_img):
    super(Container, self).__init__()
    # state of the container
    self.state = 'egg'
    self.x_center, self.y_center = SCREEN_WIDTH // 2, SCREEN_HEIGHT
    # container img
    self.orig_img = container_img
    self.img = container_img
    # rotate angle and rotate increment
    self.r = 0
    self.current_angle = 0

  def change_state(self):
    self.state = 'milk' if self.state == 'egg' else 'egg'
    self.current_angle = 0 if (self.current_angle // 180) % 2 == 0 else 180
    self.r = 10

  def rotate_animation(self):
    self.current_angle += self.r
    self.img = pygame.transform.rotate(self.orig_img, self.current_angle)
    # if the current angle reaches 180, reset to angle 0 and reset r to 0
    if self.current_angle % 180 == 0:
      self.r = 0
  		
  def move(self, x_range):
    self.x_center += x_range


class EggsAndMilk:
  def __init__(self, utils, setting):
    # utils and setting
    self.utils = utils
    self.setting = setting

    # bg image
    bg_image = pygame.image.load(os.path.join("rehab_games\\sprites", "bg.png"))
    self.bg_image_resized = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    ### game attributes ###
    # easy
    self.moving_range_easy = [440, 640, 840]
    self.objects_easy = [0]
    self.speed_easy = 2

    # medium
    self.moving_range_med = [440, 640, 840]
    self.objects_med = [0, 1]
    self.speed_med = 3

    # hard
    self.moving_range_hard = [240, 440, 640, 840, 1040]
    self.objects_hard = [0, 1]
    self.speed_hard = 3

    # container, falling object images
    self.container_img = pygame.image.load('rehab_games\\sprites\\basket_milk.png')
    self.container_img = pygame.transform.scale(self.container_img, (180, 400))

    self.egg_img = pygame.image.load('rehab_games\\sprites\\egg.png')
    self.egg_img = pygame.transform.scale(self.egg_img, (100, 100))
    self.milk_img = pygame.image.load('rehab_games\\sprites\\milk-bottle.png')
    self.milk_img = pygame.transform.scale(self.milk_img, (100, 100))

    # init game state as easy
    self.score = 0
    self.speed = self.speed_easy
    self.moving_range = self.moving_range_easy
    self.objects_list = self.objects_easy

    ### help and stop window ###
    self.state = 'help'
    self.pause_selection = 0

    # init container and falling object
    self.container = Container(self.container_img)
    self.obj = Object(self.moving_range, self.egg_img, 'egg')

  def create_random_object(self):
    choice = random.choice(self.objects_list)
    if choice == 0:
      return self.egg_img, 'egg'
    else:
      return self.milk_img, 'milk'

  def check_correct_catch(self):
    cond1 = self.obj.y_center >= self.container.y_center - 200
    cond2 = self.container.x_center - 100 <= self.obj.x_center <= self.container.x_center + 100
    cond3 = self.obj.state == self.container.state
    return cond1 and cond2 and cond3

  # render the help pop up
  def need_help(self):
    popup_width, popup_height = 1000, 300
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 255))  # set alpha to 0
    font_popup = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
    font_popup_text = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    if not self.setting.is_Vietnamese():
      help_text = 'How to Play'
      desc_text = "Collect eggs with basket, collect milk with large bottle"
      option0_text = "To move container - move palm left or right"
      option1_text = "To convert between bottle and basket - rotate palm"
      option2_text = "Make a fist to close this window"
    else:
      help_text = 'Cách chơi'
      desc_text = "Thu nhặt trứng bằng giỏ, thu thập sữa bằng bình"
      option0_text = "Để di chuyển đồ hứng - lắc cổ tay sang trái/phải"
      option1_text = "Để chuyển đổi giữa giỏ và bình - xoay cổ tay"
      option2_text = "Nắm chặt bàn tay để đóng cửa sổ này"

    text_surface = font_popup.render(help_text, True, (255, 99, 71))
    text_rect = text_surface.get_rect()
    text_rect.centerx = popup_surface.get_rect().centerx
    text_rect.top = 20
    popup_surface.blit(text_surface, text_rect)

    desc_surface = font_popup_text.render(desc_text, True, FONT_COLOR)
    desc_rect = desc_surface.get_rect()
    desc_rect.centerx = popup_surface.get_rect().centerx
    desc_rect.top = 75
    popup_surface.blit(desc_surface, desc_rect)

    option0_surface = font_popup_text.render(option0_text, True, DEFAULT_COLOR)
    option0_rect = option0_surface.get_rect()
    option0_rect.centerx = popup_surface.get_rect().centerx
    option0_rect.top = 125
    popup_surface.blit(option0_surface, option0_rect)

    option1_surface = font_popup_text.render(option1_text, True, DEFAULT_COLOR)
    option1_rect = option1_surface.get_rect()
    option1_rect.centerx = popup_surface.get_rect().centerx
    option1_rect.top = 175
    popup_surface.blit(option1_surface, option1_rect)

    option2_surface = font_popup_text.render(option2_text, True, FONT_COLOR)
    option2_rect = option2_surface.get_rect()
    option2_rect.centerx = popup_surface.get_rect().centerx
    option2_rect.top = 225
    popup_surface.blit(option2_surface, option2_rect)

    popup_rect = popup_surface.get_rect()
    popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

    self.utils.screen.blit(popup_surface, popup_rect)

	# render the pause screen
  def pause(self):
    pause_screen(self.pause_selection, self.utils.screen, self.setting.is_Vietnamese())

	# render the main screen of the game
  def play(self, pause=False):
    # bg img
    self.utils.screen.blit(self.bg_image_resized, (0, 0))

    # render falling object
    obj_img = self.obj.img
    obj_rect = obj_img.get_rect(center=(self.obj.x_center, self.obj.y_center))
    self.utils.screen.blit(obj_img, obj_rect)

    # render container
    container_img = self.container.img
    container_rect = container_img.get_rect(center=(self.container.x_center, self.container.y_center))
    self.utils.screen.blit(container_img, container_rect)

    # score window
    if not self.setting.is_Vietnamese():
      self.screen_text(f'Score: {self.score}', (50, 50, 50), (150, 50))
    else:
      self.screen_text(f'Điểm: {self.score}', (50, 50, 50), (150, 50))

    if not pause:
      # update object coordinate and container rotation animation
      self.obj.update_y(self.speed)
      self.container.rotate_animation()

      ### validate containing the object correctly or not ###
      # catch successfully
      if self.check_correct_catch():
        self.score += 1
        obj_img, obj_state = self.create_random_object()
        self.obj = Object(self.moving_range, obj_img, obj_state)
      # cannot catch
      elif self.obj.y_center >= 900:
        return "over", self.score

      # update the difficulty level
      if 8 <= self.score <= 15:
        self.speed = self.speed_med
        self.objects_list = self.objects_med
        self.moving_range = self.moving_range_med
      elif self.score >= 16:
        self.speed = self.speed_hard
        self.objects_list = self.objects_hard
        self.moving_range = self.moving_range_hard
	
	# render the game
  def render(self):
    if self.state == 'help':
      self.play(pause=True)
      self.need_help()
		
    elif self.state == 'play':
      return self.play()

    elif self.state == 'pause':
      self.play(pause=True)
      self.pause()

  def screen_text(self, text, color, center):
    text1 = self.utils.font.render(text, True, color)
    textRect1 = text1.get_rect()
    textRect1.center = center
    self.utils.screen.blit(text1, textRect1)
	
  # process input from user
  def process_key(self, key):
    # help screen
    if self.state == 'help':
      if key == pygame.K_RETURN:
        self.state = 'play'

    # playing normally
    elif self.state == 'play':
      if key == pygame.K_p:
        self.state = 'pause'
      elif key == pygame.K_h:
        self.state = 'help'
      # game action
      elif key == pygame.K_LEFT and self.container.x_center > min(self.moving_range):
        self.container.move(-200)
      elif key == pygame.K_RIGHT and self.container.x_center < max(self.moving_range):
        self.container.move(200)
      elif key == pygame.K_z:
        self.container.change_state()

    # pausing
    elif self.state == 'pause':
      if key == pygame.K_DOWN:
        self.pause_selection = (self.pause_selection + 1) % 2
      elif key == pygame.K_UP:
        self.pause_selection = (self.pause_selection - 1) % 2
      # turn back to game
      elif key == pygame.K_RETURN:
        if self.pause_selection == 0:
          self.state = 'play'
        else:
          return 'home'