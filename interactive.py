import pygame
from sprite_groups import button_group, all_sprites, cursor_group, player_group
from images import load_image
from settings import v_width, v_height


# класс кнопки
class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, x, y, size, size2):
        super().__init__(button_group, all_sprites)
        self.size = size
        self.WIDTH, self.HEIGHT = size2
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.X, self.Y = x, y

    def set_image(self, way):
        self.way = way
        self.image = load_image(way)
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.rect = self.image.get_rect().move(self.pos_x + 15, self.pos_y + 5)

    def update(self):
        # нажатие кнопки
        if pygame.sprite.spritecollideany(self, cursor_group):
            self.set_image(self.way[:-5] + '1.png')
        else:
            self.set_image(self.way[:-5] + '0.png')

    # изменение размеров обьекта при изменении размеров окна
    def resize(self, width, height):
        global v_width, v_height
        new_W, new_H = self.WIDTH * (width / v_width), self.HEIGHT * (height / v_height)
        self.image = pygame.transform.scale(self.image, (new_W, new_H))
        self.pos_x, self.pos_y = self.X * (width / v_width), self.Y * (height / v_height)
        self.rect = self.image.get_rect().move(self.pos_x + 15, self.pos_y + 5)


# собственный курсор
class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image('/start_screen/cursor.png')
        self.rect = self.image.get_rect()
