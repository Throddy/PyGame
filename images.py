import pygame
import os
import sys
from settings import *


# функция загрузки изображения(для создания фрэймов обьектов) и впринципе загруженных анимация в игре
def load_image(name, colorkey=None):
    fullname = os.path.join(f'data/{name}')
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# изменяет размер изображения под размеры экрана в данный момент
def make_img(img, w, h, persW, persH):
    return pygame.transform.scale(img, (w // (w // persW), h // (h // persH)))


# все загруженные анимации в игре
tile_images = {
    'tree': load_image(r'game/water.png'),
    'MC_bullet': load_image(r'game/Bullet.png'),
    'magician_bullet': load_image(r'game/magic_bullet.png')}

player_media = {'moving': [load_image(f'/game/horse/horse_{i}.png') for i in range(6)],
                'moving_h': [load_image(f'/game/horse_hit/horse_hit_{i}.png') for i in range(6)]}
villager_media = {'moving': [load_image(f'/game/enemy/villager/sprite_{i}.png') for i in range(4)],
                  'moving_h': [load_image(f'/game/enemy/villager/villager_hit_{i}.png') for i in range(4)]}
musketeer_media = {'moving': [load_image(f'/game/enemy/musketeer/musketeer{i}.png') for i in range(4)],
                   'moving_h': [load_image(f'/game/enemy/musketeer/musketeer_hit_{i}.png') for i in range(4)]}
magician_media = {'moving': [load_image(f'/game/enemy/magician/magician_{i}.png') for i in range(2)],
                  'moving_h': [load_image(f'/game/enemy/magician/magician_hit_{i}.png') for i in range(2)]}
enemy_images = {'moving': [load_image(r'game/enemy/EK.png')],
                'moving_h': [load_image(r'game/enemy/EK.png')]}
background = pygame.transform.scale(load_image(r'game/road.png'), (v_width, v_height))
