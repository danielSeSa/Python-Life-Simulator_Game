import pygame
import random
import time
import sys

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Life Simulator - Epic Edition")

# Colors - Improved Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_CHARCOAL = (50, 50, 50) # For main text
MEDIUM_GRAY = (150, 150, 150) # For borders and inactive elements
LIGHT_GRAY = (220, 220, 220) # For soft backgrounds
VERY_LIGHT_GRAY = (240, 240, 240) # For main page background
RED = (220, 50, 50)
DARK_RED = (150,0,0)
GREEN = (60, 179, 113) # Softer green
BLUE = (70, 130, 180) # Steel blue
LIGHT_BLUE = (173, 216, 230)
INPUT_BOX_ACTIVE_COLOR = pygame.Color('dodgerblue2')
INPUT_BOX_INACTIVE_COLOR = MEDIUM_GRAY
PINK = (255,105,180)
DARK_PINK = (200,80,150)
ORANGE = (255, 165, 0)
PURPLE = (128,0,128)
GOLD = (255,215,0)

# Theme Colors
COLOR_BACKGROUND = VERY_LIGHT_GRAY
COLOR_TEXT = DARK_CHARCOAL
COLOR_PANEL_BG = WHITE
COLOR_BORDER = MEDIUM_GRAY
COLOR_BUTTON_PRIMARY = BLUE
COLOR_BUTTON_SECONDARY = ORANGE
COLOR_BUTTON_SUCCESS = GREEN
COLOR_BUTTON_DANGER = RED
COLOR_BUTTON_TEXT = WHITE
COLOR_BUTTON_SHADOW = MEDIUM_GRAY

# Fonts
DEFAULT_FONT_NAME = None
try:
    # Prioritize common English fonts
    english_fonts = ['Arial', 'Helvetica', 'Verdana', 'Tahoma', 'DejaVuSans']
    font_found = False
    for eng_font in english_fonts:
        matched_path = pygame.font.match_font(eng_font, bold=False)
        if matched_path:
            DEFAULT_FONT_NAME = matched_path
            font_found = True
            break
    if not font_found: # Fallback to Pygame's default system font if none are found
        print("Warning: Could not find preferred English fonts. Using Pygame's default system font.")
except Exception as e:
    print(f"Warning: Could not match preferred fonts (Error: {e}). Using Pygame's default system font.")

FONT_XXSMALL = pygame.font.Font(DEFAULT_FONT_NAME, 14)
FONT_XSMALL = pygame.font.Font(DEFAULT_FONT_NAME, 16)
FONT_SMALL = pygame.font.Font(DEFAULT_FONT_NAME, 18)
FONT_MEDIUM = pygame.font.Font(DEFAULT_FONT_NAME, 20)
FONT_LARGE = pygame.font.Font(DEFAULT_FONT_NAME, 32)
FONT_TITLE = pygame.font.Font(DEFAULT_FONT_NAME, 40)
FONT_BUTTON = pygame.font.Font(DEFAULT_FONT_NAME, 18) 
FONT_BUTTON_AGE_UP = pygame.font.Font(DEFAULT_FONT_NAME, 20) # Slightly larger for Age Up button

# --- Helper: Generate Random Names (English) ---
MALE_NAMES = ["Michael", "David", "John", "James", "Robert", "Chris", "Daniel", "Paul", "Mark", "Brian"]
FEMALE_NAMES = ["Jennifer", "Linda", "Patricia", "Mary", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

def generate_random_name(gender):
    first_name = random.choice(MALE_NAMES) if gender == "male" else random.choice(FEMALE_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"

# --- Character Class ---
class Person:
    def __init__(self, name, gender, age=0):
        self.name = name
        self.gender = gender
        self.age = age

class Character(Person):
    def __init__(self, name, gender):
        super().__init__(name, gender, age=0)
        self.health = random.randint(70, 100)
        self.happiness = random.randint(50, 100)
        self.smarts = random.randint(20, 80)
        self.looks = random.randint(20, 80)
        self.money = 1000
        self.alive = True
        self.job = None
        self.part_time_job = None
        self.current_annual_salary = 0
        self.current_part_time_annual_salary = 0
        self.education_level = "Uneducated"
        self.university_major = None
        self.skills = []
        self.cause_of_death = ""
        self.significant_events = []
        self.houses_owned = []
        self.cars_owned = []
        self.in_school = False
        self.prison_time = 0
        self.criminal_record = False

        self.parents = {
            "father": Person(generate_random_name("male"), "male", random.randint(self.age + 20, self.age + 40)),
            "mother": Person(generate_random_name("female"), "female", random.randint(self.age + 18, self.age + 38))
        }
        self.relationship_with_father = random.randint(40, 80)
        self.relationship_with_mother = random.randint(40, 80)
        self.partner = None
        self.is_married = False
        self.children = []
        self.years_married = 0
        self.years_with_partner = 0


    def age_up(self):
        if not self.alive: return
        if self.prison_time > 0:
            self.prison_time -= 1
            self.happiness -= 10
            self.health -= 2
            message_log.append(f"Spent a year in prison. {self.prison_time} years remaining.")
            if self.prison_time == 0:
                message_log.append("Released from prison!")
                self.criminal_record = True
        else:
            self.age += 1
            self.significant_events.append(f"Age {self.age}: Birthday!")

            if self.parents["father"]: self.parents["father"].age += 1
            if self.parents["mother"]: self.parents["mother"].age += 1
            if self.partner:
                self.partner.age += 1
                self.years_with_partner +=1
                if self.is_married: self.years_married +=1
            for child in self.children: child.age +=1

            if self.job:
                self.money += self.current_annual_salary
                message_log.append(f"Received annual salary of ${self.current_annual_salary:,} from {self.job}.")
            if self.part_time_job:
                self.money += self.current_part_time_annual_salary
                message_log.append(f"Received annual part-time pay of ${self.current_part_time_annual_salary:,} from {self.part_time_job}.")

            total_maintenance = 0
            for house_name in self.houses_owned:
                house_data = next((h for h in AVAILABLE_ASSETS["Houses"] if h["name"] == house_name), None)
                if house_data: total_maintenance += house_data.get("maintenance", 0)
            for car_name in self.cars_owned:
                car_data = next((c for c in AVAILABLE_ASSETS["Cars"] if c["name"] == car_name), None)
                if car_data: total_maintenance += car_data.get("maintenance", 0)
            if total_maintenance > 0:
                self.money -= total_maintenance
                message_log.append(f"Paid ${total_maintenance:,} in asset maintenance.")

            if self.age > 50:
                self.health -= random.randint(1, 4)
                self.happiness -= random.randint(0, 3)
            
            if self.age == 18 and self.education_level == "High School": self.in_school = False
            if self.age > 22 and self.education_level == "University Student":
                if "Bachelor's Degree" not in self.education_level:
                    self.education_level = "Some University"; message_log.append("Dropped out of university."); self.in_school = False

            if self.partner and random.random() < 0.1: self.happiness -=1
            self.relationship_with_father = max(0, self.relationship_with_father - random.randint(0,2))
            self.relationship_with_mother = max(0, self.relationship_with_mother - random.randint(0,2))

        if self.age > 85 and random.random() < (0.03 * (self.age - 84)): self.die("Old age")
        elif self.age > 100 and random.random() < 0.2: self.die("Extreme old age")
        elif self.health <= 0: self.die("Health depleted")
        
        if not self.alive: return

        self.health = max(0, min(100, self.health))
        self.happiness = max(0, min(100, self.happiness))
        self.smarts = max(0, min(100, self.smarts))
        self.looks = max(0, min(100, self.looks))

    def die(self, cause):
        self.alive = False
        self.cause_of_death = cause
        self.significant_events.append(f"Age {self.age}: Died due to {cause}.")

    def add_event_log(self, event_description):
        self.significant_events.append(f"Age {self.age}: {event_description}")

    def can_work_part_time(self):
        return self.age >= 14 and self.age < 65 and not self.prison_time and \
               (self.education_level in ["Middle School", "High School", "University Student", "Some University"] or self.in_school)

    def can_work_full_time(self):
        return self.age >= 18 and self.age < 65 and not self.prison_time

# --- Helper Functions for Pygame ---
def draw_text(surface, text, font, color, x, y, center_aligned=False, top_right=False, max_width=None):
    # Standard LTR text drawing function
    if max_width:
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        
        line_height = font.get_linesize()
        total_height = len(lines) * line_height
        
        if center_aligned and len(lines) > 1: 
            y -= total_height // 2 - line_height // 2
        
        for i, line_text in enumerate(lines):
            text_surface = font.render(line_text, True, color)
            text_rect = text_surface.get_rect()
            current_y = y + i * line_height
            if center_aligned: text_rect.center = (x, current_y)
            elif top_right: text_rect.topright = (x, current_y)
            else: text_rect.topleft = (x, current_y)
            surface.blit(text_surface, text_rect)
        return total_height
    else:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center_aligned: text_rect.center = (x, y)
        elif top_right: text_rect.topright = (x,y)
        else: text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)
        return font.get_linesize()


# --- Game UI Drawing Functions ---
STATS_PANEL_WIDTH = SCREEN_WIDTH * 0.30
STATS_PANEL_X = 10
STATS_PANEL_Y = 10
STATS_PANEL_HEIGHT = SCREEN_HEIGHT - 20

def display_character_stats(surface, character):
    panel_rect = pygame.Rect(STATS_PANEL_X, STATS_PANEL_Y, STATS_PANEL_WIDTH, STATS_PANEL_HEIGHT)
    pygame.draw.rect(surface, COLOR_PANEL_BG, panel_rect, border_radius=10)
    pygame.draw.rect(surface, COLOR_BORDER, panel_rect, 2, border_radius=10)

    y_offset = STATS_PANEL_Y + 15
    x_margin = STATS_PANEL_X + 15
    content_width = STATS_PANEL_WIDTH - 30
    line_spacing = 5 # Added spacing between lines

    name_text = f"Name: {character.name}"
    age_text = f"Age: {character.age}"
    gender_text = f"Gender: {'Male' if character.gender == 'male' else 'Female'}"
    
    y_offset += draw_text(surface, name_text, FONT_MEDIUM, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing
    y_offset += draw_text(surface, age_text, FONT_MEDIUM, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing
    y_offset += draw_text(surface, gender_text, FONT_MEDIUM, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing + 5

    pygame.draw.line(surface, COLOR_BORDER, (x_margin, y_offset), (x_margin + content_width, y_offset), 1)
    y_offset += 10

    stats_with_bars = [("Health", character.health), ("Happiness", character.happiness), ("Smarts", character.smarts), ("Looks", character.looks)]
    bar_height = 18
    text_bar_spacing = 10 # Space between text and bar
    
    for label, value in stats_with_bars:
        # Display text (label and value)
        stat_text = f"{label}: {value}/100"
        text_surface = FONT_SMALL.render(stat_text, True, COLOR_TEXT)
        text_rect = text_surface.get_rect(topleft=(x_margin, y_offset))
        surface.blit(text_surface, text_rect)
        
        # Calculate bar position based on text width
        bar_x = x_margin + text_rect.width + text_bar_spacing
        bar_width_total = content_width - text_rect.width - text_bar_spacing - 5 # Adjusted for padding
        
        if bar_width_total > 10: # Ensure bar is wide enough to be visible
            pygame.draw.rect(surface, LIGHT_GRAY, (bar_x, y_offset + 2, bar_width_total, bar_height), border_radius=5)
            fill_width = (value / 100) * bar_width_total
            bar_color = GREEN if value > 60 else ORANGE if value > 30 else RED
            pygame.draw.rect(surface, bar_color, (bar_x, y_offset + 2, fill_width, bar_height), border_radius=5)
            pygame.draw.rect(surface, DARK_CHARCOAL, (bar_x, y_offset + 2, bar_width_total, bar_height), 1, border_radius=5)
        y_offset += FONT_SMALL.get_linesize() + line_spacing + 2

    y_offset += 10
    pygame.draw.line(surface, COLOR_BORDER, (x_margin, y_offset), (x_margin + content_width, y_offset), 1)
    y_offset += 10

    money_color = GREEN if character.money >=0 else RED
    y_offset += draw_text(surface, f"Money: ${character.money:,}", FONT_MEDIUM, money_color, x_margin, y_offset, max_width=content_width) + line_spacing

    current_job_text = character.job if character.job else 'Unemployed'
    if character.part_time_job:
        current_job_text = f"PT: {character.part_time_job}" + (f", FT: {character.job}" if character.job else "")
    y_offset += draw_text(surface, f"Job: {current_job_text}", FONT_XSMALL, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing
    
    edu_text = f"Education: {character.education_level}"
    if character.university_major: edu_text += f" ({character.university_major})"
    y_offset += draw_text(surface, edu_text, FONT_XSMALL, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing

    if character.houses_owned:
        house_text = f"House(s): {', '.join(character.houses_owned[:2])}" 
        if len(character.houses_owned) > 2: house_text += "..."
        y_offset += draw_text(surface, house_text, FONT_XXSMALL, DARK_CHARCOAL, x_margin, y_offset, max_width=content_width) + line_spacing
    if character.cars_owned:
        car_text = f"Car(s): {', '.join(character.cars_owned[:2])}"
        if len(character.cars_owned) > 2: car_text += "..."
        y_offset += draw_text(surface, car_text, FONT_XXSMALL, DARK_CHARCOAL, x_margin, y_offset, max_width=content_width) + line_spacing
    if character.skills:
        skill_text = f"Skills: {', '.join(character.skills[:3])}"
        if len(character.skills) > 3: skill_text += "..."
        y_offset += draw_text(surface, skill_text, FONT_XXSMALL, DARK_CHARCOAL, x_margin, y_offset, max_width=content_width) + line_spacing
    
    y_offset += 10
    pygame.draw.line(surface, COLOR_BORDER, (x_margin, y_offset), (x_margin + content_width, y_offset), 1)
    y_offset += 10

    partner_status = "Single"
    if character.is_married and character.partner: partner_status = f"Married to {character.partner.name}"
    elif character.partner: partner_status = f"Dating {character.partner.name}"
    y_offset += draw_text(surface, f"Status: {partner_status}", FONT_XSMALL, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing
    if character.children:
        child_text = f"Children: {len(character.children)}"
        y_offset += draw_text(surface, child_text, FONT_XSMALL, COLOR_TEXT, x_margin, y_offset, max_width=content_width) + line_spacing
    
    if character.prison_time > 0:
        draw_text(surface, f"In Prison: {character.prison_time} yrs left", FONT_SMALL, DARK_RED, x_margin, STATS_PANEL_Y + STATS_PANEL_HEIGHT - 40, max_width=content_width)


INTERACTION_PANEL_X = STATS_PANEL_X + STATS_PANEL_WIDTH + 10
INTERACTION_PANEL_Y = 10
INTERACTION_PANEL_WIDTH = SCREEN_WIDTH - INTERACTION_PANEL_X - 10
INTERACTION_PANEL_HEIGHT = SCREEN_HEIGHT * 0.70 # Adjusted to make space for buttons below

def display_main_interaction_area(surface, message_log, current_event_title, choices_text_or_buttons):
    box_rect = pygame.Rect(INTERACTION_PANEL_X, INTERACTION_PANEL_Y, INTERACTION_PANEL_WIDTH, INTERACTION_PANEL_HEIGHT)
    
    pygame.draw.rect(surface, COLOR_PANEL_BG, box_rect, border_radius=10)
    pygame.draw.rect(surface, COLOR_BORDER, box_rect, 2, border_radius=10)

    padding = 15
    log_y_start = box_rect.top + padding
    content_width = box_rect.width - 2 * padding
    
    max_log_lines_display = 5 
    effective_log = [msg for msg in message_log if msg.strip()]
    start_index = max(0, len(effective_log) - max_log_lines_display)
    temp_y = log_y_start
    for msg in effective_log[start_index:]:
        temp_y += draw_text(surface, msg, FONT_SMALL, DARK_CHARCOAL, box_rect.left + padding, temp_y, max_width=content_width) + 3
    
    title_y = temp_y + 15
    if current_event_title: 
        title_y += draw_text(surface, current_event_title, FONT_MEDIUM, COLOR_TEXT, 
                        box_rect.centerx, title_y, center_aligned=True,
                        max_width=content_width) + 20
    
    if isinstance(choices_text_or_buttons, str) and choices_text_or_buttons: 
         draw_text(surface, choices_text_or_buttons, FONT_SMALL, BLUE, 
              box_rect.left + padding, title_y, 
              max_width=content_width)


# --- Button Class ---
class Button:
    def __init__(self, x, y, width, height, text, base_color=COLOR_BUTTON_PRIMARY, text_color=COLOR_BUTTON_TEXT, font=FONT_BUTTON, border_radius=8, action=None, data=None, enabled=True, shadow_offset=3):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.base_color = base_color
        self.hover_color = (max(0, base_color[0]-20), max(0, base_color[1]-20), max(0, base_color[2]-20))
        self.pressed_color = (max(0, base_color[0]-40), max(0, base_color[1]-40), max(0, base_color[2]-40))
        self.disabled_color = MEDIUM_GRAY
        self.text_color = text_color
        self.font = font
        self.border_radius = border_radius
        self.action = action 
        self.data = data 
        self.enabled = enabled
        self.is_hovered = False
        self.is_pressed = False
        self.shadow_offset = shadow_offset
        self.shadow_color = COLOR_BUTTON_SHADOW

    def draw(self, surface):
        current_color = self.base_color
        text_col = self.text_color
        
        if not self.enabled:
            current_color = self.disabled_color
            text_col = DARK_CHARCOAL
        elif self.is_pressed:
            current_color = self.pressed_color
        elif self.is_hovered: 
            current_color = self.hover_color
        
        shadow_rect = self.rect.copy()
        shadow_rect.x += self.shadow_offset
        shadow_rect.y += self.shadow_offset
        pygame.draw.rect(surface, self.shadow_color, shadow_rect, border_radius=self.border_radius)

        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        
        draw_text(surface, self.text, self.font, text_col, self.rect.centerx, self.rect.centery, center_aligned=True, max_width=self.rect.width-10)

    def handle_event(self, event):
        if not self.enabled:
            self.is_hovered = False
            self.is_pressed = False
            return False

        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered:
                self.is_pressed = True
                return False
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.is_hovered:
                self.is_pressed = False
                return True
            self.is_pressed = False
        return False


# --- InputBox Class ---
class InputBox:
    def __init__(self, x, y, w, h, font=FONT_MEDIUM, text=''):
        self.rect = pygame.Rect(x, y, w, h); self.color = INPUT_BOX_INACTIVE_COLOR; self.text = text
        self.font = font; self.txt_surface = self.font.render(text, True, COLOR_TEXT); self.active = False
        self.max_length = 20
        self.border_radius = 5
        self.text_padding = 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = INPUT_BOX_ACTIVE_COLOR if self.active else INPUT_BOX_INACTIVE_COLOR
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN: self.active = False; self.color = INPUT_BOX_INACTIVE_COLOR; return "enter_pressed" 
            elif event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif len(self.text) < self.max_length and event.unicode.isprintable(): self.text += event.unicode
            self.txt_surface = self.font.render(self.text, True, COLOR_TEXT) 
        return None

    def draw(self, screen_surface): 
        pygame.draw.rect(screen_surface, self.color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen_surface, DARK_CHARCOAL, self.rect, 2, border_radius=self.border_radius)
        
        text_x = self.rect.x + self.text_padding
        screen_surface.blit(self.txt_surface, (text_x, self.rect.y + (self.rect.h - self.txt_surface.get_height()) // 2))
        
        if self.active and time.time() % 1 < 0.5:
            cursor_x_offset = self.txt_surface.get_width()
            cursor_pos_x = text_x + cursor_x_offset
            pygame.draw.line(screen_surface, COLOR_TEXT, (cursor_pos_x + 2, self.rect.y + 8), (cursor_pos_x + 2, self.rect.y + self.rect.h - 8), 2)


# --- Game Data & Event Definitions (English) ---
EDUCATION_HIERARCHY = ["Uneducated", "Elementary School", "Middle School", "High School", "High School Diploma", "University Student", "Some University", "Bachelor's Degree", "Master's Degree", "PhD"]
UNIVERSITY_MAJORS = ["Computer Science", "Engineering", "Medicine", "Arts", "Business", "Law", "Science", "Education"]
SKILLS_AVAILABLE = ["Programming", "Musical Instrument", "Painting", "Writing", "Foreign Language", "Cooking", "Gardening"]

POSSIBLE_JOBS = {
    "Newspaper Delivery": {"type": "part_time", "salary_range": (7, 12), "smarts_req": 5, "edu_req": "Middle School", "hourly": True, "age_min": 12, "age_max": 18},
    "Babysitter": {"type": "part_time", "salary_range": (8, 15), "smarts_req": 10, "edu_req": "Middle School", "hourly": True, "age_min": 14, "age_max": 22},
    "Fast Food Worker": {"type": "part_time", "salary_range": (10, 16), "smarts_req": 10, "edu_req": "High School", "hourly": True, "age_min": 16},
    "Retail Cashier": {"type": "part_time", "salary_range": (11, 17), "smarts_req": 15, "edu_req": "High School", "hourly": True, "age_min": 16},
    "Library Assistant (PT)": {"type": "part_time", "salary_range": (12, 20), "smarts_req": 40, "edu_req": "High School", "hourly": True, "age_min": 16},
    "Janitor": {"type": "full_time_no_degree", "salary_range": (28000, 42000), "smarts_req": 5, "edu_req": "Uneducated"},
    "Construction Worker": {"type": "full_time_no_degree", "salary_range": (35000, 60000), "smarts_req": 10, "edu_req": "Uneducated"},
    "Office Clerk": {"type": "full_time_no_degree", "salary_range": (32000, 48000), "smarts_req": 30, "edu_req": "High School Diploma"},
    "Truck Driver": {"type": "full_time_no_degree", "salary_range": (45000, 75000), "smarts_req": 20, "edu_req": "High School Diploma"},
    "Teacher": {"type": "full_time_degree", "salary_range": (48000, 75000), "smarts_req": 60, "edu_req": "Bachelor's Degree", "major_bonus": "Education"},
    "Accountant": {"type": "full_time_degree", "salary_range": (58000, 95000), "smarts_req": 65, "edu_req": "Bachelor's Degree", "major_bonus": "Business"},
    "Software Engineer": {"type": "full_time_degree", "salary_range": (75000, 130000), "smarts_req": 75, "edu_req": "Bachelor's Degree", "major_bonus": "Computer Science"},
    "Doctor": {"type": "full_time_degree", "salary_range": (160000, 350000), "smarts_req": 85, "edu_req": "Master's Degree", "major_bonus": "Medicine"},
    "Lawyer": {"type": "full_time_degree", "salary_range": (80000, 200000), "smarts_req": 80, "edu_req": "Bachelor's Degree", "major_bonus": "Law"},
    "University Professor": {"type": "full_time_degree", "salary_range": (70000, 150000), "smarts_req": 80, "edu_req": "PhD", "major_bonus": None},
}
AVAILABLE_ASSETS = {
    "Houses": [
        {"name": "Rented Apartment", "price": 5000, "effect": {"happiness": 5}, "maintenance": 200},
        {"name": "Small Starter Home", "price": 80000, "effect": {"happiness": 15}, "maintenance": 500},
        {"name": "Suburban House", "price": 250000, "effect": {"happiness": 25}, "maintenance": 1000},
        {"name": "Luxury Condo", "price": 750000, "effect": {"happiness": 35, "looks": 5}, "maintenance": 2500},
        {"name": "Mansion", "price": 2000000, "effect": {"happiness": 50, "looks": 10}, "maintenance": 5000},
    ],
    "Cars": [
        {"name": "Old Beater", "price": 2000, "effect": {"happiness": 3}, "maintenance": 100},
        {"name": "Reliable Sedan", "price": 15000, "effect": {"happiness": 10}, "maintenance": 50},
        {"name": "Sports Car", "price": 50000, "effect": {"happiness": 20, "looks": 5}, "maintenance": 300},
        {"name": "Luxury SUV", "price": 70000, "effect": {"happiness": 15, "looks": 3}, "maintenance": 200},
        {"name": "Exotic Car", "price": 250000, "effect": {"happiness": 30, "looks": 15}, "maintenance": 1000},
    ]
}
AVAILABLE_ACTIVITIES = {
    "Go to Gym": {"cost": 50, "effect": {"health": (3, 7), "looks": (1,3), "happiness": (0,2)}, "description": "Work out at the gym."},
    "Go Clubbing": {"cost": 100, "effect": {"happiness": (5,15), "health": (-5,-2), "smarts": (-2,0)}, "description": "Party all night!"},
    "Read a Book": {"cost": 0, "effect": {"smarts": (2,5), "happiness": (1,3)}, "description": "Expand your mind."},
    "Meditate": {"cost": 0, "effect": {"happiness": (3,7), "health": (0,2)}, "description": "Find inner peace."},
    "Watch TV": {"cost": 0, "effect": {"happiness": (2,5), "smarts":(-1,0)}, "description": "Relax and watch some shows."},
    "Volunteer": {"cost": 0, "effect": {"happiness": (3,8)}, "description": "Help out in the community."},
    "Go on Vacation": {"cost": 2000, "effect": {"happiness": (15,30), "health": (1,3)}, "description": "Take a relaxing vacation."},
    "Learn a Skill": {"cost": 500, "effect": {"smarts": (3,7)}, "description": "Pick up a new skill."},
    "Gamble": {"cost": 100, "effect": {}, "description": "Try your luck!"},
    "Commit Petty Crime": {"cost": 0, "effect": {}, "description": "Risky business..."},
    "Visit Doctor": {"cost": 200, "effect": {"health": (5,15)}, "description": "Get a check-up."},
    "Date Someone": {"cost": 50, "effect": {}, "description": "Try to find a partner."},
}

def check_education_requirement(character_education, required_education):
    try: return EDUCATION_HIERARCHY.index(character_education) >= EDUCATION_HIERARCHY.index(required_education)
    except ValueError: return False

# --- Event Functions (English) ---
def event_childhood_illness(character, message_log):
    if character.age >= 3 and character.age <= 10 and random.random() < 0.15 and not character.prison_time:
        severity = random.randint(5, 20); character.health -= severity; character.happiness -= severity // 2
        msg = f"Suffered an illness (severity: {severity})."; message_log.append(msg); character.add_event_log(msg)
        if character.health < 20: msg2 = "The illness was very serious!"; message_log.append(msg2); character.add_event_log(msg2)
        return True, None, None 
    return False, None, None

def event_found_money(character, message_log):
    if random.random() < 0.03 and not character.prison_time: 
        amount = random.randint(10, 100) * (character.age // 5 + 1); character.money += amount; character.happiness += 5
        msg = f"Found ${amount:,} on the street!"; message_log.append(msg); character.add_event_log(msg)
        return True, None, None
    return False, None, None

def event_school_bully(character, message_log):
    if character.in_school and character.age >= 6 and character.age <= 17 and random.random() < 0.1 and not character.prison_time:
        event_text = "A school bully is bothering you. What do you do?"
        choices_text = "1: Ignore  2: Confront  3: Tell Teacher"
        def handle_choice(key):
            res_msg = ""
            if key == pygame.K_1: character.happiness -= 10; res_msg = "Ignored the bully, felt down."
            elif key == pygame.K_2:
                if random.random() < (character.smarts + character.looks) / 150: character.happiness += 10; character.smarts += 2; res_msg = "Successfully confronted the bully!"
                else: character.happiness -= 15; character.health -= 5; res_msg = "Failed to confront bully, got roughed up."
            elif key == pygame.K_3:
                if random.random() < 0.7: character.happiness += 5; res_msg = "Told teacher, issue somewhat resolved."
                else: character.happiness -= 5; res_msg = "Told teacher, but it didn't help."
            else: return
            message_log.append(res_msg); character.add_event_log(f"Bully: {res_msg}")
        return True, event_text, (choices_text, handle_choice)
    return False, None, None

def event_education_progression(character, message_log):
    edu_text, edu_choice_info = None, None
    if character.prison_time > 0: return False, None, None 

    if character.age == 6 and character.education_level == "Uneducated": character.education_level = "Elementary School"; character.smarts += random.randint(5,10); edu_text = "Started elementary school."; character.in_school = True
    elif character.age == 12 and character.education_level == "Elementary School": character.education_level = "Middle School"; character.smarts += random.randint(5,10); edu_text = "Started middle school."; character.in_school = True
    elif character.age == 15 and character.education_level == "Middle School": character.education_level = "High School"; character.smarts += random.randint(5,10); edu_text = "Started high school."; character.in_school = True
    elif character.age == 18 and character.education_level == "High School":
        character.in_school = False 
        edu_text = "High School finished. Go to university?"
        choices = "1: Yes  2: No (Get Diploma)"
        def handle_uni(key):
            res_msg = ""
            if key == pygame.K_1:
                if character.smarts > 50: 
                    character.education_level = "University Student"; character.smarts += random.randint(10,20); cost = random.randint(5000,15000); character.money -= cost; res_msg = f"Enrolled in university! (Tuition: ${cost:,})"; character.in_school = True
                    setup_major_selection_menu() 
                    return 
                else: character.happiness -= 5; character.education_level = "High School Diploma"; res_msg = "Not smart enough for university. Got Diploma."
            elif key == pygame.K_2: character.education_level = "High School Diploma"; res_msg = "Skipped university. Got High School Diploma."
            else: return
            message_log.append(res_msg); character.add_event_log(res_msg)
        edu_choice_info = (choices, handle_uni)
    elif character.age == 22 and character.education_level == "University Student" and character.university_major: 
        character.education_level = "Bachelor's Degree"; character.smarts += random.randint(10,20); character.happiness += 10; edu_text = f"Graduated with a Bachelor's Degree in {character.university_major}!"
        character.in_school = False
    
    if edu_text and not edu_choice_info: 
        message_log.append(edu_text); character.add_event_log(edu_text)
    return True if edu_text else False, edu_text, edu_choice_info


def event_job_offer_or_promotion(character, message_log):
    if not character.job or character.prison_time > 0: return False, None, None
    if random.random() < 0.05: 
        if random.random() < 0.3: 
            message_log.append(f"You've been fired from your job as a {character.job}!"); character.add_event_log("Fired from job.")
            character.job = None; character.current_annual_salary = 0; character.happiness -= 25
        else: 
            old_salary = character.current_annual_salary
            increase_percent = random.uniform(0.05, 0.20) 
            character.current_annual_salary = int(old_salary * (1 + increase_percent))
            character.smarts += random.randint(1,3)
            character.happiness += 15
            msg = f"Promoted at your job! New annual salary: ${character.current_annual_salary:,} (previously ${old_salary:,})."
            message_log.append(msg); character.add_event_log(msg)
        return True, None, None
    return False, None, None

def event_relationship_milestone(character, message_log):
    if character.prison_time > 0: return False, None, None
    if character.is_married and character.partner and character.age >= 20 and character.age <= 45 and len(character.children) < 4 and random.random() < 0.1: 
        child_gender = random.choice(["male", "female"])
        child_name = generate_random_name(child_gender)
        new_child = Person(child_name, child_gender, age=0)
        character.children.append(new_child)
        character.happiness += 25
        if character.partner: character.happiness += 5 
        msg = f"Congratulations! Your child, {child_name} ({child_gender}), was born!"
        message_log.append(msg); character.add_event_log(msg)
        return True, None, None
    return False, None, None


# --- Game State Variables ---
player = None
game_state = "character_creation" 
message_log = []
current_event_title_on_screen = "" 
current_choices_text_on_screen = "" 
current_choice_handler = None 
dynamic_buttons = [] 

# Character Creation UI Elements
INPUT_BOX_WIDTH = 300
INPUT_BOX_HEIGHT = 40
input_name_box = InputBox(SCREEN_WIDTH // 2 - INPUT_BOX_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
GENDER_BUTTON_WIDTH = 120
GENDER_BUTTON_HEIGHT = 40
gender_button_male = Button(SCREEN_WIDTH // 2 - GENDER_BUTTON_WIDTH - 10, SCREEN_HEIGHT // 2 - 30, GENDER_BUTTON_WIDTH, GENDER_BUTTON_HEIGHT, "Male", base_color=BLUE)
gender_button_female = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 30, GENDER_BUTTON_WIDTH, GENDER_BUTTON_HEIGHT, "Female", base_color=PINK)
start_life_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Start Life", base_color=COLOR_BUTTON_SUCCESS, font=FONT_LARGE)
selected_gender_for_creation = None

# Main Action Buttons (In-Game)
MAIN_ACTION_BUTTON_WIDTH = (INTERACTION_PANEL_WIDTH - 30) // 4 
MAIN_ACTION_BUTTON_HEIGHT = 50
MAIN_ACTION_BUTTON_Y = INTERACTION_PANEL_Y + INTERACTION_PANEL_HEIGHT + 15 # Adjusted Y for spacing

age_up_button = Button(INTERACTION_PANEL_X + (INTERACTION_PANEL_WIDTH - 220) / 2 , SCREEN_HEIGHT - 70, 220, 50, "Age Up (+1 Year)", base_color=COLOR_BUTTON_SUCCESS, font=FONT_BUTTON_AGE_UP) # Wider button

career_button = Button(INTERACTION_PANEL_X, MAIN_ACTION_BUTTON_Y, MAIN_ACTION_BUTTON_WIDTH, MAIN_ACTION_BUTTON_HEIGHT, "Career", base_color=COLOR_BUTTON_PRIMARY)
assets_button = Button(INTERACTION_PANEL_X + MAIN_ACTION_BUTTON_WIDTH + 10, MAIN_ACTION_BUTTON_Y, MAIN_ACTION_BUTTON_WIDTH, MAIN_ACTION_BUTTON_HEIGHT, "Assets", base_color=COLOR_BUTTON_SECONDARY)
activities_button = Button(INTERACTION_PANEL_X + 2*(MAIN_ACTION_BUTTON_WIDTH + 10), MAIN_ACTION_BUTTON_Y, MAIN_ACTION_BUTTON_WIDTH, MAIN_ACTION_BUTTON_HEIGHT, "Activities", base_color=PURPLE)
relationships_button = Button(INTERACTION_PANEL_X + 3*(MAIN_ACTION_BUTTON_WIDTH + 10), MAIN_ACTION_BUTTON_Y, MAIN_ACTION_BUTTON_WIDTH, MAIN_ACTION_BUTTON_HEIGHT, "Relationships", base_color=PINK)


# Game Over Buttons
restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Restart", base_color=COLOR_BUTTON_PRIMARY, font=FONT_LARGE) # Adjusted Y
quit_button_game_over = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 170, 200, 50, "Quit", base_color=COLOR_BUTTON_DANGER, font=FONT_LARGE) # Adjusted Y

def reset_game_for_creation():
    global game_state, message_log, current_event_title_on_screen, current_choices_text_on_screen, dynamic_buttons
    global current_choice_handler, player, selected_gender_for_creation
    input_name_box.text = ""; input_name_box.txt_surface = input_name_box.font.render("", True, COLOR_TEXT); input_name_box.active = False
    selected_gender_for_creation = None; 
    player = None; message_log = []; current_event_title_on_screen = ""; current_choices_text_on_screen = ""
    current_choice_handler = None; dynamic_buttons = []; game_state = "character_creation"

def create_menu_buttons(options, base_y_offset_from_title, item_font=FONT_MEDIUM, btn_width_ratio=0.7, action_prefix="", btn_color=MEDIUM_GRAY, text_color=COLOR_TEXT):
    buttons = []
    btn_height = 35 # Slightly smaller buttons for menus
    btn_width = (INTERACTION_PANEL_WIDTH * 0.85) * btn_width_ratio # Wider buttons in menus
    spacing = 8 # Reduced spacing
    
    start_x = INTERACTION_PANEL_X + (INTERACTION_PANEL_WIDTH - btn_width) / 2
    
    # Calculate available height for buttons in the interaction panel
    title_height_approx = 0
    if current_event_title_on_screen: # Check if there's a title
        title_height_approx = FONT_MEDIUM.get_linesize() + 20 # Approx title height + padding

    available_height_for_buttons = INTERACTION_PANEL_HEIGHT - (base_y_offset_from_title + title_height_approx + 15) # 15 for bottom padding
    
    # Dynamically adjust spacing if too many buttons
    num_buttons = len(options)
    total_button_height = num_buttons * btn_height
    total_spacing_needed = (num_buttons - 1) * spacing
    
    if total_button_height + total_spacing_needed > available_height_for_buttons:
        if num_buttons > 1:
            spacing = (available_height_for_buttons - total_button_height) / (num_buttons - 1)
            spacing = max(2, int(spacing)) # Ensure minimum spacing
        if num_buttons * btn_height > available_height_for_buttons : # If still too much, reduce button height
             btn_height = available_height_for_buttons // num_buttons - spacing


    base_y = INTERACTION_PANEL_Y + 15 + title_height_approx + base_y_offset_from_title
    
    for i, option_data in enumerate(options):
        if len(option_data) == 3:
            text, action_suffix, data = option_data
            enabled = True
        elif len(option_data) == 4: 
            text, action_suffix, data, enabled = option_data
        else: continue 

        action_name = f"{action_prefix}_{action_suffix}" if action_prefix else action_suffix
        button_base_color = LIGHT_GRAY if not enabled else MEDIUM_GRAY
        current_text_color = DARK_CHARCOAL if not enabled else COLOR_TEXT

        buttons.append(Button(start_x, base_y + i * (btn_height + spacing), btn_width, btn_height, text, 
                              base_color=button_base_color, text_color=current_text_color, font=item_font, 
                              action=action_name, data=data, enabled=enabled, border_radius=6))
    return buttons

# --- Menu Setup Functions (English) ---
def setup_main_playing_state():
    global game_state, current_event_title_on_screen, dynamic_buttons, current_choices_text_on_screen, current_choice_handler
    game_state = "playing"
    current_event_title_on_screen = ""
    current_choices_text_on_screen = ""
    current_choice_handler = None
    dynamic_buttons = []

def setup_career_menu():
    global game_state, current_event_title_on_screen, dynamic_buttons
    game_state = "career_menu"
    current_event_title_on_screen = "Career Options"
    dynamic_buttons = create_menu_buttons([
        ("Look for Part-time Job", "job_type_select", "part_time"),
        ("Look for Full-time Job (No Degree)", "job_type_select", "full_time_no_degree"),
        ("Look for Full-time Job (Degree)", "job_type_select", "full_time_degree"),
        ("Resign from current Job(s)", "resign_job", None),
        ("Back", "back_to_playing", None)
    ], 20, item_font=FONT_SMALL, btn_width_ratio=0.9) # Increased btn_width_ratio

def setup_job_listing_menu(job_type_filter):
    global game_state, current_event_title_on_screen, dynamic_buttons, player
    game_state = "job_listing"
    job_type_title = job_type_filter.replace("_", " ").title()
    current_event_title_on_screen = f"Available {job_type_title}s"
    job_options = []
    if not player: return

    for name, details in POSSIBLE_JOBS.items():
        if details["type"] == job_type_filter:
            eligible = True
            req_text_parts = []
            if player.smarts < details['smarts_req']: req_text_parts.append(f"Smarts {details['smarts_req']}+"); eligible=False
            if not check_education_requirement(player.education_level, details['edu_req']): req_text_parts.append(f"Edu: {details['edu_req']}"); eligible=False
            if player.age < details.get('age_min', 0) or player.age > details.get('age_max', 150): req_text_parts.append(f"Age {details.get('age_min',0)}-{details.get('age_max',150)}"); eligible=False
            
            if job_type_filter == "part_time" and not player.can_work_part_time(): eligible = False
            if job_type_filter != "part_time" and not player.can_work_full_time(): eligible = False
            if (job_type_filter == "part_time" and player.part_time_job) or \
               (job_type_filter != "part_time" and player.job): eligible = False

            pay_text = f"${details['salary_range'][0]:,}-${details['salary_range'][1]:,}"
            pay_text += "/hr" if details.get("hourly") else "/yr"
            
            job_display = f"{name} ({pay_text})"
            if not eligible: job_display += " (Not Eligible: " + ", ".join(req_text_parts) + ")"
            
            job_options.append((job_display, "apply_job", {"name": name, "details": details, "eligible": eligible}, eligible)) 
    
    job_options.append(("Back to Career Menu", "back_to_career", None))
    dynamic_buttons = create_menu_buttons(job_options, 10, item_font=FONT_XXSMALL, btn_width_ratio=0.95) # Increased btn_width_ratio

def setup_assets_menu():
    global game_state, current_event_title_on_screen, dynamic_buttons
    game_state = "assets_menu"
    current_event_title_on_screen = "Asset Options"
    dynamic_buttons = create_menu_buttons([
        ("Buy House", "asset_type_select", "Houses"),
        ("Buy Car", "asset_type_select", "Cars"),
        ("Back", "back_to_playing", None)
    ], 20, item_font=FONT_SMALL, btn_width_ratio=0.9)

def setup_asset_listing_menu(asset_category):
    global game_state, current_event_title_on_screen, dynamic_buttons
    current_event_title_on_screen = f"Available {asset_category}"
    asset_options = []
    for item in AVAILABLE_ASSETS[asset_category]:
        can_afford = player.money >= item['price']
        display_text = f"{item['name']} - ${item['price']:,}"
        if not can_afford: display_text += " (Too Expensive)"
        asset_options.append((display_text, "buy_asset", {"type": asset_category, "item": item}, can_afford))
    asset_options.append((f"Back to Assets Menu", "back_to_assets", None))
    dynamic_buttons = create_menu_buttons(asset_options, 10, item_font=FONT_XSMALL, btn_width_ratio=0.95)

def setup_activities_menu():
    global game_state, current_event_title_on_screen, dynamic_buttons
    game_state = "activities_menu"
    current_event_title_on_screen = "Choose an Activity"
    activity_options = []
    for act_name, details in AVAILABLE_ACTIVITIES.items():
        can_afford = player.money >= details['cost']
        display_text = f"{act_name} (Cost: ${details['cost']:,})"
        if not can_afford and details['cost'] > 0 : display_text += " (Too Expensive)"
        activity_options.append((display_text, "do_activity", act_name, can_afford or details['cost']==0))
    activity_options.append(("Back", "back_to_playing", None))
    # Use a smaller font for activities if there are many
    item_font_for_activities = FONT_XSMALL if len(AVAILABLE_ACTIVITIES) > 8 else FONT_SMALL 
    dynamic_buttons = create_menu_buttons(activity_options, 10, item_font=item_font_for_activities, btn_width_ratio=0.95)

def setup_relationships_menu():
    global game_state, current_event_title_on_screen, dynamic_buttons, player
    game_state = "relationships_menu"
    current_event_title_on_screen = "Relationships"
    options = []
    if player.parents["father"]: options.append((f"Father: {player.parents['father'].name} ({player.relationship_with_father}%)", "interact_parent", "father"))
    if player.parents["mother"]: options.append((f"Mother: {player.parents['mother'].name} ({player.relationship_with_mother}%)", "interact_parent", "mother"))
    if player.partner:
        status = "Married to" if player.is_married else "Dating"
        options.append((f"{status} {player.partner.name}", "interact_partner", None))
    else:
        options.append(("Find a Partner (Activity)", "go_to_activity_date", None)) 
    
    if player.is_married and len(player.children) < 4 : options.append(("Try for a Baby", "try_for_baby", None))
    for i, child in enumerate(player.children):
        options.append((f"Child {i+1}: {child.name} ({child.gender}, Age {child.age})", "interact_child", i))

    options.append(("Back", "back_to_playing", None))
    dynamic_buttons = create_menu_buttons(options, 10, item_font=FONT_XSMALL, btn_width_ratio=0.95)

def setup_major_selection_menu():
    global game_state, current_event_title_on_screen, dynamic_buttons
    game_state = "major_selection"
    current_event_title_on_screen = "Choose Your University Major"
    major_options = []
    for major in UNIVERSITY_MAJORS:
        major_options.append((major, "select_major", major))
    dynamic_buttons = create_menu_buttons(major_options, 10, item_font=FONT_SMALL, btn_width_ratio=0.9)

def setup_skill_selection_menu():
    global game_state, current_event_title_on_screen, dynamic_buttons, player
    game_state = "skill_selection"
    current_event_title_on_screen = "Learn a New Skill (Cost: $500)"
    skill_options = []
    for skill in SKILLS_AVAILABLE:
        if skill not in player.skills: 
             skill_options.append((skill, "learn_skill_confirm", skill, player.money >= 500))
    if not skill_options: skill_options.append(("No new skills to learn / Cannot afford", "back_to_activities", None, False))
    else: skill_options.append(("Back to Activities", "back_to_activities", None))
    dynamic_buttons = create_menu_buttons(skill_options, 10, item_font=FONT_SMALL, btn_width_ratio=0.9)


# --- Main Game Loop ---
def game_loop():
    global game_state, player, message_log, selected_gender_for_creation, dynamic_buttons
    global current_event_title_on_screen, current_choices_text_on_screen, current_choice_handler

    clock = pygame.time.Clock()
    running = True
    reset_game_for_creation() 

    active_buttons_list = []

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        if game_state != "event_choice": current_choices_text_on_screen = "" 

        active_buttons_list = []
        if game_state == "character_creation":
            active_buttons_list.extend([gender_button_male, gender_button_female, start_life_button])
        elif game_state == "playing":
            active_buttons_list.extend([age_up_button, career_button, assets_button, activities_button, relationships_button])
        elif game_state in ["career_menu", "assets_menu", "activities_menu", "relationships_menu", "job_listing", "asset_listing", "major_selection", "skill_selection", "relationship_interaction"]:
            active_buttons_list.extend(dynamic_buttons)
        elif game_state == "game_over":
            active_buttons_list.extend([restart_button, quit_button_game_over])


        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

            for btn in active_buttons_list:
                if btn.handle_event(event): 
                    action = btn.action
                    data = btn.data
                    
                    if game_state == "character_creation":
                        if btn == gender_button_male: selected_gender_for_creation = "male"
                        elif btn == gender_button_female: selected_gender_for_creation = "female"
                        elif btn == start_life_button:
                            if input_name_box.text.strip() and selected_gender_for_creation:
                                player = Character(input_name_box.text, selected_gender_for_creation)
                                message_log = [f"A new life begins for {player.name}! Age: {player.age}"]
                                message_log.append(f"Father: {player.parents['father'].name}, Mother: {player.parents['mother'].name}")
                                setup_main_playing_state()
                            else: message_log.append("Please enter a name and select a gender.")
                        break 

                    elif game_state == "playing":
                        if btn == age_up_button and player and player.alive:
                            current_event_title_on_screen = "" 
                            dynamic_buttons = []
                            player.age_up() 
                            if not player.alive: game_state = "game_over"; message_log.append(f"Final event: {player.cause_of_death}"); break 
                            
                            if player.prison_time == 0:
                                edu_occurred, edu_text, edu_choice_info = event_education_progression(player, message_log)
                                if edu_choice_info and game_state != "major_selection": 
                                    game_state = "event_choice"; current_event_title_on_screen = edu_text if edu_text else "An educational decision awaits."
                                    current_choices_text_on_screen, current_choice_handler = edu_choice_info
                                
                                if game_state == "playing": 
                                    event_job_offer_or_promotion(player, message_log)
                                    event_relationship_milestone(player, message_log)

                                    if random.random() < 0.3: 
                                        applicable_events = [event_childhood_illness, event_found_money, event_school_bully] if player.age <= 17 else [event_found_money]
                                        if applicable_events:
                                            chosen_event_func = random.choice(applicable_events)
                                            occurred, event_text_rand, choice_info_rand = chosen_event_func(player, message_log)
                                            if occurred and choice_info_rand:
                                                game_state = "event_choice"; current_event_title_on_screen = event_text_rand
                                                current_choices_text_on_screen, current_choice_handler = choice_info_rand
                            
                            if player.health <= 0 and player.alive: player.die("Critical health failure"); game_state = "game_over"; message_log.append(f"Final event: {player.cause_of_death}")
                        elif btn == career_button: setup_career_menu()
                        elif btn == assets_button: setup_assets_menu()
                        elif btn == activities_button: setup_activities_menu()
                        elif btn == relationships_button: setup_relationships_menu()
                        break
                    
                    elif game_state in ["career_menu", "assets_menu", "activities_menu", "relationships_menu", "job_listing", "asset_listing", "major_selection", "skill_selection", "relationship_interaction"]:
                        if action == "back_to_playing": setup_main_playing_state()
                        elif action == "job_type_select": setup_job_listing_menu(data)
                        elif action == "back_to_career": setup_career_menu()
                        elif action == "asset_type_select": setup_asset_listing_menu(data)
                        elif action == "back_to_assets": setup_assets_menu()
                        elif action == "back_to_activities": setup_activities_menu()
                        elif action == "back_to_relationships": setup_relationships_menu()

                        elif action == "do_activity": 
                            activity_name = data
                            activity_details = AVAILABLE_ACTIVITIES[activity_name]
                            
                            if activity_name == "Learn a Skill": setup_skill_selection_menu(); break
                            elif activity_name == "Gamble":
                                if player.money >= activity_details['cost']:
                                    player.money -= activity_details['cost']
                                    win_chance = 0.4 
                                    if random.random() < win_chance:
                                        winnings = random.randint(activity_details['cost'] // 2, activity_details['cost'] * 3)
                                        player.money += winnings
                                        message_log.append(f"Gambled and won ${winnings:,}!")
                                        player.happiness += 10
                                    else:
                                        message_log.append("Gambled and lost.")
                                        player.happiness -= 10
                                else: message_log.append("Not enough money to gamble.")
                                setup_main_playing_state()
                            elif activity_name == "Commit Petty Crime":
                                if random.random() < 0.6: 
                                    stolen_money = random.randint(50, 500)
                                    player.money += stolen_money
                                    message_log.append(f"Successfully committed a petty crime. Stole ${stolen_money:,}.")
                                    player.happiness -= 5 
                                else:
                                    message_log.append("Got caught committing a crime! Sent to jail.")
                                    player.happiness -= 30; player.health -= 5
                                    player.prison_time = random.randint(1,3) 
                                    player.criminal_record = True
                                    if player.job: message_log.append(f"Lost your job as a {player.job} due to arrest."); player.job = None; player.current_annual_salary = 0
                                    if player.part_time_job: message_log.append(f"Lost your part-time job as a {player.part_time_job} due to arrest."); player.part_time_job = None; player.current_part_time_annual_salary = 0
                                setup_main_playing_state()
                            elif activity_name == "Date Someone":
                                if not player.partner:
                                    if player.looks > 30 and random.random() < 0.5: 
                                        partner_gender = "female" if player.gender == "male" else "male"
                                        partner_name = generate_random_name(partner_gender)
                                        partner_age = random.randint(max(18, player.age - 5), player.age + 5)
                                        player.partner = Person(partner_name, partner_gender, partner_age)
                                        player.years_with_partner = 0
                                        player.happiness += 20
                                        message_log.append(f"Went on a date and started a relationship with {partner_name}!")
                                    else:
                                        message_log.append("Your date didn't go well.")
                                        player.happiness -= 5
                                else:
                                    message_log.append("You are already in a relationship.")
                                setup_main_playing_state()
                            else: 
                                if player.money >= activity_details['cost']:
                                    player.money -= activity_details['cost']
                                    for stat, val_change in activity_details["effect"].items():
                                        current_val = getattr(player, stat)
                                        if isinstance(val_change, tuple): setattr(player, stat, current_val + random.randint(val_change[0], val_change[1]))
                                        else: setattr(player, stat, current_val + val_change)
                                    message_log.append(f"Did activity: {activity_name}. Cost: ${activity_details['cost']:,}.")
                                else: message_log.append(f"Not enough money for {activity_name}.")
                                setup_main_playing_state()
                        
                        elif action == "learn_skill_confirm":
                            skill_to_learn = data
                            cost_to_learn = AVAILABLE_ACTIVITIES["Learn a Skill"]["cost"]
                            if player.money >= cost_to_learn and skill_to_learn not in player.skills:
                                player.money -= cost_to_learn
                                player.skills.append(skill_to_learn)
                                player.smarts += random.randint(3,7)
                                player.happiness += 5
                                message_log.append(f"Successfully learned {skill_to_learn}!")
                            elif skill_to_learn in player.skills:
                                message_log.append(f"You already know {skill_to_learn}.")
                            else:
                                message_log.append(f"Not enough money to learn {skill_to_learn}.")
                            setup_activities_menu() 

                        elif action == "apply_job":
                            if data["eligible"]:
                                job_name = data["name"]; details = data["details"]
                                if details["type"] == "part_time":
                                    if player.part_time_job: message_log.append(f"You already have a part-time job: {player.part_time_job}.")
                                    else: player.part_time_job = job_name; hourly_pay = random.randint(details["salary_range"][0], details["salary_range"][1]); player.current_part_time_annual_salary = hourly_pay * 20 * 52; player.happiness += 10; message_log.append(f"Hired as {job_name} (PT) at ${hourly_pay}/hr!")
                                else: 
                                    if player.job: message_log.append(f"You already have a full-time job: {player.job}.")
                                    else: player.job = job_name; player.current_annual_salary = random.randint(details["salary_range"][0], details["salary_range"][1]); player.happiness += 15; message_log.append(f"Hired as {job_name} (FT) with salary ${player.current_annual_salary:,}!")
                            else: message_log.append(f"Cannot apply for {data['name']}. Not eligible.")
                            setup_main_playing_state()

                        elif action == "resign_job":
                            resigned = False
                            if player.job: message_log.append(f"Resigned from FT job: {player.job}."); player.job = None; player.current_annual_salary = 0; player.happiness -=5; resigned = True
                            if player.part_time_job: message_log.append(f"Resigned from PT job: {player.part_time_job}."); player.part_time_job = None; player.current_part_time_annual_salary = 0; player.happiness -=3; resigned = True
                            if not resigned: message_log.append("No job to resign from.")
                            setup_main_playing_state()

                        elif action == "buy_asset":
                            asset_type = data["type"]; item = data["item"]
                            if player.money >= item["price"]:
                                player.money -= item["price"]
                                if asset_type == "Houses": player.houses_owned.append(item["name"])
                                elif asset_type == "Cars": player.cars_owned.append(item["name"])
                                for stat, val_change in item["effect"].items():
                                    current_val = getattr(player, stat)
                                    if isinstance(val_change, tuple): setattr(player, stat, current_val + random.randint(val_change[0], val_change[1]))
                                    else: setattr(player, stat, current_val + val_change)
                                message_log.append(f"Purchased {item['name']} for ${item['price']:,}!")
                                player.happiness += 10 
                            else: message_log.append(f"Not enough money to buy {item['name']}.")
                            setup_main_playing_state()
                        
                        elif action == "select_major":
                            player.university_major = data
                            message_log.append(f"You are now majoring in {data}.")
                            setup_main_playing_state() 

                        elif action == "interact_parent": 
                            rel_attr = f"relationship_with_{data}"
                            current_rel = getattr(player, rel_attr)
                            change = random.randint(3,10)
                            setattr(player, rel_attr, min(100, current_rel + change))
                            player.happiness += random.randint(1,3)
                            message_log.append(f"Spent time with your {data}. Relationship improved to {getattr(player, rel_attr)}%.")
                            setup_relationships_menu() 
                        
                        elif action == "interact_partner":
                            if player.partner and not player.is_married:
                                if player.happiness > 60 and player.years_with_partner > 0 and random.random() < 0.7:
                                    player.is_married = True
                                    player.years_married = 0
                                    player.happiness += 30
                                    message_log.append(f"You proposed to {player.partner.name} and they said YES! You are now married.")
                                else:
                                    message_log.append(f"Your marriage proposal to {player.partner.name} was rejected.")
                                    player.happiness -= 20
                                    if random.random() < 0.2: 
                                        message_log.append(f"{player.partner.name} broke up with you after the failed proposal.")
                                        player.partner = None; player.years_with_partner = 0
                            elif player.partner and player.is_married:
                                player.happiness += random.randint(5,10)
                                message_log.append(f"Spent quality time with your spouse, {player.partner.name}.")
                            setup_relationships_menu()

                        elif action == "go_to_activity_date":
                            setup_activities_menu() 
                        
                        elif action == "try_for_baby":
                            if player.is_married and player.partner:
                                if random.random() < 0.3: 
                                    child_gender = random.choice(["male", "female"])
                                    child_name = generate_random_name(child_gender)
                                    new_child = Person(child_name, child_gender, age=0)
                                    player.children.append(new_child)
                                    player.happiness += 30
                                    message_log.append(f"Great news! You're expecting a baby with {player.partner.name}! {child_name} ({child_gender}) was born.")
                                else:
                                    message_log.append(f"You and {player.partner.name} tried for a baby, but no luck this time.")
                                    player.happiness -= 2
                            else:
                                message_log.append("You need to be married to try for a baby.")
                            setup_relationships_menu()

                        if player: 
                            player.health = max(0, min(100, player.health)); player.happiness = max(0, min(100, player.happiness))
                            player.smarts = max(0, min(100, player.smarts)); player.looks = max(0, min(100, player.looks))
                            if player.health <= 0 and player.alive: player.die("Post-action health failure"); game_state = "game_over"
                        break 

                    elif game_state == "game_over":
                        if btn == restart_button: reset_game_for_creation()
                        elif btn == quit_button_game_over: running = False
                        break

            if game_state == "character_creation":
                input_name_box.handle_event(event)
            elif game_state == "event_choice": 
                if event.type == pygame.KEYDOWN:
                    if current_choice_handler: current_choice_handler(event.key)
                    if game_state != "major_selection": 
                        setup_main_playing_state() 
                    if player and player.health <= 0 and player.alive: player.die("Post-event health failure"); game_state = "game_over"
                    elif player and not player.alive: game_state = "game_over"
        
        screen.fill(COLOR_BACKGROUND)

        if game_state == "character_creation":
            title_y = SCREEN_HEIGHT // 4 - 50
            draw_text(screen, "Create Your Character", FONT_TITLE, COLOR_TEXT, SCREEN_WIDTH // 2, title_y, center_aligned=True)
            
            draw_text(screen, "Name:", FONT_MEDIUM, COLOR_TEXT, input_name_box.rect.x - 70, input_name_box.rect.centery, center_aligned=False)
            input_name_box.draw(screen)
            
            draw_text(screen, "Gender:", FONT_MEDIUM, COLOR_TEXT, gender_button_male.rect.x - 80 , gender_button_male.rect.centery, center_aligned=False)
            
            if selected_gender_for_creation == "male":
                pygame.draw.rect(screen, GOLD, gender_button_male.rect.inflate(6,6), border_radius=gender_button_male.border_radius+2, width=3)
            elif selected_gender_for_creation == "female":
                pygame.draw.rect(screen, GOLD, gender_button_female.rect.inflate(6,6), border_radius=gender_button_female.border_radius+2, width=3)

            for btn in active_buttons_list: btn.draw(screen)
            
            if message_log:
                log_y = start_life_button.rect.bottom + 20
                for msg_idx, msg_txt in enumerate(message_log[-2:]):
                    draw_text(screen, msg_txt, FONT_SMALL, RED if "Please" in msg_txt else COLOR_TEXT, SCREEN_WIDTH // 2, log_y + msg_idx * (FONT_SMALL.get_linesize() + 5), center_aligned=True, max_width=SCREEN_WIDTH - 40)


        elif game_state in ["playing", "event_choice", "career_menu", "assets_menu", "activities_menu", "relationships_menu", "job_listing", "asset_listing", "major_selection", "skill_selection"]:
            if player: display_character_stats(screen, player)
            display_main_interaction_area(screen, message_log, current_event_title_on_screen, current_choices_text_on_screen if game_state == "event_choice" else "")
            
            for btn in active_buttons_list: btn.draw(screen) 
        
        elif game_state == "game_over":
            overlay_rect = pygame.Rect(SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8, SCREEN_WIDTH * 3 // 4, SCREEN_HEIGHT * 3 // 4)
            pygame.draw.rect(screen, COLOR_PANEL_BG, overlay_rect, border_radius=15)
            pygame.draw.rect(screen, COLOR_BORDER, overlay_rect, 3, border_radius=15)

            center_x = overlay_rect.centerx
            current_y = overlay_rect.top + 30

            current_y += draw_text(screen, "Game Over", FONT_TITLE, RED, center_x, current_y, center_aligned=True) + 30
            if player:
                current_y += draw_text(screen, f"{player.name} died at age {player.age}.", FONT_LARGE, COLOR_TEXT, center_x, current_y, center_aligned=True, max_width=overlay_rect.width - 40) + 15
                current_y += draw_text(screen, f"Cause: {player.cause_of_death}", FONT_MEDIUM, COLOR_TEXT, center_x, current_y, center_aligned=True, max_width=overlay_rect.width - 40) + 15
                current_y += draw_text(screen, f"Final Money: ${player.money:,}", FONT_MEDIUM, COLOR_TEXT, center_x, current_y, center_aligned=True) + 25
                if player.significant_events:
                     current_y += draw_text(screen, "Key Events:", FONT_MEDIUM, COLOR_TEXT, center_x, current_y, center_aligned=True) + 10
                     # Ensure key events text doesn't overlap with buttons
                     max_event_y = restart_button.rect.top - 20 # Space above restart button
                     for sig_event in player.significant_events[-min(3, len(player.significant_events)):]:
                         event_height = FONT_XSMALL.get_linesize() + 5
                         if current_y + event_height < max_event_y:
                             current_y += draw_text(screen, f"- {sig_event}", FONT_XSMALL, DARK_CHARCOAL, center_x, current_y, center_aligned=True, max_width=overlay_rect.width - 60) + 2
                         else:
                             break # Stop if no more space
            
            # Ensure buttons are within the overlay
            restart_button.rect.centerx = center_x
            restart_button.rect.bottom = overlay_rect.bottom - 70 # Moved up
            quit_button_game_over.rect.centerx = center_x
            quit_button_game_over.rect.bottom = overlay_rect.bottom - 20 # Moved up
            
            for btn in active_buttons_list: btn.draw(screen)

        pygame.display.flip()
        clock.tick(30) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
