import sys
import pygame

class KeyEvents:
    """A class to manage key press events."""

    def __init__(self, ai_game):
        """Initialize key events"""
        self.ai_game = ai_game
        self.ship = ai_game.ship

    def _check_events(self):
        """Respond to keypress and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP: 
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.ai_game._fire_bullet() 
    
    def _check_keyup_events(self, event):            
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.ai_game.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.ai_game.stats.game_active:
            # Reset the game statistics.
            self.ai_game.settings.initialize_dynamic_settings()
            self.ai_game.stats.reset_stats()
            self.ai_game.stats.game_active = True
            self.ai_game.sb.prep_score()
            self.ai_game.sb.prep_level()
            self.ai_game.sb.prep_ships()

            # Get rid of any remaining aliens and bullets.
            self.ai_game.aliens.empty()
            self.ai_game.bullets.empty()

            # Create a new fleet and center the ship.
            self.ai_game._create_fleet()
            self.ai_game.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)
