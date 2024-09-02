from config import *
from menu_assests.Button import Button
from menu_assests.ItemDisplay import ItemDisplay
import pygame

# pause menu should estentually pause the game (no updates)

class Menu:
    def __init__(self, player):
        # base surface
        self.base_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.base_surf.fill((20, 20, 20))
        self.base_surf.set_alpha(100)

        # menu settings
        self.current_menu = None

        # list of button path pairs (button, menu)
        self.buttons = []

        # refernce to player
        self.player = player

        # Exit Menu system
        self.EXIT_GAME = "quit"
        self.EXIT_MENU = "exit"
        self.BACK = "back"

    # draw method should be overriden
    def draw(self, screen):
        if self.current_menu == None:
            screen.blit(self.base_surf, (0, 0))

            for button in self.buttons:
                button[0].draw(screen)
        else:
            if self.current_menu:
                self.current_menu.draw(screen)

    # event_handler
    def event_handler(self, events):
        for event in events:
            # go back check (no matter what level of menu)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return False
            return True

        
    # retrun a menu object that represent the next menu to be displayed
    def update(self, events):
        on_menu = True
        if self.current_menu:
            on_menu = False 
       
        # check if on menu
        if on_menu:
            for buttons, menu in self.buttons:
                if buttons.update(events):
                    self.current_menu = None
                    if menu == self.EXIT_GAME:
                        return self.EXIT_GAME
                    elif menu == self.EXIT_MENU:
                        return self.EXIT_MENU
                    elif menu == self.BACK:
                        return self.BACK
                    else:
                        self.current_menu = menu(self.player)
                    break
            
            # keypress managers
            if self.current_menu == None:
                 if self.event_handler(events) == False:
                     return self.BACK
        else:
            # cascade back to game 
            ret_val = self.current_menu.update(events) 

            if ret_val == self.EXIT_GAME:
                self.current_menu = None
                return self.EXIT_GAME
            
            if ret_val == self.EXIT_MENU:
                self.current_menu = None
                return self.EXIT_MENU
            
            # go back a menu
            if ret_val == self.BACK:
                self.current_menu = None

        return True
                
    # add a button
    def add_button(self, text, x, y, type, font_size=64, padding=(20, 20, 20, 20)):
        button = Button(text, x, y, font_size=font_size, padding=padding)
        self.buttons.append((button, type))


# base menu for pausing
class PauseMenu(Menu):
    def __init__(self, player):
        super().__init__(player)

        # set up buttons
        self.add_button("Continue", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 150, self.EXIT_MENU)
        self.add_button("Equipment Bindings", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, EquipmentMenu)
        self.add_button("Exit Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150, self.EXIT_GAME)


# for changing equipment keys
class EquipmentMenu(Menu):
    def __init__(self, player):
        super().__init__(player)

        
        # item displays
        self.displays = []
        gap_width = (SCREEN_WIDTH - 4 * IT_WIDTH)/5

        # main buttons
        self.add_button("Back", gap_width, 40, self.BACK, font_size=32, padding=(10, 20, 10, 20))

        i = 0
        for item in player.items:
            if item.type == "Active":
                self.displays.append(ItemDisplay(item, (IT_WIDTH/2+gap_width)+(i)*(IT_WIDTH+gap_width), 400))
                i+=1

        

    # draw override
    def draw(self, screen):
        super().draw(screen)
        for displays in self.displays:
            displays.draw(screen)



    


        