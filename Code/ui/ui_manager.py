"""
UI Manager - Handles all UI rendering
"""
import pygame
from game.config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, UI_FONT, UI_FONT_SIZE, UI_PADDING,
    HEALTH_BAR_HEIGHT, XP_BAR_HEIGHT, COMBAT_LOG_LINES, COMBAT_LOG_WIDTH,
    COMBAT_LOG_HEIGHT, STATE_MENU, STATE_CHARACTER_SELECT, STATE_BATTLE, 
    STATE_GAME_OVER, STATE_VICTORY
)
from .combat_log import CombatLog
from .status_bars import HealthBar, XPBar, CooldownIndicator

class UIManager:
    """
    Manages all UI elements and rendering
    """
    def __init__(self, game_state):
        """
        Initialize the UI manager
        
        Args:
            game_state (GameState): Reference to the game state
        """
        self.game_state = game_state
        
        # Initialize pygame font
        pygame.font.init()
        self.font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE)
        self.title_font = pygame.font.SysFont(UI_FONT, UI_FONT_SIZE * 2)
        
        # Initialize UI components
        self.combat_log = CombatLog()
        self.health_bar = HealthBar()
        self.xp_bar = XPBar()
        self.cooldown_indicator = CooldownIndicator()
        
        # Colors
        self.colors = {
            "text": (255, 255, 255),
            "background": (0, 0, 0),
            "button": (80, 80, 80),
            "button_hover": (120, 120, 120),
            "button_text": (255, 255, 255),
            "warrior": (200, 0, 0),
            "archer": (0, 200, 0),
            "mage": (0, 0, 200)
        }
    
    def update(self, delta_time):
        """
        Update UI elements
        
        Args:
            delta_time (float): Time since last update in seconds
        """
        # UI updates if needed
        pass
    
    def render(self, screen):
        """
        Render UI based on current game state
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        # Clear screen
        screen.fill(self.colors["background"])
        
        # Render based on game state
        if self.game_state.current_state == STATE_MENU:
            self._render_menu(screen)
        elif self.game_state.current_state == STATE_CHARACTER_SELECT:
            self._render_character_select(screen)
        elif self.game_state.current_state == STATE_BATTLE:
            self._render_battle(screen)
        elif self.game_state.current_state == STATE_GAME_OVER:
            self._render_game_over(screen)
        elif self.game_state.current_state == STATE_VICTORY:
            self._render_victory(screen)
    
    def _render_menu(self, screen):
        """
        Render the main menu
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        # Title
        title_text = self.title_font.render("Auto-Battler RPG", True, self.colors["text"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Instructions
        instructions = [
            "Press ENTER to start a new game",
            "Press L to load a saved game",
            "Press ESC to exit"
        ]
        
        y_offset = SCREEN_HEIGHT // 2
        for instruction in instructions:
            text = self.font.render(instruction, True, self.colors["text"])
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(text, rect)
            y_offset += 40
        
        # Stats if any
        if self.game_state.victory_count > 0 or self.game_state.defeat_count > 0:
            stats_text = self.font.render(
                f"Victories: {self.game_state.victory_count} | Defeats: {self.game_state.defeat_count}",
                True, self.colors["text"]
            )
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(stats_text, stats_rect)
    
    def _render_character_select(self, screen):
        """
        Render the character selection screen
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        # Title
        title_text = self.title_font.render("Select Your Class", True, self.colors["text"])
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
        screen.blit(title_text, title_rect)
        
        # Character options
        characters = [
            {"name": "Warrior", "key": "1", "color": self.colors["warrior"], 
             "desc": "High HP and physical damage, low magic and speed"},
            {"name": "Archer", "key": "2", "color": self.colors["archer"], 
             "desc": "High speed and multi-hit attacks, low HP and defense"},
            {"name": "Mage", "key": "3", "color": self.colors["mage"], 
             "desc": "High magic damage and spell effects, low HP and defense"}
        ]
        
        # Calculate positions
        box_width = 250
        box_height = 300
        spacing = 30
        total_width = (box_width * len(characters)) + (spacing * (len(characters) - 1))
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, char in enumerate(characters):
            # Box position
            x = start_x + (i * (box_width + spacing))
            y = SCREEN_HEIGHT // 3
            
            # Draw box
            pygame.draw.rect(screen, char["color"], (x, y, box_width, box_height))
            pygame.draw.rect(screen, self.colors["text"], (x, y, box_width, box_height), 2)
            
            # Character name
            name_text = self.font.render(char["name"], True, self.colors["text"])
            name_rect = name_text.get_rect(center=(x + box_width // 2, y + 30))
            screen.blit(name_text, name_rect)
            
            # Key hint
            key_text = self.font.render(f"Press {char['key']} to select", True, self.colors["text"])
            key_rect = key_text.get_rect(center=(x + box_width // 2, y + box_height - 30))
            screen.blit(key_text, key_rect)
            
            # Description (word wrapped)
            words = char["desc"].split()
            line = ""
            line_height = self.font.get_height()
            y_text = y + 80
            
            for word in words:
                test_line = line + word + " "
                test_width = self.font.size(test_line)[0]
                
                if test_width > box_width - 20:
                    text = self.font.render(line, True, self.colors["text"])
                    screen.blit(text, (x + 10, y_text))
                    y_text += line_height
                    line = word + " "
                else:
                    line = test_line
            
            # Render last line
            if line:
                text = self.font.render(line, True, self.colors["text"])
                screen.blit(text, (x + 10, y_text))
        
        # Instructions
        instruction_text = self.font.render("ESC to return to menu", True, self.colors["text"])
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
    
    def _render_battle(self, screen):
        """
        Render the battle screen
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        player = self.game_state.player_character
        if not player:
            return
        
        # Render player character
        player_x = SCREEN_WIDTH // 4
        player_y = SCREEN_HEIGHT // 2
        player.render(screen, (player_x - player.sprite.get_width() // 2, 
                              player_y - player.sprite.get_height() // 2))
        
        # Render player health bar
        self._render_health_bar(screen, player, player_x, player_y + 50)
        
        # Render player XP bar
        self._render_xp_bar(screen, player, player_x, player_y + 50 + HEALTH_BAR_HEIGHT + 5)
        
        # Render player stats
        self._render_character_stats(screen, player, player_x - 100, player_y + 100)
        
        # Render enemies
        enemy_x = (SCREEN_WIDTH * 3) // 4
        enemy_y = SCREEN_HEIGHT // 2
        enemy_spacing = 80
        
        for i, enemy in enumerate(self.game_state.enemies):
            if enemy.is_alive():
                # Position enemies in a row or column based on count
                if len(self.game_state.enemies) <= 3:
                    offset_x = (i - (len(self.game_state.enemies) - 1) / 2) * enemy_spacing
                    enemy_pos_x = enemy_x + offset_x
                    enemy_pos_y = enemy_y
                else:
                    # Grid layout for more than 3 enemies
                    col = i % 2
                    row = i // 2
                    enemy_pos_x = enemy_x + (col - 0.5) * enemy_spacing
                    enemy_pos_y = enemy_y + (row - len(self.game_state.enemies) // 4) * enemy_spacing
                
                # Render enemy
                enemy.render(screen, (enemy_pos_x - enemy.sprite.get_width() // 2,
                                     enemy_pos_y - enemy.sprite.get_height() // 2))
                
                # Render enemy health bar
                self._render_health_bar(screen, enemy, enemy_pos_x, enemy_pos_y + 30)
                
                # Render enemy name and level
                name_text = self.font.render(f"{enemy.name} (Lv.{enemy.level})", True, self.colors["text"])
                name_rect = name_text.get_rect(center=(enemy_pos_x, enemy_pos_y - 30))
                screen.blit(name_text, name_rect)
        
        # Render combat log
        self._render_combat_log(screen)
        
        # Render battle controls
        if self.game_state.battle_paused:
            status_text = self.font.render("PAUSED - Press SPACE to resume", True, self.colors["text"])
        else:
            status_text = self.font.render("Press SPACE to pause, S to save", True, self.colors["text"])
        
        status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        screen.blit(status_text, status_rect)
    
    def _render_game_over(self, screen):
        """
        Render the game over screen
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        # Title
        title_text = self.title_font.render("Game Over", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Stats
        player = self.game_state.player_character
        if player:
            stats_text = self.font.render(
                f"Your {player.name} (Level {player.level}) has been defeated!",
                True, self.colors["text"]
            )
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(stats_text, stats_rect)
        
        # Instructions
        instruction_text = self.font.render("Press ENTER to return to menu", True, self.colors["text"])
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(instruction_text, instruction_rect)
    
    def _render_victory(self, screen):
        """
        Render the victory screen
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        # Title
        title_text = self.title_font.render("Victory!", True, (0, 255, 0))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        screen.blit(title_text, title_rect)
        
        # Stats
        player = self.game_state.player_character
        if player:
            stats_text = self.font.render(
                f"Your {player.name} (Level {player.level}) was victorious!",
                True, self.colors["text"]
            )
            stats_rect = stats_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(stats_text, stats_rect)
        
        # Auto-continue message or pause notification
        if self.game_state.battle_paused:
            instruction_text = self.font.render("Game PAUSED - Press SPACE to resume", True, self.colors["text"])
        else:
            # Calculate remaining time
            remaining_time = max(0, self.game_state.victory_display_duration - self.game_state.victory_display_timer)
            instruction_text = self.font.render(f"Continuing to next battle in {remaining_time:.1f}s... (SPACE to pause)", True, self.colors["text"])
        
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        screen.blit(instruction_text, instruction_rect)
    
    def _render_health_bar(self, screen, character, x, y):
        """
        Render a health bar for a character
        
        Args:
            screen (pygame.Surface): The screen to render to
            character (BaseCharacter): The character
            x (int): X position (center)
            y (int): Y position (top)
        """
        # Use the health bar component
        self.health_bar.render(screen, character, x, y, self.font)
    
    def _render_xp_bar(self, screen, character, x, y):
        """
        Render an XP bar for a character
        
        Args:
            screen (pygame.Surface): The screen to render to
            character (BaseCharacter): The character
            x (int): X position (center)
            y (int): Y position (top)
        """
        # Use the XP bar component
        self.xp_bar.render(screen, character, x, y, self.font)
    
    def _render_character_stats(self, screen, character, x, y):
        """
        Render character stats
        
        Args:
            screen (pygame.Surface): The screen to render to
            character (BaseCharacter): The character
            x (int): X position (left)
            y (int): Y position (top)
        """
        stats = [
            f"Name: {character.name}",
            f"Level: {character.level}",
            f"HP: {character.current_hp}/{character.max_hp}",
            f"Attack: {character.attack}",
            f"Defense: {character.defense}",
            f"Magic: {character.magic}",
            f"Speed: {character.speed}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font.render(stat, True, self.colors["text"])
            screen.blit(text, (x, y + i * 25))
    
    def _render_combat_log(self, screen):
        """
        Render the combat log
        
        Args:
            screen (pygame.Surface): The screen to render to
        """
        # Get log entries from battle manager if it exists
        if hasattr(self.game_state, 'battle_manager') and self.game_state.battle_manager:
            # Update our combat log with entries from battle manager
            for entry in self.game_state.battle_manager.get_recent_log(COMBAT_LOG_LINES):
                if entry not in self.combat_log.entries:
                    self.combat_log.add_entry(entry)
        
        # Render the combat log component
        log_x = SCREEN_WIDTH - COMBAT_LOG_WIDTH - UI_PADDING
        log_y = SCREEN_HEIGHT - COMBAT_LOG_HEIGHT - UI_PADDING
        self.combat_log.render(screen, self.font, log_x, log_y)