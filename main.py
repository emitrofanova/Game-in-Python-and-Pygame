'''
This Game consists of 3 levels. Each level has 1 robot, 10 coins and at least 1 monster. Level number = amount of monsters. 

Monsters can be on the ground or one level upper. The player can move the robot using the arrow keys from the left edge of 
the screen to the right. And up and down, but not higher than the player needs to jump over the monster. Coins fall from top 
to bottom. If a coin meets a monster on the upper level, the coin will go through it, but if it touches a monster on the 
ground, a player will lose. The player also loses if a coin touches the ground or a robot touches a monster. 

Monsters are static, but appear in random places at the beginning of the level. Coins are non static and also appear in 
random places and at random times when starting a level.

The player must collect as many coins as possible.

At the beginning, the player needs to enter his name and if the player wins or loses, the statistics of the top 10 best players 
will be shown.
'''

import pygame
import random

class Game:
    level = 1 #current level number
    total_points = 0 #points from the whole game
    levels = 3 #number of levels. number of levels = number of monsters
    try: #try to open a file with 10 best results. if there is no such file, it is created
        with open("Best results.txt", "r") as f:
            dct_results = {}
            for line in f:
                line = line.split()
                dct_results[line[0]] = int(line[1]) #dictionary {name: points, ...}
    except:
        with open("Best results.txt", "w") as f:
            dct_results = {}

    def __init__(self): #create a game
        pygame.init()
        pygame.display.set_caption("Monsters&Robot")
        self.window = pygame.display.set_mode((640, 480))
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.user_input()
        self.load_images()
        self.new_game(Game.level)
        self.main_loop()
        
    def user_input(self): #get a player's name only when game is opened for the first time. if it starts with F2 command it doesn't work
        self.name = ''
        self.window.fill((41, 153, 138))
        input_rect = pygame.Rect(170, 220, 300, 40)
        game_text = self.game_font.render("Please write your name (< 15 characters), then press Space", True, (50, 78, 168))
        self.window.blit(game_text, (320 - game_text.get_width()/2, 180))
        pygame.draw.rect(self.window, (255, 255, 255), input_rect)
        Flag = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    elif event.key == pygame.K_SPACE:
                        Flag = True
                    elif len(self.name) < 14:
                        self.name += event.unicode
                if Flag:
                    break
            if Flag:
                break
            
            pygame.draw.rect(self.window, (255, 255, 255), input_rect)
            game_text = self.game_font.render(self.name, True, (50, 78, 168))
            self.window.blit(game_text, (320 - game_text.get_width()/2, input_rect.y+5))
            pygame.display.flip()

        if self.name not in Game.dct_results: #add new player to the dictionary
            Game.dct_results[self.name] = 0

    def load_images(self): #load images for robot, monster and coin
        self.robot = pygame.image.load("robot.png")
        self.monster = pygame.image.load("monster.png")
        self.coin = pygame.image.load("coin.png")

    def new_game(self, num_m): #start a new game/level with num_m - number of monsters
        self.robot_f()
        self.coins_f()
        self.monsters_f(num_m)
        self.n = 0 #iteration counter
        self.points = 0 #points in a current level

    def robot_f(self): #robot start position
        self.to_right = False
        self.to_left = False
        self.to_down = False
        self.to_up = False
        self.x_robot = 0
        self.y_robot = 480 - self.robot.get_height()        

    def coins_f(self): #coins start positions
        self.num_coins = 10 #number of coins in each level
        self.x_coin = [random.randint(0, 640 - self.coin.get_width()) for i in range(self.num_coins)] #x-coordinate for each coin
        l = list(range(0, self.num_coins * 100, 100)) #possible time of appearance for each coin (no more than 1/100)
        random.shuffle(l) #shuffle possible time
        self.time = l[:self.num_coins] #random time of appearance for each coin
        self.coins = [] #all coins that have already appeared

    def monsters_f(self, num_m): #monsters start positions
        num_monsters = num_m
        l = list(range(self.robot.get_width() + 30, 640 - self.monster.get_width(), self.robot.get_width() + self.monster.get_width() + 50)) #possible x-coordinates for monsters
        random.shuffle(l) #shuffle possible x-coordinates
        x_monster = l[:num_monsters] #random x-coordinates for each monster
        height_monster = 480 - self.monster.get_height(), 480 - self.monster.get_height() - self.robot.get_height() - 10 #2 possible y-coordinates for each monster
        self.monsters = [(x_monster[i], height_monster[random.randint(0,1)]) for i in range(num_monsters)] #(x, y) coordinates for monsters

    def main_loop(self):
        while True:
            self.check_events()
            self.move_coins()
            self.draw_window()
            clock = pygame.time.Clock()
            clock.tick(60)
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: #robot movement
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                if event.key == pygame.K_DOWN:
                    self.to_down = True
                if event.key == pygame.K_F2: #start a new game for the same player
                    Game.level = 1
                    Game.total_points = 0
                    self.new_game(Game.level)
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE and self.game_solved(): #go to the next level
                    if Game.levels > Game.level:
                        Game.level += 1
                        self.new_game(Game.level)

            if event.type == pygame.KEYUP: #robot movement
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.to_up = False
                if event.key == pygame.K_DOWN:
                    self.to_down = False

            if event.type == pygame.QUIT:
                exit()

        self.move_robot() #robot movement

    def move_robot(self): #robot movement
        if self.to_right and self.x_robot < 640 - self.robot.get_width():
            self.x_robot += 3
        if self.to_left and self.x_robot > 0:
            self.x_robot -= 3
        if self.to_up and self.y_robot > 480 - self.monster.get_height() - self.robot.get_height() - 10:
            self.y_robot -= 3
        if self.to_down and self.y_robot < 480 - self.robot.get_height():
            self.y_robot += 3
        self.is_lose()

    def is_lose(self): #check if the robot has touched monsters
        if not self.game_solved():
            for monster in self.monsters:
                if (self.x_robot <= monster[0] <= self.x_robot + self.robot.get_width() or self.x_robot <= monster[0] + self.monster.get_width() <= self.x_robot + self.robot.get_width()) and (self.y_robot <= monster[1] <= self.y_robot + self.robot.get_height() or self.y_robot <= monster[1] + self.monster.get_height() <= self.y_robot + self.robot.get_height()):
                    self.num_coins = 0
                    self.coins = []

    def move_coins(self):
        for i in range(self.num_coins): #the coin appears if the coin is supposed to appear in this iteration
            if self.n == self.time[i]:
                self.coins.append([self.x_coin[i], -self.coin.get_height()]) #append a new coin with (x,y) coordinates
        self.n += 1
        for coin in self.coins: #movement for each coin
            if coin[1]+self.coin.get_height() < 480:
                coin[1] += 1
            #check if the robot caught the coin
            if (self.x_robot <= coin[0] <= self.x_robot + self.robot.get_width() or self.x_robot <= coin[0] + self.coin.get_width() <= self.x_robot + self.robot.get_width()) and (self.y_robot <= coin[1] + self.coin.get_height() <= self.y_robot + self.robot.get_height() or self.y_robot <= coin[1] <= self.y_robot + self.robot.get_height()):
                coin[0] = 650
                coin[1] = 490
                self.points += 1
                Game.total_points += 1
            if coin[1] + self.coin.get_height() == 480: #check if the coin is on the ground
                self.num_coins = 0
                self.coins = []

        for monster in self.monsters: #check if the monster on the ground has touched the coin
            for coin in self.coins:
                if monster[1] == 480 - self.monster.get_height():
                    if (monster[0] <= coin[0] <= monster[0] + self.monster.get_width() or monster[0] <= coin[0] + self.coin.get_width() <= monster[0] + self.monster.get_width()) and (coin[1] + self.coin.get_height()) == (480 - self.monster.get_height()):
                        self.num_coins = 0
                        self.coins = []

    def game_lose(self): #check if the player lost
        if self.num_coins == 0:
            self.best_results()
            return True
        return False

    def game_solved(self): #check if the player won
        if self.points == self.num_coins and self.num_coins != 0:
            if Game.levels == Game.level:
                self.best_results()
            return True
        return False
        
    def best_results(self): #check if this result is the best fot this player
        if Game.dct_results[self.name] <= Game.total_points:
            Game.dct_results[self.name] = Game.total_points
            self.new_best_result()

    def new_best_result(self): #overwrite the file with new 10 best results
        with open("Best results.txt", "w") as f:
            count = 1
            for res in sorted(Game.dct_results, key=Game.dct_results.get, reverse = True):
                f.write(f"{res} {Game.dct_results[res]}\n")
                if count == 10:
                    break
                count += 1

    def draw_window(self):
        self.window.fill((41, 153, 138))

        self.window.blit(self.robot, (self.x_robot, self.y_robot)) #draw monsters and coins
        for monster in self.monsters:
            self.window.blit(self.monster, (monster[0], monster[1]))
        for coin in self.coins:
            self.window.blit(self.coin, (coin[0], coin[1]))
        #draw text
        game_text = self.game_font.render("Points: " + str(self.points), True, (50, 78, 168))
        self.window.blit(game_text, (500, 30))

        game_text = self.game_font.render("Level: " + str(Game.level) + " / " +str(Game.levels), True, (50, 78, 168))
        self.window.blit(game_text, (500, 60))

        game_text = self.game_font.render(f"Total points: {Game.total_points}", True, (50, 78, 168))
        self.window.blit(game_text, (500, 80))
    
        game_text = self.game_font.render("F2 = new game", True, (50, 78, 168))
        self.window.blit(game_text, (5, 30))

        game_text = self.game_font.render("Esc = exit game", True, (50, 78, 168))
        self.window.blit(game_text, (5, 50))

        if self.game_lose(): #text and top 10 best results if player lost
            game_text = self.game_font.render("Oops! Game over...", True, (50, 78, 168))
            game_text_x = 320 - game_text.get_width() / 2
            game_text_y = 50
            pygame.draw.rect(self.window, (255, 255, 255), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))

            n = 1
            if len(Game.dct_results) > 10:
                    length = 10
            else:
                length = len(Game.dct_results)
            pygame.draw.rect(self.window, (255, 255, 255), (100, 110, 440, length * 30 + 40))

            game_text = self.game_font.render("TOP-10 players:", True, (50, 78, 168))
            self.window.blit(game_text, (320 - game_text.get_width() / 2, 120))

            for res in sorted(Game.dct_results, key=Game.dct_results.get, reverse = True):
                game_text = self.game_font.render(f"{res} - {Game.dct_results[res]}", True, (50, 78, 168))
                self.window.blit(game_text, (320 - game_text.get_width() / 2, n * 30 + 120))
                if n == 10:
                    break
                n += 1

        if self.game_solved():
            if Game.levels > Game.level:  #text if player win the level
                game_text = self.game_font.render("Congratulations, you solved the level!", True, (50, 78, 168))
                game_text_x = 320 - game_text.get_width() / 2
                game_text_y = 240 - game_text.get_height() / 2
                pygame.draw.rect(self.window, (255, 255, 255), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
                self.window.blit(game_text, (game_text_x, game_text_y))

                game_text = self.game_font.render("Space = go to a new level", True, (50, 78, 168))
                self.window.blit(game_text, (320 - game_text.get_width() / 2, 280))
            elif Game.levels == Game.level:  #text and top 10 best results if player win the game
                game_text = self.game_font.render(f"Congratulations, you solved the GAME!", True, (50, 78, 168))
                game_text_x = 320 - game_text.get_width() / 2
                game_text_y = 50
                pygame.draw.rect(self.window, (255, 255, 255), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
                self.window.blit(game_text, (game_text_x, game_text_y))
                
                n = 1
                if len(Game.dct_results) > 10:
                    length = 10
                else:
                    length = len(Game.dct_results)
                pygame.draw.rect(self.window, (255, 255, 255), (100, 110, 440, length * 30 + 40))

                game_text = self.game_font.render("TOP-10 players:", True, (50, 78, 168))
                self.window.blit(game_text, (320 - game_text.get_width() / 2, 120))

                for res in sorted(Game.dct_results, key=Game.dct_results.get, reverse = True):
                    game_text = self.game_font.render(f"{res} - {Game.dct_results[res]}", True, (50, 78, 168))
                    self.window.blit(game_text, (320 - game_text.get_width() / 2, n * 30 + 120))
                    if n == 10:
                        break
                    n += 1

        pygame.display.flip()
        

if __name__ == "__main__":
    Game()
