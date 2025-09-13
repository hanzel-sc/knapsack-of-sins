# -*- coding: utf-8 -*-
"""
ASYLUM OF SINS - A Dark Knapsack/Maze Game (Enhanced)
Compatible with Python 2.7
Dependencies: pygame
"""

import pygame
import random
import heapq
import math
import time
from itertools import combinations

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
MAZE_WIDTH = 51
MAZE_HEIGHT = 35
CELL_SIZE = 16
FPS = 60
VISION_RADIUS = 3  # How far player can see

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 20)
DARK_RED = (139, 0, 0)
BLOOD_RED = (102, 0, 0)
GREEN = (50, 200, 50)
DARK_GREEN = (0, 100, 0)
BLUE = (30, 144, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
YELLOW = (255, 215, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
CRIMSON = (220, 20, 60)
SHADOW = (25, 25, 25)
FLAME = (255, 69, 0)
FOG_COLOR = (30, 30, 30)

# Game States
INTRO = 1
CONFESSION = 2
SIN_SELECTION = 3
VIRTUE_SELECTION = 4
KNAPSACK_SUMMARY = 5
MAZE_PREP = 6
MAZE = 7
JUDGMENT = 8

class Item(object):
    def __init__(self, name, weight, value, description, color):
        self.name = name
        self.weight = weight
        self.value = value
        self.description = description
        self.color = color
        self.selected = False

class ParticleSystem(object):
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, color, velocity, life):
        particle = {
            'x': x, 'y': y, 'color': color,
            'vx': velocity[0], 'vy': velocity[1],
            'life': life, 'max_life': life
        }
        self.particles.append(particle)
    
    def update(self):
        particles_to_remove = []
        for i, particle in enumerate(self.particles):
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1
            particle['vy'] += 0.1  # Gravity
            
            if particle['life'] <= 0:
                particles_to_remove.append(i)
        
        for i in reversed(particles_to_remove):
            del self.particles[i]
    
    def draw(self, screen):
        for particle in self.particles:
            if particle['life'] > 0:
                size = max(1, int(3 * (float(particle['life']) / particle['max_life'])))
                pygame.draw.circle(screen, particle['color'], 
                                 (int(particle['x']), int(particle['y'])), size)

class MazeGenerator(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[1 for _ in range(width)] for _ in range(height)]
        
    def generate_sinful_maze(self, chosen_sins, chosen_virtues):
        """Generate maze based on specific moral choices"""
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Create basic maze structure
        stack = [(1, 1)]
        self.maze[1][1] = 0
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        
        while stack:
            current_x, current_y = stack[-1]
            neighbors = []
            
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy
                if (0 < nx < self.width - 1 and 0 < ny < self.height - 1 and 
                    self.maze[ny][nx] == 1):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                wall_x = current_x + dx // 2
                wall_y = current_y + dy // 2
                self.maze[wall_y][wall_x] = 0
                self.maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Add sin-specific maze features
        self._apply_sin_effects(chosen_sins)
        
        # Add virtue-specific maze features
        self._apply_virtue_effects(chosen_virtues)
        
        # Ensure accessibility
        self.maze[1][1] = 0  # Start
        self.maze[self.height-2][self.width-2] = 0  # End
        
        return self.maze
    
    def _apply_sin_effects(self, chosen_sins):
        """Apply specific effects based on chosen sins"""
        sin_effects = {
            "Wrath": self._add_aggressive_paths,
            "Envy": self._add_deceptive_loops,
            "Pride": self._add_complex_detours,
            "Greed": self._add_treasure_traps,
            "Lust": self._add_tempting_paths,
            "Gluttony": self._add_wide_corridors,
            "Sloth": self._add_blocked_shortcuts,
            "Despair": self._add_dead_ends,
            "Hatred": self._add_hostile_maze_sections
        }
        
        for sin in chosen_sins:
            if sin.name in sin_effects:
                sin_effects[sin.name](sin.weight)
    
    def _apply_virtue_effects(self, chosen_virtues):
        """Apply specific effects based on chosen virtues"""
        virtue_effects = {
            "Compassion": self._add_helpful_shortcuts,
            "Humility": self._simplify_paths,
            "Forgiveness": self._remove_some_barriers,
            "Patience": self._add_steady_progress_paths,
            "Courage": self._add_direct_routes,
            "Wisdom": self._add_efficient_connections,
            "Hope": self._add_guiding_lights
        }
        
        for virtue in chosen_virtues:
            if virtue.name in virtue_effects:
                virtue_effects[virtue.name](virtue.weight)
    
    def _add_aggressive_paths(self, intensity):
        """Wrath: Add sharp turns and aggressive angles"""
        for _ in range(intensity):
            x, y = random.randrange(1, self.width-1, 2), random.randrange(1, self.height-1, 2)
            if self.maze[y][x] == 0:
                # Create sharp branching paths
                directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
                for dx, dy in directions:
                    if random.random() < 0.4:
                        nx, ny = x + dx, y + dy
                        if 0 < nx < self.width-1 and 0 < ny < self.height-1:
                            self.maze[y + dy//2][x + dx//2] = 0
                            self.maze[ny][nx] = 0
    
    def _add_deceptive_loops(self, intensity):
        """Envy: Add loops that seem to lead somewhere but circle back"""
        for _ in range(intensity // 2):
            start_x = random.randrange(3, self.width-3, 2)
            start_y = random.randrange(3, self.height-3, 2)
            if self.maze[start_y][start_x] == 0:
                # Create small loops
                loop_points = [
                    (start_x, start_y), (start_x+2, start_y),
                    (start_x+2, start_y+2), (start_x, start_y+2)
                ]
                for i in range(len(loop_points)):
                    curr = loop_points[i]
                    next_point = loop_points[(i+1) % len(loop_points)]
                    self._connect_points(curr, next_point)
    
    def _add_complex_detours(self, intensity):
        """Pride: Add unnecessarily complex paths"""
        for _ in range(intensity):
            x, y = random.randrange(1, self.width-1, 2), random.randrange(1, self.height-1, 2)
            if self.maze[y][x] == 0:
                # Create winding detours
                path_length = random.randint(3, 6)
                curr_x, curr_y = x, y
                for _ in range(path_length):
                    directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
                    random.shuffle(directions)
                    for dx, dy in directions:
                        nx, ny = curr_x + dx, curr_y + dy
                        if 0 < nx < self.width-1 and 0 < ny < self.height-1:
                            self.maze[curr_y + dy//2][curr_x + dx//2] = 0
                            self.maze[ny][nx] = 0
                            curr_x, curr_y = nx, ny
                            break
    
    def _add_helpful_shortcuts(self, intensity):
        """Compassion: Add some helpful shortcuts"""
        for _ in range(intensity):
            x1 = random.randrange(1, self.width//2, 2)
            y1 = random.randrange(1, self.height-1, 2)
            x2 = random.randrange(self.width//2, self.width-1, 2)
            y2 = random.randrange(1, self.height-1, 2)
            
            if self.maze[y1][x1] == 0 and self.maze[y2][x2] == 0:
                self._connect_points((x1, y1), (x2, y2))
    
    def _connect_points(self, p1, p2):
        """Connect two points with a path"""
        x1, y1 = p1
        x2, y2 = p2
        
        # Simple L-shaped connection
        if random.random() < 0.5:
            # Go horizontal first, then vertical
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 < x < self.width-1:
                    self.maze[y1][x] = 0
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 < y < self.height-1:
                    self.maze[y][x2] = 0
        else:
            # Go vertical first, then horizontal
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if 0 < y < self.height-1:
                    self.maze[y][x1] = 0
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if 0 < x < self.width-1:
                    self.maze[y2][x] = 0
    
    # Placeholder implementations for other sin/virtue effects
    def _add_treasure_traps(self, intensity): pass
    def _add_tempting_paths(self, intensity): pass
    def _add_wide_corridors(self, intensity): pass
    def _add_blocked_shortcuts(self, intensity): pass
    def _add_dead_ends(self, intensity): pass
    def _add_hostile_maze_sections(self, intensity): pass
    def _simplify_paths(self, intensity): pass
    def _remove_some_barriers(self, intensity): pass
    def _add_steady_progress_paths(self, intensity): pass
    def _add_direct_routes(self, intensity): pass
    def _add_efficient_connections(self, intensity): pass
    def _add_guiding_lights(self, intensity): pass

class AsylumOfSins(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Asylum of Sins - Where Souls Meet Judgment")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Game state
        self.state = INTRO
        self.running = True
        self.text_timer = 0
        self.current_text_index = 0
        
        # Selection state
        self.selected_sin_index = 0
        self.selected_virtue_index = 0
        
        # Particle system
        self.particles = ParticleSystem()
        
        # Enhanced sins and virtues
        self.sins = [
            Item("Wrath", 8, 15, "Burning rage that consumes reason", FLAME),
            Item("Envy", 6, 12, "Bitter jealousy that poisons the heart", DARK_GREEN),
            Item("Pride", 7, 14, "Arrogance that blinds the soul", PURPLE),
            Item("Greed", 5, 10, "Insatiable hunger for more", GOLD),
            Item("Lust", 4, 8, "Desires that corrupt the spirit", CRIMSON),
            Item("Gluttony", 9, 16, "Excess that devours everything", ORANGE),
            Item("Sloth", 3, 6, "Laziness that rots potential", GRAY),
            Item("Despair", 6, 11, "Hopelessness that drowns the light", DARK_GRAY),
            Item("Hatred", 10, 18, "Pure malice that destroys all", BLOOD_RED)
        ]
        
        self.virtues = [
            Item("Compassion", 4, 12, "Empathy that heals wounds", GREEN),
            Item("Humility", 3, 9, "Modesty that opens hearts", WHITE),
            Item("Forgiveness", 5, 14, "Grace that breaks chains", SILVER),
            Item("Patience", 2, 7, "Endurance through trials", BLUE),
            Item("Courage", 6, 15, "Bravery in darkness", GOLD),
            Item("Wisdom", 7, 16, "Knowledge that guides truth", PURPLE),
            Item("Hope", 3, 10, "Light in the deepest darkness", YELLOW)
        ]
        
        # Game configuration
        self.soul_capacity = 25
        
        # Player choices and state
        self.chosen_sins = []
        self.chosen_virtues = []
        self.moral_balance = 0
        self.sin_weight = 0
        self.virtue_weight = 0
        
        # Maze variables
        self.maze = None
        self.maze_generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.player_pos = (1, 1)
        self.goal_pos = (MAZE_WIDTH-2, MAZE_HEIGHT-2)
        self.player_path = []
        self.shortest_path = []
        self.maze_offset_x = 0
        self.maze_offset_y = 0
        self.visited_cells = set()  # For fog of war
        self.maze_completed = False
        
        # Animation and effects
        self.pulse_timer = 0
        
        # Final judgment
        self.final_destination = ""
        self.judgment_text = []
        self.path_efficiency = 1.0
        
        # Story text
        self.intro_texts = [
            "You stand before the Asylum of Sins...",
            "A place where souls are weighed and judged...",
            "Your life's choices have led you here...",
            "Now you must carry your burden through the maze of judgment...",
            "Choose wisely... eternity awaits your decision."
        ]

    def calculate_current_weight(self):
        """Calculate current total weight of selected items"""
        sin_weight = sum(sin.weight for sin in self.sins if sin.selected)
        virtue_weight = sum(virtue.weight for virtue in self.virtues if virtue.selected)
        return sin_weight + virtue_weight

    def finalize_selections(self):
        """Finalize the selected sins and virtues"""
        self.chosen_sins = [sin for sin in self.sins if sin.selected]
        self.chosen_virtues = [virtue for virtue in self.virtues if virtue.selected]
        
        sin_value = sum(sin.value for sin in self.chosen_sins)
        virtue_value = sum(virtue.value for virtue in self.chosen_virtues)
        
        self.sin_weight = sum(sin.weight for sin in self.chosen_sins)
        self.virtue_weight = sum(virtue.weight for virtue in self.chosen_virtues)
        self.moral_balance = virtue_value - sin_value

    def generate_moral_maze(self):
        """Generate maze based on moral choices"""
        self.maze = self.maze_generator.generate_sinful_maze(self.chosen_sins, self.chosen_virtues)
        
        # Calculate maze display offset
        maze_pixel_width = MAZE_WIDTH * CELL_SIZE
        maze_pixel_height = MAZE_HEIGHT * CELL_SIZE
        self.maze_offset_x = (WINDOW_WIDTH - maze_pixel_width) // 2
        self.maze_offset_y = (WINDOW_HEIGHT - maze_pixel_height) // 2
        
        # Initialize fog of war
        self.visited_cells = set()
        self.reveal_around_player()

    def reveal_around_player(self):
        """Reveal cells around player position"""
        px, py = self.player_pos
        for dy in range(-VISION_RADIUS, VISION_RADIUS + 1):
            for dx in range(-VISION_RADIUS, VISION_RADIUS + 1):
                nx, ny = px + dx, py + dy
                if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT:
                    distance = math.sqrt(dx*dx + dy*dy)
                    if distance <= VISION_RADIUS:
                        self.visited_cells.add((nx, ny))

    def dijkstra_pathfinding(self, start, end):
        """Enhanced Dijkstra pathfinding"""
        rows, cols = len(self.maze), len(self.maze[0])
        distances = [[float('inf')] * cols for _ in range(rows)]
        visited = [[False] * cols for _ in range(rows)]
        parent = {start: None}
        
        distances[start[1]][start[0]] = 0
        heap = [(0, start)]
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while heap:
            current_dist, pos = heapq.heappop(heap)
            x, y = pos
            
            if visited[y][x]:
                continue
                
            visited[y][x] = True
            
            if pos == end:
                break
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < cols and 0 <= ny < rows and self.maze[ny][nx] == 0):
                    new_dist = current_dist + 1
                    
                    if new_dist < distances[ny][nx]:
                        distances[ny][nx] = new_dist
                        parent[(nx, ny)] = (x, y)
                        heapq.heappush(heap, (new_dist, (nx, ny)))
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        
        return path if path and path[0] == start else []

    def judge_soul(self, path_efficiency):
        """Enhanced judgment system"""
        moral_score = self.moral_balance
        efficiency_penalty = (path_efficiency - 1.0) * 10
        final_score = moral_score - efficiency_penalty
        
        if final_score >= 10 and path_efficiency < 1.5:
            self.final_destination = "PURGATORY"
            self.judgment_text = [
                "Your virtues outweigh your sins...",
                "Though imperfect, you showed wisdom in the maze...",
                "Purgatory awaits - a chance for redemption...",
                "Time will cleanse what remains of your burden."
            ]
        elif final_score >= 0 and path_efficiency < 2.0:
            self.final_destination = "THE GRAY REALM"
            self.judgment_text = [
                "You walk the line between salvation and damnation...",
                "Neither fully corrupted nor truly pure...",
                "The Gray Realm claims you - eternal neutrality...",
                "Forever suspended between light and darkness."
            ]
        elif final_score >= -10:
            self.final_destination = "THE LOWER CIRCLES"
            self.judgment_text = [
                "Your sins have weight, but virtue remains...",
                "The lower circles of suffering await...",
                "Pain, but not eternal torment...",
                "Hope flickers dimly in the distance."
            ]
        else:
            self.final_destination = "THE ABYSS"
            self.judgment_text = [
                "Darkness consumes your soul...",
                "Your choices have led to the deepest pit...",
                "The Abyss opens its maw to swallow you...",
                "Eternal suffering awaits the unrepentant."
            ]

    def handle_events(self):
        """Enhanced event handling"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == INTRO:
                    if event.key == pygame.K_SPACE:
                        self.state = CONFESSION
                        self.text_timer = 0
                        self.current_text_index = 0
                
                elif self.state == CONFESSION:
                    if event.key == pygame.K_SPACE:
                        self.state = SIN_SELECTION
                        self.selected_sin_index = 0
                
                elif self.state == SIN_SELECTION:
                    self._handle_sin_selection(event)
                
                elif self.state == VIRTUE_SELECTION:
                    self._handle_virtue_selection(event)
                
                elif self.state == KNAPSACK_SUMMARY:
                    if event.key == pygame.K_RETURN:
                        self.finalize_selections()
                        self.state = MAZE_PREP
                        self.generate_moral_maze()
                        self.player_pos = (1, 1)
                        self.player_path = [self.player_pos]
                        self.shortest_path = self.dijkstra_pathfinding(self.player_pos, self.goal_pos)
                
                elif self.state == MAZE_PREP:
                    if event.key == pygame.K_SPACE:
                        self.state = MAZE
                
                elif self.state == MAZE:
                    self._handle_maze_movement(event)
                
                elif self.state == JUDGMENT:
                    if event.key == pygame.K_r:
                        self._reset_game()

    def _handle_sin_selection(self, event):
        """Handle sin selection interface"""
        if event.key == pygame.K_UP:
            self.selected_sin_index = (self.selected_sin_index - 1) % len(self.sins)
        elif event.key == pygame.K_DOWN:
            self.selected_sin_index = (self.selected_sin_index + 1) % len(self.sins)
        elif event.key == pygame.K_SPACE:
            sin = self.sins[self.selected_sin_index]
            if sin.selected:
                sin.selected = False
            else:
                # Check if adding this sin would exceed capacity
                if self.calculate_current_weight() + sin.weight <= self.soul_capacity:
                    sin.selected = True
        elif event.key == pygame.K_RETURN:
            self.state = VIRTUE_SELECTION
            self.selected_virtue_index = 0

    def _handle_virtue_selection(self, event):
        """Handle virtue selection interface"""
        if event.key == pygame.K_UP:
            self.selected_virtue_index = (self.selected_virtue_index - 1) % len(self.virtues)
        elif event.key == pygame.K_DOWN:
            self.selected_virtue_index = (self.selected_virtue_index + 1) % len(self.virtues)
        elif event.key == pygame.K_SPACE:
            virtue = self.virtues[self.selected_virtue_index]
            if virtue.selected:
                virtue.selected = False
            else:
                # Check if adding this virtue would exceed capacity
                if self.calculate_current_weight() + virtue.weight <= self.soul_capacity:
                    virtue.selected = True
        elif event.key == pygame.K_RETURN:
            self.state = KNAPSACK_SUMMARY

    def _handle_maze_movement(self, event):
        """Handle player movement in maze"""
        if self.maze_completed:
            return
            
        x, y = self.player_pos
        new_x, new_y = x, y
        
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            new_x = x - 1
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            new_x = x + 1
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            new_y = y - 1
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            new_y = y + 1
        
        # Validate movement
        if (0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT and 
            self.maze[new_y][new_x] == 0):
            
            self.player_pos = (new_x, new_y)
            self.player_path.append(self.player_pos)
            self.reveal_around_player()
            
            # Add movement particles
            screen_x = self.maze_offset_x + new_x * CELL_SIZE + CELL_SIZE // 2
            screen_y = self.maze_offset_y + new_y * CELL_SIZE + CELL_SIZE // 2
            for _ in range(3):
                self.particles.add_particle(
                    screen_x + random.randint(-5, 5),
                    screen_y + random.randint(-5, 5),
                    RED, (random.uniform(-2, 2), random.uniform(-2, 2)), 30
                )
            
            # Check if goal reached
            if self.player_pos == self.goal_pos:
                self.maze_completed = True
                user_steps = len(self.player_path) - 1
                optimal_steps = len(self.shortest_path) - 1 if self.shortest_path else user_steps
                self.path_efficiency = float(user_steps) / optimal_steps if optimal_steps > 0 else 1.0
                
                self.judge_soul(self.path_efficiency)
                self.state = JUDGMENT
                self.text_timer = 0
                self.current_text_index = 0

    def _reset_game(self):
        """Reset game to initial state"""
        self.state = INTRO
        self.chosen_sins = []
        self.chosen_virtues = []
        for sin in self.sins:
            sin.selected = False
        for virtue in self.virtues:
            virtue.selected = False
        self.player_path = []
        self.text_timer = 0
        self.current_text_index = 0
        self.particles = ParticleSystem()
        self.maze_completed = False
        self.visited_cells = set()

    def update_particles(self):
        """Update particle effects"""
        self.particles.update()
        
        # Add atmospheric particles
        if random.random() < 0.1:
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            self.particles.add_particle(
                x, y, DARK_GRAY,
                (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
                random.randint(120, 240)
            )

    def draw_intro(self):
        """Draw atmospheric intro screen"""
        self.screen.fill(BLACK)
        
        # Title with glow effect
        title = self.title_font.render("ASYLUM OF SINS", True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        subtitle = self.large_font.render("Where Souls Meet Their Judgment", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 280))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Story text with typewriter effect
        self.text_timer += self.clock.get_time()
        if self.text_timer > 2000 and self.current_text_index < len(self.intro_texts):
            self.current_text_index += 1
            self.text_timer = 0
        
        y_offset = 350
        for i, text in enumerate(self.intro_texts[:self.current_text_index]):
            alpha = 255 if i < self.current_text_index - 1 else min(255, (self.text_timer // 10))
            color = (min(255, alpha), min(255, alpha), min(255, alpha))
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, y_offset + i * 40))
            self.screen.blit(text_surface, text_rect)
        
        if self.current_text_index >= len(self.intro_texts):
            prompt = self.small_font.render("Press SPACE to begin your confession", True, GRAY)
            prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH//2, 650))
            self.screen.blit(prompt, prompt_rect)

    def draw_confession(self):
        """Draw confession screen"""
        self.screen.fill(BLACK)
        
        title = self.large_font.render("CONFESSION OF THE SOUL", True, CRIMSON)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        confession_texts = [
            "Speak your sins and virtues...",
            "The weight of your choices will determine your path...",
            "In this asylum, honesty is your only salvation..."
        ]
        
        y_offset = 300
        for text in confession_texts:
            text_surface = self.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 50
        
        prompt = self.small_font.render("Press SPACE to choose your sins", True, GRAY)
        prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH//2, 500))
        self.screen.blit(prompt, prompt_rect)

    def draw_sin_selection(self):
        """Draw sin selection screen"""
        self.screen.fill(BLACK)
        
        title = self.large_font.render("CHOOSE YOUR SINS", True, DARK_RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Capacity info
        current_weight = self.calculate_current_weight()
        capacity_text = "Soul Capacity: %d/%d" % (current_weight, self.soul_capacity)
        capacity_color = RED if current_weight > self.soul_capacity else WHITE
        capacity_surface = self.font.render(capacity_text, True, capacity_color)
        self.screen.blit(capacity_surface, (50, 100))
        
        # Instructions
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "SPACE to select/deselect",
            "ENTER to continue to virtues"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, GRAY)
            self.screen.blit(inst_surface, (50, 130 + i * 25))
        
        # Draw sin list
        start_y = 220
        for i, sin in enumerate(self.sins):
            y_pos = start_y + i * 60
            
            # Highlight selected item
            if i == self.selected_sin_index:
                highlight_rect = pygame.Rect(40, y_pos - 5, WINDOW_WIDTH - 80, 50)
                pygame.draw.rect(self.screen, DARK_GRAY, highlight_rect)
                pygame.draw.rect(self.screen, WHITE, highlight_rect, 2)
            
            # Selection indicator
            indicator = "✓ " if sin.selected else "○ "
            indicator_color = sin.color if sin.selected else GRAY
            indicator_surface = self.font.render(indicator, True, indicator_color)
            self.screen.blit(indicator_surface, (50, y_pos))
            
            # Sin name and stats
            sin_text = "%s (Weight: %d, Burden: %d)" % (sin.name, sin.weight, sin.value)
            sin_color = sin.color if sin.selected else WHITE
            sin_surface = self.font.render(sin_text, True, sin_color)
            self.screen.blit(sin_surface, (100, y_pos))
            
            # Description
            desc_surface = self.small_font.render(sin.description, True, GRAY)
            self.screen.blit(desc_surface, (120, y_pos + 25))

    def draw_virtue_selection(self):
        """Draw virtue selection screen"""
        self.screen.fill(BLACK)
        
        title = self.large_font.render("CHOOSE YOUR VIRTUES", True, DARK_GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Capacity info
        current_weight = self.calculate_current_weight()
        capacity_text = "Soul Capacity: %d/%d" % (current_weight, self.soul_capacity)
        capacity_color = RED if current_weight > self.soul_capacity else WHITE
        capacity_surface = self.font.render(capacity_text, True, capacity_color)
        self.screen.blit(capacity_surface, (50, 100))
        
        # Instructions
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "SPACE to select/deselect",
            "ENTER to continue to summary"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, GRAY)
            self.screen.blit(inst_surface, (50, 130 + i * 25))
        
        # Draw virtue list
        start_y = 220
        for i, virtue in enumerate(self.virtues):
            y_pos = start_y + i * 60
            
            # Highlight selected item
            if i == self.selected_virtue_index:
                highlight_rect = pygame.Rect(40, y_pos - 5, WINDOW_WIDTH - 80, 50)
                pygame.draw.rect(self.screen, DARK_GRAY, highlight_rect)
                pygame.draw.rect(self.screen, WHITE, highlight_rect, 2)
            
            # Selection indicator
            indicator = "✓ " if virtue.selected else "○ "
            indicator_color = virtue.color if virtue.selected else GRAY
            indicator_surface = self.font.render(indicator, True, indicator_color)
            self.screen.blit(indicator_surface, (50, y_pos))
            
            # Virtue name and stats
            virtue_text = "%s (Weight: %d, Grace: %d)" % (virtue.name, virtue.weight, virtue.value)
            virtue_color = virtue.color if virtue.selected else WHITE
            virtue_surface = self.font.render(virtue_text, True, virtue_color)
            self.screen.blit(virtue_surface, (100, y_pos))
            
            # Description
            desc_surface = self.small_font.render(virtue.description, True, GRAY)
            self.screen.blit(desc_surface, (120, y_pos + 25))

    def draw_knapsack_summary(self):
        """Draw knapsack summary screen"""
        self.screen.fill(BLACK)
        
        title = self.large_font.render("THE WEIGHT OF YOUR SOUL", True, RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Summary stats
        selected_sins = [sin for sin in self.sins if sin.selected]
        selected_virtues = [virtue for virtue in self.virtues if virtue.selected]
        
        sin_weight = sum(sin.weight for sin in selected_sins)
        virtue_weight = sum(virtue.weight for virtue in selected_virtues)
        sin_value = sum(sin.value for sin in selected_sins)
        virtue_value = sum(virtue.value for virtue in selected_virtues)
        
        summary = [
            "Selected Sins: %d (Weight: %d, Burden: %d)" % (len(selected_sins), sin_weight, sin_value),
            "Selected Virtues: %d (Weight: %d, Grace: %d)" % (len(selected_virtues), virtue_weight, virtue_value),
            "Total Weight: %d/%d" % (sin_weight + virtue_weight, self.soul_capacity),
            "Moral Balance: %d" % (virtue_value - sin_value)
        ]
        
        for i, text in enumerate(summary):
            if "Balance" in text:
                color = GREEN if virtue_value > sin_value else RED if virtue_value < sin_value else WHITE
            elif "Sins" in text:
                color = DARK_RED
            elif "Virtues" in text:
                color = DARK_GREEN
            else:
                color = WHITE
                
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (50, 120 + i * 40))
        
        # List chosen sins
        if selected_sins:
            sins_title = self.font.render("CHOSEN SINS:", True, DARK_RED)
            self.screen.blit(sins_title, (50, 300))
            
            for i, sin in enumerate(selected_sins):
                sin_text = "• %s" % sin.name
                text_surface = self.small_font.render(sin_text, True, sin.color)
                self.screen.blit(text_surface, (70, 330 + i * 25))
        
        # List chosen virtues
        virtue_y = 300 + len(selected_sins) * 25 + 60 if selected_sins else 300
        if selected_virtues:
            virtues_title = self.font.render("CHOSEN VIRTUES:", True, DARK_GREEN)
            self.screen.blit(virtues_title, (50, virtue_y))
            
            for i, virtue in enumerate(selected_virtues):
                virtue_text = "• %s" % virtue.name
                text_surface = self.small_font.render(virtue_text, True, virtue.color)
                self.screen.blit(text_surface, (70, virtue_y + 30 + i * 25))
        
        # Instruction
        instruction = self.font.render("Press ENTER to enter the Maze of Judgment", True, YELLOW)
        instruction_rect = instruction.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
        self.screen.blit(instruction, instruction_rect)

    def draw_maze_prep(self):
        """Draw maze preparation screen"""
        self.screen.fill(BLACK)
        
        title = self.large_font.render("THE MAZE OF JUDGMENT AWAITS", True, CRIMSON)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(title, title_rect)
        
        warnings = [
            "Your choices have shaped the maze before you...",
            "The path ahead is shrouded in darkness...",
            "Only by moving forward will you reveal your way...",
            "",
            "Navigate wisely - your path determines your fate..."
        ]
        
        y_offset = 300
        for warning in warnings:
            if warning:
                text_surface = self.font.render(warning, True, WHITE)
                text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, y_offset))
                self.screen.blit(text_surface, text_rect)
            y_offset += 40
        
        # Controls
        controls = [
            "CONTROLS:",
            "WASD or Arrow Keys - Move",
            "Red square - Your soul",
            "Green square - Salvation gate",
            "Dark areas - Unexplored regions"
        ]
        
        y_offset = 500
        for i, control in enumerate(controls):
            color = YELLOW if i == 0 else WHITE
            text_surface = self.small_font.render(control, True, color)
            self.screen.blit(text_surface, (50, y_offset + i * 25))
        
        prompt = self.font.render("Press SPACE to begin your trial", True, GOLD)
        prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
        self.screen.blit(prompt, prompt_rect)

    def draw_maze(self):
        """Draw the maze with fog of war"""
        self.screen.fill(BLACK)
        
        # Draw maze with fog of war
        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                screen_x = self.maze_offset_x + x * CELL_SIZE
                screen_y = self.maze_offset_y + y * CELL_SIZE
                
                if (x, y) in self.visited_cells:
                    # Visible cells
                    if self.maze[y][x] == 1:  # Wall
                        pygame.draw.rect(self.screen, GRAY, 
                                       (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                        pygame.draw.rect(self.screen, DARK_GRAY, 
                                       (screen_x + 1, screen_y + 1, CELL_SIZE - 2, CELL_SIZE - 2))
                    else:  # Path
                        pygame.draw.rect(self.screen, SHADOW, 
                                       (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
                else:
                    # Fog of war - unexplored areas
                    pygame.draw.rect(self.screen, FOG_COLOR, 
                                   (screen_x, screen_y, CELL_SIZE, CELL_SIZE))
        
        # Draw player path (only visible parts)
        for i, pos in enumerate(self.player_path[:-1]):
            if pos in self.visited_cells:
                screen_x = self.maze_offset_x + pos[0] * CELL_SIZE
                screen_y = self.maze_offset_y + pos[1] * CELL_SIZE
                
                fade = max(50, 255 - (len(self.player_path) - i) * 3)
                color = (255, 215, 0) if fade > 50 else (128, 107, 0)
                
                pygame.draw.rect(self.screen, color, 
                               (screen_x + 3, screen_y + 3, CELL_SIZE - 6, CELL_SIZE - 6))
        
        # Draw goal (only if visible)
        if self.goal_pos in self.visited_cells:
            goal_screen_x = self.maze_offset_x + self.goal_pos[0] * CELL_SIZE
            goal_screen_y = self.maze_offset_y + self.goal_pos[1] * CELL_SIZE
            pygame.draw.rect(self.screen, GREEN, 
                            (goal_screen_x, goal_screen_y, CELL_SIZE, CELL_SIZE))
        
        # Draw optimal path ONLY after maze is completed
        if self.maze_completed and self.shortest_path:
            for pos in self.shortest_path:
                if pos in self.visited_cells:
                    screen_x = self.maze_offset_x + pos[0] * CELL_SIZE
                    screen_y = self.maze_offset_y + pos[1] * CELL_SIZE
                    pygame.draw.rect(self.screen, BLUE, 
                                   (screen_x + 2, screen_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
        
        # Draw player
        player_screen_x = self.maze_offset_x + self.player_pos[0] * CELL_SIZE
        player_screen_y = self.maze_offset_y + self.player_pos[1] * CELL_SIZE
        
        # Player aura based on moral balance
        aura_color = GREEN if self.moral_balance > 0 else RED
        pygame.draw.circle(self.screen, aura_color, 
                          (player_screen_x + CELL_SIZE//2, player_screen_y + CELL_SIZE//2), 
                          CELL_SIZE + 4, 2)
        
        pygame.draw.rect(self.screen, RED, 
                        (player_screen_x, player_screen_y, CELL_SIZE, CELL_SIZE))
        
        self.draw_maze_ui()

    def draw_maze_ui(self):
        """Draw maze UI elements"""
        # Top status bar
        status_bg = pygame.Rect(0, 0, WINDOW_WIDTH, 80)
        pygame.draw.rect(self.screen, (20, 20, 20), status_bg)
        pygame.draw.rect(self.screen, GRAY, status_bg, 2)
        
        # Status information
        current_steps = len(self.player_path) - 1
        
        status_info = [
            "Moral Balance: %d" % self.moral_balance,
            "Steps Taken: %d" % current_steps,
            "Sins: %d" % len(self.chosen_sins),
            "Virtues: %d" % len(self.chosen_virtues)
        ]
        
        x_positions = [50, 250, 450, 650]
        for i, info in enumerate(status_info):
            if "Balance" in info:
                color = GREEN if self.moral_balance > 0 else RED if self.moral_balance < 0 else WHITE
            else:
                color = WHITE
            text_surface = self.small_font.render(info, True, color)
            self.screen.blit(text_surface, (x_positions[i], 15))
        
        # Current burden display
        burden_y = 40
        if self.chosen_sins:
            sin_names = [sin.name for sin in self.chosen_sins[:3]]
            sin_text = "Carrying: %s" % ', '.join(sin_names)
            if len(self.chosen_sins) > 3:
                sin_text += " +%d more" % (len(self.chosen_sins) - 3)
            sin_surface = self.small_font.render(sin_text, True, DARK_RED)
            self.screen.blit(sin_surface, (50, burden_y))
        
        if self.chosen_virtues:
            virtue_names = [virtue.name for virtue in self.chosen_virtues[:3]]
            virtue_text = "Blessed with: %s" % ', '.join(virtue_names)
            if len(self.chosen_virtues) > 3:
                virtue_text += " +%d more" % (len(self.chosen_virtues) - 3)
            virtue_surface = self.small_font.render(virtue_text, True, DARK_GREEN)
            self.screen.blit(virtue_surface, (400, burden_y))
        
        # Show completion message
        if self.maze_completed:
            completion_bg = pygame.Rect(0, WINDOW_HEIGHT - 80, WINDOW_WIDTH, 80)
            pygame.draw.rect(self.screen, (40, 40, 40), completion_bg)
            pygame.draw.rect(self.screen, GOLD, completion_bg, 2)
            
            completion_text = "MAZE COMPLETED! Optimal path revealed in blue."
            comp_surface = self.font.render(completion_text, True, GOLD)
            comp_rect = comp_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 40))
            self.screen.blit(comp_surface, comp_rect)
        else:
            # Bottom instruction panel
            instruction_bg = pygame.Rect(0, WINDOW_HEIGHT - 40, WINDOW_WIDTH, 40)
            pygame.draw.rect(self.screen, (20, 20, 20), instruction_bg)
            pygame.draw.rect(self.screen, GRAY, instruction_bg, 1)
            
            instruction = "Navigate through the darkness to reach salvation"
            inst_surface = self.small_font.render(instruction, True, WHITE)
            inst_rect = inst_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 20))
            self.screen.blit(inst_surface, inst_rect)

    def draw_judgment(self):
        """Draw judgment screen with dramatic effects"""
        self.screen.fill(BLACK)
        
        # Title
        title = self.title_font.render("JUDGMENT", True, GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Final destination
        dest_color = RED if "ABYSS" in self.final_destination else YELLOW if "PURGATORY" in self.final_destination else GRAY
        destination = self.large_font.render(self.final_destination, True, dest_color)
        dest_rect = destination.get_rect(center=(WINDOW_WIDTH//2, 200))
        self.screen.blit(destination, dest_rect)
        
        # Judgment text with typewriter effect
        self.text_timer += self.clock.get_time()
        visible_lines = min(len(self.judgment_text), (self.text_timer // 1500) + 1)
        
        y_offset = 300
        for i, line in enumerate(self.judgment_text[:visible_lines]):
            alpha = 255 if i < visible_lines - 1 else min(255, (self.text_timer % 1500) // 6)
            color = (alpha, alpha, alpha)
            text_surface = self.font.render(line, True, color)
            text_rect = text_surface.get_rect(center=(WINDOW_WIDTH//2, y_offset + i * 40))
            self.screen.blit(text_surface, text_rect)
        
        # Final statistics
        if visible_lines >= len(self.judgment_text):
            optimal_steps = len(self.shortest_path) - 1 if self.shortest_path else 0
            user_steps = len(self.player_path) - 1
            
            stats = [
                "Final Moral Balance: %d" % self.moral_balance,
                "Path Efficiency: %.2f" % self.path_efficiency,
                "Steps Taken: %d" % user_steps,
                "Optimal Path: %d" % optimal_steps
            ]
            
            stats_y = y_offset + len(self.judgment_text) * 40 + 50
            for i, stat in enumerate(stats):
                color = GREEN if "Balance" in stat and self.moral_balance > 0 else RED if "Balance" in stat and self.moral_balance < 0 else WHITE
                stat_surface = self.small_font.render(stat, True, color)
                stat_rect = stat_surface.get_rect(center=(WINDOW_WIDTH//2, stats_y + i * 30))
                self.screen.blit(stat_surface, stat_rect)
            
            # Restart prompt
            restart = self.font.render("Press R to face judgment again", True, GRAY)
            restart_rect = restart.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 50))
            self.screen.blit(restart, restart_rect)

    def run(self):
        """Enhanced main game loop"""
        while self.running:
            dt = self.clock.tick(FPS)
            self.pulse_timer += dt
            
            self.handle_events()
            self.update_particles()
            
            # Draw current state
            if self.state == INTRO:
                self.draw_intro()
            elif self.state == CONFESSION:
                self.draw_confession()
            elif self.state == SIN_SELECTION:
                self.draw_sin_selection()
            elif self.state == VIRTUE_SELECTION:
                self.draw_virtue_selection()
            elif self.state == KNAPSACK_SUMMARY:
                self.draw_knapsack_summary()
            elif self.state == MAZE_PREP:
                self.draw_maze_prep()
            elif self.state == MAZE:
                self.draw_maze()
            elif self.state == JUDGMENT:
                self.draw_judgment()
            
            # Draw particle effects
            self.particles.draw(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    print("=" * 60)
    print("ASYLUM OF SINS - Where Souls Meet Their Judgment")
    print("=" * 60)
    print("A dark tale of moral choices and eternal consequences...")
    print("Your decisions shape not only your burden, but your very fate.")
    print("Navigate wisely through the maze of judgment.")
    print("=" * 60)
    print()
    
    try:
        game = AsylumOfSins()
        game.run()
    except Exception as e:
        print("Error starting game: %s" % str(e))
        print("Make sure pygame is properly installed: pip install pygame")
        if hasattr(__builtins__, 'raw_input'):
            raw_input("Press Enter to exit...")
        else:
            input("Press Enter to exit...")