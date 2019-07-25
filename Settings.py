import pygame
import Constants


class Text:
    def __init__(self, text, font: pygame.font.Font, parent: pygame.Surface=None, color=(0, 0, 0)):
        self.text = text
        self.color = color
        self.font = font
        self.image = font.render(text, True, color)
        self.image_rect = self.image.get_rect()
        self.parent = parent
        if parent is not None:
            self.parent.add_child(self)

    def __setattr__(self, key, value):
        if key in ('text', 'font', 'color') and hasattr(self, 'font') and self.__dict__[key] != value:
            self.__dict__[key] = value
            self.image = self.font.render(self.text, True, self.color)
            self.image_rect = self.image.get_rect()
        else:
            super().__setattr__(key, value)

    def copy(self):
        t = Text(self.text, self.font, self.parent, self.color)
        t.image_rect.center = self.image_rect.center
        return t

    def __str__(self):
        return 'Text(%s)' % self.text

    def __repr__(self):
        return self.__str__()


class Settings:
    pygame.init()
    #    drag plate
    drag_plate_size = [430, Constants.SCREEN_SIZE[1] // 1.5]
    drag_plate_pos = [Constants.SCREEN_SIZE[1] // 4] * 2
    drag_plate_tile = 101
    drag_plate_bcolor = [55, 115, 155]

    #    buttons of drag plate
    linesize = 10
    drag_button_pos = [linesize / 2] * 2  # [(drag_plate_tile - drag_button_size[1]) // 2] * 2
    drag_button_size = [drag_plate_size[0] - linesize, drag_plate_tile - linesize]
    drag_button_sprite = pygame.transform.scale(pygame.image.load('Sprites/Button.png'), drag_button_size)

    image_pos = [22, 28]

    text_size = 18
    text_font = pygame.font.SysFont('Arial Black', text_size)

    text_name_pos = [20, 7]
    text_level_pos = [75, 42]
    text_factor_pos = [200, 42]
    text_cost_pos = [342, 61]
    level_text = 'ур '

    buy_button_pos = [279, 13]
    buy_button_size = [127, 67]
    buy_button_images = []
    for i in ('p', 'f', 't', 'd'):
        buy_button_images.append(pygame.transform.scale(pygame.image.load('Sprites/bb-%s.png' % i), buy_button_size))
    buy_text = 'купить'
    buy_text_pos = [342, 36]
    buy_text_image = Text(buy_text, text_font, None)
    buy_text_image.image_rect.center = buy_text_pos
    upgrade_text = 'улучшить'
    text_factor_pos[1] += buy_text_image.image_rect.h / 2

