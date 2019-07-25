import pygame
import Constants
from Settings import Settings
from images import *
from Nodes import *


def load_images(filename):
    all_images = []
    for line in open('data/%s/images.txt' % filename, 'r').readlines()[2:]:
        name, cost, factor = line[:-1].split('/')
        cost, factor = Long(cost), Long(factor)
        all_images.append(
            ButtonImage(Settings.drag_button_sprite, Settings.drag_button_pos, Settings.drag_button_size, name, cost,
                        factor))
    return all_images


class Globals:
    screen = pygame.display.set_mode(Constants.SCREEN_SIZE)
    timer = pygame.time.Clock()

    #    buttons' images
    # energy_images = load_images('energy')
    miners_images = load_images('miners')
    # ships_images = load_images('ships')
