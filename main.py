import pygame
import random
import time
import math

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
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.running = True
        self.tick_length = 1 / 60
        self.BACKGROUND_COLOUR = (20, 20, 50)
        self.gamestate = 'waitingtostart'
        self.end_surface = pygame.Surface(self.window_size)
        self.end_surface.fill((255, 0, 0))

        # Platform
        self.platform_width = 0.25
        self.platform_speed = 16

        # Balls
        self.ball_speed = 7
        self.ball_radius = 0.015

        self.game_start()
        
        # Blocks
        self.blocks = []
        for y in range (0, self.gamelevel):
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
                    self.move_x = -self.platform_speed
                if event.key == pygame.K_d:
                    self.move_x = +self.platform_speed  
                if (event.key in [pygame.K_SPACE, pygame.K_RETURN]) and self.gamestate == "ending":  # RESTART!
                    self.game_start()
                    print("restarting!")

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and self.move_x == -self.platform_speed or event.key == pygame.K_d and self.move_x == self.platform_speed:
                    self.move_x = 0
            
            if event.type == pygame.VIDEORESIZE:
                self.wx, self.wy = pygame.display.get_surface().get_size()
                self.end_surface = pygame.Surface((self.wx, self.wy))  # Endscreen fix
                self.end_surface.fill((255, 0, 0))
                
    def game_start(self):
        self.blocklevel = 0
        self.gamelevel = 3
        self.end_counter = 0
        self.gamestate = 'waitingtostart'
        
        # Platform
        self.platform_x = self.wx / 2 - self.platform_width / 2
        self.platform_p = 0.5 - (self.platform_width / 2)
        self.move_x = 0

        # Balls
        self.ball_x = 0.5
        self.ball_y = 0.5
        self.balltimer = 0
        self.ball_move_x = 0
        self.ball_move_y = 0
        self.score = 0

        # Blocks
        self.blocks = []
        for y in range (0, self.gamelevel):
            for x in range (0, 10):
                self.blocks.append(Block(x, y, self.returnColor(y)))
        # self.block_padding = 5
        
        self.end_surface.set_alpha(0)

    def update(self):
        self.platform_p = clamp(self.platform_p + (self.move_x / 1000), 0, (1 - self.platform_width))
        self.ball_x = clamp(self.ball_x + (self.ball_move_x / 1000), 0, 1)
        self.ball_y = clamp(self.ball_y + (self.ball_move_y / 1000), 0, 1)

        # you missed the platform dumbass
        if self.ball_y > 1 - self.ball_radius:
            self.gamestate = 'ending'
            if self.end_counter == 1:
                print('e')

        # Ball collision with platform
        platform_height_px = int(self.wy - 2 * (self.wy / 20) - self.ball_radius * self.wy)
        ball_platform_collision_y = int(self.ball_y * self.wy) >= platform_height_px and int(self.ball_y * self.wy) < 10 + platform_height_px
        ball_platform_collision_x = self.ball_x > self.platform_p and self.ball_x < self.platform_p + self.platform_width
        if ball_platform_collision_y and ball_platform_collision_x:
            print("Platform collision!")
            self.ball_move_y = -self.ball_move_y
            if self.ball_x < self.platform_p + (self.platform_width / 2):
                self.ball_move_x -= 60*abs(self.ball_x - self.platform_p - (self.platform_width / 2))
            else:
                self.ball_move_x += 60*abs(self.ball_x - self.platform_p - (self.platform_width / 2))
            

        # Wall collision
        if self.ball_x <= self.ball_radius or self.ball_x >= 1-self.ball_radius:
            print('Wall collision')
            self.ball_move_x = -self.ball_move_x

        # Ceiling collision
        if self.ball_y <= self.ball_radius:
            print("Ceiling collision")
            self.ball_move_y = -self.ball_move_y

        ##  Mart lubas - (allkiri)
        if self.gamestate == "ending":  # Budget endscreen logic
            self.end_counter += 10
            
        if self.gamestate == 'waitingtostart':
            self.balltimer += 1
            
        if self.balltimer == 50:
            self.gamestate == 'ingame'
            self.ball_move_x = self.ball_speed
            self.ball_move_y = self.ball_speed

        # Brick collision
        # Millise bricki kohal ma olen?
        ball_brick_grid_x = self.ball_x // 0.1
        ball_brick_grid_y = self.ball_y // 0.05
        for block in self.blocks:
            if block.x == ball_brick_grid_x and block.y == ball_brick_grid_y:
                print("Brick collision.")
                self.score += 1
                self.blocks.remove(block)
                self.ball_move_y = -self.ball_move_y
            
            # if self.blocks.size() == 0:
            #     self.
        
        pass
        
    def returnColor(self, blocklevel):
        
        colors = ['ff141a', 'fda216', 'fdfa15', '76d443', '00adf2']
        hexcolor = colors[blocklevel]
        # hexcolor = hexcolor.lstrip('#')
        rgb = tuple(int(hexcolor[i:i+2], 16) for i in (0, 2, 4)) # Varastatud StackOverFlow-st Silveri poolt.
        return rgb

    def render(self):
        self.screen.fill(self.BACKGROUND_COLOUR)

        
        self.wx, self.wy = pygame.display.get_surface().get_size()
        self.block_padding_x = self.wx/128
        self.block_padding_y = self.wy/96
        self.ball_radius_px = self.wx * self.ball_radius
        # Draw platform
        pygame.draw.rect(self.screen, pygame.Color(255, 255, 255),
        (self.platform_p * self.wx, self.wy - 2 * (self.wy / 20), self.platform_width * self.wx, self.wy / 20))

        self.scoretext = self.font.render("Score : " + str(math.floor(self.score)), True, (255, 255, 255))
        self.screen.blit(self.scoretext, ((self.platform_x - self.scoretext.get_width()) / 2,
        (int(self.wy - 2 * (self.wy / 20) - self.ball_radius * self.wy) - self.scoretext.get_height()) / 2 - 30))
               
        
        # Draw ball
        
        pygame.draw.circle(self.screen, pygame.Color(230, 230, 230), (self.ball_x * self.wx, self.ball_y * self.wy), self.ball_radius_px)
        
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
        
        
        
        if self.gamestate == "ending":
            self.ball_move_x = 0
            self.ball_move_y = 0
            self.end_surface.set_alpha(self.end_counter)  # Render endscreen I think
            self.screen.blit(self.end_surface, (0, 0))
            if self.end_counter >= 200:
                # self.scoreText = self.font.render("Score : " + str(math.floor(self.score)), True, (255, 255, 255))
                self.gameovertext = self.font.render('GAME OVER!', True, (255, 255, 255))
                self.gameovertext2 = self.font.render('Press ENTER or SPACE to play again!', True, (255, 255, 255))
                # self.window.blit(self.scoreText, ((self.wx - self.scoreText.get_width()) / 2,
                #                                   (self.wy - self.scoreText.get_height()) / 2 - 30))  # sketchy AF code but it works
                self.screen.blit(self.gameovertext, ((self.wx - self.gameovertext.get_width()) / 2,
                                                     (self.wy - self.gameovertext.get_height()) / 2))  # more sketchy code
                self.screen.blit(self.gameovertext2, ((self.wx - self.gameovertext2.get_width()) / 2,
                                                      (self.wy - self.gameovertext2.get_height()) / 2 + 30))  
        
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
