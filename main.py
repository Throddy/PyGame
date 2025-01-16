import pygame, os, sys


pygame.init()
pygame.display.set_caption('Walking')
size = width, height = 1400, 800
min_width, min_height = 1200, 700
screen = pygame.display.set_mode(size, pygame.RESIZABLE, pygame.FULLSCREEN)


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


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(trees_group, all_sprites)
        self.width, self.height = tree_width, tree_height
        self.cur_img = tile_images['tree']
        self.image = pygame.transform.scale(self.cur_img,
                                            (width // (width // self.width),
                                             height // (height // self.height)))
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

    def update(self, keys, vx=0, vy=0):
        if not keys[pygame.K_SPACE]:
            if keys[pygame.K_a]:
                vx = -15
            if keys[pygame.K_d]:
                vx = 15
            if keys[pygame.K_w]:
                vy = -15
            if keys[pygame.K_s]:
                vy = 15

            if abs(vx) == abs(vy) == 15:
                vx = vx / (2 ** 0.5)
                vy = vy / (2 ** 0.5)

            self.rect.x += vx
            if pygame.sprite.spritecollideany(self, trees_group):
                self.rect.x -= vx
                vx = 0

            self.rect.y += vy
            if pygame.sprite.spritecollideany(self, trees_group):
                self.rect.y -= vy
                vy = 0
        else:
            self.rect.x, self.rect.y = width // 2, height // 2


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

    while True:
        screen.fill('black')
        screen.blit(background, (0, 0))
        keys = pygame.key.get_pressed()
        generate_borders(width, height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                return
            if event.type == pygame.VIDEORESIZE:
                new_width = max(event.w, min_width)
                new_height = max(event.h, min_height)
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
                resized_flag = True
                new_SW, new_SH = new_width, new_height
                background = pygame.transform.scale(background, (new_SW, new_SH))

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
        player_group.draw(screen)

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


all_sprites = pygame.sprite.Group()
trees_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'tree': load_image(r'game\tree.png')
}
Ntrees_horz, Ntrees_vert = 30, 18
background = pygame.transform.scale(load_image(r'game\background1.jpg'), (width, height))

player_image = load_image('game\maincharacter.png')
MC_width, MC_height = 50, 70
tree_width = tree_height = 100
MainCharacter = Player(width // 2, height // 2)

clock = pygame.time.Clock()
FPS = 60

"""
player, level_x, level_y = generate_level(load_level('lvl1.txt'))
"""


if __name__ == '__main__':
    start_screen()
    level1(screen)
    final_screen()
    terminate()