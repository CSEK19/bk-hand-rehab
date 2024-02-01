import pygame
import random
import math
import os
from rehab_games.utils.constants import *
from rehab_games.utils.functions import *

class ShapesAndColors:
  def __init__(self, utils, setting):
    # utils and setting
    self.utils = utils
    self.setting = setting
    
    # bg image
    bg_image = pygame.image.load(os.path.join("rehab_games\\sprites", "bg.png"))
    self.bg_image_resized = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # all other attributes
    self.answer_list = None
    self.correct_answer = None
    self.score = 0
    self.num_answer = 3
    self.shape_width = 175
    self.color_code_list = EASY_COLOR_CODE_LIST
    if not self.setting.is_Vietnamese():
      self.color_list = EASY_COLOR_LIST
      self.shape_list = EASY_SHAPE_LIST
    else:
      self.color_list = VIE_EASY_COLOR_LIST
      self.shape_list = VIE_EASY_SHAPE_LIST

    # random the initial answers
    self.random_answers()
    self.selection = 0

    # Setting for border shape
    self.border_color = (0, 0, 0)
    self.border_width = 2

    ### help and stop window ###
    self.state = 'help'
    self.pause_selection = 0

  # function to random the answer list
  def random_answers(self):
    self.answer_list = [(random.choice(self.color_code_list), random.choice(self.shape_list)) \
      for _ in range(self.num_answer)]

    while len(set(self.answer_list)) < self.num_answer:
      self.answer_list = [(random.choice(self.color_code_list), random.choice(self.shape_list)) \
        for _ in range(self.num_answer)]
    self.correct_answer = random.choice(self.answer_list)

  def update(self, num_answer):
    self.num_answer = num_answer
    if not self.setting.is_Vietnamese():
      if num_answer == 3:
        self.color_list = EASY_COLOR_LIST
        self.color_code_list = EASY_COLOR_CODE_LIST
        self.shape_list = EASY_SHAPE_LIST
      elif num_answer == 4:
        self.color_list = MEDIUM_COLOR_LIST
        self.color_code_list = MEDIUM_COLOR_CODE_LIST
        self.shape_list = MEDIUM_SHAPE_LIST
      elif num_answer == 5:
        self.color_list = HARD_COLOR_LIST
        self.color_code_list = HARD_COLOR_CODE_LIST
        self.shape_list = HARD_SHAPE_LIST
    else:
      if num_answer == 3:
        self.color_list = VIE_EASY_COLOR_LIST
        self.color_code_list = EASY_COLOR_CODE_LIST
        self.shape_list = VIE_EASY_SHAPE_LIST
      elif num_answer == 4:
        self.color_list = VIE_MEDIUM_COLOR_LIST
        self.color_code_list = MEDIUM_COLOR_CODE_LIST
        self.shape_list = VIE_MEDIUM_SHAPE_LIST
      elif num_answer == 5:
        self.color_list = VIE_HARD_COLOR_LIST
        self.color_code_list = HARD_COLOR_CODE_LIST
        self.shape_list = VIE_HARD_SHAPE_LIST

  def switch_selection(self, key):
    if key == pygame.K_RIGHT:
        self.selection = self.selection + 1 if self.selection < self.num_answer - 1 else 0
    if key == pygame.K_LEFT:
        self.selection = self.selection - 1 if self.selection > 0 else self.num_answer - 1

  # render the game play
  def render(self):
    if self.state == 'help':
      self.play()
      self.need_help()
    
    elif self.state == 'play':
      self.play()

    elif self.state == 'pause':
      self.play()
      self.pause()

  def play(self):
    color_map = {self.color_code_list[i]: self.color_list[i] for i in range(len(self.color_code_list))}
    self.utils.screen.blit(self.bg_image_resized, (0, 0))
    if not self.setting.is_Vietnamese():
      self.screen_text(f'Score: {self.score}', (50, 50, 50), (150, 50))
      self.screen_text(f'Choose the {color_map[self.correct_answer[0]]} {self.correct_answer[1]}',
                  (50, 50, 50),
                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    else:
      self.screen_text(f'Điểm: {self.score}', (50, 50, 50), (150, 50))
      self.screen_text(f'Chọn hình {self.correct_answer[1]} màu {color_map[self.correct_answer[0]]}',
                  (50, 50, 50),
                  (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    selection = self.selection
    # draw the shape and the selection box
    for index, (color, shape) in enumerate(self.answer_list):
      self.draw_shape_color(color, shape, index, self.num_answer, self.shape_width)

    self.draw_selection((56, 83, 153), self.selection, self.num_answer)

  def pause(self):
    pause_screen(self.pause_selection, self.utils.screen, self.setting.is_Vietnamese())

  def need_help(self):
    popup_width, popup_height = 1000, 300
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 255))  # set alpha to 0
    font_popup = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
    font_popup_text = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

    if not self.setting.is_Vietnamese():
      help_text = 'How to Play'
      desc_text = "Select the right shape following the description"
      option0_text = "To change selection - move palm left or right"
      option1_text = "To select - make a fist"
      option2_text = "Make a fist to close this window"
    else:
      help_text = 'Cách chơi'
      desc_text = "Chọn hình đúng theo mô tả"
      option0_text = "Để thay đổi lựa chọn - lắc cổ tay sang trái/phải"
      option1_text = "Để chọn - nắm chặt bàn tay"
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


  def screen_text(self, text, color, center):
    text_render = self.utils.font.render(text, True, color)
    text_rect = text_render.get_rect()
    text_rect.center = center
    self.utils.screen.blit(text_render, text_rect)
    return text_rect

  # functions to draw shapes and colors
  def draw_shape_color(self, color, shape, index, num_answer, shape_width):
    gap_width = self.shape_width // 2
    total_width = self.shape_width * num_answer + gap_width * (num_answer - 1)
    left = ((SCREEN_WIDTH - total_width) // 2) + (self.shape_width + gap_width) * index
    top = SCREEN_HEIGHT * 2 // 3
    shape_rect = [left, top, left + self.shape_width, top + self.shape_width]

    if shape == 'oval' or shape == 'bầu dục':
      pygame.draw.ellipse(self.utils.screen, color,
                          pygame.Rect(shape_rect[0] + 50, shape_rect[1], self.shape_width - 100, self.shape_width))
      pygame.draw.ellipse(self.utils.screen, self.border_color,
                          pygame.Rect(shape_rect[0] + 50, shape_rect[1], self.shape_width - 100, self.shape_width),
                          self.border_width)

    if shape == 'square' or shape == 'vuông':
      pygame.draw.rect(self.utils.screen, color, pygame.Rect(shape_rect[0], shape_rect[1], self.shape_width, self.shape_width))
      pygame.draw.rect(self.utils.screen, self.border_color, pygame.Rect(shape_rect[0], shape_rect[1], self.shape_width, self.shape_width),
                      self.border_width)

    if shape == 'triangle' or shape == 'tam giác':
      triangle_points = [[(shape_rect[0] + shape_rect[2]) // 2, shape_rect[1]], [shape_rect[0], shape_rect[3]],
                        [shape_rect[2], shape_rect[3]]]
      pygame.draw.polygon(self.utils.screen, color, triangle_points)
      pygame.draw.polygon(self.utils.screen, self.border_color, triangle_points, self.border_width)

    if shape == 'circle' or shape == 'tròn':
      circle_points = [(shape_rect[0] + shape_rect[2]) // 2, (shape_rect[1] + shape_rect[3]) // 2]
      pygame.draw.circle(self.utils.screen, color, circle_points, self.shape_width // 2)
      pygame.draw.circle(self.utils.screen, self.border_color,
                        [(shape_rect[0] + shape_rect[2]) // 2, (shape_rect[1] + shape_rect[3]) // 2],
                        self.shape_width // 2,
                        self.border_width)

    if shape == 'star' or shape == 'ngôi sao':
      left, top, right, bottom = shape_rect
      width = right - left
      height = bottom - top
      centre_coord = (left + width // 2, top + height // 2)
      radius = min(width, height) * 0.5
      star_points = []
      for i in range(10):
          angle = i * 2 * math.pi / 10
          if i % 2 == 0:
              x = centre_coord[0] + radius * math.cos(angle - math.pi / 2)
              y = centre_coord[1] + radius * math.sin(angle - math.pi / 2)
          else:
              x = centre_coord[0] + radius / 2 * math.cos(angle - math.pi / 2)
              y = centre_coord[1] + radius / 2 * math.sin(angle - math.pi / 2)
          star_points.append((int(x), int(y)))
      star_points.reverse()
      pygame.draw.polygon(self.utils.screen, color, star_points)
      pygame.draw.polygon(self.utils.screen, self.border_color, star_points, self.border_width)

    if shape == 'diamond' or shape == 'kim cương':
      diamond_points = [(shape_rect[0] + self.shape_width // 2, shape_rect[1]),  # top point
                        (shape_rect[0] + self.shape_width, shape_rect[1] + self.shape_width // 2),  # right point
                        (shape_rect[0] + self.shape_width // 2, shape_rect[1] + self.shape_width),  # bottom point
                        (shape_rect[0], shape_rect[1] + self.shape_width // 2)]  # left point

      # Draw the filled diamond
      pygame.draw.polygon(self.utils.screen, color, diamond_points)
      # Draw the diamond border
      pygame.draw.polygon(self.utils.screen, self.border_color, diamond_points, self.border_width)


  def draw_selection(self, color, index, num_answer):
    gap_width = self.shape_width // 2
    total_width = self.shape_width * num_answer + gap_width * (num_answer - 1)
    left = ((SCREEN_WIDTH - total_width) // 2) + (self.shape_width + gap_width) * index
    top = SCREEN_HEIGHT * 2 // 3
    shape_rect = [left, top, left + self.shape_width, top + self.shape_width]

    pygame.draw.rect(self.utils.screen, color, \
      pygame.Rect(shape_rect[0] - 20, shape_rect[1] - 20, self.shape_width + 40, self.shape_width + 40), 5)

  def check_valid_answer(self):
    if self.selection == self.answer_list.index(self.correct_answer):
      self.score += 1
      # update level
      if 8 <= self.score <= 15 and self.num_answer != 4:
          self.update(4)
      elif self.score >= 16 and self.num_answer != 5:
          self.update(5)
      self.random_answers()
    else:
      return 'over', self.score

  # process input from user
  def process_key(self, key):
    if self.state == 'help':
      if key == pygame.K_RETURN:
        self.state = 'play'

    elif self.state == 'play':
      if key == pygame.K_p:
        self.state = 'pause'
      elif key == pygame.K_h:
        self.state = 'help'
      elif key == pygame.K_LEFT:
        self.selection = (self.selection - 1) % self.num_answer
      elif key == pygame.K_RIGHT:
        self.selection = (self.selection + 1) % self.num_answer
      elif key == pygame.K_RETURN:
        # check_valid_answer
        return self.check_valid_answer()

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

