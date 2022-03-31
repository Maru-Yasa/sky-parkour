import pygame
import random
from config import *
from tiles import Tile
from player import Player
from equipment import Equipment
from light import Light

class Level:
    """
    Attributes:
        all_platform (List): all of platforms's object
        display (TYPE): pygame.display
        equipment (TYPE): Description
        equipment_pos (list): Description
        fog (TYPE): Description
        INCREASE_SCORE (TYPE): Description
        interval_handler_for_increase_score (TYPE): Description
        interval_handler_for_spwan_platform (TYPE): Description
        level_speed (int): Description
        light (TYPE): Description
        light_pos (list): Description
        menu (TYPE): Description
        player (TYPE): Description
        score (int): Description
        SPWAN_PLATFORM (TYPE): Description
        time_to_increase_score (int): Description
        time_to_spwan_platform (int): Description
    """
    def __init__(self, surface, menu, clock):
        """Summary
        
        Args:
            surface (TYPE): Description
            menu (TYPE): Description
            clock (TYPE): Description
        """
        self.display = surface
        self.all_platform = pygame.sprite.Group()
        self.equipment_pos = [0,0]
        self.level_speed = 2
        self.menu = menu
        self.score = 0

        self.clock = clock

        self.setup_level()

    """
    #######################################################
        Utils
    #######################################################
    """

    def stop_all_interval(self):
        """Summary
        """
        self.interval_handler_for_increase_score.stop()
        self.interval_handler_for_spwan_platform.stop()

    def increase_score(self):
        """Summary
        """
        self.score += 1
        self.increase_speed_level()

    def show_score(self):
        """Summary
        """
        self.text_header(str(self.score), (WIDTH/2,HEIGHT/2), 100, self.display)

    def draw_circle_for_lighting(self,surface,pos):
        """Summary
        
        Args:
            surface (TYPE): Description
            pos (Tuple): (x,y)
        """
        img = './assets/light.png'
        self.light.add(Light(img, (350,350), pos))
        self.light.draw(surface)

    def text_header(self, text, pos, size, surface):
        """Summary
        
        Args:
            text (String): Description
            pos (Tuple): (x,y)
            size (Int): size of text 
            surface (pygame.Surface): whare rendering goes to
        """
        font = pygame.font.Font('./assets/Pixeled.ttf', size)
        text = font.render(text, True, (255,255,255))
        textRect = text.get_rect(center = pos)
        surface.blit(text,textRect)

    def add_fog(self,display):
        """Summary
        
        Args:
            display (pygame.display / pygame.Surface): Render to x's surface
        """
        player = self.player.sprite
        self.fog = pygame.surface.Surface((WIDTH,HEIGHT))
        self.fog.fill((50,50,50))
        self.light_pos[0] += (self.equipment_pos[0] - self.light_pos[0])
        self.light_pos[1] += (self.equipment_pos[1]- self.light_pos[1])

        self.draw_circle_for_lighting(self.fog,(self.light_pos[0],self.light_pos[1]))
        self.display.blit(self.fog,(0,0),special_flags=pygame.BLEND_MULT)

    def spwan_platform(self):
        """ 
            This method randomly generate (random_x,random_y,random_amount) for randomly spwanning 
            platform when it called. Also this method called outside of classes, in main loop,
            when USEREVENT + 0 detect or self.SPWAN_PLATFORM
        """
        random_amount = random.randint(15,20)
        random_x = random.randint(0,WIDTH-86)
        random_y = random.randint(10,30)
        random_y = -random_y
        for i in range(random_amount):
            self.all_platform.add(Tile('./assets/plat1.png', (86,16), (random_x,random_y+HEIGHT)))

    def spwan_player(self):
        """
            This method hadnle Spwanning of player
        """
        self.player.add(Player('./assets/player.png',(32,32),(WIDTH/2-86,100)))

    def render_group(self,group):
        """
        This method will help to render pygame.sprite.Group for 
        easyliy render the object
        
        Args:
            group (pygame.sprite.Group): List of object
        """
        for sprite in group:
            self.display.blit(sprite.image,(sprite.rect.x,sprite.rect.y))

    def move_all_platform(self):
        """This method hadnle all_platform movement, so all_platform can move uply
        """
        for sprite in self.all_platform:
            sprite.move_y(self.level_speed)

    """

    ######################################################%
        UI Utils
    #######################################################

    """

    def show_fps(self):
        """
            Show game's fps into screed 
        """
        self.text_header("FPS " + str(int(self.clock.get_fps())), (65,15), 20, self.display)

    def show_life(self):
        """
            Show player's life into screen
        """
        self.text_header(str(self.player.sprite.life), (WIDTH-50,50), 30, self.display)

    """

    #######################################################
        Game Logix
    #######################################################

    """

    def setup_level(self):
        """
            This method will setup lavel, it's just short cut for better __init__.
            Also this method called in __init__ in Level Class
        """
        # set time to randomly spwan platform
        self.SPWAN_PLATFORM = pygame.USEREVENT + 0
        self.time_to_spwan_platform = 300
        self.interval_handler_for_spwan_platform = pygame.time.set_timer(self.SPWAN_PLATFORM, self.time_to_spwan_platform)

        # increase score every 5 second
        self.INCREASE_SCORE = pygame.USEREVENT + 1
        self.time_to_increase_score = 2000
        self.interval_handler_for_increase_score = pygame.time.set_timer(self.INCREASE_SCORE, self.time_to_increase_score)

        # initial platform
        self.all_platform.add(Tile('./assets/plat1.png',(86,16),(WIDTH/2-86,HEIGHT)))

        # make player
        self.player = pygame.sprite.GroupSingle()
        self.spwan_player()

        # make equipment
        self.equipment = pygame.sprite.GroupSingle()
        self.equipment_pos[0] = self.player.sprite.rect.x - 30
        self.equipment_pos[1] = self.player.sprite.rect.y - 10
        self.equipment.add(Equipment('./assets/pet.png', (16,16), (self.equipment_pos[0], self.equipment_pos[1])))

        # light position
        self.light = pygame.sprite.GroupSingle()
        self.light_pos = [0,0]

    def increase_speed_level(self):
        """
            This method will increase level speed and time_to_spwan_platform
            Logic:
                when score += 1, level speed will increase and 
                time_to_spwan_platform to.

                this method called inside clasess,
                specificly in increase_score method
        """
        if self.time_to_spwan_platform <= 100:
            pygame.time.set_timer(self.SPWAN_PLATFORM, self.time_to_spwan_platform-100)
        self.level_speed += 1

    def update_equipment_pos(self):
        """
            This method handle equipment
            position, near to player
        """
        x = None
        if self.player.sprite.flipped:
            x = 30
        else:
            x = -10
        self.equipment_pos[0] += (self.player.sprite.rect.centerx - self.equipment_pos[0] - 15 + x) / 10
        self.equipment_pos[1] += (self.player.sprite.rect.centery - self.equipment_pos[1] - 20) / 10
        self.equipment.update(self.equipment_pos[0],self.equipment_pos[1])

    def vertical_movement_col(self):
        """
            This method handle the gravitym and 
            collision among player and platform
        """
        player = self.player.sprite
        self.player.sprite.apply_gravity()

        for sprite in self.all_platform.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.rect.bottom >= sprite.rect.top:
                    if player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0


    def check_game_over(self):
        """
            Checking player is game over or not

            Logic:
                if player.life > 0 : player will respwan in 
                certian coordinates belong the platform

                and if player.life <= 0 : will be show 
                game over's screen
        """
        if self.player.sprite.life > 0 and self.player.sprite.is_fall:
            self.player.sprite.die()
            self.player.sprite.move((WIDTH/2-86,HEIGHT-130))
            self.all_platform.add(Tile('./assets/plat1.png',(86,16),(WIDTH/2-86,HEIGHT-100)))
        elif self.player.sprite.life <= 0:
            self.player.sprite.kill()
            self.menu(self.score)

    def render(self):
        """
            Render all graphical assets
        """

        # Game Render
        self.show_score()
        self.render_group(self.all_platform)
        self.player.draw(self.display)
        self.equipment.draw(self.display)
        self.add_fog(self.display)

        # Render Ui
        self.show_fps()
        self.show_life()


    def update(self):
        """
            Update's logic will pass below
        """
        self.check_game_over()
        self.move_all_platform()
        self.all_platform.update()
        self.player.update()
        self.vertical_movement_col()
        self.update_equipment_pos()

    """

    ######################################################
        Output Method
    #######################################################

    """

    def run(self):
        """
            This method called update method and render method, 
            adn this method called out of classes
        """
        self.render()
        self.update()
