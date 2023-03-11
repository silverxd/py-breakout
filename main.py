import pygame
import random
import time

def clamp(value, _min, _max):
    if _min > _max: raise Exception('Minimum value cannot be bigger than the max value!')
    if value < _min: return _min
    if value > _max: return _max
    return value 

class Block():
    def __init__(self, x, y, color):
        self.x = x # Grid X
        self.y = y # Grid Y
        self.color = color
        # self.width = (self.wx/10)-10 # 10 blocks per row, 5 pixels of free space on either side
        # self.height = (self.wy/60)-10 # 

block_colors = []

class Game:
    def __init__(self):
        # Test
        pygame.init()
        self.window_size = (640, 480)
        self.screen = pygame.display.set_mode((self.window_size), pygame.RESIZABLE)
        self.wx, self.wy = pygame.display.get_surface().get_size()  # Get window resolution
        
        pygame.display.set_caption("Breakout Game")
        self.level = 0
        self.running = True
        self.tick_length = 1 / 60
        self.BACKGROUND_COLOUR = (20, 20, 50)

        # Player
        self.player_width = 0.25
        self.player_x = self.wx / 2 - self.player_width / 2
        self.player_p = 0.5 - (self.player_width / 2 * self.wx)
        self.move_x = 0
        self.player_speed = 16

        # Blocks
        self.blocks = []
        for y in range (0, 4):
            for x in range (0, 10):
                self.blocks.append(Block(x, y, self.returnColor(y)))
        # self.block_padding = 5

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False
                if event.key == pygame.K_a:
                    self.move_x = -self.player_speed
                if event.key == pygame.K_d:
                    self.move_x = +self.player_speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and self.move_x == -self.player_speed or event.key == pygame.K_d and self.move_x == self.player_speed:
                    self.move_x = 0

    def update(self):
        self.wx, self.wy = pygame.display.get_surface().get_size()
        self.player_p = clamp(self.player_p + (self.move_x / 1000), 0, (1 - self.player_width))
        self.player_x = self.player_p * self.wx
        self.block_padding_x = self.wx/128
        self.block_padding_y = self.wy/96
        #self.player_x = clamp(self.player_x + self.move_x, 0, self.wx - self.player_width)
        pass
    
    def returnColor(self, level):
        
        colors = ['ff141a', 'fda216', 'fdfa15', '76d443', '00adf2']
        hexcolor = colors[level]
        # hexcolor = hexcolor.lstrip('#')
        rgb = tuple(int(hexcolor[i:i+2], 16) for i in (0, 2, 4)) # Varastatud StackOverFlow-st Silveri poolt.
        return rgb

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOUR)

        # Draw player
        pygame.draw.rect(self.screen, pygame.Color(255, 255, 255),
        (self.player_x, self.wy - 2 * (self.wy / 20), self.player_width * self.wx, self.wy / 20))

        # Blocks
        block_width = (self.wx - 10 * self.block_padding_x) / 10
        block_height = (self.wy - 20 * self.block_padding_y) / 20
        for i in self.blocks:
            pygame.draw.rect(
                self.screen, pygame.Color(i.color),
                (
                    i.x*(block_width + self.block_padding_x) + self.block_padding_x, # Rect left
                    i.y*(block_height + self.block_padding_y) + self.block_padding_y, # Rect top
                    block_width - self.block_padding_x, # Rect width
                    block_height - (self.block_padding_y / 2) # Rect height
                )
            )
            
            
        pygame.display.flip()

    def run(self):
        while self.running:
            start = time.time()
            self.input()
            self.update()
            self.render()
            time.sleep(max(self.tick_length - (time.time() - start), 0))
        pygame.quit()


game = Game()
game.run()
