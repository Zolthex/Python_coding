import pygame, sys
from pygame.locals import *

# Initiates pygame and clock-set start
pygame.init()
clock = pygame.time.Clock()
# Initiates pygame and clock-set end

# Graphic initialisation begin
WINDOW_SIZE = (1280,720)
pygame.display.set_caption("Kira's Quest")
screen = pygame.display.set_mode(WINDOW_SIZE,0,32) # initiate the window
display = pygame.Surface((300,200)) # used as the surface for rendering, which is scaled
# Graphic initialisation end

# Sound initialisation begin
sound = pygame.mixer.Sound("Sounds/Background2.mp3")
pygame.mixer.Sound.set_volume(sound, 0.12)
pygame.mixer.Sound.play(sound)

sound2 = pygame.mixer.Sound("Sounds/Background.mp3")
pygame.mixer.Sound.set_volume(sound2, 0.12)
# Sound initialisation end

# Movement and scroll variables begin
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
flag = False
true_scroll = [0,0]
# Movement and scroll variables end

# Condition variables begin
end_condition = False
init_end = True
first_rum = True
runs = 1
# Condition variables end

# Credit-text variable begin
text_list_end = '''
In a world far far away
Kira searching for Saya.
She was kidnapped days ago.

"Kitsuna Haru" the evil witch 
hide Saya in a castle near by 
and force Kira to leave his home.

After running around looking for her
he found many castles to trap him. 
Than he found the right one.

Inside many enemies waiting for him
and hidden traps taken all his mind.
At last he found Kitsuna in her throne room.

A tough fight ensues but Kira wins.
In a hidden room behind a painting
he found his lost Saya. He's happy.

Kitsuna will been punished soon
and Kira and Saya will continue
their lifes in freedom and pease.

--- THE END ---
'''.split('\n')

text_list = '''
Sorry Kira but Saya isn't here
a bird twitter down form a tree.

Look at the next Level, maybe
with luck you can find her there.

--- Next Level ---
'''.split('\n')
# Credit-text variable end

# Graphic objects variable start
grass_img = pygame.image.load('grass.png')
dirt_img = pygame.image.load('dirt.png')
pipe_img = pygame.image.load('pipe.png')
flag_img = pygame.image.load('flag.png')
chest_img = pygame.image.load('chest.png')
root_img = pygame.image.load('plantroot.png')
style_img = pygame.image.load('plantstyle.png')
head_img = pygame.image.load('planthead.png')

player_img = pygame.image.load('player_char.png').convert()
player_img.set_colorkey((255,255,255))

player_rect = pygame.Rect(100,100,12,21)

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
# Graphic objects variable end

# Load Game-Map start
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map("map1")  #Map 2: Minimal time 44 Seconds
# Load Game-Map end

# Collision routine start
def collision_test(rect,tiles):
    global flag
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect,movement,tiles):
    collision_types = {'top':False,'bottom':False,'right':False,'left':False}
    rect.x += movement[0]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect,tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
# Collision routine end


# Credit routine start
class Credits:
    def __init__(self, screen_rect, lst):
        self.srect = screen_rect
        self.lst = lst
        self.size = 24
        self.color = (255, 0, 0)
        self.buff_centery = self.srect.height / 2 + 5
        self.buff_lines = 40
        self.timer = 0.0
        self.delay = 30
        print("Credits start!")
        self.make_surfaces()
        print("Credits finished!")

    def make_text(self, message):
        font = pygame.font.SysFont('Arial', self.size)
        text = font.render(message, True, self.color)
        rect = text.get_rect(center=(self.srect.centerx, self.srect.centery + self.buff_centery))
        #print("Text ready! Text: ", message)
        return text, rect

    def make_surfaces(self):
        self.text = []
        for i, line in enumerate(self.lst):
            l = self.make_text(line)
            l[1].y += i * self.buff_lines
            self.text.append(l)


    def update(self):
        if pygame.time.get_ticks() - self.timer > self.delay:
            self.timer = pygame.time.get_ticks()
            for text, rect in self.text:
                rect.y -= 2


    def render(self, surf):
        """
        image = pygame.image.load("verloren.png").convert()
        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = image.get_rect()
        group = pygame.sprite.Group()
        """
        for text, rect in self.text:
            """
            sprite.image.blit(text, sprite.rect)
            group.add(sprite)
            
            surf.blit(text, rect)
            surf.blit(verlorenBild, (0, 20))
            """
            surf.blit(text, rect)
        """
        group.draw(screen)
        pygame.display.flip()
        """


# Credit routine end


# Main Program / Loop begin
while True:
    screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window
    player_img.set_colorkey((255, 255, 255))
    player_rect = pygame.Rect(150, 100, 12, 21)
    background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

    mapname = "map" + str(runs)
    print(mapname)
    game_map = load_map(mapname)

    count = 76
    restart = 76
    mem = 76
    checkpoint = False
    endpoint = False
    x_point = 5375

    if not first_rum:
        pygame.mixer.Sound.stop(sound2)
        pygame.mixer.Sound.play(sound)
        end_condition = False

    while not end_condition:  # game loop
        ##--Background-Sound Start--##
        if int(count) == 76:
            print("Sound starts!!")
        elif mem > int(count):
            if int(count) in [10, 20, 30, 40, 50, 60, 70]:
                print(int(count), "Seconds to Sound-Repeat")
            """else:
                print(int(count))"""
        mem = int(count)
        if count <= 1:
            count = restart
            print("Restart Sound!!")
            pygame.mixer.Sound.play(sound)
        ##--Background-Sound End--##

        display.fill((146,244,255)) # clear screen by filling it with blue

        true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        true_scroll[1] += (player_rect.y-true_scroll[1]-106)/20
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
        for background_object in background_objects:
            obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
            if background_object[0] == 0.5:
                pygame.draw.rect(display,(14,222,150),obj_rect)
                pygame.draw.rect(display, (14,222,150), obj_rect)
            else:
                pygame.draw.rect(display,(9,91,85),obj_rect)

        tile_rects = []
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == '1':
                    display.blit(dirt_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '2':
                    display.blit(grass_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '3':
                    display.blit(pipe_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '4':
                    display.blit(flag_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '5':
                    display.blit(chest_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '6':
                    display.blit(root_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '7':
                    display.blit(style_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile == '8':
                    display.blit(head_img,(x*16-scroll[0],y*16-scroll[1]))
                if tile != '0':
                    tile_rects.append(pygame.Rect(x*16,y*16,16,16))
                x += 1
            y += 1

        player_movement = [0,0]
        if moving_right == True:
            if player_rect.x < 5380:
                player_movement[0] += 2
        if moving_left == True:
            if player_rect.x > 152:
                player_movement[0] -= 2
        player_movement[1] += vertical_momentum
        vertical_momentum += 0.2
        if vertical_momentum > 3:
            vertical_momentum = 3

        player_rect,collisions = move(player_rect,player_movement,tile_rects)
        #print("Player-X: ", player_rect.x)
        """
        if player_rect.x > 5250:
            if x_point <= player_rect.x:
                print("Player-X: ", player_rect.x)
                x_point += 1
        """

        if collisions['bottom'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 1

        if collisions['top'] == True:
            air_timer = 0
            vertical_momentum = 0
        else:
            air_timer += 0.5

        if player_rect.x > 420 and player_rect.x < 447:
            if not checkpoint:
                print("Checkpoint!")
                checkpoint= True

        if player_rect.x > 5379:
            if not endpoint:
                print("Its done!")
                print("You need ", int(restart - count), "seconds to finish the Level")
                endpoint = True

        #if collisions['right'] == True:
            #for layer in game_map:
             #   for tile in layer:
              #      if tile == '4':
           #ok = False
           #for tile in tile_rects:
            #   if player_rect.colliderect(tile):
             #      if tile == '4':
              #         ok = True
           #if ok:
            #    flag = True
           #if flag == True:
            #    print("Sieg!!!")

        display.blit(player_img,(player_rect.x-scroll[0],player_rect.y-scroll[1]))

        for event in pygame.event.get(): # event loop
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_UP or event.key == K_SPACE:
                    if air_timer < 6:
                        vertical_momentum = -5
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False

        screen.blit(pygame.transform.scale(display,WINDOW_SIZE),(0,0))
        pygame.display.update()
        clock.tick(60)
        count -= 0.01667

        if player_rect.y >= 230 or player_rect.x > 5379:

            """
            screen = pygame.display.set_mode([1200, 595])
            screen.blit(verlorenBild, (0, 0))
            """

            cred_screen = pygame.display.set_mode((1200,595))  # 800,600
            screen_rect = cred_screen.get_rect()
            if runs < 3:
                cred = Credits(screen_rect, text_list)
            elif runs == 3:
                cred = Credits(screen_rect, text_list_end)

            pygame.mixer.Sound.stop(sound)
            pygame.mixer.Sound.play(sound2)

            end_condition = True
            if runs < 3:
                c_count = 850
            elif runs == 3:
                c_count = 1200

            if not first_rum:
                init_end = True


    while init_end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        c_count -= 0.01667

        if not c_count <= 0:
            screen.fill((0, 0, 0))
            #image = pygame.image.load("verloren.png").convert()
            #cred_screen.blit(image, (0, 0))
            cred.update()
            cred.render(cred_screen)
            pygame.display.update()
        else:
            pygame.mixer.Sound.stop(sound2)
            end_condition = False
            init_end = False
            first_rum = False
            moving_right = False
            if runs < 3:
                runs += 1
            else:
                runs = 1
# Main Program / Loop end
