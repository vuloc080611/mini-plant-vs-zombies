import pygame
import random
import sys

# --- SETUP PYGAME ---
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini PvZ - Full Version")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 20, bold=True)
big_font = pygame.font.SysFont("arial", 40, bold=True)

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 215, 0)
BROWN = (139, 69, 19)
GRAY = (128, 128, 128)
RED = (220, 20, 60)
BLUE = (135, 206, 235)

# --- GRID SETTINGS ---
GRID_COLS = 9
GRID_ROWS = 5
CELL_W = 80
CELL_H = 100
GRID_OFFSET_X = 150
GRID_OFFSET_Y = 100

# --- GAME STATE ---
MENU = 0
SEED_SELECTION = 1
PLAYING = 2
GAME_OVER = 3
WIN = 4
game_state = MENU

sun_score = 150
suns = []
plants = []
peas = []
zombies = []
lawnmowers = []
explosions = []

selected_seed = None
shovel_active = False
wave_progress = 0
max_waves = 5
current_wave = 0
zombies_in_wave = 0
zombies_spawned = 0
wave_start_time = 0
huge_wave = False

# Plant Definitions (Name, Cost, Cooldown, Health, Color)
PLANT_TYPES = {
    "peashooter": {"cost": 100, "cooldown": 5000, "health": 100, "color": DARK_GREEN},
    "sunflower":  {"cost": 50,  "cooldown": 5000, "health": 100, "color": YELLOW},
    "wallnut":    {"cost": 50,  "cooldown": 10000, "health": 400, "color": BROWN},
    "cherrybomb": {"cost": 150, "cooldown": 20000, "health": 100, "color": RED},
}

# --- CLASSES ---
class Sun:
    def __init__(self, x, y, target_y=None):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.target_y = target_y if target_y else y
        self.lifetime = 5000
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if self.rect.y < self.target_y:
            self.rect.y += 1

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (self.rect.centerx, self.rect.centery), 20)
        pygame.draw.circle(surface, (255, 255, 224), (self.rect.centerx, self.rect.centery), 10)

class Plant:
    def __init__(self, row, col, p_type):
        self.row = row
        self.col = col
        self.type = p_type
        self.rect = pygame.Rect(GRID_OFFSET_X + col * CELL_W + 10, GRID_OFFSET_Y + row * CELL_H + 10, CELL_W - 20, CELL_H - 20)
        self.health = PLANT_TYPES[p_type]["health"]
        self.timer = 0

    def update(self):
        self.timer += clock.get_time()
        if self.type == "peashooter":
            if self.timer > 1500:
                # Check if zombie is in this row
                for z in zombies:
                    if z.row == self.row and z.rect.x > self.rect.x:
                        peas.append(Pea(self.rect.right, self.rect.centery))
                        self.timer = 0
                        break
        elif self.type == "sunflower":
            if self.timer > 8000:
                suns.append(Sun(self.rect.x + 10, self.rect.y - 20, self.rect.y - 20))
                self.timer = 0
        elif self.type == "cherrybomb":
            if self.timer > 1000:
                explosions.append(Explosion(self.rect.centerx, self.rect.centery))
                self.health = 0 # Destroy itself

    def draw(self, surface):
        color = PLANT_TYPES[self.type]["color"]
        if self.type == "wallnut":
            pygame.draw.ellipse(surface, color, self.rect)
        elif self.type == "cherrybomb":
            pygame.draw.circle(surface, color, self.rect.center, 30)
            pygame.draw.circle(surface, BLACK, (self.rect.centerx - 10, self.rect.centery - 10), 5)
            pygame.draw.circle(surface, BLACK, (self.rect.centerx + 10, self.rect.centery - 10), 5)
        else:
            pygame.draw.rect(surface, color, (self.rect.x, self.rect.y + 20, self.rect.width, self.rect.height - 20))
            pygame.draw.circle(surface, color, (self.rect.centerx, self.rect.y + 30), 25)

class Pea:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed = 6
        self.damage = 25

    def update(self):
        self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN, self.rect.center, 7)

class Zombie:
    def __init__(self, row, z_type="normal"):
        self.row = row
        self.type = z_type
        self.rect = pygame.Rect(WIDTH, GRID_OFFSET_Y + row * CELL_H, 60, 100)
        self.speed = 0.4
        self.eating = False
        
        if z_type == "normal":
            self.health = 100
            self.color = GRAY
        elif z_type == "cone":
            self.health = 250
            self.color = (255, 140, 0)
        elif z_type == "bucket":
            self.health = 500
            self.color = (100, 100, 100)

    def update(self):
        self.eating = False
        for p in plants:
            if self.row == p.row and self.rect.colliderect(p.rect):
                self.eating = True
                p.health -= 0.5
                if p.health <= 0:
                    plants.remove(p)
                return
        self.rect.x -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.rect.x + 10, self.rect.y + 20, 40, 80))
        pygame.draw.circle(surface, self.color, (self.rect.centerx, self.rect.y + 30), 20)
        if self.type == "cone":
            pygame.draw.polygon(surface, (255, 140, 0), [(self.rect.centerx, self.rect.y), (self.rect.centerx-15, self.rect.y+30), (self.rect.centerx+15, self.rect.y+30)])
        elif self.type == "bucket":
            pygame.draw.rect(surface, (169, 169, 169), (self.rect.centerx-15, self.rect.y+5, 30, 25))
            
        # Health bar
        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y, 60, 5))
        pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y, 60 * (self.health / (100 if self.type=='normal' else 250 if self.type=='cone' else 500)), 5))

class Explosion:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x-60, y-60, 120, 120)
        self.timer = 300
        self.damage_dealt = False

    def update(self):
        if not self.damage_dealt:
            for z in zombies[:]:
                if self.rect.colliderect(z.rect):
                    zombies.remove(z)
            self.damage_dealt = True
        self.timer -= clock.get_time()

    def draw(self, surface):
        if self.timer > 0:
            alpha = self.timer / 300.0
            pygame.draw.circle(surface, RED, self.rect.center, int(60 * alpha))

class Lawnmower:
    def __init__(self, row):
        self.row = row
        self.rect = pygame.Rect(GRID_OFFSET_X - 60, GRID_OFFSET_Y + row * CELL_H + 20, 50, 60)
        self.active = False
        self.speed = 5

    def update(self):
        if self.active:
            self.rect.x += self.speed
            for z in zombies[:]:
                if z.row == self.row and self.rect.colliderect(z.rect):
                    zombies.remove(z)
            if self.rect.x > WIDTH:
                lawnmowers.remove(self)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)

# --- HELPER FUNCTIONS ---
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            rect = pygame.Rect(GRID_OFFSET_X + col * CELL_W, GRID_OFFSET_Y + row * CELL_H, CELL_W, CELL_H)
            color = (200, 230, 200) if (row + col) % 2 == 0 else (180, 210, 180)
            pygame.draw.rect(screen, color, rect)

def draw_menu_bar():
    pygame.draw.rect(screen, (100, 50, 0), (0, 0, WIDTH, 80))
    screen.blit(font.render(f"Sun: {int(sun_score)}", True, YELLOW), (20, 30))
    
    # Seed slots
    x_start = 150
    for p_name, data in PLANT_TYPES.items():
        rect = pygame.Rect(x_start, 10, 70, 60)
        pygame.draw.rect(screen, GRAY, rect, 2)
        pygame.draw.rect(screen, data["color"], rect.inflate(-10, -10))
        screen.blit(font.render(f"{data['cost']}", True, BLACK), (x_start + 5, 40))
        
        # Cooldown overlay
        if "last_planted" in data:
            time_passed = pygame.time.get_ticks() - data["last_planted"]
            if time_passed < data["cooldown"]:
                cd_height = 60 * (1 - time_passed / data["cooldown"])
                cd_rect = pygame.Rect(x_start, 10, 70, cd_height)
                s = pygame.Surface((70, cd_height), pygame.SRCALPHA)
                s.fill((0, 0, 0, 150))
                screen.blit(s, (x_start, 10))
                
        x_start += 80

    # Shovel
    shovel_rect = pygame.Rect(WIDTH - 80, 10, 60, 60)
    pygame.draw.rect(screen, BLUE if shovel_active else GRAY, shovel_rect, 2)
    screen.blit(font.render("DIG", True, BLACK), (WIDTH - 65, 30))
    return shovel_rect

def spawn_zombie():
    global zombies_spawned
    if zombies_spawned < zombies_in_wave:
        row = random.randint(0, GRID_ROWS - 1)
        z_type = "normal"
        r = random.random()
        if current_wave > 1 and r < 0.3: z_type = "cone"
        if current_wave > 2 and r < 0.15: z_type = "bucket"
        zombies.append(Zombie(row, z_type))
        zombies_spawned += 1

# --- GAME LOOP ---
running = True
while running:
    screen.fill(WHITE)
    current_time = pygame.time.get_ticks()
    dt = clock.tick(60)

    # 1. EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            if game_state == MENU:
                if pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50).collidepoint(mx, my):
                    game_state = SEED_SELECTION
                    
            elif game_state == SEED_SELECTION:
                # Basic Seed Selection (Auto pick all for simplicity in this version)
                if pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50).collidepoint(mx, my):
                    game_state = PLAYING
                    # Init Lawnmowers
                    for r in range(GRID_ROWS):
                        lawnmowers.append(Lawnmower(r))
                    wave_start_time = current_time
                    current_wave = 1
                    zombies_in_wave = 5
                    zombies_spawned = 0
                    
            elif game_state == PLAYING:
                # Top Bar clicks (Seeds & Shovel)
                shovel_rect = draw_menu_bar()
                
                # Check Shovel
                if shovel_rect.collidepoint(mx, my):
                    shovel_active = not shovel_active
                    selected_seed = None
                else:
                    # Check Seeds
                    x_start = 150
                    clicked_seed = False
                    for p_name, data in PLANT_TYPES.items():
                        if pygame.Rect(x_start, 10, 70, 60).collidepoint(mx, my):
                            if sun_score >= data["cost"] and ("last_planted" not in data or current_time - data["last_planted"] >= data["cooldown"]):
                                selected_seed = p_name
                                shovel_active = False
                            clicked_seed = True
                            break
                        x_start += 80
                    
                    if not clicked_seed:
                        # Check Grid
                        col = (mx - GRID_OFFSET_X) // CELL_W
                        row = (my - GRID_OFFSET_Y) // CELL_H
                        if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
                            if shovel_active:
                                for p in plants[:]:
                                    if p.row == row and p.col == col:
                                        plants.remove(p)
                                        break
                                shovel_active = False
                            elif selected_seed:
                                spot_taken = any(p.row == row and p.col == col for p in plants)
                                if not spot_taken:
                                    plants.append(Plant(row, col, selected_seed))
                                    sun_score -= PLANT_TYPES[selected_seed]["cost"]
                                    PLANT_TYPES[selected_seed]["last_planted"] = current_time
                                    selected_seed = None
                
                # Collect Sun
                for sun in suns[:]:
                    if sun.rect.collidepoint(mx, my):
                        sun_score += 25
                        suns.remove(sun)

    # 2. GAME LOGIC
    if game_state == PLAYING:
        # Spawn Sun from sky
        if random.random() < 0.005:
            suns.append(Sun(random.randint(GRID_OFFSET_X, WIDTH - 100), 0, random.randint(100, 400)))
            
        # Spawn Zombies
        if current_time - wave_start_time > 2000: # 2 sec delay before wave starts
            if random.random() < 0.02:
                spawn_zombie()
                
        # Check Wave Progression
        if zombies_spawned >= zombies_in_wave and len(zombies) == 0:
            current_wave += 1
            if current_wave > max_waves:
                game_state = WIN
            else:
                wave_start_time = current_time
                zombies_in_wave = 5 + current_wave * 3
                zombies_spawned = 0
                if current_wave == max_waves:
                    huge_wave = True

        # Update Objects
        for s in suns[:]: s.update()
        for p in plants[:]: 
            p.update()
            if p.health <= 0: plants.remove(p)
        for pea in peas[:]:
            pea.update()
            if pea.rect.x > WIDTH: peas.remove(pea)
            else:
                for z in zombies[:]:
                    if pea.rect.colliderect(z.rect):
                        z.health -= pea.damage
                        peas.remove(pea)
                        if z.health <= 0: zombies.remove(z)
                        break
        for z in zombies[:]:
            z.update()
            # Trigger Lawnmower
            if z.rect.x < GRID_OFFSET_X:
                for lw in lawnmowers:
                    if lw.row == z.row and not lw.active:
                        lw.active = True
                    elif lw.row == z.row and lw.active == False:
                        pass # already handled by lw.update
                if z.rect.x < 50: # Passed lawnmower
                    game_state = GAME_OVER
        
        for lw in lawnmowers: lw.update()
        for ex in explosions[:]:
            ex.update()
            if ex.timer <= 0: explosions.remove(ex)

    # 3. DRAWING
    if game_state == MENU:
        screen.fill((50, 150, 50))
        text = big_font.render("PLANTS VS ZOMBIES", True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 100))
        btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        pygame.draw.rect(screen, YELLOW, btn)
        screen.blit(font.render("START GAME", True, BLACK), (WIDTH//2 - 60, HEIGHT//2 + 15))
        
    elif game_state == SEED_SELECTION:
        screen.fill((200, 200, 200))
        screen.blit(big_font.render("CHOOSE YOUR SEEDS", True, BLACK), (WIDTH//2 - 200, 100))
        # Fake selection screen, click start to begin
        btn = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 100, 200, 50)
        pygame.draw.rect(screen, GREEN, btn)
        screen.blit(font.render("START LEVEL", True, WHITE), (WIDTH//2 - 60, HEIGHT//2 + 115))
        
    elif game_state == PLAYING or game_state == GAME_OVER or game_state == WIN:
        draw_grid()
        draw_menu_bar()
        
        # Draw Wave Progress Bar
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - 30, WIDTH, 30))
        progress = sum([1 for z in zombies if z.row >= 0]) # rough calc
        wave_pct = (zombies_spawned / zombies_in_wave) if zombies_in_wave > 0 else 0
        pygame.draw.rect(screen, RED, (0, HEIGHT - 30, WIDTH * wave_pct, 30))
        screen.blit(font.render(f"Wave {current_wave}/{max_waves}", True, WHITE), (10, HEIGHT - 25))
        if huge_wave:
            screen.blit(big_font.render("A HUGE WAVE OF ZOMBIES IS APPROACHING!", True, RED), (WIDTH//2 - 300, HEIGHT//2 - 200))

        # Draw Objects
        for lw in lawnmowers: lw.draw(screen)
        for p in plants: p.draw(screen)
        for s in suns: s.draw(screen)
        for pea in peas: pea.draw(screen)
        for z in zombies: z.draw(screen)
        for ex in explosions: ex.draw(screen)
        
        # Highlight selected seed
        if selected_seed:
            x_start = 150
            for p_name in PLANT_TYPES:
                if p_name == selected_seed:
                    pygame.draw.rect(screen, YELLOW, (x_start, 10, 70, 60), 3)
                x_start += 80

        if game_state == GAME_OVER:
            screen.fill((0,0,0, 180))
            text = big_font.render("GAME OVER", True, RED)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            screen.blit(font.render("Zombies ate your brains!", True, WHITE), (WIDTH//2 - 100, HEIGHT//2 + 50))
            
        elif game_state == WIN:
            screen.fill((0,100,0, 180))
            text = big_font.render("VICTORY!", True, YELLOW)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            screen.blit(font.render("You defended your house!", True, WHITE), (WIDTH//2 - 100, HEIGHT//2 + 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
