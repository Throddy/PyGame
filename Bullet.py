import pygame
from math import atan2, hypot, degrees
from sprite_groups import *
from images import *


# класс пули
class Bullet(pygame.sprite.Sprite):
    global enemies_firing_range, MC_firing_range

    def __init__(self, MC_coords, mouse_coords, width, height, enemy=''):
        # выбираем кому принадлежит пуля и добавляем в соотв. группу
        if not enemy:
            super().__init__(MCbullet_group, all_sprites)
            self.image = tile_images['MC_bullet']
            self.firing_range = MC_firing_range
        elif enemy == 'Musketeer':
            super().__init__(musketeer_bullet_group, all_sprites)
            self.image = tile_images['MC_bullet']
            self.firing_range = enemies_firing_range
        else:
            super().__init__(magician_bullet_group, all_sprites)
            self.image = tile_images['magician_bullet']
            self.firing_range = enemies_firing_range
        self.image = make_img(self.image, v_width, v_height, MCbullet_width, MCbullet_height)
        self.rect = self.image.get_rect().move(
            MC_coords[0] + MCbullet_width // 5.5, MC_coords[1] + MCbullet_height // 2)
        # высчитываем движение
        self.speed = bullet_def_v
        vx = (mouse_coords[0] * (v_width / width) - MCbullet_width // 2) - MC_coords[0]
        vy = (mouse_coords[1] * (v_height / height) - MCbullet_height // 2) - MC_coords[1]
        dist = hypot(vx, vy)
        self.vx = (vx / dist) * self.speed
        self.vy = (vy / dist) * self.speed

        self.angle = degrees(atan2(-vy, vx))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.dist = 0

    def update(self):  # изменение движения с каждым кадром
        if self.dist > self.firing_range:
            self.kill()
        if not -MCbullet_width <= self.rect.x <= v_width + MCbullet_width or \
                not -MCbullet_height <= self.rect.y <= v_height + MCbullet_height:
            self.kill()
        else:
            self.dist += hypot(self.rect.x - (self.rect.x + self.vx), self.rect.y - (self.rect.y + self.vy))
            self.rect.x += self.vx
            self.rect.y += self.vy
