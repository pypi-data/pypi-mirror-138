loc_ver = '0.2' # Version of Oilukla

print('Oilukla2D - ' + loc_ver + '!')
print('Oilukla uses PyGame for drawing graphics, and Keyboard for getting input data!')
print('')

# USED MODULES =============================================================== #

import pygame 
import keyboard

# PUBLIC VARIABLES =========================================================== #

una_w = 0
una_h = 0
running = True

# KEY INTERACT =============================================================== #

key_put = keyboard.is_pressed
key_one = keyboard.on_release_key

# WINDOW ===================================================================== #

w_window = pygame.display.set_mode

class window(): # Main class of Window
    def __init__(self, width, height, title, bg_color, fps, icon): # Init procces 'wind = oilukla.window(width, height, title, bg_color, fps, icon)'
        global una_w, una_h

        self.fullscr = False


        self.fps = fps

        self.bg_color = bg_color

        self.w = width
        self.h = height
        self.title = title
        self.icon = icon
        
        una_w = self.w
        una_h = self.h

        self.clocker = pygame.time.Clock() # Init pygame clock
        self.window = w_window((self.w, self.h)) # Making window

        self.window.fill(self.bg_color) #Filling window with color

        if self.title == '': # Setting up window title
            pygame.display.set_caption('Oilukla2D - ' + loc_ver)
        else:
            pygame.display.set_caption(self.title)

        if self.icon != None: # Setting icon
            w_icon = pygame.image.load(self.icon)
            pygame.display.set_icon(w_icon)

        pygame.display.flip() # For correct displaying, window will flip

    def w_name(self, nname): # Renaming window 'wind.w_name(nname)'
        pygame.display.set_caption(nname)

    def w_update(self): # Update window (Uses in WHILE) !IMPORTAND!
        pygame.display.update()
        self.clocker.tick(self.fps)

    def w_clear(self): # Clearing window (I dont know why it doesn't works!)
        self.window_rect = self.window.get_rect()
        self.window.fill(self.bg_color, self.window_rect)

    def w_close(self): # Close event (Uses in WHILE) !IMPORTAND!
        global running

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False

    def toggle_fullscreen(self): # Toggle Fullscreen mode (Doesn't works correctly)
        mon_info = pygame.display.Info()
        if self.fullscr == True:
            w_window((una_w, una_h), pygame.SCALED + pygame.NOFRAME + pygame.FULLSCREEN, 32, vsync=1)
            self.fullscr = False
        else:
            w_window((una_h, una_w), pygame.SCALED + pygame.RESIZABLE, 32, vsync=1)
            self.fullscr = True


class entity():
    def __init__(self, sprite):
        self.sprite = sprite

        self.spr_surf = pygame.image.load(self.sprite)

    def transform(self, x, y):
        self.x = x
        self.y = y

        w_window((una_w, una_h)).blit(self.spr_surf, (self.x ,self.y))

    def scale_up(self, nx, ny):
        self.nx = nx
        self.ny = ny
        self.spr_surf = pygame.transform.scale(self.spr_surf, (nx, ny))

    def flip(self, flip_x, flip_y):
        self.spr_surf = pygame.transform.flip(self.spr_surf, flip_x, flip_y)

    def gravity(self, y, w_height, p_resy, p_phys, p_phys_am):
        self.y = y
        self.p_phys = p_phys
        if self.y <= (w_height - (p_resy - 1)):
            self.p_phys += p_phys_am
            self.y += self.p_phys
        else:
            self.p_phys = 0
            self.y += self.p_phys
        print(str(self.p_phys) + ', ' + str(self.y))
        return self.y, self.p_phys

    def platformer(self, player, x, w_width, p_resx, orient, p_speed, is_right):
        self.x = x
        self.is_right = is_right
        self.orient = orient
        if key_put('a'): 
            if self.x >= 0:
                self.x -= p_speed 
            self.orient = 'l'
            if self.orient == 'l':
                if self.is_right == False:
                    player.flip(True, False)
                    self.is_right = True
                    print(str(orient) + ', ' + str(is_right))
        if key_put('d'): 
            if self.x <= (w_width - (p_resx - 1)):
                self.x += p_speed 
            self.orient = 'r'
            if self.orient == 'r':
                if self.is_right == True:
                    player.flip(True, False)
                    self.is_right = False
                    print(str(orient) + ', ' + str(is_right))
        return self.x, self.is_right, self.orient

