import pygame


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        font,
        enabled=True
    ):
        self.rect = pygame.Rect(x, y, width, height)

        self.text = text
        self.font = font

        self.enabled = enabled

        self.normal_color = (60, 60, 60)
        self.hover_color = (90, 90, 90)
        self.disabled_color = (40, 40, 40)

        self.text_color = (240, 240, 240)
        self.disabled_text_color = (120, 120, 120)

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()

        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        if not self.enabled:
            color = self.disabled_color
        elif self.is_hovered():
            color = self.hover_color
        else:
            color = self.normal_color

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=12
        )

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color if self.enabled else self.disabled_text_color
        )

        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def clicked(self, event):
        if not self.enabled:
            return False

        return (
            event.type == pygame.MOUSEBUTTONDOWN and
            event.button == 1 and
            self.is_hovered()
        )