import pygame, os, sys
from random import randint
from PIL import Image
from math import atan2, hypot, degrees

pygame.init()
pygame.display.set_caption('Walking')
size = width, height = 1400, 800
min_width, min_height = 1200, 700
screen = pygame.display.set_mode(size, pygame.RESIZABLE, pygame.FULLSCREEN)


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


def convert_gif(name):
    path = os.path.join(f'data/{name}')  # Заменил \ на / для кроссплатформенности
    if not os.path.isfile(path):
        print(f"Файл с изображением '{path}' не найден")
        sys.exit()

    gif = Image.open(path)
    frames = []

    # Определяем прозрачный цвет (если есть)
    transparent_color = None
    if gif.info.get("transparency") is not None:
        transparent_color = gif.info["transparency"]

    while True:
        frame = gif.convert("RGBA")  # Преобразуем в RGBA

        # Создаем новое изображение с прозрачностью
        new_frame = Image.new("RGBA", frame.size, (0, 0, 0, 0))

        # Копируем пиксели, игнорируя фон
        for x in range(frame.width):
            for y in range(frame.height):
                pixel = frame.getpixel((x, y))
                if transparent_color is None or pixel[:3] != (transparent_color, transparent_color, transparent_color):
                    new_frame.putpixel((x, y), pixel)

        # Преобразуем в Pygame-совместимый формат
        pygame_frame = pygame.image.fromstring(new_frame.tobytes(), new_frame.size, "RGBA")
        frames.append(pygame_frame)

        try:
            gif.seek(gif.tell() + 1)
        except EOFError:
            break

    return frames


"""
def load_level(filename):
    filename = "data/game/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('tree', x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y
"""


# test


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)

    title = Button(410, 10, (550, 120))
    title.set_image('start_screen/title/title_0.png')

    start_button = Button(500, 200, (350, 100))
    start_button.set_image('start_screen/startbutton/sprite_0.png')

    exit_button = Button(500, 350, (350, 100))
    exit_button.set_image('start_screen/exitbutton/exitbutton_0.png')

    non_stop_button = Button(500, 500, (350, 100))
    non_stop_button.set_image('start_screen/nonstopbutton/nonstop_0.png')

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(load_image('/start_screen/start_background.png'), (width, height))
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        return
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()

            if event.type == pygame.MOUSEMOTION:
                cords = event.pos
                flag = pygame.mouse.get_focused()
                cursor.rect.x, cursor.rect.y = cords
        button_group.update()
        button_group.draw(screen)
        if flag:
            cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def comic():
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)
    start_button = Button(0, 700, (300, 80))
    start_button.set_image('start_screen/startbutton/sprite_0.png')

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(load_image('start_screen/comic.png'), (width, height))
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        return

            if event.type == pygame.MOUSEMOTION:
                cords = event.pos
                flag = pygame.mouse.get_focused()
                cursor.rect.x, cursor.rect.y = cords
        button_group.update()
        button_group.draw(screen)
        if flag:
            cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def bad_end():
    global cur_wave
    button_group.empty()
    cursor_group.empty()
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)
    start_button = Button(300, 600, (350, 100))
    start_button.set_image('start_screen/startbutton/sprite_0.png')

    exit_button = Button(700, 600, (350, 100))
    exit_button.set_image('start_screen/exitbutton/exitbutton_0.png')

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(load_image('start_screen/game_over.jpeg'), (width, height))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        cur_wave = 0
                        return
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()

            if event.type == pygame.MOUSEMOTION:
                cords = event.pos
                flag = pygame.mouse.get_focused()
                cursor.rect.x, cursor.rect.y = cords
        button_group.update()
        button_group.draw(screen)
        if flag:
            cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def final_screen():
    outro_text = ["Окочание",
                  "Спасибо за тестирование игры.",
                  "Покедава!"]
    screen.fill('white')
    fon = pygame.transform.scale(load_image('fon2.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in outro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        outro_rect = string_rendered.get_rect()
        text_coord += 30
        outro_rect.top = text_coord
        outro_rect.x = 30
        text_coord += outro_rect.height
        screen.blit(string_rendered, outro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def make_img(img, w, h, persW, persH):
    return pygame.transform.scale(img, (w // (w // persW), h // (h // persH)))


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(trees_group, all_sprites)
        self.width, self.height = tree_width, tree_height
        self.cur_img = tile_images['tree']
        self.image = make_img(self.cur_img, width, height, self.width, self.height)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)

    def resize(self, SW, SH):
        global tree_width, tree_height, width, height
        new_W, new_H = self.width * (SW / width), self.height * (SH / height)
        self.image = pygame.transform.scale(self.cur_img,
                                            (new_W, new_H))
        tree_width, tree_height = new_W, new_H


class Player(pygame.sprite.Sprite):
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
        self.image = make_img(self.frames[self.save_dir][0], width, height, UNIT_width, UNIT_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.prev_direction = ''
        self.hp = MC_hp
        self.hit = False
        self.time = 0

    def resize(self, SW, SH):
        global UNIT_width, UNIT_height, width, height
        new_W, new_H = UNIT_width * (SW / width), UNIT_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        UNIT_width, UNIT_height = new_W, new_H

    def update(self, keys, vx=0, vy=0):
        global bad_end_flag
        if self.hp <= 0:
            bad_end_flag = True
            self.kill()
        if pygame.sprite.spritecollide(self, musketeer_bullet_group, dokill=True):
            self.hit = True
            self.hp -= Musk_damage
        if pygame.sprite.spritecollide(self, magician_bullet_group, dokill=True):
            self.hit = True
            self.hp -= Mag_damage
        if pygame.sprite.spritecollideany(self, enemy_group) and self.time >= v_damage_delay:
            self.hit = True
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
                                          width, height, UNIT_width, UNIT_height)
                else:
                    if cur_direction in 'fd':
                        if self.prev_direction not in 'fd ':  # не пауза фд == норм двиэ
                            self.save_dir = self.prev_direction
                            self.image = make_img(
                                self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame], width,
                                height, UNIT_width, UNIT_height)
                        elif self.prev_direction not in ' ':  # == fd
                            self.image = make_img(
                                self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame], width,
                                height, UNIT_width, UNIT_height)
                        else:
                            self.cur_frame = 0
                            self.image = make_img(
                                self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame], width,
                                height, UNIT_width, UNIT_height)
                    else:
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][0], width,
                                              height, UNIT_width, UNIT_height)
                self.prev_direction = cur_direction
                self.time_counter = 0
                self.hit = False

        else:
            self.rect.x, self.rect.y = width // 2, height // 2
        self.time += 1


class Bullet(pygame.sprite.Sprite):
    global enemies_firing_range, MC_firing_range

    def __init__(self, MC_coords, mouse_coords, enemy=''):
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
        self.image = make_img(self.image, width, height, MCbullet_width, MCbullet_height)
        self.rect = self.image.get_rect().move(
            MC_coords[0] + MCbullet_width // 5.5, MC_coords[1] + MCbullet_height // 2)

        self.speed = bullet_def_v
        vx = (mouse_coords[0] - MCbullet_width // 2) - MC_coords[0]
        vy = (mouse_coords[1] - MCbullet_height // 2) - MC_coords[1]
        dist = hypot(vx, vy)
        self.vx = (vx / dist) * self.speed
        self.vy = (vy / dist) * self.speed

        self.angle = degrees(atan2(-vy, vx))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.dist = 0

    def resize(self, SW, SH):
        global MCbullet_width, MCbullet_height, width, height
        new_W, new_H = MCbullet_width * (SW / width), MCbullet_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MCbullet_width, MCbullet_height = new_W, new_H

    def update(self):
        if self.dist > self.firing_range:
            self.kill()
        if not -MCbullet_width <= self.rect.x <= width + MCbullet_width or \
                not -MCbullet_height <= self.rect.y <= height + MCbullet_height:
            self.kill()
        else:
            self.dist += hypot(self.rect.x - (self.rect.x + self.vx), self.rect.y - (self.rect.y + self.vy))
            self.rect.x += self.vx
            self.rect.y += self.vy


class Villager(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.frames_amount = len(villager_media['moving'])
        self.frames = {'l': villager_media['moving'],
                       'lh': villager_media['moving_h'],
                       'r': list(map(lambda pic:
                                     pygame.transform.flip(pic, True, False),
                                     villager_media['moving'])),
                       'rh': list(map(lambda pic:
                                      pygame.transform.flip(pic, True, False),
                                      villager_media['moving_h']))}
        self.cur_frame = 0
        self.frame_delay = 15
        self.time_counter = 0
        self.save_dir = 'r'
        self.image = make_img(self.frames[self.save_dir][0], width, height, UNIT_width, UNIT_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.prev_direction = ''
        self.hp = Vil_hp
        self.hit = False

    def update(self, x2, y2, norm_v=3 / (2 ** 0.5)):
        if self.hp <= 0:
            self.kill()

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
                self.image = make_img(self.frames[cur_direction[0] + ('h' if self.hit else '')][self.cur_frame], width,
                                      height, UNIT_width, UNIT_height)
            else:
                if cur_direction in 'fd':
                    if self.prev_direction not in 'fd ':  # не пауза фд == норм двиэ
                        self.save_dir = self.prev_direction
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              width, height, UNIT_width, UNIT_height)
                    elif self.prev_direction not in ' ':  # == fd
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              width, height, UNIT_width, UNIT_height)
                    else:
                        self.cur_frame = 0
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              width, height, UNIT_width, UNIT_height)
                else:
                    self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][0], width, height,
                                          UNIT_width, UNIT_height)
            self.prev_direction = cur_direction
            self.time_counter = 0
            self.hit = False

    def resize(self, SW, SH):
        global MCbullet_width, MCbullet_height, width, height
        new_W, new_H = MCbullet_width * (SW / width), MCbullet_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MCbullet_width, MCbullet_height = new_W, new_H


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
        self.image = make_img(self.frames[self.save_dir][0], width, height, UNIT_width, UNIT_height)
        self.rect = self.image.get_rect().move(
            pos_x + 15, pos_y + 5)
        self.prev_direction = ''

    def update(self, x2, y2, norm_v=3 / (2 ** 0.5)):
        if self.hp <= 0:
            self.kill()

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
                self.image = make_img(self.frames[cur_direction[0] + ('h' if self.hit else '')][self.cur_frame], width,
                                      height, UNIT_width, UNIT_height)
            else:
                if cur_direction in 'fd':
                    if self.prev_direction not in 'fd ':  # не пауза фд == норм движ
                        self.save_dir = self.prev_direction
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              width, height, UNIT_width, UNIT_height)
                    elif self.prev_direction not in ' ':  # == fd
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              width, height, UNIT_width, UNIT_height)
                    else:
                        self.cur_frame = 0
                        self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][self.cur_frame],
                                              width, height, UNIT_width, UNIT_height)
                else:
                    self.image = make_img(self.frames[self.save_dir[0] + ('h' if self.hit else '')][0], width, height,
                                          UNIT_width, UNIT_height)
            self.prev_direction = cur_direction
            self.time_counter = 0
            self.hit = False

    def shot(self, x2, y2, dist):
        self.shot_counter += 1
        x1, y1 = self.rect.x, self.rect.y
        if dist < 1000 and self.shot_counter >= self.shot_freq:
            self.shot_counter = 0
            Bullet((x1, y1), (x2, y2), 'Musketeer')

    def resize(self, SW, SH):
        global MCbullet_width, MCbullet_height, width, height
        new_W, new_H = MCbullet_width * (SW / width), MCbullet_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MCbullet_width, MCbullet_height = new_W, new_H


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


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size):
        super().__init__(button_group, all_sprites)
        self.size = size
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_image(self, way):
        self.way = way
        self.image = load_image(way)
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.rect = self.image.get_rect().move(self.pos_x + 15, self.pos_y + 5)

    def resize(self, SW, SH):
        global MCbullet_width, MCbullet_height, width, height
        new_W, new_H = MCbullet_width * (SW / width), MCbullet_height * (SH / height)
        self.image = pygame.transform.scale(self.image,
                                            (new_W, new_H))
        MCbullet_width, MCbullet_height = new_W, new_H

    def update(self):
        if pygame.sprite.spritecollideany(self, cursor_group):
            self.set_image(self.way[:-5] + '1.png')
        else:
            self.set_image(self.way[:-5] + '0.png')


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image('/start_screen/cursor.png')
        self.rect = self.image.get_rect()

    def resize(self, SW, SH):
        ...


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = 0  # -(target.rect.x + target.rect.w // 2 - width // 2) - tile_width
        self.dy = 0  # -(target.rect.y + target.rect.h // 2 - height // 2) - tile_height


def wave1(screen):
    global width, height
    MainCharacter.rect.x, MainCharacter.rect.y = width // 2, height // 2
    pygame.mouse.set_visible(True)

    update_level(screen, Villager)


def wave2(screen):
    global width, height
    MainCharacter.rect.x, MainCharacter.rect.y = width // 2, height // 2
    pygame.mouse.set_visible(True)

    update_level(screen, Musketeer)


def wave3(screen):
    global width, height
    MainCharacter.rect.x, MainCharacter.rect.y = width // 2, height // 2
    pygame.mouse.set_visible(True)

    update_level(screen, Magician)


def update_level(screen, enemy):
    global background, width, height, bad_end_flag, cur_wave
    bad_end_flag = False
    all_sprites.empty()
    enemy_group.empty()
    resized_flag = False
    camera = Camera()
    generate_enemies(3, enemy)
    n_enemies = 0
    while True:
        screen.fill('black')
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        generate_borders(width, height)

        if n_enemies < 15:
            if len(enemy_group) < 2:
                generate_enemies(n := randint(1, 5), enemy)
                n_enemies += n
        else:
            if len(enemy_group) == 0:
                for tree in trees_group:
                    if (tree.rect.x == width - tree_width and
                            (height // 2 - tree_height) <= tree.rect.y <= (height // 2 + tree_height)):
                        tree.kill()
            if MainCharacter.rect.x > width:
                cur_wave += 1
                if cur_wave <= 2:
                    waves[cur_wave](screen)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                for sprite in enemy_group:
                    sprite.kill()
            if event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                resized_flag = True
                new_SW, new_SH = new_width, new_height
                background = pygame.transform.scale(background, (new_SW, new_SH))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Bullet((MainCharacter.rect.x, MainCharacter.rect.y), event.pos)

        camera.update(MainCharacter)
        for sprite in all_sprites:
            if resized_flag:
                sprite.resize(new_SW, new_SH)
            camera.apply(sprite)
        if resized_flag:
            width, height = new_SW, new_SH
        resized_flag = False

        trees_group.draw(screen)
        player_group.update(keys)
        if bad_end_flag:
            return
        player_group.draw(screen)
        MCbullet_group.update()
        MCbullet_group.draw(screen)
        enemy_group.update(MainCharacter.rect.x, MainCharacter.rect.y)
        enemy_group.draw(screen)
        musketeer_bullet_group.update()
        musketeer_bullet_group.draw(screen)
        magician_bullet_group.update()
        magician_bullet_group.draw(screen)
        draw_hp_bar(MainCharacter, MainCharacter.rect.x, MainCharacter.rect.y, MainCharacter.hp)
        for sprite in all_sprites:
            if sprite in enemy_group:
                draw_hp_bar(sprite, sprite.rect.x, sprite.rect.y, sprite.hp)

        pygame.display.flip()
        clock.tick(FPS)


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


def generate_enemies(n, enemy):
    for _ in range(n):
        side = randint(1, 4)
        if side == 1:
            enemy(0, randint(0, height))
        elif side == 2:
            enemy(randint(0, width), 0)
        elif side == 4:
            enemy(width, randint(0, height))
        else:
            enemy(randint(0, width), height)


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
    pygame.draw.rect(screen, color1, fill_rect)
    pygame.draw.rect(screen, color2, outline_rect, 1)


all_sprites = pygame.sprite.Group()
cursor_group = pygame.sprite.Group()
trees_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
MCbullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
musketeer_bullet_group = pygame.sprite.Group()
magician_bullet_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

tile_images = {
    'tree': load_image(r'game/tree.png'),
    'MC_bullet': load_image(r'game/Bullet.png'),
    'magician_bullet': load_image(r'game/magic_bullet.png')}

background = pygame.transform.scale(load_image(r'game/background1.jpg'), (width, height))

player_media = {'moving': [load_image(f'/game/horse/horse_{i}.png') for i in range(6)],
                'moving_h': [load_image(f'/game/horse_hit/horse_hit_{i}.png') for i in range(6)]}
villager_media = {'moving': [load_image(f'/game/enemy/villager/sprite_{i}.png') for i in range(4)],
                  'moving_h': [load_image(f'/game/enemy/villager/villager_hit_{i}.png') for i in range(4)]}
musketeer_media = {'moving': [load_image(f'/game/enemy/musketeer/musketeer{i}.png') for i in range(4)],
                   'moving_h': [load_image(f'/game/enemy/musketeer/musketeer_hit_{i}.png') for i in range(4)]}
magician_media = {'moving': [load_image(f'/game/enemy/magician/magician_{i}.png') for i in range(2)],
                  'moving_h': [load_image(f'/game/enemy/magician/magician_hit_{i}.png') for i in range(2)]}
enemy_images = {'stay': load_image(r'game/enemy/EK.png')}

UNIT_width, UNIT_height = 80, 80
angles_dict = {'f': ...}

MC_width, MC_height = 80, 80
mc_def_v = 7
MCbullet_width, MCbullet_height = 40, 40
bullet_def_v = 20
tree_width = tree_height = 100
Ntrees_horz, Ntrees_vert = 30, 18

MC_hp, Vil_hp, Musk_hp, Mag_hp = 100, 100, 75, 150
MC_damage, Vil_damage, Musk_damage, Mag_damage = 10, 10, 10, 10
v_damage_delay = 120

enemies_firing_range = 250
MC_firing_range = 300
musketeer_firing_delay = 300

BAR_LENGTH, BAR_HEIGHT = UNIT_width, 10

waves = [wave1, wave2, wave3]
cur_wave = 0

clock = pygame.time.Clock()
FPS = 60

bad_end_flag = False
exit_flag = False
"""
player, level_x, level_y = generate_level(load_level('lvl1.txt'))
"""

if __name__ == '__main__':
    while True:
        start_screen()
        comic()
        MainCharacter = Player(width // 2, height // 2)
        wave1(screen)
        if bad_end_flag:
            bad_end()
            continue
        final_screen()
        terminate()
