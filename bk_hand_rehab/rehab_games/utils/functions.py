import pygame
from rehab_games.utils.constants import *

def paused(screen, enable_Vie_language):
  selection = 0
  option_list(selection, screen, enable_Vie_language)
  while pause:
      for event in pygame.event.get():
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_DOWN:
                  selection = (selection + 1) % 2
                  option_list(selection, screen, enable_Vie_language)
              elif event.key == pygame.K_UP:
                  selection = (selection - 1) % 2
                  option_list(selection, screen, enable_Vie_language)
              elif event.key == pygame.K_RETURN:
                  return selection

def replay_or_return(selection, screen, enable_Vie_language):
    popup_width, popup_height = 800, 180
    popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
    popup_surface.fill((211, 211, 211, 0))  # set alpha to 0
    font_popup_text = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)
    if not enable_Vie_language:
        options = ['Replay', 'Home']
    else:
        options = ['Chơi lại', 'Quay lại màn hình chính']
    texts = [font_popup_text.render(text, True, DEFAULT_COLOR) if i != selection else font_popup_text.render(text, True,
                                                                                                             FONT_COLOR)
             for (i, text) in enumerate(options)]
    textRects = [text.get_rect() for text in texts]

    textRects[0].centerx = popup_surface.get_rect().centerx
    textRects[0].top = 0
    textRects[1].centerx = popup_surface.get_rect().centerx
    textRects[1].top = 40
    [popup_surface.blit(text, textRect) for text, textRect in zip(texts, textRects)]

    popup_rect = popup_surface.get_rect()
    popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

    screen.blit(popup_surface, popup_rect)
    pygame.display.update()

def pause_screen(selection, screen, enable_Vie_language, alpha=255):
  popup_width, popup_height = 800, 180
  popup_surface = pygame.Surface((popup_width, popup_height), pygame.SRCALPHA)
  popup_surface.fill((211, 211, 211, alpha))  # set alpha to 0
  font_popup = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 40)
  font_popup_text = pygame.font.Font('rehab_games/Be_Vietnam_Pro/BeVietnamPro-Black.ttf', 30)

  text_surface = font_popup.render("Game Paused", True, (255, 99, 71))
  
  if not enable_Vie_language:
    text_surface = font_popup.render("Game Paused", True, (255, 99, 71))
    options = ['Continue', 'Home']
  else:
    text_surface = font_popup.render("Trò chơi tạm dừng", True, (255, 99, 71))
    options = ['Tiếp tục', 'Quay lại màn hình chính']

  text_rect = text_surface.get_rect()
  text_rect.centerx = popup_surface.get_rect().centerx
  text_rect.top = 20
  popup_surface.blit(text_surface, text_rect)

  texts = [font_popup_text.render(text, True, DEFAULT_COLOR) if i != selection \
    else font_popup_text.render(text, True, FONT_COLOR) for (i, text) in enumerate(options)]
  textRects = [text.get_rect() for text in texts]

  textRects[0].centerx = popup_surface.get_rect().centerx
  textRects[0].top = 80
  textRects[1].centerx = popup_surface.get_rect().centerx
  textRects[1].top = 120
  [popup_surface.blit(text, textRect) for text, textRect in zip(texts, textRects)]

  popup_rect = popup_surface.get_rect()
  popup_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)

  screen.blit(popup_surface, popup_rect)
  pygame.display.update()
