import os
import random
import pygame
from rehab_games.utils.constants import *
from rehab_games.utils.functions import *


RUNNING = [
  pygame.image.load(os.path.join("rehab_games\\sprites\\Dino", "DinoRun1.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Dino", "DinoRun2.png")),
]
JUMPING = pygame.image.load(os.path.join("rehab_games\\sprites\\Dino", "DinoJump.png"))
DUCKING = [
  pygame.image.load(os.path.join("rehab_games\\sprites\\Dino", "DinoDuck1.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Dino", "DinoDuck2.png")),
]

SMALL_CACTUS = [
  pygame.image.load(os.path.join("rehab_games\\sprites\\Cactus", "SmallCactus1.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Cactus", "SmallCactus2.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Cactus", "SmallCactus3.png")),
]
LARGE_CACTUS = [
  pygame.image.load(os.path.join("rehab_games\\sprites\\Cactus", "LargeCactus1.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Cactus", "LargeCactus2.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Cactus", "LargeCactus3.png")),
]

BIRD = [
  pygame.image.load(os.path.join("rehab_games\\sprites\\Bird", "Bird1.png")),
  pygame.image.load(os.path.join("rehab_games\\sprites\\Bird", "Bird2.png")),
]

CLOUD = pygame.image.load(os.path.join("rehab_games\\sprites\\Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("rehab_games\\sprites\\Other", "Track.png"))


class Dinosaur:
  X_POS = 80
  Y_POS = 510
  Y_POS_DUCK = 540
  JUMP_VEL = 8

  def __init__(self):
    self.duck_img = DUCKING
    self.run_img = RUNNING
    self.jump_img = JUMPING

    self.dino_duck = False
    self.dino_run = True
    self.dino_jump = False

    self.step_index = 0
    self.jump_vel = self.JUMP_VEL
    self.image = self.run_img[0]
    self.dino_rect = self.image.get_rect()
    self.dino_rect.x = self.X_POS
    self.dino_rect.y = self.Y_POS

    self.duck_interval = 25
    self.duck_count = 0

  def update(self, key=None):
    if self.dino_duck:
      self.duck()
    if self.dino_run:
      self.run()
    if self.dino_jump:
      self.jump()

    if self.step_index >= 10:
      self.step_index = 0

    if (key == pygame.K_UP) and not self.dino_jump and self.dino_rect.y == 510:
      self.dino_duck = False
      self.dino_run = False
      self.dino_jump = True
    elif (key == pygame.K_DOWN and not self.dino_jump) or self.duck_count > 0:
      self.duck_count += 1
      if self.duck_count == self.duck_interval:
        self.duck_count = 0
      self.dino_duck = True
      self.dino_run = False
      self.dino_jump = False
    elif not key and not self.dino_jump:
      self.dino_duck = False
      self.dino_run = True
      self.dino_jump = False

  def duck(self):
    self.image = self.duck_img[self.step_index // 5]
    self.dino_rect = self.image.get_rect()
    self.dino_rect.x = self.X_POS
    self.dino_rect.y = self.Y_POS_DUCK
    self.step_index += 1

  def run(self):
    self.image = self.run_img[self.step_index // 5]
    self.dino_rect = self.image.get_rect()
    self.dino_rect.x = self.X_POS
    self.dino_rect.y = self.Y_POS
    self.step_index += 1

  def jump(self):
    self.image = self.jump_img
    if self.dino_jump:
      self.dino_rect.y -= self.jump_vel * 2
      self.jump_vel -= 0.4
    if self.jump_vel < -self.JUMP_VEL:
      self.dino_jump = False
      self.jump_vel = self.JUMP_VEL

  def draw(self, my_screen):
    my_screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
  def __init__(self):
    self.x = SCREEN_WIDTH + random.randint(800, 1000)
    self.y = random.randint(50, 100)
    self.image = CLOUD
    self.width = self.image.get_width()

  def update(self, game_speed):
    self.x -= game_speed
    if self.x < -self.width:
      self.x = SCREEN_WIDTH + random.randint(2500, 3000)
      self.y = random.randint(50, 100)

  def draw(self, my_screen):
    my_screen.blit(self.image, (self.x, self.y))


class Obstacle:
  def __init__(self, image, type):
    self.image = image
    self.type = type
    self.rect = self.image[self.type].get_rect()
    self.rect.x = SCREEN_WIDTH

  def update(self, game_speed):
    self.rect.x -= game_speed
    if self.rect.x < -self.rect.width:
      return False

  def draw(self, SCREEN):
    SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
  def __init__(self, image):
    self.type = random.randint(0, 2)
    super().__init__(image, self.type)
    self.rect.y = 525


class LargeCactus(Obstacle):
  def __init__(self, image):
    self.type = random.randint(0, 2)
    super().__init__(image, self.type)
    self.rect.y = 500


class Bird(Obstacle):
  BIRD_HEIGHTS = [450, 490, 520]

  def __init__(self, image):
    self.type = 0
    super().__init__(image, self.type)
    self.rect.y = random.choice(self.BIRD_HEIGHTS)
    self.index = 0

  def draw(self, SCREEN):
    if self.index >= 9:
      self.index = 0
    SCREEN.blit(self.image[self.index // 5], self.rect)
    self.index += 1


class DinoRun:
  def __init__(self, utils, setting):
    # utils and setting
    self.utils = utils
    self.setting = setting

    # game parameters
    self.player = Dinosaur()
    self.cloud = Cloud()
    self.game_speed = 7
    self.x_pos_bg = 0
    self.y_pos_bg = 580
    self.points = 0
    self.obstacles = []
    self.state = 'help'
    self.pause_selection = 0

  def render(self):
    if self.state == 'help':
      self.play(pause=True)
      self.need_help()
		
    elif self.state == 'play':
      return self.play()

    elif self.state == 'pause':
      self.play(pause=True)
      self.pause()

    # pygame.display.update()

  # help pop up
  def need_help(self):
    popup_width, popup_height = 1000, 300
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
    font_popup = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
    font_popup_text = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    if not self.setting.is_Vietnamese():
      help_text = 'How to Play'
      desc_text = "Control the dinosaur to avoid obstacles as much as possible"
      option0_text = "To jump - move palm up"
      option1_text = "To duck - move palm down"
      option2_text = "Make a fist to continue"
    else:
      help_text = 'Cách chơi'
      desc_text = "Điều khiển chú khủng long để tránh các chướng ngại vật"
      option0_text = "Để nhảy - lắc cổ tay hướng lên"
      option1_text = "Để cúi - lắc cổ tay hướng xuống"
      option2_text = "Nắm chặt bàn tay để tiếp tục"

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

  def play(self, pause=False):
    # draw background, score, cloud and dinosaur
    self.utils.screen.fill(WHITE_COLOR)
    self.background()
    self.score()
    self.cloud.draw(self.utils.screen)
    self.player.draw(self.utils.screen)

    # update background, score, cloud and dinosaur and generate new obstacles
    if not pause:
      self.update_background()
      self.update_score()
      self.player.update()
      self.cloud.update(self.game_speed)

      # generate new obstacles if needed
      if len(self.obstacles) == 0:
        if random.randint(0, 2) == 0:
          self.obstacles.append(SmallCactus(SMALL_CACTUS))
        elif random.randint(0, 2) == 1:
          self.obstacles.append(Bird(BIRD))
        elif random.randint(0, 2) == 2:
          self.obstacles.append(LargeCactus(LARGE_CACTUS))

    # draw out and update obstacles
    rm_indices = []
    for idx, obstacle in enumerate(self.obstacles):
      obstacle.draw(self.utils.screen)
      if not pause:
        valid = obstacle.update(self.game_speed)
        if valid == False:
          rm_indices.append(idx)

        # game over
        if self.player.dino_rect.collidepoint(obstacle.rect.center):
          pygame.time.delay(500)
          return 'over', int(self.points)
    
    for rm_idx in rm_indices:
      del self.obstacles[rm_idx]

  # pause window
  def pause(self):
    pause_screen(self.pause_selection, self.utils.screen, self.setting.is_Vietnamese(), alpha=0)

  # calculate score
  def update_score(self):
    self.points += 0.05
    if int(self.points) % 5 == 0 and int(self.points) != 0 and int(self.points) <= 100:
      self.points += 0.01
      self.game_speed += 0.015

  # display score
  def score(self):
    if not self.setting.is_Vietnamese():
      text = self.utils.font.render("Score: " + str(int(self.points)), True, FONT_COLOR)
    else:
      text = self.utils.font.render("Điểm: " + str(int(self.points)), True, FONT_COLOR)
    textRect = text.get_rect()
    textRect.center = (150, 50)
    self.utils.screen.blit(text, textRect)

  # display background
  def background(self):
    image_width = BG.get_width()
    self.utils.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
    self.utils.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
    if self.x_pos_bg <= -image_width:
      self.utils.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
      self.x_pos_bg = 0

  def update_background(self):
    self.x_pos_bg -= self.game_speed

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
      # game action: jump or dodge
      elif key == pygame.K_UP or key == pygame.K_DOWN:
        self.player.update(key)

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