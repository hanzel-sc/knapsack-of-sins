#!/usr/bin/env python3
"""
Asylum of Sins - A Dark CLI Adventure Game
Combines Knapsack DP for sin selection with Dijkstra pathfinding
"""

import time
import random
import heapq
import os
import sys
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum

class SinType(Enum):
    ENVY = "envy"
    WRATH = "wrath"
    DESPAIR = "despair"
    OBSESSION = "obsession"
    GREED = "greed"
    PRIDE = "pride"
    SLOTH = "sloth"

class Ending(Enum):
    HELL = "hell"
    PURGATORY = "purgatory"
    ETERNAL_SILENCE = "eternal_silence"

@dataclass
class Sin:
    sin_type: SinType
    weight: int
    consequence_value: int
    description: str
    narrative_text: str

class AsylumGame:
    def __init__(self):
        self.sins = self._initialize_sins()
        self.max_weight = 15  # Maximum sin weight you can carry
        self.selected_sins = []
        self.maze = None
        self.maze_size = 15
        self.player_pos = [1, 1]
        self.exit_pos = [13, 13]
        self.path_taken = []
        self.optimal_path = []
        self.game_state = "intro"
        
    def _initialize_sins(self) -> List[Sin]:
        """Initialize all available sins with their properties"""
        return [
            Sin(SinType.ENVY, 4, 8, "Jade-eyed Envy", 
                "The bitter taste of others' fortune burns your throat..."),
            Sin(SinType.WRATH, 6, 12, "Crimson Wrath", 
                "Fury courses through your veins like molten iron..."),
            Sin(SinType.DESPAIR, 3, 6, "Abyssal Despair", 
                "The weight of hopelessness settles in your chest..."),
            Sin(SinType.OBSESSION, 5, 10, "Consuming Obsession", 
                "Your mind fixates on forbidden desires..."),
            Sin(SinType.GREED, 7, 15, "Golden Greed", 
                "The hunger for more gnaws at your soul..."),
            Sin(SinType.PRIDE, 4, 9, "Towering Pride", 
                "Your ego swells like a grotesque tumor..."),
            Sin(SinType.SLOTH, 2, 4, "Leaden Sloth", 
                "Apathy weighs down your every movement...")
        ]

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def typewriter_effect(self, text: str, delay: float = 0.03):
        """Print text with typewriter effect"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def animate_title(self):
        """Display animated title screen"""
        self.clear_screen()
        title = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║        █████╗ ███████╗██╗   ██╗██╗     ██╗   ██╗███╗   ███╗       ║
    ║       ██╔══██╗██╔════╝╚██╗ ██╔╝██║     ██║   ██║████╗ ████║       ║
    ║       ███████║███████╗ ╚████╔╝ ██║     ██║   ██║██╔████╔██║       ║
    ║       ██╔══██║╚════██║  ╚██╔╝  ██║     ██║   ██║██║╚██╔╝██║       ║
    ║       ██║  ██║███████║   ██║   ███████╗╚██████╔╝██║ ╚═╝ ██║       ║
    ║       ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝     ╚═╝       ║
    ║                                                                   ║
    ║                    ██████╗ ███████╗                               ║
    ║                   ██╔═══██╗██╔════╝                               ║
    ║                   ██║   ██║█████╗                                 ║
    ║                   ██║   ██║██╔══╝                                 ║
    ║                   ╚██████╔╝██║                                    ║
    ║                    ╚═════╝ ╚═╝                                    ║
    ║                                                                   ║
    ║               ███████╗██╗███╗   ██╗███████╗                       ║
    ║               ██╔════╝██║████╗  ██║██╔════╝                       ║
    ║               ███████╗██║██╔██╗ ██║███████╗                       ║
    ║               ╚════██║██║██║╚██╗██║╚════██║                       ║
    ║               ███████║██║██║ ╚████║███████║                       ║
    ║               ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
        """
        
        for line in title.split('\n'):
            print(line)
            time.sleep(0.1)
        
        time.sleep(1)
        self.typewriter_effect("\n    The gates of judgment await your final burden...\n", 0.05)
        time.sleep(2)

    def show_intro(self):
        """Display game introduction"""
        self.clear_screen()
        
        intro_text = """
    ═══════════════════════════════════════════════════════════════════
    
    You stand at the threshold between life and death, your soul heavy
    with the weight of mortal sins. The Asylum of Judgment looms before
    you - a labyrinthine prison where the damned must choose their
    eternal burden.
    
    You cannot carry all your sins into the afterlife. The cosmic laws
    demand a choice: which transgressions will you bear, and which will
    you abandon to the void?
    
    Your selection will determine not just your path through the maze
    of judgment, but your final destination in the realms beyond...
    
    There is no paradise for souls like yours.
    Only degrees of damnation.
    
    ═══════════════════════════════════════════════════════════════════
        """
        
        self.typewriter_effect(intro_text)
        input("\n    Press Enter to confront your sins...")

    def display_sins(self):
        """Display available sins for selection"""
        self.clear_screen()
        print("\n    ╔═══════════════════ YOUR SINS ═══════════════════╗")
        print("    ║                                                 ║")
        
        for i, sin in enumerate(self.sins, 1):
            print(f"    ║  {i}. {sin.description:<25} Weight: {sin.weight:2}    ║")
            print(f"    ║     {sin.narrative_text:<42} ║")
            print(f"    ║     Consequence Value: {sin.consequence_value:<22} ║")
            print("    ║                                                 ║")
        
        print("    ╚═════════════════════════════════════════════════╝")
        print(f"\n    Maximum weight you can carry: {self.max_weight}")
        print(f"    Current selection weight: {sum(sin.weight for sin in self.selected_sins)}")

    def fractional_knapsack_dp(self) -> List[Sin]:
        """
        Solve fractional knapsack problem to find optimal sin combination
        Using dynamic programming approach
        """
        n = len(self.sins)
        W = self.max_weight
        
        # Create DP table
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        
        # Fill DP table
        for i in range(1, n + 1):
            for w in range(1, W + 1):
                if self.sins[i-1].weight <= w:
                    dp[i][w] = max(
                        dp[i-1][w],
                        dp[i-1][w - self.sins[i-1].weight] + self.sins[i-1].consequence_value
                    )
                else:
                    dp[i][w] = dp[i-1][w]
        
        # Backtrack to find selected items
        selected = []
        w = W
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected.append(self.sins[i-1])
                w -= self.sins[i-1].weight
        
        return selected

    def sin_selection_phase(self):
        """Handle sin selection with player choice or optimization"""
        while True:
            self.display_sins()
            
            print("\n    ╔════════════════ CHOICE ═══════════════╗")
            print("    ║ 1. Select sins manually               ║")
            print("    ║ 2. Let the algorithm decide (optimal) ║")
            print("    ║ 3. View current selection             ║")
            print("    ║ 4. Proceed to judgment                ║")
            print("    ╚═══════════════════════════════════════╝")
            
            choice = input("\n    Your choice: ").strip()
            
            if choice == '1':
                self._manual_sin_selection()
            elif choice == '2':
                self._optimal_sin_selection()
            elif choice == '3':
                self._show_current_selection()
            elif choice == '4':
                if self.selected_sins:
                    break
                else:
                    self.typewriter_effect("\n    You cannot proceed without bearing at least one sin...")
                    time.sleep(2)
            else:
                self.typewriter_effect("    Invalid choice. The void whispers of your indecision...")
                time.sleep(1)

    def _manual_sin_selection(self):
        """Handle manual sin selection by player"""
        self.clear_screen()
        self.display_sins()
        
        try:
            sin_num = int(input("\n    Select a sin (number): ")) - 1
            if 0 <= sin_num < len(self.sins):
                sin = self.sins[sin_num]
                current_weight = sum(s.weight for s in self.selected_sins)
                
                if sin in self.selected_sins:
                    self.selected_sins.remove(sin)
                    self.typewriter_effect(f"\n    You release {sin.description} into the void...")
                elif current_weight + sin.weight <= self.max_weight:
                    self.selected_sins.append(sin)
                    self.typewriter_effect(f"\n    {sin.description} clings to your soul...")
                    self.typewriter_effect(f"    {sin.narrative_text}")
                else:
                    self.typewriter_effect("\n    Your soul cannot bear this additional weight...")
            else:
                self.typewriter_effect("    That sin does not exist in your repertoire...")
        except ValueError:
            self.typewriter_effect("    Numbers, mortal. Use numbers...")
        
        time.sleep(2)

    def _optimal_sin_selection(self):
        """Use DP algorithm to select optimal sins"""
        self.selected_sins = self.fractional_knapsack_dp()
        self.clear_screen()
        
        self.typewriter_effect("\n    The cosmic algorithm weighs your sins...\n")
        time.sleep(2)
        
        for sin in self.selected_sins:
            self.typewriter_effect(f"    • {sin.description} - Weight: {sin.weight}")
            time.sleep(0.5)
        
        total_value = sum(sin.consequence_value for sin in self.selected_sins)
        total_weight = sum(sin.weight for sin in self.selected_sins)
        
        self.typewriter_effect(f"\n    Total consequence value: {total_value}")
        self.typewriter_effect(f"    Total weight: {total_weight}/{self.max_weight}")
        
        input("\n    Press Enter to accept this burden...")

    def _show_current_selection(self):
        """Display currently selected sins"""
        self.clear_screen()
        
        if not self.selected_sins:
            self.typewriter_effect("\n    No sins currently burden your soul...")
        else:
            print("\n    ╔═══════════════ CURRENT BURDEN ═══════════════╗")
            for sin in self.selected_sins:
                print(f"    ║ • {sin.description:<25} Weight: {sin.weight:2} ║")
            
            total_weight = sum(sin.weight for sin in self.selected_sins)
            total_value = sum(sin.consequence_value for sin in self.selected_sins)
            
            print("    ║                                              ║")
            print(f"    ║ Total Weight: {total_weight:2}/{self.max_weight}                      ║")
            print(f"    ║ Total Consequence Value: {total_value:3}              ║")
            print("    ╚══════════════════════════════════════════════╝")
        
        input("\n    Press Enter to continue...")

    def generate_maze(self):
        """Generate a random maze using recursive backtracking"""
        size = self.maze_size
        maze = [['█' for _ in range(size)] for _ in range(size)]
        
        def carve_path(x, y):
            maze[y][x] = ' '
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < size - 1 and 0 < ny < size - 1 and maze[ny][nx] == '█':
                    maze[y + dy//2][x + dx//2] = ' '
                    carve_path(nx, ny)
        
        carve_path(1, 1)
        maze[1][1] = '☠'  # Player start
        maze[self.exit_pos[0]][self.exit_pos[1]] = '⚰'  # Exit
        
        # Add some sin-influenced obstacles
        self._add_sin_obstacles(maze)
        
        self.maze = maze

    def _add_sin_obstacles(self, maze):
        """Add obstacles based on selected sins"""
        for sin in self.selected_sins:
            for _ in range(sin.weight):
                while True:
                    x, y = random.randint(2, self.maze_size-3), random.randint(2, self.maze_size-3)
                    if maze[y][x] == ' ' and (x, y) != tuple(self.player_pos) and (x, y) != tuple(self.exit_pos):
                        if sin.sin_type == SinType.WRATH:
                            maze[y][x] = '🔥'  # Fire obstacles
                        elif sin.sin_type == SinType.ENVY:
                            maze[y][x] = '👁'  # Watching eyes
                        elif sin.sin_type == SinType.DESPAIR:
                            maze[y][x] = '💀'  # Skull obstacles
                        elif sin.sin_type == SinType.GREED:
                            maze[y][x] = '💰'  # Gold obstacles
                        else:
                            maze[y][x] = '▓'  # Generic sin obstacle
                        break

    def display_maze(self):
        """Display the current maze state"""
        print("\n    ╔" + "═" * (self.maze_size * 2 + 1) + "╗")
        
        for y, row in enumerate(self.maze):
            line = "    ║ "
            for x, cell in enumerate(row):
                if [x, y] == self.player_pos:
                    line += "☠ "
                else:
                    line += cell + " "
            line += "║"
            print(line)
        
        print("    ╚" + "═" * (self.maze_size * 2 + 1) + "╝")

    def dijkstra_shortest_path(self) -> List[Tuple[int, int]]:
        """Find shortest path using Dijkstra's algorithm"""
        start = tuple(self.player_pos)
        end = tuple(self.exit_pos)
        
        # Priority queue: (distance, position)
        pq = [(0, start)]
        distances = {start: 0}
        previous = {}
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current == end:
                break
            
            if current_dist > distances.get(current, float('inf')):
                continue
            
            x, y = current
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < self.maze_size and 0 <= ny < self.maze_size and
                    self.maze[ny][nx] != '█'):
                    
                    # Calculate weight based on cell type
                    weight = 1
                    cell = self.maze[ny][nx]
                    if cell in ['🔥', '👁', '💀', '💰', '▓']:
                        weight = 3  # Sin obstacles cost more
                    
                    distance = current_dist + weight
                    
                    if distance < distances.get((nx, ny), float('inf')):
                        distances[(nx, ny)] = distance
                        previous[(nx, ny)] = current
                        heapq.heappush(pq, (distance, (nx, ny)))
        
        # Reconstruct path
        path = []
        current = end
        while current in previous:
            path.append(current)
            current = previous[current]
        path.append(start)
        
        return path[::-1]

    def maze_phase(self):
        """Handle the maze navigation phase"""
        self.generate_maze()
        self.optimal_path = self.dijkstra_shortest_path()
        self.path_taken = [tuple(self.player_pos)]
        
        self.clear_screen()
        self.typewriter_effect("\n    The Asylum's labyrinth manifests before you...")
        self.typewriter_effect("    Your sins have shaped its very structure...")
        self.typewriter_effect("\n    Navigate to the exit (⚰) to face judgment.")
        self.typewriter_effect("    Use WASD to move, Q to quit, H for help.")
        
        while True:
            self.display_maze()
            
            # Show current stats
            print(f"\n    Position: ({self.player_pos[0]}, {self.player_pos[1]})")
            print(f"    Steps taken: {len(self.path_taken) - 1}")
            print(f"    Optimal path length: {len(self.optimal_path) - 1}")
            
            if self.player_pos == self.exit_pos:
                self.typewriter_effect("\n    You have reached the exit...")
                break
            
            move = input("\n    Move: ").lower().strip()
            
            if move == 'q':
                self.typewriter_effect("    There is no escape from judgment...")
                continue
            elif move == 'h':
                self._show_help()
                continue
            
            self._handle_movement(move)

    def _show_help(self):
        """Display help information"""
        self.clear_screen()
        help_text = """
    ╔═══════════════════ ASYLUM NAVIGATION ═══════════════════╗
    ║                                                         ║
    ║  W - Move North    🔥 - Wrath's Fire (slows you down)   ║
    ║  A - Move West     👁 - Envy's Gaze (watching you)      ║
    ║  S - Move South    💀 - Despair's Bones (obstacles)     ║
    ║  D - Move East     💰 - Greed's Gold (heavy burden)     ║
    ║  Q - Quit          ▓ - Generic Sin Obstacle            ║
    ║  H - Help          █ - Impassable Walls                ║
    ║  M - Show full map ☠ - Your Soul                       ║
    ║                    ⚰ - Exit to Judgment                ║
    ║                    ▒ - Fog of War (unknown)            ║
    ║                    ∙ - Your Trail (visited areas)      ║
    ║                                                         ║
    ║  LIMITED VISIBILITY: You can only see 2 spaces around  ║
    ║  your current position. Your sins have clouded your    ║
    ║  perception of the maze's true layout.                  ║
    ║                                                         ║
    ║  The algorithm knows the shortest path, but can you    ║
    ║  find it while navigating in darkness?                 ║
    ║                                                         ║
    ╚═════════════════════════════════════════════════════════╝
        """
        print(help_text)
        input("\n    Press Enter to continue...")
        self.clear_screen()

    def _show_full_map(self):
        """Show the complete maze (cheat mode)"""
        self.clear_screen()
        self.typewriter_effect("    The cosmic algorithm reveals the true structure...")
        print("\n    ╔" + "═" * (self.maze_size * 2 + 1) + "╗")
        
        for y, row in enumerate(self.maze):
            line = "    ║ "
            for x, cell in enumerate(row):
                if [x, y] == self.player_pos:
                    line += "☠ "
                elif (x, y) in [tuple(pos) for pos in self.path_taken]:
                    line += "∙ "
                elif (x, y) in self.optimal_path:
                    # Show optimal path in a different marker
                    line += "○ " if cell == ' ' else cell + " "
                else:
                    line += cell + " "
            line += "║"
            print(line)
        
        print("    ╚" + "═" * (self.maze_size * 2 + 1) + "╝")
        print("\n    Legend: ○ = Optimal Path, ∙ = Your Trail")
        self.typewriter_effect("    But knowledge of the optimal path is a burden too...")
        input("\n    Press Enter to return to limited vision...")
        self.clear_screen()

    def _handle_movement(self, move):
        """Handle player movement"""
        directions = {
            'w': (0, -1),  # North
            'a': (-1, 0),  # West
            's': (0, 1),   # South
            'd': (1, 0)    # East
        }
        
        if move in directions:
            dx, dy = directions[move]
            new_x = self.player_pos[0] + dx
            new_y = self.player_pos[1] + dy
            
            # Check bounds and walls
            if (0 <= new_x < self.maze_size and 
                0 <= new_y < self.maze_size and 
                self.maze[new_y][new_x] != '█'):
                
                self.player_pos = [new_x, new_y]
                self.path_taken.append(tuple(self.player_pos))
                
                # Check for sin obstacles
                cell = self.maze[new_y][new_x]
                if cell in ['🔥', '👁', '💀', '💰', '▓']:
                    self._handle_sin_obstacle(cell)
                
                self.clear_screen()
            else:
                self.typewriter_effect("    The walls of judgment block your path...")
                time.sleep(1)
        else:
            self.typewriter_effect("    Invalid movement. The void whispers mockingly...")
            time.sleep(1)

    def _handle_sin_obstacle(self, cell):
        """Handle encounters with sin-based obstacles"""
        messages = {
            '🔥': "The fires of wrath burn your soul...",
            '👁': "Envious eyes track your every movement...",
            '💀': "The bones of despair rattle beneath your feet...",
            '💰': "Greed's weight slows your progress...",
            '▓': "Your sins manifest as barriers..."
        }
        
        if cell in messages:
            self.typewriter_effect(f"\n    {messages[cell]}")
            time.sleep(1.5)

    def calculate_ending(self) -> Ending:
        """Calculate the ending based on sins and path efficiency"""
        total_consequence = sum(sin.consequence_value for sin in self.selected_sins)
        path_efficiency = len(self.optimal_path) / len(self.path_taken) if self.path_taken else 0
        
        # Check for specific sin combinations
        sin_types = {sin.sin_type for sin in self.selected_sins}
        
        # Hell ending conditions
        if (total_consequence >= 25 or 
            SinType.WRATH in sin_types and SinType.GREED in sin_types or
            len(self.selected_sins) >= 5):
            return Ending.HELL
        
        # Eternal Silence ending (most mysterious)
        if (path_efficiency > 0.8 and 
            SinType.DESPAIR in sin_types and 
            total_consequence <= 15):
            return Ending.ETERNAL_SILENCE
        
        # Default to Purgatory
        return Ending.PURGATORY

    def show_ending(self, ending: Ending):
        """Display the appropriate ending sequence"""
        self.clear_screen()
        
        # Show path analysis
        self.typewriter_effect("\n    ═══════════════ JUDGMENT ANALYSIS ═══════════════")
        self.typewriter_effect(f"    Your path length: {len(self.path_taken) - 1}")
        self.typewriter_effect(f"    Optimal path length: {len(self.optimal_path) - 1}")
        efficiency = len(self.optimal_path) / len(self.path_taken) if self.path_taken else 0
        self.typewriter_effect(f"    Path efficiency: {efficiency:.2%}")
        
        total_consequence = sum(sin.consequence_value for sin in self.selected_sins)
        self.typewriter_effect(f"    Total sin weight: {total_consequence}")
        
        time.sleep(3)
        
        if ending == Ending.HELL:
            self._show_hell_ending()
        elif ending == Ending.PURGATORY:
            self._show_purgatory_ending()
        elif ending == Ending.ETERNAL_SILENCE:
            self._show_eternal_silence_ending()

    def _show_hell_ending(self):
        """Display Hell ending sequence"""
        self.clear_screen()
        
        hell_art = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥     ║
    ║    🔥                 THE GATES OF HELL               🔥     ║
    ║    🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥     ║
    ║                                                                   ║
    ║         Your sins burn eternal, their weight unbearable.          ║
    ║         The flames welcome you as an old friend.                  ║
    ║         Here, algorithms and suffering intertwine                 ║
    ║         in an infinite loop of torment.                           ║
    ║                                                                   ║
    ║         You chose poorly. You carried too much.                   ║
    ║         The optimal path was never about the maze—                ║
    ║         it was about the burden you accepted.                     ║
    ║                                                                   ║
    ║    💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀     ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
        """
        
        print(hell_art)
        self.typewriter_effect("\n    The screams of the damned echo your poor optimization...", 0.05)

    def _show_purgatory_ending(self):
        """Display Purgatory ending sequence"""
        self.clear_screen()
        
        purgatory_art = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║    ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋     ║
    ║                        THE GRAY BETWEEN                           ║
    ║    ≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋≋     ║
    ║                                                                   ║
    ║         Neither fully damned nor completely lost,                 ║
    ║         you wander the endless mists of calculation.              ║
    ║         Your sins were balanced, your path adequate.              ║
    ║                                                                   ║
    ║         Here, you will solve infinite problems,                   ║
    ║         each solution bringing you closer to understanding        ║
    ║         the true weight of your choices.                          ║
    ║                                                                   ║
    ║         The algorithm judges you... sufficient.                   ║
    ║         But optimization remains forever out of reach.            ║
    ║                                                                   ║
    ║    ～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～                       ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
        """
        
        print(purgatory_art)
        self.typewriter_effect("\n    Your journey continues in the endless gray...", 0.05)

    def _show_eternal_silence_ending(self):
        """Display Eternal Silence ending sequence"""
        self.clear_screen()
        
        silence_art = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     ║
    ║                      THE ETERNAL VOID                             ║
    ║    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     ║
    ║                                                                   ║
    ║         You found the optimal path through both maze              ║
    ║         and moral complexity. Your burden was light,              ║
    ║         your navigation precise.                                   ║
    ║                                                                   ║
    ║         In reward, you are granted the most mysterious            ║
    ║         of fates: complete dissolution into the void.             ║
    ║         No torment, no redemption—only the silence               ║
    ║         between algorithms.                                       ║
    ║                                                                   ║
    ║         You have achieved the closest thing to peace              ║
    ║         available to a corrupted soul:                            ║
    ║                                                                   ║
    ║                        Nonexistence.                              ║
    ║                                                                   ║
    ║    ∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅∅     ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
        """
        
        print(silence_art)
        for i in range(5):
            time.sleep(1)
            print("    " + "." * (i + 1))
        
        self.typewriter_effect("\n    The void embraces your optimized soul...", 0.08)

    def show_credits(self):
        """Display game credits"""
        self.clear_screen()
        
        credits = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                            ASYLUM OF SINS                         ║
    ║                                                                   ║
    ║                    A Dark Algorithmic Journey                     ║
    ║                                                                   ║
    ║    Algorithms Used:                                               ║
    ║    • Dynamic Programming (Knapsack Problem)                       ║
    ║    • Dijkstra's Shortest Path Algorithm                           ║
    ║    • Recursive Backtracking (Maze Generation)                     ║
    ║                                                                   ║
    ║    "In the end, we are all just optimization problems            ║
    ║     seeking the minimal path through maximum suffering."          ║
    ║                                                                   ║
    ║    Game Design Philosophy:                                        ║
    ║    Every choice carries weight. Every path has consequences.      ║
    ║    The algorithm knows the optimal solution,                      ║
    ║    but do you have the wisdom to find it?                        ║
    ║                                                                   ║
    ║    Thank you for playing Asylum of Sins.                         ║
    ║    May your real-life optimization problems                       ║
    ║    be less existentially terrifying.                             ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
        """
        
        print(credits)

    def play_again_prompt(self) -> bool:
        """Ask player if they want to play again"""
        while True:
            choice = input("\n    Face judgment again? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                self.typewriter_effect("    The void demands a clear answer...")

    def reset_game(self):
        """Reset game state for new playthrough"""
        self.selected_sins = []
        self.maze = None
        self.player_pos = [1, 1]
        self.path_taken = []
        self.optimal_path = []
        self.game_state = "intro"

    def run(self):
        """Main game loop"""
        try:
            while True:
                # Title and intro
                self.animate_title()
                self.show_intro()
                
                # Sin selection phase
                self.sin_selection_phase()
                
                # Maze navigation phase
                self.maze_phase()
                
                # Judgment and ending
                ending = self.calculate_ending()
                self.show_ending(ending)
                
                # Credits
                time.sleep(3)
                self.show_credits()
                
                # Play again?
                if not self.play_again_prompt():
                    break
                
                self.reset_game()
                
        except KeyboardInterrupt:
            self.clear_screen()
            self.typewriter_effect("\n    The algorithm judges your interruption... harshly.")
            self.typewriter_effect("    But even the damned deserve a clean exit.")
            time.sleep(2)
        
        self.clear_screen()
        final_message = """
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║    "Every soul carries the weight of its choices,                 ║
    ║     and every choice echoes in the algorithms of eternity."       ║
    ║                                                                   ║
    ║                        - The Asylum                               ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
        """
        print(final_message)


def main():
    """Entry point for the game"""
    print("Loading the Asylum of Sins...")
    time.sleep(1)
    
    game = AsylumGame()
    game.run()


if __name__ == "__main__":
    main()