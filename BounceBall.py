import pygame
import random
import math
import sys

pygame.init()
pygame.display.set_caption("Bounce Ball Adventure - Ultimate Edition")

# ค่าคงที่
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 120

# สีต่างๆ
COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 50, 50),
    "green": (50, 255, 100),
    "blue": (80, 150, 255),
    "purple": (180, 70, 255),
    "orange": (255, 150, 50),
    "yellow": (255, 255, 100),
    "dark_blue": (20, 30, 60),
    "light_blue": (100, 180, 255),
    "pink": (255, 100, 180),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "neon_green": (57, 255, 20),
    "neon_pink": (255, 20, 147),
    "neon_blue": (20, 100, 255),
    "deep_purple": (75, 0, 130),
    "lava": (255, 69, 0)
}

# Particle effect class สำหรับเอฟเฟกต์ระเบิด!
class Particle:
    def __init__(self, x, y, color, particle_type="normal"):
        self.x = x
        self.y = y
        self.color = color
        self.type = particle_type
        
        if particle_type == "sparkle":
            self.size = random.uniform(1.5, 4)
            self.speed_x = random.uniform(-5, 5)
            self.speed_y = random.uniform(-5, 5)
            self.life = random.randint(15, 30)
            self.glow = True
        elif particle_type == "firework":
            self.size = random.uniform(2, 6)
            self.speed_x = random.uniform(-8, 8)
            self.speed_y = random.uniform(-8, 8)
            self.life = random.randint(25, 50)
            self.glow = True
        else:  # normal
            self.size = random.randint(3, 8)
            self.speed_x = random.uniform(-3, 3)
            self.speed_y = random.uniform(-3, 3)
            self.life = random.randint(20, 40)
            self.glow = False
            
        self.original_color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.rotation_speed = random.uniform(-0.2, 0.2)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # เพิ่มความต้านทานอากาศ
        self.speed_x *= 0.98
        self.speed_y *= 0.98
        
        self.life -= 1
        
        if self.type == "sparkle":
            self.size = max(0, self.size - 0.08)
            # เปลี่ยนสีแบบเรืองแสง
            pulse = abs(math.sin(self.life * 0.3)) * 100
            self.color = (
                min(255, self.original_color[0] + int(pulse)),
                min(255, self.original_color[1] + int(pulse)),
                min(255, self.original_color[2] + int(pulse))
            )
        else:
            self.size = max(0, self.size - 0.1)
            
        self.angle += self.rotation_speed
        
        return self.life > 0
        
    def draw(self, screen):
        if self.life > 0:
            # วาด glow effect
            if self.glow:
                glow_size = int(self.size * 2.5)
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                for i in range(3):
                    alpha = 150 - i * 50
                    radius = glow_size - i * 3
                    pygame.draw.circle(glow_surface, (*self.color[:3], alpha), 
                                      (glow_size, glow_size), radius)
                screen.blit(glow_surface, (int(self.x) - glow_size, int(self.y) - glow_size))
            
            # วาด particle หลัก
            if self.type == "sparkle":
                # วาดดาวกระพริบ
                points = []
                for i in range(5):
                    angle = self.angle + i * 2 * math.pi / 5
                    px = self.x + math.cos(angle) * self.size
                    py = self.y + math.sin(angle) * self.size
                    points.append((px, py))
                    px = self.x + math.cos(angle + 0.2) * self.size * 0.5
                    py = self.y + math.sin(angle + 0.2) * self.size * 0.5
                    points.append((px, py))
                if len(points) >= 3:
                    pygame.draw.polygon(screen, self.color, points)
            else:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
                
                # วาดวงกลมรอบ particle
                if self.type == "firework":
                    pygame.draw.circle(screen, COLORS["white"], 
                                     (int(self.x), int(self.y)), int(self.size * 0.7), 1)

# Star background class!
class Star:
    def __init__(self, star_type="normal"):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.type = star_type
        
        if star_type == "shooting":
            self.size = random.uniform(1.5, 3)
            self.brightness = random.uniform(0.8, 1.0)
            self.speed = random.uniform(3, 8)
            self.tail_length = random.randint(5, 15)
            self.tail = []
            self.color = random.choice([COLORS["cyan"], COLORS["light_blue"], COLORS["white"]])
        elif star_type == "twinkling":
            self.size = random.uniform(1, 2)
            self.brightness = random.uniform(0.3, 0.7)
            self.speed = random.uniform(0.1, 0.3)
            self.twinkle_speed = random.uniform(0.05, 0.15)
            self.twinkle_dir = random.choice([-1, 1])
            self.color = COLORS["white"]
        else:  # normal
            self.size = random.uniform(0.1, 2)
            self.brightness = random.uniform(0.3, 1.0)
            self.speed = random.uniform(0.2, 0.8)
            self.color = COLORS["white"]
        
        self.original_brightness = self.brightness
        
    def update(self):
        if self.type == "shooting":
            self.y += self.speed
            self.x += random.uniform(-0.5, 0.5)  # เติมการเคลื่อนที่ในแนวนอนนิดหน่อย
            
            # หางดาว
            self.tail.append((self.x, self.y))
            if len(self.tail) > self.tail_length:
                self.tail.pop(0)
            
            if self.y > SCREEN_HEIGHT + 20:
                self.y = -20
                self.x = random.randint(0, SCREEN_WIDTH)
                self.tail = []
                
        elif self.type == "twinkling":
            self.y += self.speed
            # การกระพริบ
            self.brightness += self.twinkle_speed * self.twinkle_dir
            if self.brightness >= 1.0 or self.brightness <= 0.3:
                self.twinkle_dir *= -1
                
            if self.y > SCREEN_HEIGHT:
                self.y = 0
                self.x = random.randint(0, SCREEN_WIDTH)
        else:
            self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.y = 0
                self.x = random.randint(0, SCREEN_WIDTH)
                
    def draw(self, screen):
        if self.type == "shooting":
            # วาดหางดาว
            for i, (tx, ty) in enumerate(self.tail):
                alpha = int(255 * (i / len(self.tail)))
                size = self.size * (i / len(self.tail))
                color = (*self.color[:3], alpha)
                pygame.draw.circle(screen, color, (int(tx), int(ty)), int(size))
            
            # วาดหัวดาว
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))
            
        elif self.type == "twinkling":
            brightness = int(255 * self.brightness)
            # ทำให้ดาวกระพริบมีสีสัน
            pulse = abs(math.sin(pygame.time.get_ticks() * 0.001 * random.uniform(1, 3))) * 100
            color = (
                min(255, brightness + int(pulse * 0.3)),
                min(255, brightness + int(pulse * 0.5)),
                min(255, brightness)
            )
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))
        else:
            brightness = int(255 * self.brightness)
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

# เอฟเฟกต์ : วงกลมคลื่น
class RippleEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 5
        self.max_radius = 100
        self.width = 3
        self.alpha = 200
        self.speed = 5
        self.alive = True
        
    def update(self):
        self.radius += self.speed
        self.alpha -= 4
        self.width = max(1, self.width - 0.1)
        
        if self.alpha <= 0 or self.radius > self.max_radius:
            self.alive = False
            
    def draw(self, screen):
        if self.alive:
            # สร้าง surface สำหรับ transparency
            ripple_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ripple_surface, (*self.color, self.alpha), 
                             (self.radius, self.radius), self.radius, int(self.width))
            screen.blit(ripple_surface, (int(self.x - self.radius), int(self.y - self.radius)))

# Power-up items
class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.choice(["extra_life", "slow_motion", "double_points", "big_paddle", "shield"])
        self.size = 20
        self.speed_y = 2
        self.rotation = 0
        self.rotation_speed = random.uniform(2, 4)
        self.collected = False
        self.pulse = 0
        self.pulse_speed = 0.1
        self.pulse_dir = 1
        
        # กำหนดสีตามประเภท
        if self.type == "extra_life":
            self.color = COLORS["green"]
            self.glow_color = COLORS["neon_green"]
        elif self.type == "slow_motion":
            self.color = COLORS["cyan"]
            self.glow_color = COLORS["light_blue"]
        elif self.type == "double_points":
            self.color = COLORS["gold"]
            self.glow_color = COLORS["yellow"]
        elif self.type == "big_paddle":
            self.color = COLORS["purple"]
            self.glow_color = COLORS["magenta"]
        elif self.type == "shield":
            self.color = COLORS["blue"]
            self.glow_color = COLORS["neon_blue"]
            
    def update(self):
        self.y += self.speed_y
        self.rotation += self.rotation_speed
        
        # Pulse effect
        self.pulse += self.pulse_speed * self.pulse_dir
        if self.pulse >= 1.0 or self.pulse <= 0:
            self.pulse_dir *= -1
            
        return self.y < SCREEN_HEIGHT + 50 and not self.collected
    
    def draw(self, screen):
        if not self.collected:
            # Glow effect
            glow_size = int(self.size * (1.5 + self.pulse * 0.5))
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            for i in range(3):
                alpha = 100 - i * 30
                radius = glow_size - i * 5
                pygame.draw.circle(glow_surface, (*self.glow_color[:3], alpha), 
                                 (glow_size, glow_size), radius)
            screen.blit(glow_surface, (int(self.x) - glow_size, int(self.y) - glow_size))
            
            # วาด power-up หลัก
            points = []
            for i in range(6):
                angle = math.radians(self.rotation + i * 60)
                px = self.x + math.cos(angle) * self.size
                py = self.y + math.sin(angle) * self.size
                points.append((px, py))
            
            pygame.draw.polygon(screen, self.color, points)
            
            # วาดไอคอนตรงกลาง
            if self.type == "extra_life":
                pygame.draw.circle(screen, COLORS["white"], (int(self.x), int(self.y)), int(self.size * 0.4))
            elif self.type == "slow_motion":
                pygame.draw.rect(screen, COLORS["white"], 
                               (int(self.x - self.size * 0.3), int(self.y - self.size * 0.3), 
                                int(self.size * 0.6), int(self.size * 0.6)))
            elif self.type == "double_points":
                pygame.draw.circle(screen, COLORS["white"], (int(self.x), int(self.y)), int(self.size * 0.3))
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size * 0.2))
            elif self.type == "big_paddle":
                pygame.draw.rect(screen, COLORS["white"], 
                               (int(self.x - self.size * 0.4), int(self.y - self.size * 0.2), 
                                int(self.size * 0.8), int(self.size * 0.4)))
            elif self.type == "shield":
                pygame.draw.circle(screen, COLORS["white"], (int(self.x), int(self.y)), int(self.size * 0.5), 3)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# สร้างพื้นหลังดาวที่หลากหลายมากขึ้น
stars = []
for _ in range(100):
    stars.append(Star("normal"))
for _ in range(20):
    stars.append(Star("twinkling"))
for _ in range(5):
    stars.append(Star("shooting"))

# Load fonts
try:
    title_font = pygame.font.Font("font/Coiny.ttf", 72)
    score_font = pygame.font.Font("font/Coiny.ttf", 40)
    menu_font = pygame.font.Font("font/Coiny.ttf", 28)
    info_font = pygame.font.Font("font/Coiny.ttf", 18)
    glow_font = pygame.font.Font("font/Coiny.ttf", 48)
except:
    # Fallback fonts if Coiny.ttf is not available
    title_font = pygame.font.SysFont("arialblack", 72)
    score_font = pygame.font.SysFont("arialblack", 42)
    menu_font = pygame.font.SysFont("arialblack", 48)
    info_font = pygame.font.SysFont("arial", 28)
    glow_font = pygame.font.SysFont("arialblack", 48)

# ฟังก์ชันสร้างพื้นหลัง gradient
def draw_gradient_background():
    # พื้นหลังแบบ gradient สองทิศทาง
    for y in range(SCREEN_HEIGHT):
        # สีจะค่อยๆ เปลี่ยนจากสีน้ำเงินเข้มด้านบนเป็นสีม่วงเข้มด้านล่าง
        factor = y / SCREEN_HEIGHT
        r = int(20 * (1 - factor) + 75 * factor)
        g = int(30 * (1 - factor) + 0 * factor)
        b = int(60 * (1 - factor) + 130 * factor)
        pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # เพิ่มแสงสว่างที่มุม
    for i in range(3):
        radius = 200 + i * 50
        alpha = 30 - i * 10
        gradient_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(gradient_surface, (255, 255, 255, alpha), (radius, radius), radius)
        screen.blit(gradient_surface, (-100, -100))
        screen.blit(gradient_surface, (SCREEN_WIDTH - radius + 100, SCREEN_HEIGHT - radius + 100))

# สร้างปุ่มแบบมีเอฟเฟกต์มากขึ้น
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, glow_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.glow_color = glow_color if glow_color else color
        self.is_hovered = False
        self.pulse = 0
        self.pulse_speed = 0.05
        self.pulse_dir = 1
        
    def draw(self, screen):
        # Pulse effect
        self.pulse += self.pulse_speed * self.pulse_dir
        if self.pulse >= 1.0 or self.pulse <= 0:
            self.pulse_dir *= -1
            
        color = self.hover_color if self.is_hovered else self.color
        
        # Glow effect เมื่อ hover
        if self.is_hovered:
            glow_size = 15
            glow_surface = pygame.Surface((self.rect.width + glow_size * 2, 
                                         self.rect.height + glow_size * 2), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*self.glow_color, 100), 
                           (0, 0, self.rect.width + glow_size * 2, self.rect.height + glow_size * 2), 
                           border_radius=20)
            screen.blit(glow_surface, (self.rect.x - glow_size, self.rect.y - glow_size))
        
        # วาดปุ่มหลัก
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        
        # ขอบปุ่มแบบไล่สี
        border_color = (
            min(255, color[0] + 50),
            min(255, color[1] + 50),
            min(255, color[2] + 50)
        )
        pygame.draw.rect(screen, border_color, self.rect, 4, border_radius=15)
        
        # เอฟเฟกต์แสงด้านใน
        highlight = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 
                              self.rect.width - 10, self.rect.height // 4 - 5)
        pygame.draw.rect(screen, (255, 255, 255, 50), highlight, border_radius=10)
        
        # ข้อความ
        text_surface = menu_font.render(self.text, True, COLORS["white"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # เงาข้อความ
        shadow_surface = menu_font.render(self.text, True, (0, 0, 0, 150))
        shadow_rect = shadow_surface.get_rect(center=(self.rect.centerx + 3, self.rect.centery + 3))
        screen.blit(shadow_surface, shadow_rect)
        
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# วัตถุในเกม
def create_paddle(width=140, color=None):
    paddle_width = width
    paddle_surface = pygame.Surface((paddle_width, 25), pygame.SRCALPHA)
    
    if color is None:
        color = COLORS["blue"]
    
    # วาดพัดเดิลแบบมีเงาและไล่สี
    pygame.draw.rect(paddle_surface, color, (0, 0, paddle_width, 25), border_radius=8)
    
    # ไล่สีจากบนลงล่าง
    for i in range(10):
        y_pos = i * 2
        alpha = 200 - i * 20
        line_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30), alpha)
        pygame.draw.line(paddle_surface, line_color, (5, y_pos), (paddle_width - 5, y_pos), 1)
    
    # เอฟเฟกต์ความเงา
    pygame.draw.rect(paddle_surface, (255, 255, 255, 150), (5, 5, paddle_width - 10, 8), border_radius=4)
    
    # ขอบพัดเดิลแบบเรืองแสง
    pygame.draw.rect(paddle_surface, (255, 255, 255, 100), (0, 0, paddle_width, 25), 2, border_radius=8)
    
    return paddle_surface

def create_ball(size=25, color_scheme="fire"):
    ball_size = size
    ball_surface = pygame.Surface((ball_size * 2, ball_size * 2), pygame.SRCALPHA)
    
    # ธีมสีต่างๆ สำหรับลูกบอล
    if color_scheme == "fire":
        inner_color = COLORS["red"]
        mid_color = COLORS["orange"]
        outer_color = COLORS["yellow"]
    elif color_scheme == "ice":
        inner_color = COLORS["cyan"]
        mid_color = COLORS["light_blue"]
        outer_color = COLORS["white"]
    elif color_scheme == "energy":
        inner_color = COLORS["neon_green"]
        mid_color = COLORS["green"]
        outer_color = COLORS["yellow"]
    else: 
        inner_color = COLORS["purple"]
        mid_color = COLORS["magenta"]
        outer_color = COLORS["pink"]
    
    # วาดลูกบอลแบบมีไล่สีหลายชั้น
    pygame.draw.circle(ball_surface, outer_color, (ball_size, ball_size), ball_size)
    pygame.draw.circle(ball_surface, mid_color, (ball_size, ball_size), int(ball_size * 0.8))
    pygame.draw.circle(ball_surface, inner_color, (ball_size, ball_size), int(ball_size * 0.6))
    
    # เอฟเฟกต์ความเงาแบบวงกลม
    pygame.draw.circle(ball_surface, (255, 255, 255, 200), 
                      (int(ball_size * 0.7), int(ball_size * 0.7)), int(ball_size * 0.2))
    
    # เอฟเฟกต์แสงด้านใน
    for i in range(3):
        radius = int(ball_size * 0.3 - i * 2)
        alpha = 100 - i * 30
        pygame.draw.circle(ball_surface, (255, 255, 255, alpha), 
                          (int(ball_size * 0.7), int(ball_size * 0.7)), radius)
    
    return ball_surface

def create_life_icon():
    life_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # วาดหัวใจแทนวงกลมธรรมดา
    points = [
        (20, 35),
        (8, 20),
        (20, 10),
        (32, 20)
    ]
    
    # หัวใจสีแดงไล่สี
    pygame.draw.polygon(life_surface, COLORS["red"], points)
    
    # แสงสว่างกลางหัวใจ
    pygame.draw.polygon(life_surface, COLORS["pink"], [
        (20, 25),
        (15, 20),
        (20, 15),
        (25, 20)
    ])
    
    # ขอบหัวใจเรืองแสง
    pygame.draw.polygon(life_surface, (255, 100, 100, 150), points, 3)
    
    return life_surface

# Initialize game objects
paddle_width = 140
paddle_color = COLORS["blue"]
paddle = create_paddle(paddle_width, paddle_color)
paddle_rect = paddle.get_rect()
paddle_rect.centerx = SCREEN_WIDTH // 2
paddle_rect.bottom = SCREEN_HEIGHT - 30

ball_size = 25
ball_color_scheme = "fire"
ball = create_ball(ball_size, ball_color_scheme)
ball_rect = ball.get_rect()
ball_rect.x = random.randint(50, SCREEN_WIDTH - 100)
ball_rect.y = 50

# ตัวแปรเกม
score = 0
high_score = 0
lives = 3
game_speed = 2
ball_speed_x = random.choice([-2, 2]) * game_speed
ball_speed_y = game_speed
game_state = "menu"  # "menu", "playing", "game_over"
particles = []
ripples = []
power_ups = []
active_power_ups = {}  # พลังพิเศษที่กำลังใช้งาน
combo_counter = 0
combo_timer = 0
last_hit_time = 0
shield_active = False
shield_timer = 0
slow_motion = False
slow_motion_timer = 0
double_points = False
double_points_timer = 0
trail_effect = []
max_trail_length = 10

# สร้างปุ่มใหม่ที่มีสีสันมากขึ้น
play_button = Button(SCREEN_WIDTH//2 - 120, 300, 240, 70, "START ADVENTURE", 
                     COLORS["neon_blue"], COLORS["cyan"], COLORS["light_blue"])
quit_button = Button(SCREEN_WIDTH//2 - 120, 390, 240, 70, "EXIT GAME", 
                     COLORS["neon_pink"], COLORS["magenta"], COLORS["pink"])
restart_button = Button(SCREEN_WIDTH//2 - 120, 350, 240, 70, "PLAY AGAIN", 
                        COLORS["neon_green"], COLORS["green"], COLORS["light_blue"])

# ฟังก์ชันสำหรับเอฟเฟกต์ต่างๆ
def create_particle_effect(x, y, color, effect_type="normal", count=15):
    if effect_type == "sparkle":
        for _ in range(count):
            particles.append(Particle(x, y, color, "sparkle"))
    elif effect_type == "firework":
        for _ in range(count * 2):
            particles.append(Particle(x, y, color, "firework"))
    else:
        for _ in range(count):
            particles.append(Particle(x, y, color))

def create_ripple_effect(x, y, color):
    ripples.append(RippleEffect(x, y, color))

def spawn_power_up(x, y):
    if random.random() < 0.25:  # 25% โอกาสที่ power-up จะปรากฏ
        power_ups.append(PowerUp(x, y))

def activate_power_up(power_type):
    active_power_ups[power_type] = pygame.time.get_ticks()
    
    if power_type == "extra_life":
        global lives
        lives = min(5, lives + 1)
        create_particle_effect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 
                              COLORS["green"], "firework", 30)
    elif power_type == "slow_motion":
        global slow_motion, slow_motion_timer
        slow_motion = True
        slow_motion_timer = 5000  # 5 วินาที
        create_particle_effect(SCREEN_WIDTH // 2, 100, COLORS["cyan"], "sparkle", 20)
    elif power_type == "double_points":
        global double_points, double_points_timer
        double_points = True
        double_points_timer = 10000  # 10 วินาที
        create_particle_effect(SCREEN_WIDTH // 2, 100, COLORS["gold"], "firework", 25)
    elif power_type == "big_paddle":
        global paddle_width, paddle, paddle_color
        paddle_width = 200
        paddle_color = COLORS["purple"]
        paddle = create_paddle(paddle_width, paddle_color)
        create_particle_effect(paddle_rect.centerx, paddle_rect.centery, 
                              COLORS["purple"], "sparkle", 15)
    elif power_type == "shield":
        global shield_active, shield_timer
        shield_active = True
        shield_timer = 8000  # 8 วินาที
        create_particle_effect(paddle_rect.centerx, paddle_rect.centery, 
                              COLORS["blue"], "firework", 20)

def deactivate_power_up(power_type):
    if power_type in active_power_ups:
        del active_power_ups[power_type]
    
    if power_type == "slow_motion":
        global slow_motion
        slow_motion = False
    elif power_type == "double_points":
        global double_points
        double_points = False
    elif power_type == "big_paddle":
        global paddle_width, paddle, paddle_color
        paddle_width = 140
        paddle_color = COLORS["blue"]
        paddle = create_paddle(paddle_width, paddle_color)
    elif power_type == "shield":
        global shield_active
        shield_active = False

# วาดข้อความที่มีเอฟเฟกต์พิเศษ
def draw_text_with_effect(text, font, color, x, y, center=True, effect="shadow", effect_color=None):
    if effect_color is None:
        effect_color = COLORS["black"]
    
    if effect == "glow":
        # Glow effect
        for i in range(5, 0, -1):
            glow_surface = font.render(text, True, (*color[:3], 50))
            if center:
                glow_rect = glow_surface.get_rect(center=(x, y))
            else:
                glow_rect = glow_surface.get_rect(topleft=(x, y))
            glow_rect.x += random.randint(-i, i)
            glow_rect.y += random.randint(-i, i)
            screen.blit(glow_surface, glow_rect)
    
    elif effect == "neon":
        # Neon glow effect
        for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
            neon_surface = font.render(text, True, effect_color)
            if center:
                neon_rect = neon_surface.get_rect(center=(x + offset[0], y + offset[1]))
            else:
                neon_rect = neon_surface.get_rect(topleft=(x + offset[0], y + offset[1]))
            screen.blit(neon_surface, neon_rect)
    
    # ข้อความหลัก
    main_surface = font.render(text, True, color)
    if center:
        main_rect = main_surface.get_rect(center=(x, y))
    else:
        main_rect = main_surface.get_rect(topleft=(x, y))
    screen.blit(main_surface, main_rect)

# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    # เอฟเฟกต์ต่างๆ
    for star in stars:
        star.update()
    
    particles = [p for p in particles if p.update()]
    
    ripples = [r for r in ripples if r.alive]
    for ripple in ripples:
        ripple.update()
    
    power_ups = [p for p in power_ups if p.update()]
    for power_up in power_ups:
        power_up.update()
    
    # combo timer
    if combo_timer > 0:
        combo_timer -= 1
        if combo_timer == 0:
            combo_counter = 0
    
    # power-up timers
    current_ticks = pygame.time.get_ticks()
    
    if slow_motion and slow_motion_timer > 0:
        slow_motion_timer -= 16  # ประมาณ 1 frame ที่ 60 FPS
        if slow_motion_timer <= 0:
            deactivate_power_up("slow_motion")
    
    if double_points and double_points_timer > 0:
        double_points_timer -= 16
        if double_points_timer <= 0:
            deactivate_power_up("double_points")
    
    if shield_active and shield_timer > 0:
        shield_timer -= 16
        if shield_timer <= 0:
            deactivate_power_up("shield")
    
    # ตรวจสอบการชนกับ power-ups
    for power_up in power_ups[:]:
        if paddle_rect.colliderect(pygame.Rect(power_up.x - power_up.size, 
                                             power_up.y - power_up.size,
                                             power_up.size * 2, power_up.size * 2)):
            activate_power_up(power_up.type)
            power_up.collected = True
            create_particle_effect(power_up.x, power_up.y, power_up.color, "firework", 20)
            create_ripple_effect(power_up.x, power_up.y, power_up.glow_color)
            power_ups.remove(power_up)
    
    # trail effect ของลูกบอล
    if game_state == "playing":
        trail_effect.append((ball_rect.centerx, ball_rect.centery))
        if len(trail_effect) > max_trail_length:
            trail_effect.pop(0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "menu"
                elif game_state == "menu":
                    running = False
            
            if event.key == pygame.K_SPACE and game_state == "menu":
                game_state = "playing"
                score = 0
                lives = 3
                game_speed = 2
                ball_speed_y = game_speed
                power_ups.clear()
                active_power_ups.clear()
                combo_counter = 0
                trail_effect.clear()
                
            if event.key == pygame.K_r and game_state == "playing":
                # รีเซ็ต power-ups เมื่อกด R
                for power_type in list(active_power_ups.keys()):
                    deactivate_power_up(power_type)
                power_ups.clear()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if play_button.is_clicked(mouse_pos, event):
                    game_state = "playing"
                    score = 0
                    lives = 3
                    game_speed = 2
                    ball_speed_y = game_speed
                    power_ups.clear()
                    active_power_ups.clear()
                    combo_counter = 0
                    trail_effect.clear()
                elif quit_button.is_clicked(mouse_pos, event):
                    running = False
                    
            elif game_state == "game_over":
                if restart_button.is_clicked(mouse_pos, event):
                    game_state = "playing"
                    score = 0
                    lives = 3
                    game_speed = 2
                    ball_speed_y = game_speed
                    power_ups.clear()
                    active_power_ups.clear()
                    combo_counter = 0
                    trail_effect.clear()
                    
                    # รีเซ็ตตำแหน่งพัดเดิลและลูกบอล
                    paddle_rect.centerx = SCREEN_WIDTH // 2
                    paddle_rect.bottom = SCREEN_HEIGHT - 30
                    ball_rect.x = random.randint(50, SCREEN_WIDTH - 100)
                    ball_rect.y = 50
                    ball_speed_x = random.choice([-2, 2]) * game_speed
    
    # ตรวจสอบการ hover ปุ่ม
    if game_state == "menu":
        play_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
    elif game_state == "game_over":
        restart_button.check_hover(mouse_pos)
    
    # Game logic
    if game_state == "playing":
        # การควบคุมพัดเดิล
        keys = pygame.key.get_pressed()
        paddle_speed = 8 if not slow_motion else 12
        
        if keys[pygame.K_LEFT] and paddle_rect.left > 0:
            paddle_rect.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_rect.right < SCREEN_WIDTH:
            paddle_rect.x += paddle_speed
        if keys[pygame.K_a] and paddle_rect.left > 0:
            paddle_rect.x -= paddle_speed
        if keys[pygame.K_d] and paddle_rect.right < SCREEN_WIDTH:
            paddle_rect.x += paddle_speed
        
        # การเคลื่อนที่ของลูกบอล
        speed_multiplier = 0.5 if slow_motion else 1.0
        ball_rect.x += ball_speed_x * speed_multiplier
        ball_rect.y += ball_speed_y * speed_multiplier
        
        # ตรวจสอบการชนขอบจอ
        if ball_rect.left <= 0:
            ball_rect.left = 1
            ball_speed_x = abs(ball_speed_x) * 1.05  # เพิ่มความเร็วเล็กน้อย
            create_particle_effect(ball_rect.left, ball_rect.centery, COLORS["purple"], "sparkle")
            create_ripple_effect(ball_rect.left, ball_rect.centery, COLORS["magenta"])
            
        elif ball_rect.right >= SCREEN_WIDTH:
            ball_rect.right = SCREEN_WIDTH - 1
            ball_speed_x = -abs(ball_speed_x) * 1.05
            create_particle_effect(ball_rect.right, ball_rect.centery, COLORS["purple"], "sparkle")
            create_ripple_effect(ball_rect.right, ball_rect.centery, COLORS["magenta"])
            
        if ball_rect.top <= 0:
            ball_rect.top = 1
            ball_speed_y = abs(ball_speed_y) * 1.05
            create_particle_effect(ball_rect.centerx, ball_rect.top, COLORS["purple"], "sparkle")
            create_ripple_effect(ball_rect.centerx, ball_rect.top, COLORS["magenta"])
        
        # ตรวจสอบการชนพัดเดิล
        if ball_rect.colliderect(paddle_rect) and ball_speed_y > 0:
            # คำนวณมุมการสะท้อนตามจุดที่ลูกบอลชนพัดเดิล
            relative_intersect_x = (paddle_rect.centerx - ball_rect.centerx) / (paddle_rect.width / 2)
            bounce_angle = relative_intersect_x * 0.8  # ค่ามุมสูงสุด
            
            ball_speed_y = -game_speed * (1 + abs(bounce_angle) * 0.3)
            ball_speed_x = -bounce_angle * game_speed * 2
            
            # คะแนน
            points_earned = 10
            if double_points:
                points_earned *= 2
            
            # Combo system
            if current_time - last_hit_time < 1000:  # ภายใน 1 วินาที
                combo_counter += 1
                combo_timer = 60  # รีเซ็ต combo timer
                points_earned += combo_counter * 5  # โบนัส combo
            else:
                combo_counter = 1
            
            score += points_earned
            last_hit_time = current_time
            
            # เอฟเฟกต์
            create_particle_effect(ball_rect.centerx, ball_rect.bottom, COLORS["yellow"], "firework")
            create_ripple_effect(ball_rect.centerx, ball_rect.bottom, COLORS["gold"])
            
            # สุ่มเปลี่ยนธีมสีของลูกบอล
            if random.random() < 0.1:
                ball_color_scheme = random.choice(["fire", "ice", "energy", "rainbow"])
                ball = create_ball(ball_size, ball_color_scheme)
            
            # มีโอกาสเกิด power-up
            spawn_power_up(ball_rect.centerx, ball_rect.top)
            
            # เพิ่มความเร็วเกมทุกๆ 50 คะแนน
            if score % 50 == 0:
                game_speed += 0.5
                ball_speed_y = game_speed if ball_speed_y > 0 else -game_speed
        
        # ตรวจสอบว่าลูกบอลตกด้านล่าง
        if ball_rect.top > SCREEN_HEIGHT:
            if shield_active:
                # ใช้ shield ป้องกัน
                ball_rect.bottom = SCREEN_HEIGHT - 50
                ball_speed_y = -abs(ball_speed_y)
                create_particle_effect(ball_rect.centerx, ball_rect.centery, 
                                      COLORS["blue"], "firework", 25)
                shield_timer -= 2000  # ลดเวลาของ shield ลง
            else:
                lives -= 1
                create_particle_effect(ball_rect.centerx, ball_rect.centery, 
                                      COLORS["red"], "firework", 30)
                create_ripple_effect(ball_rect.centerx, ball_rect.centery, COLORS["lava"])
                
                if lives <= 0:
                    game_state = "game_over"
                    if score > high_score:
                        high_score = score
                        # เอฟเฟกต์สำหรับ high score
                        for _ in range(50):
                            particles.append(Particle(
                                SCREEN_WIDTH // 2, 
                                SCREEN_HEIGHT // 2,
                                COLORS["gold"],
                                "firework"
                            ))
                else:
                    # รีเซ็ตลูกบอล
                    ball_rect.x = random.randint(50, SCREEN_WIDTH - 100)
                    ball_rect.y = 50
                    ball_speed_x = random.choice([-2, 2]) * game_speed
                    ball_speed_y = game_speed
                    combo_counter = 0
                    trail_effect.clear()
    
    # วาดกราฟิก
    # วาดพื้นหลัง
    draw_gradient_background()
    
    # วาดดาว
    for star in stars:
        star.draw(screen)
    
    # วาดเส้นขอบสนามแบบเรืองแสง
    pygame.draw.rect(screen, (100, 180, 255, 100), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)
    pygame.draw.rect(screen, (255, 255, 255, 50), (2, 2, SCREEN_WIDTH-4, SCREEN_HEIGHT-4), 2)
    
    # วาดเส้นแบ่งกลางแบบพิเศษ
    pulse = abs(math.sin(pygame.time.get_ticks() * 0.001)) * 255
    for y in range(0, SCREEN_HEIGHT, 40):
        height = 20 + math.sin(pygame.time.get_ticks() * 0.002 + y * 0.01) * 5
        color = (100, 180, 255, int(150 + pulse * 0.4))
        pygame.draw.rect(screen, color, (SCREEN_WIDTH//2 - 3, y, 6, int(height)))
    
    # วาด trail effect ของลูกบอล
    if game_state == "playing":
        for i, (trail_x, trail_y) in enumerate(trail_effect):
            alpha = int(255 * (i / len(trail_effect)))
            size = ball_size * 0.5 * (i / len(trail_effect))
            trail_color = (255, 255, 255, alpha)
            pygame.draw.circle(screen, trail_color, (int(trail_x), int(trail_y)), int(size))
    
    if game_state == "menu":
        # วาดเมนู
        draw_text_with_effect("BOUNCE BALL", title_font, COLORS["yellow"], 
                             SCREEN_WIDTH//2, 120, center=True, effect="neon", 
                             effect_color=COLORS["orange"])
        draw_text_with_effect("ADVENTURE", title_font, COLORS["cyan"], 
                             SCREEN_WIDTH//2, 190, center=True, effect="glow")
        
        # เอฟเฟกต์ลูกบอลในเมนู
        menu_ball_x = SCREEN_WIDTH//2 + math.sin(pygame.time.get_ticks() * 0.001) * 200
        menu_ball_y = 260 + math.cos(pygame.time.get_ticks() * 0.001) * 30
        menu_ball = create_ball(20, "rainbow")
        screen.blit(menu_ball, (int(menu_ball_x - 20), int(menu_ball_y - 20)))
        
        play_button.draw(screen)
        quit_button.draw(screen)
        
        # วาดคำแนะนำ
        draw_text_with_effect("CONTROLS: LEFT/RIGHT ARROW or A/D", info_font, 
                             COLORS["white"], SCREEN_WIDTH//2, 500, center=True)
        draw_text_with_effect("PRESS SPACE TO START", info_font, 
                             (255, 255, int(abs(math.sin(pygame.time.get_ticks() * 0.003)) * 255)), 
                             SCREEN_WIDTH//2, 540, center=True)
        draw_text_with_effect("HIGH SCORE: " + str(high_score), info_font, 
                             COLORS["gold"], SCREEN_WIDTH//2, 580, center=True)
        
    elif game_state == "playing" or game_state == "game_over":
        # วาด shield ถ้ามี
        if shield_active:
            shield_radius = max(paddle_rect.width, paddle_rect.height) // 2 + 20
            shield_alpha = int(abs(math.sin(pygame.time.get_ticks() * 0.01)) * 150 + 100)
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (100, 200, 255, shield_alpha), 
                             (shield_radius, shield_radius), shield_radius, 3)
            screen.blit(shield_surface, (paddle_rect.centerx - shield_radius, 
                                       paddle_rect.centery - shield_radius))
        
        # วาด power-ups
        for power_up in power_ups:
            power_up.draw(screen)
        
        # วาด ripple effects
        for ripple in ripples:
            ripple.draw(screen)
        
        # วาด particles
        for particle in particles:
            particle.draw(screen)
        
        # วาดวัตถุในเกม
        screen.blit(paddle, paddle_rect)
        screen.blit(ball, ball_rect)
        
        # วาดคะแนน
        score_color = COLORS["gold"] if double_points else COLORS["yellow"]
        draw_text_with_effect("SCORE: " + str(score), score_font, score_color, 
                             SCREEN_WIDTH//2, 40, center=True, effect="shadow")
        
        # วาด combo
        if combo_counter > 1:
            combo_alpha = int(abs(math.sin(pygame.time.get_ticks() * 0.01)) * 200 + 55)
            combo_text = f"COMBO x{combo_counter}!"
            combo_surface = info_font.render(combo_text, True, (255, 255, 255, combo_alpha))
            combo_rect = combo_surface.get_rect(center=(SCREEN_WIDTH//2, 60))
            screen.blit(combo_surface, combo_rect)
        
        # วาดชีวิต
        for i in range(lives):
            life_icon = create_life_icon()
            screen.blit(life_icon, (20 + i * 45, 15))
        
        # วาดความเร็วเกม
        speed_text = f"SPEED: {game_speed:.1f}"
        speed_color = COLORS["cyan"] if slow_motion else COLORS["light_blue"]
        speed_surface = info_font.render(speed_text, True, speed_color)
        screen.blit(speed_surface, (SCREEN_WIDTH - speed_surface.get_width() - 20, 20))
        
        # วาด power-up indicators
        y_offset = 60
        for power_type, start_time in active_power_ups.items():
            time_left = 0
            if power_type == "slow_motion":
                time_left = slow_motion_timer / 1000
                color = COLORS["cyan"]
                symbol = "⏱"
            elif power_type == "double_points":
                time_left = double_points_timer / 1000
                color = COLORS["gold"]
                symbol = "2X"
            elif power_type == "big_paddle":
                color = COLORS["purple"]
                symbol = "🔨"
            elif power_type == "shield":
                time_left = shield_timer / 1000
                color = COLORS["blue"]
                symbol = "🛡"
            else:
                continue
            
            if time_left > 0:
                power_text = f"{symbol} {time_left:.1f}s"
            else:
                power_text = symbol
                
            power_surface = pygame.font.SysFont("arial", 20).render(power_text, True, color)
            screen.blit(power_surface, (SCREEN_WIDTH - power_surface.get_width() - 20, y_offset))
            y_offset += 25
        
        # วาดคำแนะนำในเกม
        draw_text_with_effect("ESC: MENU  R: RESET POWER-UPS", info_font, 
                             COLORS["white"], SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30, center=True)
        
        if game_state == "game_over":
            # วาดหน้าจอ Game Over
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            draw_text_with_effect("GAME OVER", title_font, COLORS["red"], 
                                 SCREEN_WIDTH//2, 180, center=True, effect="neon", 
                                 effect_color=COLORS["orange"])
            draw_text_with_effect("SCORE: " + str(score), score_font, COLORS["yellow"], 
                                 SCREEN_WIDTH//2, 260, center=True, effect="shadow")
            
            if score == high_score:
                draw_text_with_effect("NEW HIGH SCORE!", score_font, COLORS["gold"], 
                                     SCREEN_WIDTH//2, 310, center=True, effect="glow")
            
            restart_button.draw(screen)
            
            # เอฟเฟกต์ particle ในหน้า Game Over
            if len(particles) < 100 and random.random() < 0.3:
                particles.append(Particle(
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                    random.choice([COLORS["red"], COLORS["orange"], COLORS["yellow"]]),
                    "firework"
                ))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()