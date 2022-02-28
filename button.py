import pygame.font

class Button:
    
    def __init__(self, screen, msg, x, y):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("other\\ARCADECLASSIC.TTF", 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _check_button(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)