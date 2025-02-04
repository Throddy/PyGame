import pygame, os, sys, csv
from fractions import Fraction
from random import randint
from random import choice as ch
from PIL import Image
from math import atan2, hypot, degrees

pygame.init()

gun_snd = pygame.mixer.Sound('data/game/sounds/gun.mp3')
gun_snd.set_volume(0.1)
musket_snd = pygame.mixer.Sound('data/game/sounds/musket.mp3')
musket_snd.set_volume(0.03)
ouch_snd = pygame.mixer.Sound('data/game/sounds/ouch.wav')
ouch_snd.set_volume(0.3)
spell_snd = pygame.mixer.Sound('data/game/sounds/spell.wav')
spell_snd.set_volume(0.2)

pygame.display.set_caption('The Horsehead')
size = width, height = v_width, v_height = 1400, 800
min_width, min_height = 1200, 700
screen = pygame.display.set_mode(size, pygame.RESIZABLE, pygame.FULLSCREEN)
virtual_surface = pygame.Surface((width, height))


# screen = pygame.display.set_mode(size)


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global width, height, screen, v_width, v_height, non_stop_mode_flag, start_mode_flag, MainCharacter
    start_mode_flag, non_stop_mode_flag = False, False
    pygame.mixer.music.load('data/game/music/main_menu.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)

    k_w, k_h = (width / v_width), (height / v_height)
    title = Button(410 * k_w, 10 * k_h, 410, 10, (550 * k_w, 120 * k_h), (550, 120))
    title.set_image('start_screen/title/title_0.png')

    start_button = Button(500 * k_w, 200 * k_h, 500, 200, (350 * k_w, 100 * k_h), (350, 100))
    start_button.set_image('start_screen/startbutton/sprite_0.png')

    exit_button = Button(500 * k_w, 350 * k_h, 500, 350, (350 * k_w, 100 * k_h), (350, 100))
    exit_button.set_image('start_screen/exitbutton/exitbutton_0.png')

    non_stop_button = Button(500 * k_w, 500 * k_h, 500, 500, (350 * k_w, 100 * k_h), (350, 100))
    non_stop_button.set_image('start_screen/nonstopbutton/nonstop_0.png')
    fon = pygame.transform.scale(load_image('/start_screen/start_background.png'), (width, height))

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(fon, (width, height))
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        start_mode_flag = True
                        MainCharacter = Player(v_width // 2, v_height // 2)
                        return comic()
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()
                    if pygame.sprite.spritecollideany(non_stop_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        non_stop_mode_flag = True
                        MainCharacter = Player(v_width // 2, v_height // 2)
                        return non_stopMODE()
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize()

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
    global width, height, screen, v_width, v_height, MainCharacter, cur_wave, button_group
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)
    k_w, k_h = (width / v_width), (height / v_height)
    start_button = Button(0 * k_w, 700 * k_h, 0, 700, (300 * k_w, 80 * k_h), (300, 80))
    start_button.set_image('start_screen/startbutton/sprite_0.png')
    fon = pygame.transform.scale(load_image(f'start_screen/comic{cur_wave}.png'), (width, height))

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(fon, (width, height))
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        return waves[cur_wave]()
            if event.type == pygame.MOUSEMOTION:
                cords = event.pos
                flag = pygame.mouse.get_focused()
                cursor.rect.x, cursor.rect.y = cords
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize()
        button_group.update()
        button_group.draw(screen)
        if flag:
            cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def bad_end():
    global cur_wave, screen, width, height, v_width, v_height, non_stop_mode_flag
    pygame.mixer.music.load('data/game/music/bad_end.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    button_group.empty()
    cursor_group.empty()
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)
    k_w, k_h = (width / v_width), (height / v_height)
    start_button = Button(300 * k_w, 600 * k_h, 300, 600, (350 * k_w, 100 * k_h), (350, 100))
    start_button.set_image('start_screen/startbutton/sprite_0.png')

    exit_button = Button(700 * k_w, 600 * k_h, 700, 600, (350 * k_w, 100 * k_h), (350, 100))
    exit_button.set_image('start_screen/exitbutton/exitbutton_0.png')
    fon = pygame.transform.scale(load_image('start_screen/game_over2.png'), (width, height))

    if non_stop_mode_flag:
        results = stat_results(stat_file_name)

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(fon, (width, height))
        screen.blit(fon, (0, 0))

        if non_stop_mode_flag:
            text_x = 10
            text_y = 10
            for title, value in results:
                font = pygame.font.Font(None, 30)
                text = font.render(f'{title} ---> {value}', True, 'pink')
                text_h = text.get_height()
                screen.blit(text, (text_x, text_y))
                text_y += text_h * 1.2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        cur_wave = 0
                        start_button, non_stop_mode_flag = False, False
                        return start_screen()
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize()
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
    global cur_wave, screen, width, height, v_width, v_height
    pygame.mixer.music.load('data/game/music/happy_end.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    button_group.empty()
    cursor_group.empty()
    cursor = Cursor()
    all_sprites.add(cursor)
    cursor_group.add(cursor)
    flag = False
    pygame.mouse.set_visible(False)
    k_w, k_h = (width / v_width), (height / v_height)
    start_button = Button(300 * k_w, 600 * k_h, 300, 600, (350 * k_w, 100 * k_h), (350, 100))
    start_button.set_image('start_screen/startbutton/sprite_0.png')

    exit_button = Button(700 * k_w, 600 * k_h, 700, 600, (350 * k_w, 100 * k_h), (350, 100))
    exit_button.set_image('start_screen/exitbutton/exitbutton_0.png')
    fon = pygame.transform.scale(load_image('game/final_screen.png'), (width, height))

    while True:
        screen.fill(pygame.Color('black'))
        fon = pygame.transform.scale(fon, (width, height))
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
                        return start_screen()
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize()
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


def make_img(img, w, h, persW, persH):
    return pygame.transform.scale(img, (w // (w // persW), h // (h // persH)))


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(trees_group, all_sprites)
        self.width, self.height = tree_width, tree_height
        self.cur_img = tile_images['tree']
        self.image = make_img(self.cur_img, v_width, v_height, self.width, self.height)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


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
        self.image = make_img(self.image, v_width, v_height, MCbullet_width, MCbullet_height)
        self.rect = self.image.get_rect().move(
            MC_coords[0] + MCbullet_width // 5.5, MC_coords[1] + MCbullet_height // 2)

        self.speed = bullet_def_v
        vx = (mouse_coords[0] * (v_width / width) - MCbullet_width // 2) - MC_coords[0]
        vy = (mouse_coords[1] * (v_height / height) - MCbullet_height // 2) - MC_coords[1]
        dist = hypot(vx, vy)
        self.vx = (vx / dist) * self.speed
        self.vy = (vy / dist) * self.speed

        self.angle = degrees(atan2(-vy, vx))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.dist = 0

    def update(self):
        if self.dist > self.firing_range:
            self.kill()
        if not -MCbullet_width <= self.rect.x <= v_width + MCbullet_width or \
                not -MCbullet_height <= self.rect.y <= v_height + MCbullet_height:
            self.kill()
        else:
            self.dist += hypot(self.rect.x - (self.rect.x + self.vx), self.rect.y - (self.rect.y + self.vy))
            self.rect.x += self.vx
            self.rect.y += self.vy


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
        if pygame.sprite.spritecollideany(self, cursor_group):
            self.set_image(self.way[:-5] + '1.png')
        else:
            self.set_image(self.way[:-5] + '0.png')

    def resize(self):
        global v_width, v_height, width, height
        new_W, new_H = self.WIDTH * (width / v_width), self.HEIGHT * (height / v_height)
        self.image = pygame.transform.scale(self.image, (new_W, new_H))
        self.pos_x, self.pos_y = self.X * (width / v_width), self.Y * (height / v_height)
        self.rect = self.image.get_rect().move(self.pos_x + 15, self.pos_y + 5)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = load_image('/start_screen/cursor.png')
        self.rect = self.image.get_rect()


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


def wave1():
    global background, tile_images, v_height, v_width
    pygame.mixer.music.load('data/game/music/vil_bgm.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    MainCharacter.rect.x, MainCharacter.rect.y = v_width // 2, v_height // 2
    pygame.mouse.set_visible(True)

    tile_images['tree'] = load_image(r'game/tree.png')
    background = pygame.transform.scale(load_image(r'game/background1.jpg'), (v_width, v_height))

    update_level(Villager)


def wave2():
    global v_width, v_height, background, tile_images
    pygame.mixer.music.load('data/game/music/musket_bgm.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    MainCharacter.rect.x, MainCharacter.rect.y = v_width // 2, v_height // 2
    pygame.mouse.set_visible(True)

    tile_images['tree'] = load_image(r'game/torch-Photoroom.png')
    background = pygame.transform.scale(load_image(r'game/brick-1.png'), (v_width, v_height))

    update_level(Musketeer)


def wave3():
    global v_width, v_height, background, tile_images
    pygame.mixer.music.load('data/game/music/mag_bgm.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.05)
    MainCharacter.rect.x, MainCharacter.rect.y = v_width // 2, v_height // 2
    pygame.mouse.set_visible(True)

    tile_images['tree'] = load_image(r'game/el.png')
    background = pygame.transform.scale(load_image(r'game/background_mag-1.png'), (v_width, v_height))

    update_level(Magician)


def non_stopMODE():
    global background, width, height, bad_end_flag, cur_wave, virtual_surface, screen, headers, stat_file_name
    pygame.mouse.set_visible(True)

    tile_images['tree'] = load_image(r'game/el.png')
    background = pygame.transform.scale(load_image(r'game/background_mag-1.png'), (v_width, v_height))
    start_stats(stat_file_name)

    bad_end_flag = False
    all_sprites.empty()
    enemy_group.empty()
    MCbullet_group.empty()
    musketeer_bullet_group.empty()
    magician_bullet_group.empty()
    resized_flag = False
    timer, a, cnt_enemies = 0, 600, 2
    camera = Camera()
    generate_borders(v_width, v_height)
    av_enemies = [Villager, Musketeer, Magician]
    for _ in range(2):
        generate_enemies(2, ch(av_enemies))

    while True:
        timer += 1
        virtual_surface.fill('black')
        virtual_surface.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        if len(enemy_group) < cnt_enemies or timer % a == 0:
            generate_enemies(randint(2, 5), ch(av_enemies))

        if timer // 60 == 60:
            a = max(a - 60, 30)
            cnt_enemies += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                for sprite in enemy_group:
                    sprite.load_animation(sprite.rect.x, sprite.rect.y, enemy_images)
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gun_snd.play()
                    Bullet((MainCharacter.rect.x, MainCharacter.rect.y), event.pos)
                    review_stats(stat_file_name, shoted=True)

        camera.update(MainCharacter)
        trees_group.draw(virtual_surface)
        player_group.update(keys)
        if bad_end_flag:
            return bad_end()
        player_group.draw(virtual_surface)
        MCbullet_group.update()
        MCbullet_group.draw(virtual_surface)
        enemy_group.update(MainCharacter.rect.x, MainCharacter.rect.y)
        enemy_group.draw(virtual_surface)
        musketeer_bullet_group.update()
        musketeer_bullet_group.draw(virtual_surface)
        magician_bullet_group.update()
        magician_bullet_group.draw(virtual_surface)
        draw_hp_bar(MainCharacter, MainCharacter.rect.x, MainCharacter.rect.y, MainCharacter.hp)
        for sprite in all_sprites:
            if sprite in enemy_group:
                draw_hp_bar(sprite, sprite.rect.x, sprite.rect.y, sprite.hp)
        scaled_surface = pygame.transform.scale(virtual_surface, (width, height))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


def update_level(enemy):
    global background, width, height, bad_end_flag, cur_wave, virtual_surface, screen
    bad_end_flag = False
    all_sprites.empty()
    enemy_group.empty()
    MCbullet_group.empty()
    musketeer_bullet_group.empty()
    magician_bullet_group.empty()
    resized_flag = False
    camera = Camera()
    generate_enemies(3, enemy)
    generate_borders(v_width, v_height)
    n_enemies = 0
    while True:
        virtual_surface.fill('black')
        virtual_surface.blit(background, (0, 0))
        keys = pygame.key.get_pressed()

        if n_enemies < 15:
            if len(enemy_group) < 2:
                generate_enemies(n := randint(1, 5), enemy)
                n_enemies += n
        else:
            if len(enemy_group) == 0:
                mx_x = max(trees_group, key=lambda spr: spr.rect.x).rect.x
                for tree in trees_group:
                    x, y = tree.rect.x, tree.rect.y
                    if x == mx_x and ((height - 1) // 2 - tree_height) <= y <= ((height + 1) // 2 + tree_height):
                        tree.kill()
            if MainCharacter.rect.x > v_width:
                cur_wave += 1
                if cur_wave <= 3:
                    if cur_wave <= 2:
                        comic()
                    waves[cur_wave]()
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                for sprite in enemy_group:
                    sprite.kill()
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    gun_snd.play()
                    Bullet((MainCharacter.rect.x, MainCharacter.rect.y), event.pos)

        camera.update(MainCharacter)
        trees_group.draw(virtual_surface)
        player_group.update(keys)
        if bad_end_flag:
            return bad_end()
        player_group.draw(virtual_surface)
        MCbullet_group.update()
        MCbullet_group.draw(virtual_surface)
        enemy_group.update(MainCharacter.rect.x, MainCharacter.rect.y)
        enemy_group.draw(virtual_surface)
        musketeer_bullet_group.update()
        musketeer_bullet_group.draw(virtual_surface)
        magician_bullet_group.update()
        magician_bullet_group.draw(virtual_surface)
        draw_hp_bar(MainCharacter, MainCharacter.rect.x, MainCharacter.rect.y, MainCharacter.hp)
        for sprite in all_sprites:
            if sprite in enemy_group:
                draw_hp_bar(sprite, sprite.rect.x, sprite.rect.y, sprite.hp)
        scaled_surface = pygame.transform.scale(virtual_surface, (width, height))
        screen.blit(scaled_surface, (0, 0))
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
            enemy(0, randint(0, v_height))
        elif side == 2:
            enemy(randint(0, v_width), 0)
        elif side == 4:
            enemy(v_width, randint(0, v_height))
        else:
            enemy(randint(0, v_width), v_height)


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


def start_stats(file_name):
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers,
                                delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        start_data = {}
        for header, start_vals in zip(headers, [0] * len(headers)):
            start_data[header] = start_vals
        writer.writerow(start_data)


def review_stats(file_name, enemy=None, killed=False, time_ticked=False, shoted=False):
    global headers
    if killed:
        if type(enemy) == Villager:
            change_col = headers[0]
        elif type(enemy) == Musketeer:
            change_col = headers[1]
        elif type(enemy) == Magician:
            change_col = headers[2]
    elif shoted:
        change_col = headers[4]
    elif time_ticked:
        change_col = headers[5]

    with open(file_name, 'r') as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))
        new_row = {k: int(v) + 1 if k == change_col else v for k, v in data[len(data) - 1].items()}
        if killed:
            new_row = {k: int(v) + 1 if k == headers[3] else v for k, v in new_row.items()}
        data.append(new_row)

    with open(stat_file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def stat_results(file_name):
    with open(file_name, 'r') as csv_file:
        data = list(csv.DictReader(csv_file, delimiter=';', quotechar='"'))
    return data[-1].items()


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
    'tree': load_image(r'game/water.png'),
    'MC_bullet': load_image(r'game/Bullet.png'),
    'magician_bullet': load_image(r'game/magic_bullet.png')}

background = pygame.transform.scale(load_image(r'game/road.png'), (v_width, v_height))

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
v_damage_delay = 2

enemies_firing_range = 250
MC_firing_range = 300
musketeer_firing_delay = 300

BAR_LENGTH, BAR_HEIGHT = UNIT_width, 10

waves = [wave1, wave2, wave3, final_screen]
cur_wave = 0

stat_file_name = 'stat.csv'
headers = ["Total VILLAGERS you've destroyed", "Total MUSKETEERS you've destroyed",
           "Total MAGICIANS you've destroyed", "Total ENEMIES you've killed",
           "Total SHOTS you've done", "Total TIME(seconds) you' spent"]

clock = pygame.time.Clock()
FPS = 60

start_mode_flag = False
non_stop_mode_flag = False
bad_end_flag = False
exit_flag = False

if __name__ == '__main__':
    start_screen()
