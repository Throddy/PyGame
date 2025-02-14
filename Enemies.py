import pygame, os, sys, csv
from fractions import Fraction
from random import randint
from random import choice as ch
from PIL import Image
from math import atan2, hypot, degrees

from Bullet import Bullet
from sprite_groups import *
from images import *
from settings import *
from sounds import *
from stat_functions import *


class Villager(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.load_animation(pos_x, pos_y, villager_media)
        self.hp = Vil_hp
        self.hit = False

    def load_animation(self, pos_x, pos_y, media):
        self.frames_amount = len(media['moving'])
        self.frames = {'l': media['moving'],
                       'lh': media['moving_h'],
                       'r': list(map(lambda pic:
                                     pygame.transform.flip(pic, True, False),
                                     media['moving'])),
                       'rh': list(map(lambda pic:
                                      pygame.transform.flip(pic, True, False),
                                      media['moving_h']))}
        self.cur_frame = 0
        self.frame_delay = 15
        self.time_counter = 0
        self.save_dir = 'r'
        self.image = make_img(self.frames[self.save_dir][0], v_width, v_height, UNIT_width, UNIT_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.prev_direction = ''

    def update(self, x2, y2, norm_v=3 / (2 ** 0.5)):
        if self.hp <= 0:
            self.kill()
            if non_stop_mode_flag:
                review_stats(stat_file_name, self, killed=True)

        if pygame.sprite.spritecollide(self, MCbullet_group, dokill=True):
            self.hit = True
            self.hp -= MC_damage

        x1, y1 = self.rect.x, self.rect.y

        perp_x = x2 - x1
        perp_y = y2 - y1

        dist = (perp_x ** 2 + perp_y ** 2) ** 0.5
        if dist != 0:
            vx = (perp_x / dist) * norm_v
            vy = (perp_y / dist) * norm_v
            if not (pygame.sprite.spritecollideany(self, MCbullet_group)):
                self.rect = self.rect.move(vx, vy)

        l, r, f, d = '', '', '', ''
        if perp_y > 0:
            d = 'd'
        if perp_y < 0:
            f = 'f'
        if perp_x > 0:
            l = 'l'
        if perp_x < 0:
            r = 'r'
        cur_direction = l + r + f + d

        self.time_counter += 1
        if self.time_counter >= self.frame_delay:
            self.cur_frame = (self.cur_frame + 1) % self.frames_amount
            if cur_direction not in 'fd ':
                self.image = make_img(self.frames[cur_direction[0] + ('h' if self.hit else '')][self.cur_frame],
                                      v_width, v_height, UNIT_width, UNIT_height)
            else:
                if cur_direction in 'fd':
                    if self.prev_direction not in 'fd ':  # не пауза фд == норм двиэ
                        self.save_dir = self.prev_direction
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              v_width, v_height, UNIT_width, UNIT_height)
                    elif self.prev_direction not in ' ':  # == fd
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              v_width, v_height, UNIT_width, UNIT_height)
                    else:
                        self.cur_frame = 0
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              v_width, v_height, UNIT_width, UNIT_height)
                else:
                    self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][0], v_width,
                                          v_height, UNIT_width, UNIT_height)
            self.prev_direction = cur_direction
            self.time_counter = 0
            self.hit = False


class Musketeer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.shot_freq = musketeer_firing_delay
        self.load_animation(pos_x, pos_y, musketeer_media)
        self.hp = Musk_hp
        self.hit = False

    def load_animation(self, pos_x, pos_y, media):
        self.frames_amount = len(media['moving'])
        self.frames = {'l': media['moving'],
                       'lh': media['moving_h'],
                       'r': list(map(lambda pic:
                                     pygame.transform.flip(pic, True, False),
                                     media['moving'])),
                       'rh': list(map(lambda pic:
                                      pygame.transform.flip(pic, True, False),
                                      media['moving_h']))}
        self.cur_frame = 0
        self.frame_delay = 15
        self.time_counter = 0
        self.shot_counter = 0
        self.save_dir = 'r'
        self.image = make_img(self.frames[self.save_dir][0], v_width, v_height, UNIT_width, UNIT_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.prev_direction = ''

    def update(self, x2, y2, norm_v=3 / (2 ** 0.5)):
        if self.hp <= 0:
            self.kill()
            if non_stop_mode_flag:
                review_stats(stat_file_name, self, killed=True)

        if pygame.sprite.spritecollide(self, MCbullet_group, dokill=True):
            self.hit = True
            self.hp -= MC_damage

        x1, y1 = self.rect.x, self.rect.y

        perp_x = x2 - x1
        perp_y = y2 - y1

        dist = (perp_x ** 2 + perp_y ** 2) ** 0.5

        self.shot(x2, y2, dist)

        if dist != 0:
            vx = (perp_x / dist) * norm_v
            vy = (perp_y / dist) * norm_v
            if pygame.sprite.spritecollideany(self, MCbullet_group):
                pygame.sprite.spritecollide(self, MCbullet_group, dokill=True)
                self.kill()
            else:
                self.rect = self.rect.move(vx, vy)
        self.animation(perp_x, perp_y)

    def animation(self, perp_x, perp_y):
        l, r, f, d = '', '', '', ''
        if perp_y > 0:
            d = 'd'
        if perp_y < 0:
            f = 'f'
        if perp_x > 0:
            l = 'l'
        if perp_x < 0:
            r = 'r'
        cur_direction = l + r + f + d

        self.time_counter += 1
        if self.time_counter >= self.frame_delay:
            self.cur_frame = (self.cur_frame + 1) % self.frames_amount
            if cur_direction not in 'fd ':
                self.image = make_img(self.frames[cur_direction[0] + ('h' if self.hit else '')][self.cur_frame],
                                      v_width, v_height, UNIT_width, UNIT_height)
            else:
                if cur_direction in 'fd':
                    if self.prev_direction not in 'fd ':  # не пауза фд == норм движ
                        self.save_dir = self.prev_direction
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              v_width, v_height, UNIT_width, UNIT_height)
                    elif self.prev_direction not in ' ':  # == fd
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              v_width, v_height, UNIT_width, UNIT_height)
                    else:
                        self.cur_frame = 0
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              v_width, v_height, UNIT_width, UNIT_height)
                else:
                    self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][0], v_width,
                                          v_height, UNIT_width, UNIT_height)
            self.prev_direction = cur_direction
            self.time_counter = 0
            self.hit = False

    def shot(self, x2, y2, dist):
        self.shot_counter += 1
        x1, y1 = self.rect.x, self.rect.y
        if dist < 1000 and self.shot_counter >= self.shot_freq:
            self.shot_counter = 0
            Bullet((x1, y1), (x2, y2), 'Musketeer')
            musket_snd.play()


class Magician(Musketeer):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.load_animation(pos_x, pos_y, magician_media)
        self.hp = Mag_hp

    def shot(self, x2, y2, dist):
        self.shot_counter += 1
        x1, y1 = self.rect.x, self.rect.y
        if dist < 1000 and self.shot_counter >= self.shot_freq:
            self.shot_counter = 0
            Bullet((x1, y1), (x2, y2), 'Magician')
            spell_snd.play()