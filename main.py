import pygame
from random import choice as ch

from images import *
from stat_functions import *
from interactive import *
from tools import *


# первая волна(сельчане), загрузка соответсвующей уровню музыки, барьеров, заднего фона
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


# вторая волна(мушкетеры), загрузка ресурсов аналогично другим волнам с уникальными ресурсами
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


# третья волна(маги)
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


# режим нонстопа-соответсвующие элементы и запись статистики
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
    generate_borders(v_width, v_height)
    av_enemies = [Villager, Musketeer, Magician]
    for _ in range(2):
        generate_enemies(2, ch(av_enemies), non_stop_mode_flag)

    while True:
        timer += 1
        virtual_surface.fill('black')
        virtual_surface.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        # сбалансированная генерация врагов по определенным таймингам и событиям
        # генерация врагов с флагом нонстоп-значит из каждого класса персонажа идет запись нужной данной в статистику
        if (timer / FPS) < 60:  # увеличиваем минимальное количество врагов каждые 10 сек если прошло меньше минуты
            if (timer / FPS) % 10 == 0:
                cnt_enemies += 1
        else:
            if (timer / FPS) % 20 == 0: # каждые 20 сек если больше минуты
                cnt_enemies += 1

        if (timer / FPS) % 60 == 0:  # увеличиваем коэффицент спавна врагов при прохождении каждой минуты
            enemies_max_coeff += 1

        if len(enemy_group) < cnt_enemies:  # generating enemies
            for n in range(randint(2, 4) * enemies_max_coeff):
                generate_enemies(1, ch(av_enemies), non_stop_mode_flag)

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
                    Bullet((MainCharacter.rect.x, MainCharacter.rect.y), event.pos, width, height)
                    review_stats(stat_file_name, shoted=True)
        trees_group.draw(virtual_surface)
        player_group.update(keys)
        if MainCharacter.hp <= 0:
            return bad_end()
        player_group.draw(virtual_surface)
        MCbullet_group.update()
        MCbullet_group.draw(virtual_surface)
        enemy_group.update(MainCharacter.rect.x, MainCharacter.rect.y, width, height)
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


# стори режим, обновление уровня в соответствии с предидущей волной
def update_level(enemy):
    global background, width, height, bad_end_flag, cur_wave, virtual_surface, screen
    bad_end_flag = False
    all_sprites.empty()
    enemy_group.empty()
    MCbullet_group.empty()
    musketeer_bullet_group.empty()
    magician_bullet_group.empty()
    resized_flag = False
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
                    Bullet((MainCharacter.rect.x, MainCharacter.rect.y), event.pos, width, height)
        trees_group.draw(virtual_surface)
        player_group.update(keys)
        if MainCharacter.hp <= 0:
            return bad_end()
        player_group.draw(virtual_surface)
        MCbullet_group.update()
        MCbullet_group.draw(virtual_surface)
        enemy_group.update(MainCharacter.rect.x, MainCharacter.rect.y, width, height)
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


# начальный экран, собственная музыка, кнопки и курсор
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

    #загрузка нужных фрэймов обьектам
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
                    #обработка нажания кнопок по коллайду и нажатию на курсор
                    #создание основного персонажа при нажатии на кнопку режима игры
                    #выбирается определенный флаг в соответствии с выбранным режимом
                    if pygame.sprite.spritecollideany(start_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        start_mode_flag = True
                        MainCharacter = Player(v_width // 2, v_height // 2, non_stop_mode_flag=False)
                        return comic()
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()
                    if pygame.sprite.spritecollideany(non_stop_button, cursor_group):
                        cursor.kill()
                        button_group.empty()
                        non_stop_mode_flag = True
                        MainCharacter = Player(v_width // 2, v_height // 2, non_stop_mode_flag=non_stop_mode_flag)
                        return non_stopMODE()
            # изменение размеров окна
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize(width, height)

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


# анимация комикса(стори режим)
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
                        return waves[cur_wave]()    # загрузка первой волны(сельчан) при нажатии на кнопку старта
            if event.type == pygame.MOUSEMOTION:
                cords = event.pos
                flag = pygame.mouse.get_focused()
                cursor.rect.x, cursor.rect.y = cords
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize(width, height)   # изменение размеров кнопок при изменении размеров экрана
        button_group.update()
        button_group.draw(screen)
        if flag:
            cursor_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


# плохая концовка(гибель персонажа)
# свой задний фон, музыкаи курсор
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
                        return start_screen()   # возвращение в главное меню
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()
            if event.type == pygame.VIDEORESIZE:
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize(width, height)
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


# финальный экран при победе персонажа
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
                        return start_screen()   # начать заново
                    if pygame.sprite.spritecollideany(exit_button, cursor_group):
                        terminate()
            if event.type == pygame.VIDEORESIZE:    # изменение размеров окна
                width = max(event.w, min_width)
                height = max(event.h, min_height)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                for btn in button_group:
                    btn.resize(width, height)
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


start_mode_flag = False
bad_end_flag = False
exit_flag = False

waves = [wave1, wave2, wave3, final_screen]
cur_wave = 0