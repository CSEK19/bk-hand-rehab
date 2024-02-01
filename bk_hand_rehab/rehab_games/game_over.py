import pygame
from rehab_games.utils.constants import *

class GameOver:
  def __init__(self, utils, setting, game_state, score):
    self.utils = utils
    self.setting = setting
    self.game_state = game_state
    self.score = score
    self.selection = 0

  def render(self):
    # game over screen
    self.utils.screen.fill(WHITE_COLOR)
    if not self.setting.is_Vietnamese():
      text = self.utils.font.render("Game Over", True, (255, 99, 71))
      text1 = self.utils.font.render(f'Your Score: {self.score}', True, (56, 83, 153))
    else:
      text = self.utils.font.render("Trò chơi kết thúc", True, (255, 99, 71))
      text1 = self.utils.font.render(f'Điểm của bạn: {self.score}', True, (56, 83, 153))
    textRect1 = text1.get_rect()
    textRect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    self.utils.screen.blit(text, textRect)
    self.utils.screen.blit(text1, textRect1)

    # options popup
    popup_width, popup_height = 800, 180
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
    font_popup_text = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)
    if not self.setting.is_Vietnamese():
      options = ['Replay', 'Home']
    else:
      options = ['Chơi lại', 'Quay lại màn hình chính']
    texts = [font_popup_text.render(text, True, DEFAULT_COLOR) if i != self.selection \
      else font_popup_text.render(text, True, FONT_COLOR) for (i, text) in enumerate(options)]
    textRects = [text.get_rect() for text in texts]

    textRects[0].centerx = popup_surface.get_rect().centerx
    textRects[0].top = 0
    textRects[1].centerx = popup_surface.get_rect().centerx
    textRects[1].top = 40
    [popup_surface.blit(text, textRect) for text, textRect in zip(texts, textRects)]

    popup_rect = popup_surface.get_rect()
    popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    self.utils.screen.blit(popup_surface, popup_rect)

  def process_key(self, key):
    if key == pygame.K_UP:
      self.selection = (self.selection - 1) % 2
    elif key == pygame.K_DOWN:
      self.selection = (self.selection + 1) % 2
    elif key == pygame.K_RETURN:
      if self.selection == 0:
        return self.game_state
      else:
        return 'home'
