import pygame, os, sys, csv
from fractions import Fraction
from random import randint
from random import choice as ch
from PIL import Image
from math import atan2, hypot, degrees

from sprite_groups import *
from MainCharacter import Player
from images import *
from settings import *
from sounds import *
from stat_functions import *


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


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(trees_group, all_sprites)
        self.width, self.height = tree_width, tree_height
        self.cur_img = tile_images['tree']
        self.image = make_img(self.cur_img, v_width, v_height, self.width, self.height)
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)


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
    timer, cnt_enemies, enemies_max_coeff = 0, 2, 1
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

        if (timer / FPS) < 60:  # increasing minimal count of enemies every 8 sec
            if (timer / FPS) % 8 == 0:
                cnt_enemies += 1
        else:
            if (timer / FPS) % 14 == 0:
                cnt_enemies += 1

        if (timer / FPS) % 40 == 0:  # 40 sec passed, increasing coeff of enemies spawning
            enemies_max_coeff += 1

        if len(enemy_group) < cnt_enemies:  # generating enemies
            for n in range(randint(2, 4) * enemies_max_coeff):
                generate_enemies(1, ch(av_enemies))

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
        if MainCharacter.hp <= 0:
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
        if MainCharacter.hp <= 0:
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


waves = [wave1, wave2, wave3, final_screen]
cur_wave = 0



clock = pygame.time.Clock()

start_mode_flag = False
bad_end_flag = False
exit_flag = False


if __name__ == '__main__':
    start_screen()
