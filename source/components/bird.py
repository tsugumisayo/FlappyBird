import pygame
from .. import setup, tools, sound


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = 0
        self.y = 0
        self.load_frames()
        self.fly_timer = 0
        self.float_timer = 0
        self.frame_index = 0
        self.y_vel = 0.4
        self.state = 'float'
        self.dead = False
        self.over = False
        self.sound_played = False
        self.image = self.bird_frames[0]
        self.rect = self.image.get_rect()
        self.gravity = 0.25
        self.mouse_old = pygame.mouse.get_pressed(3)
        self.angel = 0

    def load_frames(self):
        self.bird_blue_up_frame = tools.get_image(setup.GRAPHICS['atlas'], 174, 982, 34, 24)
        self.bird_blue_mid_frame = tools.get_image(setup.GRAPHICS['atlas'], 230, 658, 34, 24)
        self.bird_blue_down_frame = tools.get_image(setup.GRAPHICS['atlas'], 230, 710, 34, 24)

        self.bird_red_up_frame = tools.get_image(setup.GRAPHICS['atlas'], 230, 762, 34, 24)
        self.bird_red_mid_frame = tools.get_image(setup.GRAPHICS['atlas'], 230, 814, 34, 24)
        self.bird_red_down_frame = tools.get_image(setup.GRAPHICS['atlas'], 230, 866, 34, 24)

        self.bird_yellow_up_frame = tools.get_image(setup.GRAPHICS['atlas'], 6, 982, 34, 24)
        self.bird_yellow_mid_frame = tools.get_image(setup.GRAPHICS['atlas'], 62, 982, 34, 24)
        self.bird_yellow_down_frame = tools.get_image(setup.GRAPHICS['atlas'], 118, 982, 34, 24)

        self.bird_blue_frames = [self.bird_blue_up_frame, self.bird_blue_mid_frame, self.bird_blue_down_frame,
                                 self.bird_blue_mid_frame]
        self.bird_red_frames = [self.bird_red_up_frame, self.bird_red_mid_frame, self.bird_red_down_frame,
                                self.bird_red_mid_frame]
        self.bird_yellow_frames = [self.bird_yellow_up_frame, self.bird_yellow_mid_frame, self.bird_yellow_down_frame,
                                   self.bird_yellow_mid_frame]

        if setup.random < 2/3:
            self.bird_frames = self.bird_blue_frames
        elif setup.random > 4/3:
            self.bird_frames = self.bird_red_frames
        else:
            self.bird_frames = self.bird_yellow_frames
        self.bird_size = self.bird_frames[0].get_size()

    def update(self, mouse, level):
        self.rect.x = self.x
        self.rect.y = self.y

        if self.state == 'float':
            if self.float_timer == 0:
                self.float_timer = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.float_timer > 350:
                self.float_timer = pygame.time.get_ticks()
                self.y_vel *= -1


        if self.state == 'fly':
            if mouse[0] and mouse[0] is not self.mouse_old[0] and not self.dead:
                self.y_vel = -5.5
                sound.wing.play()
            self.y_vel += self.gravity

        if not self.dead:
            if self.fly_timer == 0:
                self.fly_timer = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.fly_timer > 100:
                self.fly_timer = pygame.time.get_ticks()
                self.frame_index += 1
                self.frame_index %= 4
            self.image = self.bird_frames[self.frame_index]
            if self.state == 'fly':
                self.cal_angel()
                self.image = pygame.transform.rotate(self.image, self.angel)
            self.y += self.y_vel

        if self.y > level.game_ground_h - level.ground_size[1] - self.image.get_size()[1]:
            self.dead = True
            if not self.sound_played and not level.hit_played:
                sound.hit.play()
                self.sound_played = True

        if self.dead:
            if self.y < level.game_ground_h - level.ground_size[1] - self.image.get_size()[1]:
                self.y += self.y_vel
            if self.angel > -90:
                self.angel -= 3
                self.image = self.bird_frames[self.frame_index]
                self.image = pygame.transform.rotate(self.image, self.angel)
            if self.y > level.game_ground_h - level.ground_size[1] - self.image.get_size()[1] and not self.over:
                self.over = True

        self.mouse_old = mouse

    def cal_angel(self):
        if self.y_vel > 0:
            self.angel = self.y_vel / 10 * -90
        else:
            self.angel = self.y_vel / 7 * -90
        if self.angel > 25:
            self.angel = 25
        elif self.angel < -90:
            self.angel = -90


