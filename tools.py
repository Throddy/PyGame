import pygame
import sys
from random import randint
from sprite_groups import trees_group, all_sprites
from settings import tree_width, tree_height, v_width, v_height
from images import (tile_images, make_img, Ntrees_horz, Ntrees_vert, MC_hp, Vil_hp, Mag_hp, Musk_hp, BAR_LENGTH,
                    BAR_HEIGHT, virtual_surface)
from Enemies import Villager, Musketeer, Magician
from MainCharacter import Player


# класс дерева(барьер)
class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(trees_group, all_sprites)
        self.width, self.height = tree_width, tree_height
        self.cur_img = tile_images['tree']
        self.image = make_img(self.cur_img, v_width, v_height, self.width, self.height)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


# автоматическое создание барьеров
def generate_borders(w, h):
    for sprite in trees_group:
        sprite.kill()

    horz_step = max(1, (w - tree_width) // (Ntrees_horz - 1))
    for i in range(Ntrees_horz):
        Tree(i * horz_step, 0)
        Tree(i * horz_step, h - tree_height)

    vert_step = max(1, (h - tree_height) // (Ntrees_vert - 1))
    for i in range(Ntrees_vert):
        Tree(0, i * vert_step)
        Tree(w - tree_width, i * vert_step)


# генерация врагов в случайных позициях
def generate_enemies(n, enemy, mode=False):
    for _ in range(n):
        side = randint(1, 4)
        if side == 1:
            enemy(0, randint(0, v_height), mode)
        elif side == 2:
            enemy(randint(0, v_width), 0, mode)
        elif side == 4:
            enemy(v_width, randint(0, v_height), mode)
        else:
            enemy(randint(0, v_width), v_height, mode)


# отрисовка шкалы здоровья действующих персонажей
def draw_hp_bar(self, x, y, cur_hp):
    if type(self) is Villager:
        color1, color2 = 'purple', 'black'
        hp = Vil_hp
    elif type(self) is Musketeer:
        color1, color2 = 'pink', 'black'
        hp = Musk_hp
    elif type(self) is Magician:
        color1, color2 = 'red', 'black'
        hp = Mag_hp
    elif type(self) is Player:
        color1, color2 = 'green', 'white'
        hp = MC_hp

    outline_rect = pygame.Rect(x, y - BAR_HEIGHT * 2, BAR_LENGTH, BAR_HEIGHT)
    cur_hp = (cur_hp / hp) * BAR_LENGTH
    fill_rect = pygame.Rect(x, y - BAR_HEIGHT * 2, cur_hp, BAR_HEIGHT)
    pygame.draw.rect(virtual_surface, color1, fill_rect)
    pygame.draw.rect(virtual_surface, color2, outline_rect, 1)


def terminate():
    pygame.quit()
    sys.exit()
