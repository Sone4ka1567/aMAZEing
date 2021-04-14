import pygame
import sys
from os import path
import settings as const
from map import Map
from sprites import Player, Wall, Finish
from camera import Camera
from map_generator import map_generator


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        pygame.display.set_caption(const.TITLE)
        self.clock = pygame.time.Clock()

    def load_map(self):
        folder = path.dirname(__file__)
        if self.make_me_a_map:  # Если False, то надо подгрузить самому
            map_generator(self.difficulty, self.difficulty)
        self.map = Map(path.join(folder, 'map.txt'))

    def new(self):
        self.load_map()
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.finish = pygame.sprite.Group()
        for row, cells in enumerate(self.map.data):
            for col, cell in enumerate(cells):
                if cell == '1':
                    Wall(self, col, row)
                if cell == 'S':
                    self.player = Player(self, col, row)
                if cell == 'F':
                    Finish(self, col, row)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(const.FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, const.WIDTH, const.CELL_SIZE):
            pygame.draw.line(self.screen, const.DARKBLUE,
                             (x, 0), (x, const.HEIGHT))
        for y in range(0, const.HEIGHT, const.CELL_SIZE):
            pygame.draw.line(self.screen, const.DARKBLUE,
                             (0, y), (const.WIDTH, y))

    def draw(self):
        self.screen.fill(const.BACKGROUND_COLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    def create_button(self, message, x, y, width, height,
                      hovercolor, defaultcolor, level):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hovercolor, (x, y, width, height))
            if click[0] == 1:
                if level == 0:
                    self.start_screen_playing = False
                elif level == 1:
                    self.make_me_a_map = False
                    self.choose_screen_playing = False
                elif level == 2:
                    self.make_me_a_map = True
                    self.choose_screen_playing = False
                elif level == 'easy':
                    self.difficulty = 50
                    self.choose_dif_playing = False
                elif level == 'medium':
                    self.difficulty = 100
                    self.choose_dif_playing = False
                elif level == 'hardcore':
                    self.difficulty = 150
                    self.choose_dif_playing = False
                elif level == 'instruction':
                    self.instruction_playing = False
                elif level == 'bye':
                    self.quit()

        else:
            pygame.draw.rect(self.screen, defaultcolor, (x, y, width, height))

        self.button_text = self.small_font.render(message, True, const.BLACK)
        self.screen.blit(self.button_text, (x + (width - self.button_text.get_width()) / 2,
                                            y + (height - self.button_text.get_height()) / 2))

    def show_start_screen(self):
        self.big_font = pygame.font.SysFont("comicsansms", 200)
        self.font = pygame.font.SysFont("comicsansms", 100)
        self.small_font = pygame.font.SysFont("comicsansms", 50)
        self.start_text = self.big_font.render("aMAZEing", True, const.ORCHID)
        self.start_screen_playing = True

        while self.start_screen_playing:
            self.screen.fill(const.BACKGROUND_COLOR)
            self.screen.blit(self.start_text,
                             ((const.WIDTH - self.start_text.get_width()) / 2, 60))

            self.create_button("LET'S GO", const.WIDTH / 2 - 150, const.HEIGHT / 2,
                               300, 100, const.WHITE, const.LIGHTPURPLE, 0)

            self.events()

            pygame.display.update()
            self.clock.tick(const.FPS)

    def choose_map(self):
        self.choose_a_map_text = self.font.render(
            "Which map do you want?", True, const.ORCHID
        )
        self.choose_screen_playing = True

        while self.choose_screen_playing:
            self.screen.fill(const.BACKGROUND_COLOR)
            self.screen.blit(self.choose_a_map_text,
                             ((const.WIDTH - self.choose_a_map_text.get_width()) / 2, 60))

            self.create_button("Download my map", 50, const.HEIGHT / 2,
                               350, 100, const.WHITE, const.LIGHTPURPLE, 1)

            self.create_button("Make me a map", const.WIDTH - 400, const.HEIGHT / 2,
                               350, 100, const.WHITE, const.LIGHTPURPLE, 2)

            self.events()

            pygame.display.update()
            self.clock.tick(const.FPS)

    def instruction_download(self):
        self.instruction_text1 = self.small_font.render(
            "Add your map as map.txt file.", True, const.ORCHID
        )
        self.instruction_text2 = self.small_font.render(
            "Make sure, that the file consists", True, const.ORCHID
        )
        self.instruction_text3 = self.small_font.render(
            "only of the next symbols:", True, const.ORCHID
        )
        self.instruction_text4 = self.small_font.render(
            "1 - stands for a wall", True, const.ORCHID
        )
        self.instruction_text5 = self.small_font.render(
            ". - stands for a cell", True, const.ORCHID
        )
        self.instruction_text6 = self.small_font.render(
            "S - stands for start position", True, const.ORCHID
        )
        self.instruction_text7 = self.small_font.render(
            "F - stands for finish", True, const.ORCHID
        )

        self.instruction_playing = True

        while self.instruction_playing:
            self.screen.fill(const.BACKGROUND_COLOR)
            self.screen.blit(self.instruction_text1,
                             ((const.WIDTH - self.instruction_text1.get_width()) / 2, 20))
            self.screen.blit(self.instruction_text2,
                             ((const.WIDTH - self.instruction_text2.get_width()) / 2, 60))
            self.screen.blit(self.instruction_text3,
                             ((const.WIDTH - self.instruction_text3.get_width()) / 2, 100))
            self.screen.blit(self.instruction_text4,
                             ((const.WIDTH - self.instruction_text4.get_width()) / 2, 140))
            self.screen.blit(self.instruction_text5,
                             ((const.WIDTH - self.instruction_text5.get_width()) / 2, 180))
            self.screen.blit(self.instruction_text6,
                             ((const.WIDTH - self.instruction_text6.get_width()) / 2, 220))
            self.screen.blit(self.instruction_text7,
                             ((const.WIDTH - self.instruction_text7.get_width()) / 2, 260))

            self.create_button("Done", const.WIDTH / 2 - 150, const.HEIGHT - 300,
                               300, 100, const.WHITE, const.LIGHTPURPLE, 'instruction')

            self.events()

            pygame.display.update()
            self.clock.tick(const.FPS)

    def choose_difficulty(self):
        self.choose_dif_text = self.font.render(
            "Choose difficulty", True, const.ORCHID
        )
        self.choose_dif_playing = True

        while self.choose_dif_playing:
            self.screen.fill(const.BACKGROUND_COLOR)
            self.screen.blit(self.choose_dif_text,
                             ((const.WIDTH - self.choose_dif_text.get_width()) / 2, 100))

            self.create_button("EASY", 100, const.HEIGHT / 2 + 100,
                               250, 100, const.WHITE, const.LIGHTPURPLE, 'easy')

            self.create_button("MEDIUM", const.WIDTH / 2 - 125,
                               const.HEIGHT / 2 + 100, 250, 100, const.WHITE, const.LIGHTPURPLE, 'medium')

            self.create_button("HARDCORE", const.WIDTH - 350,
                               const.HEIGHT / 2 + 100, 250, 100, const.WHITE, const.LIGHTPURPLE, 'hardcore')

            self.events()

            pygame.display.update()
            self.clock.tick(const.FPS)

    def show_go_screen(self):
        self.go_text = self.font.render(
            "YOU ARE AWESOME!!!", True, const.ORCHID
        )
        self.go_playing = True

        while self.go_playing:
            self.screen.fill(const.BLACK)
            self.screen.blit(self.go_text,
                             ((const.WIDTH - self.go_text.get_width()) / 2, 250))

            self.create_button("I'M AWESOME!!", const.WIDTH / 2 - 200,
                               const.HEIGHT / 2 + 75, 400, 100, const.WHITE, const.LIGHTPURPLE, 'bye')

            self.events()

            pygame.display.update()
            self.clock.tick(const.FPS)


game = Game()
game.show_start_screen()
game.choose_map()
if game.make_me_a_map:
    game.choose_difficulty()
else:
    game.instruction_download()
game.new()
game.run()
game.show_go_screen()

