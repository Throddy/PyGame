import pygame, os, sys, csv
from fractions import Fraction
from random import randint
from random import choice as ch
from PIL import Image
from math import atan2, hypot, degrees

from sprite_groups import *
from images import player_media, make_img
from settings import *
from sounds import *
from stat_functions import *


class Player(pygame.sprite.Sprite):
    global bad_end_flag

    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.frames_amount = len(player_media['moving'])
        self.frames = {'l': player_media['moving'],
                       'r': list(map(lambda pic:
                                     pygame.transform.flip(pic, True, False),
                                     player_media['moving'])),
                       'lh': player_media['moving_h'],
                       'rh': list(map(lambda pic:
                                      pygame.transform.flip(pic, True, False),
                                      player_media['moving_h']))
                       }
        self.cur_frame = 0
        self.frame_delay = 8
        self.time_counter = 0
        self.save_dir = 'r'
        self.image = make_img(self.frames[self.save_dir][0], v_width, v_height, UNIT_width, UNIT_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.prev_direction = ''
        self.hp = MC_hp
        self.hit = False
        self.time = 0

    def update(self, keys, vx=0, vy=0):
        global bad_end_flag
        if self.time.denominator == 1 and non_stop_mode_flag:
            review_stats(stat_file_name, time_ticked=True)
        if self.hp <= 0:
            bad_end_flag = True
            self.kill()
            if non_stop_mode_flag:
                return
        if pygame.sprite.spritecollide(self, musketeer_bullet_group, dokill=True):
            self.hit = True
            ouch_snd.play()
            self.hp -= Musk_damage
        if pygame.sprite.spritecollide(self, magician_bullet_group, dokill=True):
            self.hit = True
            ouch_snd.play()
            self.hp -= Mag_damage
        if pygame.sprite.spritecollideany(self, enemy_group) and self.time >= v_damage_delay:
            self.hit = True
            ouch_snd.play()
            self.hp -= Vil_damage
            self.time = 0

        l, r, f, d = '', '', '', ''
        if not keys[pygame.K_SPACE]:
            if keys[pygame.K_a]:
                vx = -mc_def_v
                l = 'l'
            if keys[pygame.K_d]:
                vx = mc_def_v
                r = 'r'
            if keys[pygame.K_w]:
                vy = -mc_def_v
                f = 'f'
            if keys[pygame.K_s]:
                vy = mc_def_v
                d = 'd'

            cur_direction = l + r + f + d

            if abs(vx) == abs(vy) == mc_def_v:
                vx = vx / (2 ** 0.5) + 1
                vy = vy / (2 ** 0.5) + 1

            self.rect.x += vx
            if pygame.sprite.spritecollideany(self, trees_group):
                self.rect.x -= vx
                vx = 0

            self.rect.y += vy
            if pygame.sprite.spritecollideany(self, trees_group):
                self.rect.y -= vy
                vy = 0

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
                            self.image = make_img(
                                self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame], v_width,
                                v_height, UNIT_width, UNIT_height)
                        elif self.prev_direction not in ' ':  # == fd
                            self.image = make_img(
                                self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame], v_width,
                                v_height, UNIT_width, UNIT_height)
                        else:
                            self.cur_frame = 0
                            self.image = make_img(
                                self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame], v_width,
                                v_height, UNIT_width, UNIT_height)
                    else:
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][0], v_width,
                                              v_height, UNIT_width, UNIT_height)
                self.prev_direction = cur_direction
                self.time_counter = 0
                self.hit = False

        else:
            self.rect.x, self.rect.y = v_width // 2, v_height // 2
        self.time += Fraction(1, FPS)
