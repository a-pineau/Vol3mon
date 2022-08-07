"""Implements the game loop and handles the user's events."""

import os
import time
import pygame as pg

from itertools import cycle
from player import Player
from ball import Ball
from bot import Bot
from obstacle import Obstacle
from settings import *
from os.path import join, dirname, abspath

vec = pg.math.Vector2
n_snap = 0

# Manually places the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 50)

class Game:
    def __init__(self) -> None:
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode([WIDTH, HEIGHT])
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.last_time = time.time()
        self.running = True  
        self.record = False
        self.start_round = False
        self.stop_timer = False
        self.n_frame = 0
        self.scores = {"Player": 0, "Bot": 0}
    
    def new(self):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        try:
            os.makedirs(SNAP_FOLDER)
        except FileExistsError:
            print(f"Folder \"{SNAP_FOLDER}\" already exists. Ignoring.")
        if os.path.isdir(SNAP_FOLDER):
            for file_name in os.listdir(SNAP_FOLDER):
                file = os.path.join(SNAP_FOLDER, file_name)
                os.remove(file)
        # Defining sprite groups
        self.balls = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        # Defining balls
        self.player = Player(self, *PLAYER_SETTINGS) # Player
        self.ball = Ball(self, *BALL_SETTINGS) # Ball  
        self.bot = Bot(self, *BOT_SETTINGS) # Bot
        # Defining obstacles
        self.net = Obstacle(self, *NET_SETTINGS) # Net
        self.bottom = Obstacle(self, WIDTH*0.5, HEIGHT, WIDTH, 1) # Bottom border
        self.top = Obstacle(self, WIDTH*0.5, 1, WIDTH-1, 1) # Top border
        self.left = Obstacle(self, -1, HEIGHT*0.5, 1, HEIGHT) # Left border
        self.right = Obstacle(self, WIDTH, HEIGHT*0.5, 1, HEIGHT) # Right border
        # Adding to sprite groups
        self.balls.add(
            self.player, 
        )
        self.obstacles.add(
            self.net, 
            self.bottom, 
            self.top, 
            self.left,  
            self.right,
        )
        # Doing the first ball drop
        self.ball.drop()
        self.bot.predict_move()
    
    def delta_time(self):
        current_time = time.time()
        self.dt = current_time - self.last_time
        self.last_time = current_time
    
    def run(self):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        self.playing = True
        ball_init = cycle([BOT_INIT_X, PLAYER_INIT_X])
        while self.playing: 
            self.n_frame += 1
            # self.delta_time()
            self.dt = self.clock.tick(FPS)*1e-3
            self.events()
            self.update(ball_init) 
            self.display()
    
    def update(self, ball_init):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        if self.start_round:
            if not self.stop_timer: 
                self.timer += self.dt
            self.balls.update()
            self.obstacles.update()
            for sprite in self.balls.sprites():
                if sprite.end_round_conditions():
                    self.start_round = False
                    self.setup_round(next(ball_init))
                    return None
                    
    def events(self):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if self.start_round:
                        self.player.jump()
                    else:
                        self.start_round = True
                        self.timer = 0
                elif event.key == pg.K_q:
                    if self.playing:
                        self.playing = False
                    self.running = False

    def setup_round(self, ball_init_x):
        """
        TODO
        """
        # Ball game
        self.ball.pos.x = ball_init_x
        self.ball.pos.y = BALL_INIT_Y
        self.ball.vel = vec(BALL_INIT_VEL_X, BALL_INIT_VEL_Y)
        self.ball.drop() 
        # Player
        self.player.pos.x = PLAYER_INIT_X
        self.player.pos.y = PLAYER_INIT_Y
        self.player.vel = vec(0, 0)
        # Bot
        self.bot.pos.x = BOT_INIT_X
        self.bot.pos.y = BOT_INIT_Y
        self.bot.vel = vec(0, 0)
        self.bot.predict_move()
                             
    def display(self):
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        self.screen.fill(BACKGROUND)
        for ball in self.balls.sprites():
            pg.draw.circle(self.screen, ball.color, ball.pos, ball.r)
        self.obstacles.draw(self.screen)
        if not self.start_round:
            self.display_message(self.screen, *START_ROUND_SETTINGS)
        self.display_infos()
        if self.record:
            self.record_game()
        pg.display.flip()  

    def display_infos(self): 
        """
        TODO

        Parameters
        ----------

        Returns
        -------
        """
        # Player text (top-left)
        player_font = pg.font.SysFont("Calibri", 40)
        player_text = player_font.render("Player", True, RED)
        player_text_rect = player_text.get_rect(topleft=(WIDTH*0.005, 5))
        # Bot text (top-left)
        bot_font = pg.font.SysFont("Calibri", 40)
        bot_text = bot_font.render("Bot", True, BLUE)
        bot_text_rect = bot_text.get_rect(topright=(WIDTH*0.995, 5))
        # FPS (top-center)
        n_fps = int(self.clock.get_fps())
        fps_font = pg.font.SysFont("Calibri", 23)
        fps_text = fps_font.render(f"FPS: {n_fps}", True, WHITE)
        fps_text_rect = fps_text.get_rect()
        fps_text_rect.centerx = WIDTH*0.5
        fps_text_rect.top = 55
        # Current score (top-center)
        score_player, score_bot = self.scores["Player"], self.scores["Bot"]
        font_scores = pg.font.SysFont("Calibri", 50)
        scores_text = font_scores.render(
            f"{score_player}   -   {score_bot}", 
            True, 
            WHITE)
        scores_text_rect = scores_text.get_rect()
        scores_text_rect.centerx = WIDTH*0.5
        scores_text_rect.top = 5 
        # Drawing to screen
        self.screen.blit(player_text, player_text_rect)
        self.screen.blit(bot_text, bot_text_rect)
        self.screen.blit(fps_text, fps_text_rect)
        self.screen.blit(scores_text, scores_text_rect)

    def record_game(self) -> None:
        """Save a snapshot of the current screen to the SNAP_FOLDER.

        Parameter
        ---------
        screen: pygame.Surface (required)
            Game window
        """

        global n_snap
        extension = "png"
        file_name = f"snapshot_{n_snap}.{extension}"
        pg.image.save(self.screen, os.path.join(SNAP_FOLDER, file_name))
        n_snap += 1

    @staticmethod
    def display_message(screen, message, font_size, color, position):
        """
        TODO
        """ 
        font = pg.font.SysFont("Calibri", font_size)
        text = font.render(message, True, color)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.top = position
        screen.blit(text, text_rect)

def main():
    g = Game()
    while g.running:
        g.new()
        g.run()
    pg.quit()

if __name__ == "__main__":
    main()