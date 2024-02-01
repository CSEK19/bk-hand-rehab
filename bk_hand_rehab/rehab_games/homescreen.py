from rehab_games.utils.constants import *
import pygame
class HomeScreen:
  def __init__(self, utils, setting):
    # attributes
    self.utils = utils
    self.setting = setting
    self.selection = 0
    self.enable_setting = False
    self.setting_selection = 0
    
  # setting window rendering
  def setting_window(self):
    if not self.setting.is_Vietnamese():
      text2 = self.utils.font_setting.render('Settings', True, FONT_COLOR)
      text3 = self.utils.font.render('Settings', True, (255, 99, 71))

    else:
      text2 = self.utils.font_setting.render('Cài đặt', True, FONT_COLOR)
      text3 = self.utils.font.render('Cài đặt', True, (255, 99, 71))

    textRect2 = text2.get_rect()
    textRect2.center = (SCREEN_WIDTH - 100, 50)
    self.utils.screen.blit(text2, textRect2)

    popup_rect = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 25)
    pygame.draw.rect(self.utils.screen, WHITE_COLOR, popup_rect)
    pygame.draw.rect(self.utils.screen, (0, 0, 0), popup_rect, 1)

    textRect3 = text3.get_rect()
    textRect3.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50)
    self.utils.screen.blit(text3, textRect3)
    self.setting_list()


  def setting_list(self):
    # setting texts
    if self.setting.is_Vietnamese():
      music_text = 'Âm nhạc: Bật' if self.setting.is_music() else 'Âm nhạc: Tắt'
      language_text = 'Ngôn ngữ: Tiếng Việt'
      save_text = 'Lưu'
    else:
      music_text = 'Music: Enabled' if self.setting.is_music() else 'Music: Disabled'
      language_text = 'Language: English'
      save_text = 'Save'
    
    # render all the texts
    games = [music_text, language_text, save_text]
    texts = [ self.utils.font_setting.render(text, True, (64, 61, 57)) if i != self.setting_selection\
        else self.utils.font_setting.render(text, True, FONT_COLOR) for (i, text) in enumerate(games)]
    
    # text rectangle
    textRects = [text.get_rect() for text in texts]
    textRects[0].midleft = (SCREEN_WIDTH // 3, 350)
    textRects[0].centerx = SCREEN_WIDTH // 2
    textRects[1].midleft = (SCREEN_WIDTH // 3, 400)
    textRects[1].centerx = SCREEN_WIDTH // 2
    textRects[2].midleft = (SCREEN_WIDTH // 3, 450)
    textRects[2].centerx = SCREEN_WIDTH // 2

    # display text on screen
    [self.utils.screen.blit(text, textRect) for text, textRect in zip(texts, textRects)]

  # home screen rendering
  def render(self):
    # fill the screen with white color
    self.utils.screen.fill(WHITE_COLOR)

    # create the text
    if not self.setting.is_Vietnamese():
      text1 = self.utils.font.render('Video Games for Hand Rehabilitation', True, FONT_COLOR)
      text2 = self.utils.font_setting.render('Settings', True, (64, 61, 57))
    else:
      text1 = self.utils.font.render('Trò chơi tập luyện và phục hồi chức năng tay', True, FONT_COLOR)
      text2 = self.utils.font_setting.render('Cài đặt', True, (64, 61, 57))

    # render the text to screen
    textRect1 = text1.get_rect()
    textRect1.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    self.utils.screen.blit(text1, textRect1)

    textRect2 = text2.get_rect()
    textRect2.center = (SCREEN_WIDTH - 100, 50)
    self.utils.screen.blit(text2, textRect2)

    # render setting
    if self.enable_setting:
      self.setting_window()
    else:
      self.game_list()

  def game_list(self):
    # texts
    games = ['1. Shapes and Colors', '2. Eggs and Milk', '3. Dino Run']
    texts = [self.utils.font.render(text, True, (64, 61, 57)) if i != self.selection \
      else self.utils.font.render(text, True, FONT_COLOR) for (i, text) in enumerate(games)]
    # text rectangles
    textRects = [text.get_rect() for text in texts]
    textRects[0].midleft = (SCREEN_WIDTH // 3, 300)
    textRects[1].midleft = (SCREEN_WIDTH // 3, 400)
    textRects[2].midleft = (SCREEN_WIDTH // 3, 500)
    # display text on screen
    [self.utils.screen.blit(text, textRect) for text, textRect in zip(texts, textRects)]

  # process when there is a key pressed
  def process_key(self, key):
    # normal homescreen
    if not self.enable_setting:
      # up, down or enter to select game
      if key == pygame.K_UP:
        self.selection = (self.selection - 1) % 3
      elif key == pygame.K_DOWN:
        self.selection = (self.selection + 1) % 3
      elif key == pygame.K_RETURN:
        return f'game{self.selection + 1}'
      # setting screen
      elif key == pygame.K_p:
        self.enable_setting = not self.enable_setting

    # homescreen with setting window on
    else:
      # move the setting cursor up or down
      if key == pygame.K_UP:
        self.setting_selection = (self.setting_selection - 1) % 3
      elif key == pygame.K_DOWN:
        self.setting_selection = (self.setting_selection + 1) % 3
      # set something in the setting
      elif key == pygame.K_RETURN:
        if self.setting_selection == 0:
          self.setting.set_music()
        elif self.setting_selection == 1:
          self.setting.set_language()
        elif self.setting_selection == 2:
          self.setting_selection = 0
          self.enable_setting = False