import pygame
from ..components import bird
from .. import setup, tools
from .. import constants as C


class Menu:
    def __init__(self):
        self.start()

    def start(self):
        self.setup_background()
        self.setup_bird()
        self.setup_button()
        self.finished = False
        self.finishing = False
        self.next = 'level'
        self.finish_timer = 0
        self.ground_x1 = 0
        self.ground_x2 = self.ground_x1 + self.ground_size[0]
        self.ground_vel = 2
        self.button_start_y = self.button_rank_y = self.game_ground_h * 0.6643

    def setup_background(self):
        if setup.random < 1:
            self.background = tools.get_image(setup.GRAPHICS['atlas'], 0, 0, 288, 512)
        else:
            self.background = tools.get_image(setup.GRAPHICS['atlas'], 292, 0, 288, 512)

        self.title = tools.get_image(setup.GRAPHICS['atlas'], 702, 182, 178, 48)
        self.title_size = self.title.get_size()

        self.ground = tools.get_image(setup.GRAPHICS['atlas'], 584, 0, 336, 112)
        self.ground_size = self.ground.get_size()

        self.viewport = setup.SCREEN.get_rect()
        self.game_ground = pygame.Surface((288, 512))
        self.game_ground_w, self.game_ground_h = self.game_ground.get_size()

    def setup_button(self):
        self.button_start = tools.get_image(setup.GRAPHICS['atlas'], 702, 234, 116, 70)
        self.button_start_size = self.button_start.get_size()

        self.button_rank = tools.get_image(setup.GRAPHICS['atlas'], 822, 234, 116, 70)
        self.button_rank_size = self.button_rank.get_size()

    def setup_bird(self):
        self.bird = bird.Bird()
        self.bird.x = (self.game_ground_w - self.bird.image.get_size()[0]) / 2
        self.bird.y = self.game_ground_h * 1.3 / 4 + self.title_size[1]

    def update(self, surface, keys, mouse):
        self.game_ground.blit(self.background, self.viewport)
        self.game_ground.blit(self.title, ((self.game_ground_w - self.title_size[0]) / 2, (self.game_ground_h * 1.2 / 4)))

        self.bird.update(mouse, self)
        self.game_ground.blit(self.bird.image, (self.bird.x, self.bird.y))

        self.update_ground()
        self.game_ground.blit(self.ground, (self.ground_x1, self.game_ground_h - self.ground_size[1]))
        self.game_ground.blit(self.ground, (self.ground_x2, self.game_ground_h - self.ground_size[1]))

        self.update_button(mouse, surface)
        self.game_ground.blit(self.button_start, (self.game_ground_w / 18, self.button_start_y))
        self.game_ground.blit(self.button_rank, (self.game_ground_w * 17 / 18 - self.button_rank_size[0], self.button_rank_y))

        self.finish(self.game_ground)

        surface.blit(tools.change_multi(self.game_ground), (0, 0))

    def update_ground(self):
        self.ground_x1 -= self.ground_vel
        self.ground_x2 -= self.ground_vel
        if self.ground_x1 < -self.ground_size[0] - self.ground_vel:
            self.ground_x1 = self.ground_x2 + self.ground_size[0]
        if self.ground_x2 < -self.ground_size[0] - self.ground_vel:
            self.ground_x2 = self.ground_x1 + self.ground_size[0]

    def update_button(self, mouse, surface):
        if mouse[0]:
            if C.SCREEN_W / 18 < pygame.mouse.get_pos()[0] < C.SCREEN_W / 18 + self.button_start_size[0]*C.MULTI and self.button_start_y*C.MULTI < pygame.mouse.get_pos()[1] < self.button_start_y*C.MULTI + self.button_start_size[1]*C.MULTI:
                self.button_start_y = self.game_ground_h * 0.668
                if not self.finishing:
                    self.finishing = True
                    self.next = 'level'
            if C.SCREEN_W * 17 / 18 - self.button_rank_size[0]*C.MULTI < pygame.mouse.get_pos()[0] < C.SCREEN_W * 17 / 18 + self.button_start_size[0] and self.button_rank_y*C.MULTI < pygame.mouse.get_pos()[1] < self.button_rank_y*C.MULTI + self.button_start_size[1]*C.MULTI:
                self.button_rank_y = self.game_ground_h * 0.668
                if not self.finishing:
                    self.finishing = True
                    self.next = 'rank'
        elif not mouse[0]:
            self.button_start_y = self.button_rank_y = self.game_ground_h * 0.6643

    def finish(self, surface):
        if self.finishing:
            if self.finish_timer == 0:
                self.finish_timer = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - self.finish_timer < 510:
                    black = pygame.Surface((self.game_ground_w, self.game_ground_h))
                    black = black.convert_alpha()
                    black.fill((0, 0, 0, int((pygame.time.get_ticks() - self.finish_timer) / 2)))
                    self.game_ground.blit(black, (0, 0))
                else:
                    self.game_ground.fill((0, 0, 0, 255))
                    self.finished = True
