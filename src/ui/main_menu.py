import pygame

from game import GameConfig
from ui.button import Button


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.title_font = pygame.font.SysFont(None, 72)
        self.button_font = pygame.font.SysFont(None, 42)
        self.small_font = pygame.font.SysFont(None, 28)

        center_x = screen_width // 2

        button_width = 320
        button_height = 60

        spacing = 20

        start_y = 220

        self.two_player_button = Button(
            center_x - button_width // 2,
            start_y,
            button_width,
            button_height,
            "2 Players",
            self.button_font
        )

        self.four_player_button = Button(
            center_x - button_width // 2,
            start_y + (button_height + spacing),
            button_width,
            button_height,
            "4 Players",
            self.button_font
        )

    def draw(self, screen):
        screen.fill((24, 24, 24))

        title_surface = self.title_font.render(
            "Quoridor",
            True,
            (240, 240, 240)
        )

        title_rect = title_surface.get_rect(
            center=(screen.get_width() // 2, 110)
        )

        screen.blit(title_surface, title_rect)

        subtitle_surface = self.small_font.render(
            "Select a game mode",
            True,
            (180, 180, 180)
        )

        subtitle_rect = subtitle_surface.get_rect(
            center=(screen.get_width() // 2, 160)
        )

        screen.blit(subtitle_surface, subtitle_rect)

        self.two_player_button.draw(screen)
        self.four_player_button.draw(screen)

    def handle_event(self, event):
        if self.two_player_button.clicked(event):
            config = GameConfig(
                player_count=2
            )
            return config

        if self.four_player_button.clicked(event):
            config = GameConfig(
                player_count=4
            )
            return config

        return None