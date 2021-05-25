import pygame
import sys
import os
from . import constants as C
import random


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed(3)
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start()
        self.state.update(self.screen, self.keys, self.mouse)

    def run(self):
        while True:
            from . import setup
            setup.random = random.randint(0, 2)
            for event in pygame.event.get(pygame.VIDEORESIZE):
                C.SCREEN_W = event.size[0]
                C.SCREEN_H = int(C.SCREEN_W * 512 / 288)
                C.SCREEN_SIZE = C.SCREEN_W, C.SCREEN_H
                C.MULTI = C.SCREEN_W / 288
                setup.SCREEN = pygame.display.set_mode(C.SCREEN_SIZE, pygame.RESIZABLE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse = pygame.mouse.get_pressed(5)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse = pygame.mouse.get_pressed(5)

            self.update()
            pygame.display.update()
            self.clock.tick(C.FPS)


def load_graphics(path, accept=('.ipg', '.png', '.bmp', '.gif')):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


def get_image(sheet, x, y, width, height, colorkey=None, scale=1):
    image = pygame.Surface((width, height))
    image.set_colorkey((0, 0, 0))
    area = pygame.Rect(x, y, width, height)
    image.blit(sheet, (0, 0), area)
    if colorkey is not None:
        image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image


def get_font():
    from . import setup
    font_big = {'0': get_image(setup.GRAPHICS['atlas'], 992, 120, 24, 36, None, C.MULTI),
                '1': get_image(setup.GRAPHICS['atlas'], 272, 910, 16, 36, None, C.MULTI),
                '2': get_image(setup.GRAPHICS['atlas'], 584, 320, 24, 36, None, C.MULTI),
                '3': get_image(setup.GRAPHICS['atlas'], 612, 320, 24, 36, None, C.MULTI),
                '4': get_image(setup.GRAPHICS['atlas'], 640, 320, 24, 36, None, C.MULTI),
                '5': get_image(setup.GRAPHICS['atlas'], 668, 320, 24, 36, None, C.MULTI),
                '6': get_image(setup.GRAPHICS['atlas'], 584, 368, 24, 36, None, C.MULTI),
                '7': get_image(setup.GRAPHICS['atlas'], 612, 368, 24, 36, None, C.MULTI),
                '8': get_image(setup.GRAPHICS['atlas'], 640, 368, 24, 36, None, C.MULTI),
                '9': get_image(setup.GRAPHICS['atlas'], 668, 368, 24, 36, None, C.MULTI)}
    font_small = {'0': get_image(setup.GRAPHICS['atlas'], 276, 646, 12, 14, None, C.MULTI),
                  '1': get_image(setup.GRAPHICS['atlas'], 282, 664, 6, 14, None, C.MULTI),
                  '2': get_image(setup.GRAPHICS['atlas'], 276, 698, 12, 14, None, C.MULTI),
                  '3': get_image(setup.GRAPHICS['atlas'], 276, 716, 12, 14, None, C.MULTI),
                  '4': get_image(setup.GRAPHICS['atlas'], 276, 750, 12, 14, None, C.MULTI),
                  '5': get_image(setup.GRAPHICS['atlas'], 276, 768, 12, 14, None, C.MULTI),
                  '6': get_image(setup.GRAPHICS['atlas'], 276, 802, 12, 14, None, C.MULTI),
                  '7': get_image(setup.GRAPHICS['atlas'], 276, 820, 12, 14, None, C.MULTI),
                  '8': get_image(setup.GRAPHICS['atlas'], 276, 854, 12, 14, None, C.MULTI),
                  '9': get_image(setup.GRAPHICS['atlas'], 276, 872, 12, 14, None, C.MULTI)}
    return {'big': font_big, 'small': font_small}


def change_multi(img):
    width, height = img.get_size()
    img = pygame.transform.scale(img, (int(C.MULTI * width), int(C.MULTI * height)))
    return img


def creat_labels(label, font, colorkey=(0, 0, 0)):
    totalWidth = 0
    totalHeight = 0
    x_location = 0
    for letter in list(label):
        totalWidth += (font[letter].get_width() + 2)
        if font[letter].get_height() > totalHeight:
            totalHeight = font[letter].get_height()
    label_image = pygame.Surface((totalWidth, totalHeight))
    for letter in list(label):
        label_image.blit(font[letter], (x_location, 0))
        x_location += (font[letter].get_width() + 2)
    label_image.set_colorkey(colorkey)
    return label_image


def get_rank():
    rank = open("./resources/rank.txt", "r+")
    rank_str = rank.read()
    rank_list = rank_str.split('\n')
    for i in range(len(rank_list)):
        rank_list[i] = int(rank_list[i])
    return rank_list


def update_rank(rank_list, mark):
    rank = open("./resources/rank.txt", "r+")
    if mark > rank_list[9]:
        rank_list[9] = mark
        rank_list.sort(reverse=True)
        rank_list = rank_list
        for i in range(len(rank_list)-1):
            rank.write(str(rank_list[i]))
            rank.write("\n")
        rank.write(str(rank_list[9]))
