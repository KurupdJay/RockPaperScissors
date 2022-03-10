import pygame
from RPSnetwork import Network
import pickle
import time
pygame.font.init()
pygame.init()



width = 650
height = 650
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

#time_passed = 0
#for x in range(1, 2048):
#    time_passed += 1
#    time.sleep(1)

paper_img = pygame.image.load('RPS_paper.png').convert_alpha()
rock_img = pygame.image.load('RPS_rock.png').convert_alpha()
scissors_img = pygame.image.load('RPS_scissors.png').convert_alpha()

class Button:
    def __init__(self, text, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.text = text
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y
        self.width = 150
        self.height = 100

    def draw(self, win):

        #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(self.image, (self.rect.x, self.rect.y))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (((self.x + round(self.width / 2) - round(text.get_width() / 2)) - 10),
                      self.y + round(self.height * 2) - round(text.get_height() * 1)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


btns = [Button("Rock", 50, 450, rock_img, .25),
        Button("Paper", 240, 445, paper_img, .2),
        Button("Scissors", 470, 450, scissors_img, .15)]


def redrawWindow(win, game, p):
    win.fill((0, 139, 0))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, (255, 0, 0), True)
        win.blit(text, (45, 200))
        #win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 52)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (28, 120))


        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (340, 120))

        font = pygame.font.SysFont("comicsans", 65)
        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (45, 200))
            win.blit(text1, (345, 200))
        else:
            win.blit(text1, (45, 200))
            win.blit(text2, (345, 200))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


def main() -> object:
    run: bool = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break
        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(1000)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255, 0, 0), True)
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255, 0, 0), True)
            else:
                text = font.render("You Lost...", 1, (255, 0, 0), True)
            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 5))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

class Time:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks()
        if game.connected():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            counting_time = pygame.time.get_ticks() - start_time

            counting_minutes = str(counting_time / 60000).zfill(2)
            counting_seconds = str((counting_time % 60000) / 1000).zfill(2)
            counting_millisecond = str(counting_time % 1000).zfill(3)

            counting_string = "%s:%s:%s" % (counting_minutes, counting_seconds, counting_millisecond)

            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render(str(counting_str), 1, (255, 0, 0), True)
            win.blit("Time Elapsed: ", counting_string, (200, 20))

            #counting_text = font.render(str(counting_string), 1, (255, 255, 255))
            #counting_rect = counting_text.get_rect(center=screen.get_rect().center)

        #screen.fill((0, 0, 0))
        #screen.blit(counting_text, counting_rect)

        pygame.display.update()

        clock.tick(25)




        #f'Time Elapsed: {time_elapsed}' (200, 20)


def menu_screen() -> object:
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0, 139, 0))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255, 0, 0), True)
        win.blit(text, (150, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()


while True:
    menu_screen()
