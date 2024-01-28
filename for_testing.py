import pygame
import math
import random


class Button:
    def __init__(self, text, size, left_up_pos, font_size=96, distance=20):
        self.distance = distance
        self.text = text
        self.size = size
        self.position = left_up_pos
        self.font_size = font_size

    def render(self, screen):
        if player.player_coords[0] >= self.position[0] and player.player_coords[0] < self.position[0] + self.size[0]:
            if player.player_coords[1] >= self.position[1] and player.player_coords[1] < self.position[1] + self.size[1]:
                pygame.draw.rect(screen, (color_for_locations, color_for_locations, color_for_locations), (self.position[0], self.position[1], self.size[0], self.size[1]), width=5)
        font = pygame.font.SysFont(None, self.font_size)
        img = font.render(self.text, True, (color_for_locations, color_for_locations, color_for_locations))
        screen.blit(img, (self.position[0] + self.distance, self.position[1] + self.distance))

class info_bar:
    def __init__(self, entity, size, left_up_pos):
        self.entity = entity
        self.size = size
        self.position = left_up_pos

    def render(self, screen, current_position):
        if self.entity == boss:
            health_lenth = 84 *  boss.boss_health / 500
            pygame.draw.rect(screen, "white", (current_position[0] - 50, current_position[1] - 57, self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (current_position[0] - 47, current_position[1] - 54, health_lenth, self.size[1] - 6), width=0)

        if self.entity == player:
            health_lenth = 34 *  player.player_health / 100
            pygame.draw.rect(screen, "white", (player.player_coords[0] - 20, player.player_coords[1] - 35, self.size[0], self.size[1]), width=3)
            pygame.draw.rect(screen, "white", (player.player_coords[0] - 17, player.player_coords[1] - 32, health_lenth, self.size[1] - 6), width=0)


class Player:
    def __init__(self, player_coords):
        self.homing = False
        self.player_coords = player_coords
        self.movement_speed = [0, 0]
        self.player_health = 100
        self.shot_reload = 0
        self.bullet_spread = 0.01
        self.bullet_life_time = 100
        self.bullet_speed = 2
        self.way = [0, 0]
        self.aim_dash = False
        self.movement_direction_history = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
        self.last_direction = [0, 0]
        self.sprite_counter = 0   
        self.lookng_way = "right"
        self.keys = []
    
    def player_movment(self, movement_button, movment_type):
        global current_location
        global running
        if movment_type == pygame.KEYDOWN:
            if movement_button == pygame.K_w:
                movement_speed[1] -= 5
                self.way[1] -= 1
            if movement_button == pygame.K_s:
                movement_speed[1] += 5
                self.way[1] += 1
            if movement_button == pygame.K_a:
                movement_speed[0] -= 5
                self.way[0] -= 1
            if movement_button == pygame.K_d:
                movement_speed[0] += 5
                self.way[0] += 1
            if movement_button == pygame.K_SPACE:
                self.aim_dash = True

            if movement_button == pygame.K_e:
                if current_location == "main":
                    if self.player_coords[0] >= 300 and self.player_coords[0] <= 500:
                        if self.player_coords[1] >= 200 and self.player_coords[1] <= 300:
                            location_switch()
                            current_location = "battle"
                if current_location == "main":
                    if self.player_coords[0] >= 300 and self.player_coords[0] <= 500:
                        if self.player_coords[1] >= 460 and self.player_coords[1] <= 560:
                            location_switch()
                            running = False
                if current_location == "main":
                    if self.player_coords[0] >= 300 and self.player_coords[0] <= 500:
                        if self.player_coords[1] >= 330 and self.player_coords[1] <= 430:
                            location_switch()
                            current_location = "store"
                if current_location == "start":
                    if self.player_coords[0] >= 85 and self.player_coords[0] <= 715:
                        if self.player_coords[1] >= 350 and self.player_coords[1] <= 450:
                            location_switch()
                            current_location = "main"
                if current_location == "store":
                    if self.player_coords[0] >= 30 and self.player_coords[0] <= 130:
                        if self.player_coords[1] >= 730 and self.player_coords[1] <= 780:
                            location_switch()
                            current_location = "main"
                                     
        elif movment_type == pygame.KEYUP:
            if movement_button == pygame.K_w:
                movement_speed[1] += 5
                self.way[1] += 1
            if movement_button == pygame.K_s:
                movement_speed[1] -= 5
                self.way[1] -= 1
            if movement_button == pygame.K_a:
                movement_speed[0] += 5
                self.way[0] += 1
            if movement_button == pygame.K_d:
                movement_speed[0] -= 5
                self.way[0] -= 1
            if movement_button == pygame.K_SPACE:
                self.aim_dash = False
                for i in range(1, 14):
                    pygame.draw.circle(screen, ("white"), (self.player_coords[0] + 10 * i * self.last_direction[0], self.player_coords[1] + 10 * i * self.last_direction [1]), 15)
                
                self.player_coords[0] += 140 * self.last_direction[0]
                self.player_coords[1] += 140 * self.last_direction[1]
            self.keys = pygame.key.get_pressed()
    
    def player_render(self, screen):
        if self.shot_reload > 0:
            self.shot_reload -= 1
        if player.player_coords[0] > 775:
            player.player_coords[0] = 775
        if player.player_coords[1] > 775:
            player.player_coords[1] = 775
        if player.player_coords[0] < 35:
            player.player_coords[0] = 35
        if player.player_coords[1] < 35:
            player.player_coords[1] = 35
        self.sprite_counter += 1
        if movement_speed[0] > 0 or movement_speed[0] == 0 and self.lookng_way == "right"  and movement_speed[1] != 0:
            self.lookng_way = "right"
            if self.sprite_counter <= 10:
                player_right_stand.rect.x = player.player_coords[0] - 25
                player_right_stand.rect.y = player.player_coords[1] - 30
                player_right_stand_group.draw(screen)
            elif self.sprite_counter > 10 and self.sprite_counter <= 20:
                player_right_walk1.rect.x = player.player_coords[0] - 25
                player_right_walk1.rect.y = player.player_coords[1] - 30
                player_right_walk1_group.draw(screen)
            elif self.sprite_counter > 20 and self.sprite_counter <= 30:
                player_right_walk2.rect.x = player.player_coords[0] - 25
                player_right_walk2.rect.y = player.player_coords[1] - 30
                player_right_walk2_group.draw(screen)
        if movement_speed[0] < 0 or movement_speed[0] == 0 and self.lookng_way == "left" and movement_speed[1] != 0:
            self.lookng_way = "left"
            if self.sprite_counter <= 10:
                player_left_stand.rect.x = player.player_coords[0] - 25
                player_left_stand.rect.y = player.player_coords[1] - 30
                player_left_stand_group.draw(screen)
            elif self.sprite_counter > 10 and self.sprite_counter <= 20:
                player_left_walk1.rect.x = player.player_coords[0] - 25
                player_left_walk1.rect.y = player.player_coords[1] - 30
                player_left_walk1_group.draw(screen)
            elif self.sprite_counter > 20 and self.sprite_counter <= 30:
                player_left_walk2.rect.x = player.player_coords[0] - 25
                player_left_walk2.rect.y = player.player_coords[1] - 30
                player_left_walk2_group.draw(screen)
        if movement_speed[0] == 0 and self.lookng_way == "left" and movement_speed[1] == 0:
            player_left_stand.rect.x = player.player_coords[0] - 25
            player_left_stand.rect.y = player.player_coords[1] - 30
            player_left_stand_group.draw(screen)
        if movement_speed[0] == 0 and self.lookng_way == "right" and movement_speed[1] == 0:
            player_right_stand.rect.x = player.player_coords[0] - 25
            player_right_stand.rect.y = player.player_coords[1] - 30
            player_right_stand_group.draw(screen)
        if self.sprite_counter == 30:
            self.sprite_counter = 0

class Boss:
    def __init__(self, boss_coords):
        self.boss_coords = boss_coords
        self.boss_health = 500
        self.bullet_reload = 300
        self.bullet_spread = 0.1
        self.bullet_life_time = 100
        self.r = 1
        self.y_inert = 0
        self.x_inert = 0
        self.bullet_speed = 1
    
    def boss_movement(self):
        x_lengh = self.boss_coords[0] - player.player_coords[0]
        y_lengh = self.boss_coords[1] - player.player_coords[1]
        if self.boss_coords[1] > player.player_coords[1]:
            self.he = -1
        else:
            self.he = 1
        if x_lengh != 0:
            self.yx = y_lengh / x_lengh
        else:
            self.yx = y_lengh / 1
        self.g = (y_lengh ** 2 + x_lengh ** 2) ** 0.5
        self.an = math.asin(x_lengh / self.g)
        if self.g < 650:
            self.r = -1
        elif self.g > 650:
            self.r = 1
        #if self.g > 500:
        self.x_inert += 1 * math.sin(self.an) * 5 * -1 * 0.002 * ((self.g / 100 ) ** 2)
        self.y_inert += math.cos(self.an) * 5 * self.he * 0.002 * ((self.g / 100 ) ** 2)
        self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5

        if self.inert_g > 6:
            self.x_inert /= self.inert_g / 6
            self.y_inert /= self.inert_g / 6
        self.boss_coords[0] += self.x_inert + (1 * math.sin(self.an) * 5 * -1 * self.r * 0.6) 
        self.boss_coords[1] += self.y_inert + (math.cos(self.an) * 5 * self.he * self.r * 0.6) 

        if boss.boss_coords[0] > 760:
            boss.boss_coords[0] = 760
        if boss.boss_coords[1] > 760:
            boss.boss_coords[1] = 760
        if boss.boss_coords[0] < 40:
            boss.boss_coords[0] = 40
        if boss.boss_coords[1] < 40:
            boss.boss_coords[1] = 40

    
    def boss_render(self, screen):
        boss_right.rect.x = self.boss_coords[0] - 45
        boss_right.rect.y = self.boss_coords[1] - 45
        boss_left.rect.x = self.boss_coords[0] - 45
        boss_left.rect.y = self.boss_coords[1] - 45
        #pygame.draw.circle(screen, ("green"), self.boss_coords, 50)
        if self.bullet_reload == 0:
            self.bullet_reload = 60
            bullet = Bullet(self.boss_coords, player.player_coords, boss)
            bullet_storage.append(bullet)
            bullet = Bullet(self.boss_coords, player.player_coords, boss, 0.3)
            bullet_storage.append(bullet)
            bullet = Bullet(self.boss_coords, player.player_coords, boss, -0.3)
            bullet_storage.append(bullet)
        else:
            self.bullet_reload -= 1
        if boss.boss_coords[0] >= player.player_coords[0]:
            boss_left_group.draw(screen)
        else:
            boss_right_group.draw(screen)

class Bullet:
    def __init__(self, current_pos, end_pos, bullet_owner, ang_ch=0, size1=6):
        self.current_pos = current_pos.copy()
        self.effects_pos1 = self.current_pos
        self.effects_pos2 = self.current_pos
        self.effects_pos3 = self.current_pos
        self.effects_pos4 = self.current_pos
        self.effects_pos5 = self.current_pos
        self.effects_pos6 = self.current_pos
        self.bullet_owner = bullet_owner
        self.size = size1
        self.x_inert = 0
        self.y_inert = 0
    
        self.end_pos = end_pos
        
        self.bullet_appear = True
        self.lifetime = bullet_owner.bullet_life_time
        x_lengh = self.current_pos[0] - self.end_pos[0]
        y_lengh = self.current_pos[1] - self.end_pos[1]
        self.ang_ch = ang_ch
        try:
            self.yx = y_lengh / x_lengh
            self.g = (y_lengh ** 2 + x_lengh ** 2) ** 0.5
            if current_pos[1] > end_pos[1]:
                self.he = -1
            else:
                self.he = 1
            self.an = math.asin(x_lengh / self.g) + random.uniform(- bullet_owner.bullet_spread, bullet_owner.bullet_spread) + self.ang_ch
        except:
            self.bullet_appear = False
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), self.size)
            
        
    def render(self, screen):
        if self.bullet_owner == player and player.homing:
            x_lengh1 = self.current_pos[0] - boss.boss_coords[0]
            y_lengh1 = self.current_pos[1] - boss.boss_coords[1]
            if self.current_pos[1] > boss.boss_coords[1]:
                self.he1 = -1
            else:
                self.he1 = 1
            self.yx1 = y_lengh1 / x_lengh1
            self.g1 = (y_lengh1 ** 2 + x_lengh1 ** 2) ** 0.5
            self.an1 = math.asin(x_lengh1 / self.g1)
            self.x_inert += math.sin(self.an1) / self.g1 * 100 * -1
            self.y_inert += math.cos(self.an1) * self.he1 / self.g1 * 100 * 1
            #self.inert_g = (self.x_inert ** 2 + self.y_inert ** 2) ** 0.5

        self.current_pos[0] += self.bullet_owner.bullet_speed * math.sin(self.an) * 5 * -1 + self.x_inert
        self.current_pos[1] += self.bullet_owner.bullet_speed * math.cos(self.an) * 5 * self.he + self.y_inert
        pygame.draw.circle(screen, ("green"), (int(self.current_pos[0]), int(self.current_pos[1])), self.size)
        self.effects_pos6 = self.effects_pos5
        self.effects_pos5 = self.effects_pos4
        self.effects_pos4 = self.effects_pos3
        self.effects_pos3 = self.effects_pos2
        self.effects_pos2 = self.effects_pos1
        self.effects_pos1 = self.current_pos.copy()
        pygame.draw.circle(screen, (105, 214, 130), (self.effects_pos3), self.size - 1)
        pygame.draw.circle(screen, (121, 212, 142), (self.effects_pos5), self.size - 2)
        pygame.draw.circle(screen, (148, 212, 163), (self.effects_pos6), self.size - 3)
        self.lifetime -= 1
        if self.lifetime == 0:
            self.bullet_appear = False
        if self.current_pos[1] == self.end_pos[1] and self.current_pos[0] == self.end_pos[0]:
            self.bullet_appear = False
        if self.current_pos[0] - boss.boss_coords[0] >= -38 and self.current_pos[0] - boss.boss_coords[0] <= 38 and self.bullet_owner == player and boss_render == True:
            if self.current_pos[1] - boss.boss_coords[1] >= -38 and self.current_pos[1] - boss.boss_coords[1] <= 38:
                self.bullet_appear = False
                boss.boss_health -= 15
        if self.current_pos[0] - player.player_coords[0] >= -15 and self.current_pos[0] - player.player_coords[0] <= 15 and self.bullet_owner == boss:
            if self.current_pos[1] - player.player_coords[1] >= -15 and self.current_pos[1] - player.player_coords[1] <= 15:
                self.bullet_appear = False
                player.player_health -= 15


def location_switch():
    global color_for_locations
    while color_for_locations > 1:
        color_for_locations -= 2
        if current_location == "main":
            main_menu()
        if current_location == "start":
            start_location()
        if current_location == "store":
            store_location()


def store_location():
    global running
    global bullet_appear
    global boss_render
    
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.player_movment(event.key, event.type)
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0]:
        if player.shot_reload == 0:
                
            end_pos = [pos[0], pos[1]]
            bullet_appear = True
            bullet = Bullet(player.player_coords, end_pos, player) 
            bullet_storage.append(bullet)
            player.shot_reload = 30

    store_exit_button.render(screen)

    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)


    if not player.way == [0, 0]:
        p = player.way[::]
        player.movement_direction_history.append(p)

        player.movement_direction_history = player.movement_direction_history[-5:]

    player.last_direction = player.movement_direction_history[-3]

            
    if player.aim_dash:
        pygame.draw.circle(screen, ("white"), (player.player_coords[0] + 140 * player.last_direction[0], player.player_coords[1] + 140 * player.last_direction[1]), 6)
    for elem in bullet_storage:
        if elem.bullet_appear == True:
            elem.render(screen)
        else:
            bullet_storage.remove(elem)

    pygame.display.flip()
    clock.tick(50)


def start_location():
    global running
    global bullet_appear
    global boss_render
    
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.player_movment(event.key, event.type)
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0]:
        if player.shot_reload == 0:
                
            end_pos = [pos[0], pos[1]]
            bullet_appear = True
            bullet = Bullet(player.player_coords, end_pos, player) 
            bullet_storage.append(bullet)
            player.shot_reload = 30

    first_button.render(screen)

    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)


    if not player.way == [0, 0]:
        p = player.way[::]
        player.movement_direction_history.append(p)

        player.movement_direction_history = player.movement_direction_history[-5:]

    player.last_direction = player.movement_direction_history[-3]

            
    if player.aim_dash:
        pygame.draw.circle(screen, ("white"), (player.player_coords[0] + 140 * player.last_direction[0], player.player_coords[1] + 140 * player.last_direction[1]), 6)
    for elem in bullet_storage:
        if elem.bullet_appear == True:
            elem.render(screen)
        else:
            bullet_storage.remove(elem)

    pygame.display.flip()
    clock.tick(50)

def main_menu():
    global running
    global bullet_appear
    global boss_render
    
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.player_movment(event.key, event.type)
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0]:
        if player.shot_reload == 0:
                
            end_pos = [pos[0], pos[1]]
            bullet_appear = True
            bullet = Bullet(player.player_coords, end_pos, player) 
            bullet_storage.append(bullet)
            player.shot_reload = 30

    start_button.render(screen)
    store_button.render(screen)
    exit_button.render(screen)

    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)


    if not player.way == [0, 0]:
        p = player.way[::]
        player.movement_direction_history.append(p)

        player.movement_direction_history = player.movement_direction_history[-5:]

    player.last_direction = player.movement_direction_history[-3]

            
    if player.aim_dash:
        pygame.draw.circle(screen, ("white"), (player.player_coords[0] + 140 * player.last_direction[0], player.player_coords[1] + 140 * player.last_direction[1]), 6)
    for elem in bullet_storage:
        if elem.bullet_appear == True:
            elem.render(screen)
        else:
            bullet_storage.remove(elem)

    pygame.display.flip()
    clock.tick(50)


def battle_field():
    global running
    global bullet_appear
    global boss_render
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player.player_movment(event.key, event.type)
    pressed = pygame.mouse.get_pressed()
    pos = pygame.mouse.get_pos()
    if pressed[0]:
        if player.shot_reload == 0:
                
            end_pos = [pos[0], pos[1]]
            bullet_appear = True
            bullet = Bullet(player.player_coords, end_pos, player) 
            bullet_storage.append(bullet)
            player.shot_reload = 30
        
    player.player_coords[0] += movement_speed[0]
    player.player_coords[1] += movement_speed[1]
    player.player_render(screen)
    player_healthbar.render(screen, player.player_coords)

    if boss_render == True:
        boss.boss_movement() 
        boss.boss_render(screen)
        boss_healthbar.render(screen, boss.boss_coords)
    if boss.boss_health <= 0:
        boss_render = False

    if not player.way == [0, 0]:
        p = player.way[::]
        player.movement_direction_history.append(p)

        player.movement_direction_history = player.movement_direction_history[-5:]

    player.last_direction = player.movement_direction_history[-3]

            
    if player.aim_dash:
        pygame.draw.circle(screen, ("white"), (player.player_coords[0] + 140 * player.last_direction[0], player.player_coords[1] + 140 * player.last_direction[1]), 6)
    for elem in bullet_storage:
        if elem.bullet_appear == True:
            elem.render(screen)
        else:
            bullet_storage.remove(elem)
    pygame.display.flip()
    clock.tick(50)

if __name__ == '__main__': 
    pygame.init()
    pygame.display.set_caption('Тестовое')
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    running = True
    boss_render = True
    bullet_storage = []
    current_location = "start"
    color_for_locations = 255

    v = 20  # пикселей в секунду
    fps = 60
    clock = pygame.time.Clock()

    start_player_coords = [200, 200]
    start_boss_coordinates = [700, 700]
    movement_speed = [0, 0]
    player = Player(start_player_coords)
    boss = Boss(start_boss_coordinates)
    boss_healthbar = info_bar(boss, (90, 10), (200, 10))
    player_healthbar = info_bar(player, (40, 10), (10, 10))

    first_button = Button("Press E to interact", [630, 100], [85, 350])
    start_button = Button("Start", [200, 100], [300, 200])
    store_button = Button("Store", [200, 100], [300, 330])
    exit_button = Button("Exit", [200, 100], [300, 460])
    store_exit_button = Button("Exit", [100, 50], [30, 730], 54, 10)

    # спрайты
    boss_left_group = pygame.sprite.Group()
    boss_right_group = pygame.sprite.Group()

    player_left_stand_group = pygame.sprite.Group()
    player_right_stand_group = pygame.sprite.Group()
    player_left_walk1_group = pygame.sprite.Group()
    player_right_walk1_group = pygame.sprite.Group()
    player_left_walk2_group = pygame.sprite.Group()
    player_right_walk2_group = pygame.sprite.Group()

    boss_left = pygame.sprite.Sprite()
    boss_right = pygame.sprite.Sprite()

    player_left_stand = pygame.sprite.Sprite()
    player_right_stand = pygame.sprite.Sprite()
    player_left_walk1 = pygame.sprite.Sprite()
    player_right_walk1 = pygame.sprite.Sprite()
    player_left_walk2 = pygame.sprite.Sprite()
    player_right_walk2 = pygame.sprite.Sprite()

    boss_left.image = pygame.image.load("Sprite_boss_left_for_pj.png")
    boss_right.image = pygame.image.load("Sprite_boss_right_for_pj.png")
    player_left_stand.image = pygame.image.load("Sprite_player_left_for_pj.png")
    player_right_stand.image = pygame.image.load("Sprite_player_right_for_pj.png")
    player_left_walk1.image = pygame.image.load("Sprite_player1_left_for_pj.png")
    player_right_walk1.image = pygame.image.load("Sprite_player1_right_for_pj.png")
    player_left_walk2.image = pygame.image.load("Sprite_player2_left_for_pj.png")
    player_right_walk2.image = pygame.image.load("Sprite_player2_right_for_pj.png")

    boss_left.rect = boss_left.image.get_rect()
    boss_right.rect = boss_right.image.get_rect()
    player_left_stand.rect = player_left_stand.image.get_rect()
    player_right_stand.rect = player_right_stand.image.get_rect()
    player_left_walk1.rect = player_left_walk1.image.get_rect()
    player_right_walk1.rect = player_left_walk1.image.get_rect()
    player_left_walk2.rect = player_left_walk1.image.get_rect()
    player_right_walk2.rect = player_left_walk1.image.get_rect()
    
    player_left_stand_group.add(player_left_stand)
    player_right_stand_group.add(player_right_stand)
    player_left_walk1_group.add(player_left_walk1)
    player_right_walk1_group.add(player_right_walk1)
    player_left_walk2_group.add(player_left_walk2)
    player_right_walk2_group.add(player_right_walk2)
    boss_left_group.add(boss_left)
    boss_right_group.add(boss_right)

    while running:
        if current_location == "start":
            start_location()
            color_for_locations = 255
        if current_location == "main":
            main_menu()
            color_for_locations = 255
        if current_location == "battle":
            battle_field()
            color_for_locations = 255
        if current_location == "store":
            store_location()
            color_for_locations = 255
    pygame.quit()
