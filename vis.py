# vis.py
import pygame
import sys
import random
from enum import Enum
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BOARD_SIZE = 600
STATUS_WIDTH = 300
SPACE_COUNT = 28  # 4 sides * 7 spaces
SPACES_PER_SIDE = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Define SpaceType Enum
class SpaceType(Enum):
    SALARY = 1
    RAND_EVENT = 2
    EMPTY = 3

# Space class
class Space:
    def __init__(self, space_type):
        self.type = space_type

# Board class
class Board:
    def __init__(self):
        self.spaces = []
        # Create 28 spaces with alternating types
        for i in range(SPACE_COUNT):
            if i % 7 == 0:  # Every 7th space is salary
                self.spaces.append(Space(SpaceType.SALARY))
            elif i % 3 == 0:  # Every 3rd space is random event
                self.spaces.append(Space(SpaceType.RAND_EVENT))
            else:
                self.spaces.append(Space(SpaceType.EMPTY))

# Player class
class Player:
    def __init__(self):
        self.space = 0
        self.balance = 500  # Starting balance
        self.mood = 70
        self.month = 1
        self.days = 0
        self.investments = []
        self.game_over = False
        self.salary_received_this_month = False  # Track if salary received this month

    @staticmethod
    def mood_to_word(mood):
        if mood <= 20:
            return "terrible"
        elif 20 < mood <= 40:
            return "bad"
        elif 40 < mood <= 60:
            return "average"
        elif 60 < mood <= 80:
            return "good"
        elif 80 < mood <= 100:
            return "amazing"

    def status(self):
        if self.mood < 0:
            self.mood_punishment()
            if self.game_over:
                return
        
        if self.mood > 100:
            self.mood = 100

    def next_day(self):
        self.space = (self.space + 1) % SPACE_COUNT
        self.days += 1
        
        # Check if it's the first day of the month (salary day)
        if (self.days - 1) % 28 == 0:  # First day of new month
            self.month += 1
            self.salary_received_this_month = False  # Reset for new month
        
        # Give生活费 on the first day of each month
        if (self.days - 1) % 28 == 0 and not self.salary_received_this_month:
            self.balance += 840  # £210 per week * 4 weeks = £840 per month
            self.salary_received_this_month = True
        
        self.check_investments()

    def mood_punishment(self):
        if self.balance < 200:
            self.game_over = True
        else:
            # For visualization, we'll handle this differently
            self.balance -= 200
            self.mood = 100

    def add_investment(self, invest_type, amount):
        if amount > self.balance:
            return False

        if invest_type == "short":
            rate, duration = 0.10, 30
        elif invest_type == "long":
            rate, duration = 0.30, 90
        elif invest_type == "flexible":
            rate, duration = 0.02, 1
        else:
            return False

        self.balance -= amount
        self.investments.append({
            "type": invest_type,
            "amount": amount,
            "start_day": self.days,
            "duration": duration,
            "rate": rate
        })
        return True

    def check_investments(self):
        matured = []
        for inv in self.investments:
            elapsed = self.days - inv["start_day"]

            if inv["type"] in ("short", "long"):
                if elapsed >= inv["duration"]:
                    profit = round(inv["amount"] * inv["rate"])
                    total = inv["amount"] + profit
                    self.balance += total
                    matured.append(inv)
            else:
                daily_profit = inv["amount"] * inv["rate"] / 30
                self.balance += round(daily_profit, 2)

        for inv in matured:
            self.investments.remove(inv)

# Event functions
def yn_input(prompt):
    # This is for text-based, we'll handle differently in visualization
    return random.choice([True, False])

def abc_input(prompt, options):
    return random.choice(options)

def event(player, event_id):
    old_balance = player.balance
    old_mood = player.mood
    
    if event_id == 1:
        x = random.randint(10,50)
        player.balance += x
        player.mood += round(x/2.5)
        return f"You find £{x} on the street. Lucky you!"
    
    elif event_id == 2:
        x = random.randint(10,50)
        player.balance -= x
        player.mood -= round(x/2.5)
        return f"You are robbed by some plucky seagulls. You lose £{x}."
    
    elif event_id == 3:
        x = random.randint(1,5)
        if x == 1:
            player.balance += 50
            player.mood += 25
            return "You somehow turn a tidy profit of £50. Don't let it get to your head!"
        elif x == 2:
            return "You manage to break even before losing any money. Close shave!"
        else:
            player.balance -= 50
            player.mood -= 30
            return "You lose everything. Maybe invest in something better next time?"
    
    elif event_id == 4:
        x = random.randint(1, 3)
        player.balance -= 25
        if x == 1:
            player.mood += 20
            return "You have a great time and meet new friends! Worth every penny."
        elif x == 2:
            player.mood += 10
            return "It was fun but also time-consuming. You enjoy it a bit but lose some sleep."
        else:
            return "You didn't really click with anyone, but at least you tried something new."
    
    elif event_id == 5:
        options = ["Rent: -£30", "Buy used: -£50", "Buy new: -£80"]
        choice = random.choice(options)
        if "30" in choice:
            player.balance -= 30
        elif "50" in choice:
            player.balance -= 50
        else:
            player.balance -= 80
        return f"You need to buy textbooks. You choose: {choice}"
    
    elif event_id == 6:
        player.mood += 20
        return "You went to the library today. You feel more fulfilled and happier."
    
    elif event_id == 7:
        player.mood -= 10
        return "You feel like you have too many assignments and are under a huge pressure."
    
    elif event_id == 8:
        if random.choice([True, False]):
            player.mood -= 20
            player.balance += 30
            return "You help your friend cover his shift. -20 mood, +£30"
        else:
            return "You decline to help your friend."
    
    elif event_id == 9:
        x = random.randint(20, 50)
        player.balance -= x
        player.mood -= round(x / 2.5)
        return f"You're feeling unwell and spend £{x} on medicine."
    
    elif event_id == 10:
        x = random.randint(30, 80)
        player.balance -= x
        player.mood -= round(x / 2.5)
        return f"Your laptop slipped off the desk! You spend £{x} to get it repaired."
    
    else:
        # Simple events for other IDs
        if event_id % 2 == 0:
            gain = random.randint(10, 30)
            player.balance += gain
            player.mood += 5
            return f"Lucky day! You gain £{gain}."
        else:
            loss = random.randint(10, 30)
            player.balance -= loss
            player.mood -= 5
            return f"Unlucky day! You lose £{loss}."

# Space type colors
SPACE_COLORS = {
    SpaceType.SALARY: GREEN,
    SpaceType.RAND_EVENT: YELLOW,
    SpaceType.EMPTY: LIGHT_BLUE
}

class VisualGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("University Life - Financial Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 16)
        self.title_font = pygame.font.SysFont('Arial', 24, bold=True)
        
        # Load background images
        self.background = self.load_image("img/monopoly-money-board-game-real-background-free-vector.jpg", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.center_logo = self.load_image("img/Monopoly-Emblem.png", 200, 200)
        
        self.board = Board()
        self.player = Player()
        self.player_positions = [None] * SPACE_COUNT
        self.calculate_board_positions()
        self.current_event = None
        self.event_active = False
        self.event_choices = []
        self.investment_menu_active = False
        self.input_text = ""
        self.input_active = False
        self.message = ""
        self.message_timer = 0
        self.investment_option = None

    def load_image(self, path, width, height):
        """Load and scale an image"""
        try:
            if os.path.exists(path):
                image = pygame.image.load(path)
                return pygame.transform.scale(image, (width, height))
            else:
                print(f"Warning: Image not found at {path}")
                # Create a placeholder surface
                surface = pygame.Surface((width, height))
                surface.fill(LIGHT_BLUE)
                return surface
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            # Create a placeholder surface
            surface = pygame.Surface((width, height))
            surface.fill(LIGHT_BLUE)
            return surface

    def calculate_board_positions(self):
        """Calculate the positions for each space on the board"""
        board_margin = 50
        inner_size = BOARD_SIZE - 2 * board_margin
        space_size = inner_size // SPACES_PER_SIDE
        
        # Calculate positions for each side
        for i in range(SPACE_COUNT):
            side = i // SPACES_PER_SIDE
            pos_in_side = i % SPACES_PER_SIDE
            
            if side == 0:  # Top side (left to right)
                x = board_margin + pos_in_side * space_size + space_size // 2
                y = board_margin
            elif side == 1:  # Right side (top to bottom)
                x = BOARD_SIZE - board_margin
                y = board_margin + pos_in_side * space_size + space_size // 2
            elif side == 2:  # Bottom side (right to left)
                x = BOARD_SIZE - board_margin - pos_in_side * space_size - space_size // 2
                y = BOARD_SIZE - board_margin
            else:  # Left side (bottom to top)
                x = board_margin
                y = BOARD_SIZE - board_margin - pos_in_side * space_size - space_size // 2
            
            self.player_positions[i] = (x, y)

    def draw_board(self):
        """Draw the game board"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            pygame.draw.rect(self.screen, LIGHT_BLUE, (0, 0, BOARD_SIZE, BOARD_SIZE))
        
        # Draw center logo
        if self.center_logo:
            logo_x = (BOARD_SIZE - 200) // 2
            logo_y = (BOARD_SIZE - 200) // 2
            self.screen.blit(self.center_logo, (logo_x, logo_y))
        
        # Draw semi-transparent overlay for board area
        board_overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA)
        board_overlay.fill((255, 255, 255, 128))  # Semi-transparent white
        self.screen.blit(board_overlay, (0, 0))
        
        # Draw spaces
        for i, pos in enumerate(self.player_positions):
            space_type = self.board.spaces[i].type
            color = SPACE_COLORS.get(space_type, LIGHT_BLUE)
            
            # Draw space with semi-transparent background
            space_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(space_surface, (*color, 200), (20, 20), 20)  # Semi-transparent
            pygame.draw.circle(space_surface, BLACK, (20, 20), 20, 2)
            self.screen.blit(space_surface, (pos[0]-20, pos[1]-20))
            
            # Draw space number
            text = self.font.render(str(i+1), True, BLACK)
            text_rect = text.get_rect(center=pos)
            self.screen.blit(text, text_rect)
            
            # Draw space type indicator
            type_text = ""
            if space_type == SpaceType.SALARY:
                type_text = "£"
            elif space_type == SpaceType.RAND_EVENT:
                type_text = "?"
            
            type_surface = self.font.render(type_text, True, BLACK)
            type_rect = type_surface.get_rect(center=(pos[0], pos[1] - 25))
            self.screen.blit(type_surface, type_rect)
        
        # Draw player
        player_pos = self.player_positions[self.player.space]
        pygame.draw.circle(self.screen, RED, player_pos, 15)
        
        # Draw player indicator
        player_text = self.font.render("YOU", True, WHITE)
        player_text_rect = player_text.get_rect(center=player_pos)
        self.screen.blit(player_text, player_text_rect)

    def draw_status_panel(self):
        """Draw the status panel on the right side"""
        panel_x = BOARD_SIZE + 10
        
        # Draw panel background with semi-transparency
        panel_surface = pygame.Surface((STATUS_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel_surface.fill((255, 255, 255, 200))  # Semi-transparent white
        self.screen.blit(panel_surface, (panel_x, 0))
        pygame.draw.rect(self.screen, BLACK, (panel_x, 0, STATUS_WIDTH, SCREEN_HEIGHT), 2)
        
        # Draw title
        title = self.title_font.render("Student Status", True, BLACK)
        self.screen.blit(title, (panel_x + 20, 20))
        
        # Draw balance
        balance_text = self.font.render(f"Balance: £{self.player.balance:.2f}", True, BLACK)
        self.screen.blit(balance_text, (panel_x + 20, 60))
        
        # Draw mood with color coding
        mood_word = self.player.mood_to_word(self.player.mood)
        mood_color = BLACK
        if self.player.mood <= 20:
            mood_color = RED
        elif self.player.mood <= 40:
            mood_color = ORANGE
        elif self.player.mood <= 60:
            mood_color = YELLOW
        elif self.player.mood <= 80:
            mood_color = BLUE
        else:
            mood_color = GREEN
            
        mood_text = self.font.render(f"Mood: {self.player.mood} ({mood_word})", True, mood_color)
        self.screen.blit(mood_text, (panel_x + 20, 90))
        
        # Draw mood bar
        mood_bar_width = 200
        mood_fill = max(0, (self.player.mood / 100) * mood_bar_width)
        pygame.draw.rect(self.screen, GRAY, (panel_x + 20, 115, mood_bar_width, 15))
        pygame.draw.rect(self.screen, mood_color, (panel_x + 20, 115, mood_fill, 15))
        pygame.draw.rect(self.screen, BLACK, (panel_x + 20, 115, mood_bar_width, 15), 1)
        
        # Draw date
        date_text = self.font.render(f"Day: {self.player.space+1} of Month {self.player.month}", True, BLACK)
        self.screen.blit(date_text, (panel_x + 20, 140))
        
        # Draw next生活费 info
        days_until_salary = 28 - ((self.player.days - 1) % 28)
        salary_text = self.font.render(f"Time until the next living allowance is issued: {days_until_salary} days", True, GREEN)
        self.screen.blit(salary_text, (panel_x + 20, 170))
        
        # Draw current space info
        current_space = self.board.spaces[self.player.space]
        space_type_text = f"Current Space: {current_space.type.name}"
        space_text = self.font.render(space_type_text, True, BLACK)
        self.screen.blit(space_text, (panel_x + 20, 200))
        
        # Draw investments
        inv_title = self.title_font.render("Investments:", True, BLACK)
        self.screen.blit(inv_title, (panel_x + 20, 230))
        
        if not self.player.investments:
            no_inv_text = self.font.render("No active investments", True, GRAY)
            self.screen.blit(no_inv_text, (panel_x + 20, 260))
        else:
            for i, inv in enumerate(self.player.investments):
                days_left = inv["duration"] - (self.player.days - inv["start_day"])
                inv_text = self.font.render(
                    f"{inv['type']}: £{inv['amount']} ({days_left} days left)", 
                    True, BLACK
                )
                self.screen.blit(inv_text, (panel_x + 20, 260 + i * 25))
        
        # Draw controls
        controls_title = self.title_font.render("Controls:", True, BLACK)
        self.screen.blit(controls_title, (panel_x + 20, 380))
        
        controls = [
            "SPACE: Next day",
            "I: Open investment menu",
            "R: Restart game",
            "ESC: Quit game"
        ]
        
        for i, control in enumerate(controls):
            control_text = self.font.render(control, True, BLACK)
            self.screen.blit(control_text, (panel_x + 20, 410 + i * 25))
        
        # Draw生活费 info
        salary_info = self.font.render("生活费: £840/month", True, GREEN)
        self.screen.blit(salary_info, (panel_x + 20, 490))
        
        # Draw message if any
        if self.message and self.message_timer > 0:
            message_y = 520
            message_lines = self.wrap_text(self.message, self.font, STATUS_WIDTH - 40)
            for i, line in enumerate(message_lines):
                message_text = self.font.render(line, True, BLUE)
                self.screen.blit(message_text, (panel_x + 20, message_y + i * 20))
            self.message_timer -= 1
        
        # Draw game over if applicable
        if self.player.game_over:
            game_over_text = self.title_font.render("GAME OVER", True, RED)
            self.screen.blit(game_over_text, (panel_x + 20, 580))
            restart_text = self.font.render("Press R to restart", True, BLACK)
            self.screen.blit(restart_text, (panel_x + 20, 610))

    def draw_event_dialog(self):
        """Draw event dialog when an event occurs"""
        if not self.event_active or not self.current_event:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw dialog box
        dialog_width = 600
        dialog_height = 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Draw title
        title = self.title_font.render("Random Event!", True, BLUE)
        self.screen.blit(title, (dialog_x + 20, dialog_y + 20))
        
        # Draw event text (wrapped)
        event_lines = self.wrap_text(self.current_event, self.font, dialog_width - 40)
        for i, line in enumerate(event_lines):
            text = self.font.render(line, True, BLACK)
            self.screen.blit(text, (dialog_x + 20, dialog_y + 60 + i * 25))
        
        # Draw instruction
        inst_text = self.font.render("Press any key to continue...", True, GRAY)
        self.screen.blit(inst_text, (dialog_x + 20, dialog_y + dialog_height - 40))

    def draw_investment_menu(self):
        """Draw investment menu"""
        if not self.investment_menu_active:
            return
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw dialog box
        dialog_width = 500
        dialog_height = 400
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Draw title
        title = self.title_font.render("Investment Options", True, BLACK)
        self.screen.blit(title, (dialog_x + 20, dialog_y + 20))
        
        # Draw balance
        balance_text = self.font.render(f"Available: £{self.player.balance:.2f}", True, BLACK)
        self.screen.blit(balance_text, (dialog_x + 20, dialog_y + 60))
        
        # Draw investment options
        options = [
            "A: Short-term (3 months, 10% interest)",
            "B: Long-term (1 year, 30% interest)", 
            "C: Flexible (daily interest, 2% annual)",
            "D: Cancel"
        ]
        
        for i, option in enumerate(options):
            option_text = self.font.render(option, True, BLACK)
            self.screen.blit(option_text, (dialog_x + 20, dialog_y + 100 + i * 30))
        
        # Draw amount input
        amount_text = self.font.render(f"Amount: £{self.input_text}", True, BLACK)
        self.screen.blit(amount_text, (dialog_x + 20, dialog_y + 250))
        
        # Draw instruction
        if self.input_active:
            inst_text = self.font.render("Enter amount and press ENTER to confirm", True, BLUE)
            cancel_text = self.font.render("Press ESC to cancel", True, GRAY)
            self.screen.blit(inst_text, (dialog_x + 20, dialog_y + 280))
            self.screen.blit(cancel_text, (dialog_x + 20, dialog_y + 300))
        else:
            inst_text = self.font.render("Press A-D to choose investment type", True, GRAY)
            self.screen.blit(inst_text, (dialog_x + 20, dialog_y + 280))

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

    def set_message(self, message, duration=180):
        """Set a temporary message to display"""
        self.message = message
        self.message_timer = duration

    def handle_random_event(self):
        """Handle random event when landing on event space"""
        event_id = random.randint(1, 22)
        self.current_event = event(self.player, event_id)
        self.event_active = True

    def next_day(self):
        """Advance to the next day"""
        if self.player.game_over:
            return
            
        # Check current space type
        current_space = self.board.spaces[self.player.space]
        
        # Give生活费 on the first day of each month
        if (self.player.days) % 28 == 0 and not self.player.salary_received_this_month:
            self.player.balance += 840  # £210 per week * 4 weeks = £840 per month
            self.player.salary_received_this_month = True
            self.set_message("生活费 day! +£840", 120)
        
        if current_space.type == SpaceType.RAND_EVENT and not self.event_active:
            self.handle_random_event()
        
        # Move to next day
        self.player.next_day()
        
        # Check for game over due to mood
        if self.player.mood <= 0:
            self.player.mood_punishment()
            if self.player.game_over:
                self.set_message("Game Over! Your mood dropped too low.", 300)

    def handle_investment_input(self, amount_str, option):
        """Handle investment input"""
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.set_message("Amount must be positive")
                return
            if amount > self.player.balance:
                self.set_message("Not enough balance")
                return
            
            success = False
            if option == 'A':
                success = self.player.add_investment("short", amount)
                if success:
                    self.set_message(f"Invested £{amount} in short-term account")
            elif option == 'B':
                success = self.player.add_investment("long", amount)
                if success:
                    self.set_message(f"Invested £{amount} in long-term account")
            elif option == 'C':
                success = self.player.add_investment("flexible", amount)
                if success:
                    self.set_message(f"Invested £{amount} in flexible account")
            
            if success:
                self.investment_menu_active = False
                self.input_text = ""
                self.input_active = False
                self.investment_option = None
            
        except ValueError:
            self.set_message("Invalid amount")

    def restart_game(self):
        """Restart the game"""
        self.player = Player()
        self.event_active = False
        self.investment_menu_active = False
        self.input_text = ""
        self.input_active = False
        self.message = "Game restarted!"
        self.message_timer = 120

    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.event_active:
                        # Close event dialog
                        self.event_active = False
                    
                    elif self.investment_menu_active:
                        if self.input_active:
                            if event.key == pygame.K_RETURN:
                                # Process the entered amount with the selected option
                                if self.investment_option:
                                    self.handle_investment_input(self.input_text, self.investment_option)
                            elif event.key == pygame.K_BACKSPACE:
                                self.input_text = self.input_text[:-1]
                            elif event.key == pygame.K_ESCAPE:
                                self.investment_menu_active = False
                                self.input_active = False
                                self.input_text = ""
                                self.investment_option = None
                            else:
                                # Add character to input if it's a digit or decimal point
                                if event.unicode.isdigit() or event.unicode == '.':
                                    self.input_text += event.unicode
                        else:
                            if event.key in [pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d]:
                                option = chr(event.key).upper()
                                if option in ['A', 'B', 'C']:
                                    self.investment_option = option
                                    self.input_active = True
                                elif option == 'D':
                                    self.investment_menu_active = False
                                    self.set_message("Investment cancelled")
                            elif event.key == pygame.K_ESCAPE:
                                self.investment_menu_active = False
                    
                    else:
                        # Main game controls
                        if event.key == pygame.K_SPACE and not self.player.game_over:
                            self.next_day()
                        elif event.key == pygame.K_i and not self.player.game_over:
                            self.investment_menu_active = True
                            self.input_active = False
                            self.input_text = ""
                            self.investment_option = None
                        elif event.key == pygame.K_r:
                            self.restart_game()
                        elif event.key == pygame.K_ESCAPE:
                            running = False
            
            # Draw everything
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_status_panel()
            self.draw_event_dialog()
            self.draw_investment_menu()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = VisualGame()
    game.run()