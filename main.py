import pygame, os, sys


pygame.init()
pygame.display.set_caption('Walking')
size = width, height = 1400, 800
screen = pygame.display.set_mode(size, pygame.RESIZABLE)


def load_image(name, colorkey=None):
    fullname = os.path.join(f'data\{name}')
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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'tree':
            self.tile_width, self.tile_height = 100, 100
        self.cur_img = tile_images[tile_type]
        self.image = pygame.transform.scale(self.cur_img,
                                            (width // (width // self.tile_width),
                                             height // (height // self.tile_height)))
        self.rect = self.image.get_rect().move(
            pos_x, pos_y)

    def resize(self, SW, SH):
        global width, height
        new_W, new_H = self.tile_width * (SW / width), self.tile_height * (SH / height)
        self.image = pygame.transform.scale(self.cur_img,
                                            (new_W, new_H))
        self.tile_width, self.tile_height = new_W, new_H


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.MC_img = player_image
        self.image = pygame.transform.scale(self.MC_img, (width // (width // MC_width), height // (height // MC_height)))
        self.rect = self.image.get_rect().move(
             pos_x + 15, pos_y + 5)

    def resize(self, SW, SH):
        global MC_width, MC_height, width, height
        new_W, new_H = MC_width * (SW / width), MC_height * (SH / height)
        self.image = pygame.transform.scale(self.MC_img,
                                            (new_W, new_H))
        MC_width, MC_height = new_W, new_H


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = 0 #-(target.rect.x + target.rect.w // 2 - width // 2) - tile_width
        self.dy = 0 #-(target.rect.y + target.rect.h // 2 - height // 2) - tile_height


def level1(screen):
    global background, width, height
    resized_flag = False
    camera = Camera()
    tree_ab_x, tree_ab_y = width // int(1.3 * tree_n_w), height // int(0.7 * tree_n_h)
    for x in range(0, width, tree_ab_x):
        for y in range(0, height, tree_ab_y):
            if x == 0 or y == 0:
                Tile('tree', x, y)

    while True:
        screen.fill('black')
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return
            if keys[pygame.K_a]:
                MainCharacter.rect.x -= step
            if keys[pygame.K_d]:
                MainCharacter.rect.x += step
            if keys[pygame.K_w]:
                MainCharacter.rect.y -= step
            if keys[pygame.K_s]:
                MainCharacter.rect.y += step
            if event.type == pygame.VIDEORESIZE:
                resized_flag = True
                new_SW, new_SH = event.w, event.h
                background = pygame.transform.scale(background, (new_SW, new_SH))

        camera.update(MainCharacter)
        for sprite in all_sprites:
            if resized_flag:
                sprite.resize(new_SW, new_SH)
            camera.apply(sprite)
        if resized_flag:
            width, height = new_SW, new_SH
        resized_flag = False
        tiles_group.draw(screen)
        player_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'tree': load_image(r'game\tree.png')
}
tree_n_w, tree_n_h = 20, 16
background = pygame.transform.scale(load_image(r'game\background1.jpg'), (width, height))

player_image = load_image('game\maincharacter.png')
MC_width, MC_height = 50, 70
MainCharacter = Player(width // 2, height // 2)

clock = pygame.time.Clock()
FPS = 60
step = 10

"""
player, level_x, level_y = generate_level(load_level('lvl1.txt'))
"""


if __name__ == '__main__':
    start_screen()
    level1(screen)
    final_screen()
    terminate()