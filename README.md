# Asylum of Sins

A dark atmospheric puzzle-adventure game combining moral decision-making with classic computer science algorithms. Navigate through a narrative where your sins and virtues determine both your burden and the structure of the maze you must traverse to reach salvation.

![Python](https://img.shields.io/badge/python-v2.7%2B-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-v1.9.1%2B-green.svg)

## Overview

**Asylum of Sins** demonstrates practical applications of fundamental algorithms in game development:
- **Knapsack Problem** for moral choice optimization within capacity constraints
- **Recursive Backtracking** for dynamic maze generation
- **Dijkstra's Algorithm** for optimal pathfinding
- **Fog of War** system with geometric visibility

Players progress through eight distinct phases, from confession to final judgment, where every choice influences both gameplay mechanics and narrative outcomes.

## Features

- **Interactive Moral Selection**: Choose sins and virtues within soul capacity limits
- **Dynamic Maze Generation**: Maze structure influenced by moral choices
- **Fog of War Navigation**: Limited visibility that reveals the maze gradually  
- **Multiple Endings**: Four different fates based on moral balance and performance
- **Atmospheric Design**: Particle effects, thematic colors, and immersive UI
- **Algorithm Visualization**: See optimal paths and efficiency calculations

## Game Flow

1. **Introduction** - Atmospheric story setup
2. **Confession** - Preparation for moral choices
3. **Sin Selection** - Interactive burden selection
4. **Virtue Selection** - Interactive redemption selection  
5. **Summary** - Review moral weight and balance
6. **Maze Preparation** - Setup for the trial
7. **Maze Navigation** - Traverse the judgment maze
8. **Final Judgment** - Discover your eternal fate

## Algorithm Implementation

### Knapsack Problem - Interactive Selection

```python
def calculate_current_weight(self):
    """Calculate current total weight of selected items"""
    sin_weight = sum(sin.weight for sin in self.sins if sin.selected)
    virtue_weight = sum(virtue.weight for virtue in self.virtues if virtue.selected)
    return sin_weight + virtue_weight

# Capacity validation during selection
if self.calculate_current_weight() + item.weight <= self.soul_capacity:
    item.selected = True
```

**Complexity**: O(n) for validation, O(1) for individual operations  
**Application**: Real-time capacity checking during interactive moral selection

### Recursive Backtracking - Maze Generation

```python
def generate_sinful_maze(self, chosen_sins, chosen_virtues):
    """Generate maze based on moral choices using recursive backtracking"""
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
    
    # Apply moral choice modifications
    self._apply_sin_effects(chosen_sins)
    self._apply_virtue_effects(chosen_virtues)
```

**Complexity**: O(n×m) time, O(n×m) space  
**Enhancement**: Post-processing applies sin/virtue-specific maze modifications

### Dijkstra's Algorithm - Pathfinding

```python
def dijkstra_pathfinding(self, start, end):
    """Calculate optimal path using Dijkstra's algorithm"""
    distances = [[float('inf')] * cols for _ in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    parent = {start: None}
    
    distances[start[1]][start[0]] = 0
    heap = [(0, start)]
    
    while heap:
        current_dist, pos = heapq.heappop(heap)
        x, y = pos
        
        if visited[y][x]:
            continue
        visited[y][x] = True
        
        if pos == end:
            break
        
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
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
```

**Complexity**: O((V + E) log V) where V = cells, E = edges  
**Purpose**: Calculate optimal path for performance comparison (revealed after completion)

### Fog of War - Visibility System

```python
def reveal_around_player(self):
    """Reveal cells within vision radius using Euclidean distance"""
    px, py = self.player_pos
    for dy in range(-VISION_RADIUS, VISION_RADIUS + 1):
        for dx in range(-VISION_RADIUS, VISION_RADIUS + 1):
            nx, ny = px + dx, py + dy
            if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT:
                distance = math.sqrt(dx*dx + dy*dy)
                if distance <= VISION_RADIUS:
                    self.visited_cells.add((nx, ny))
```

**Complexity**: O(r²) where r = vision radius  
**Effect**: Creates atmospheric exploration with limited visibility

## Installation

### Requirements

- Python 2.7+ or Python 3.x
- Pygame 1.9.1+
- Standard libraries: `random`, `heapq`, `math`, `time`, `itertools`

### Quick Setup

```bash
# Clone repository
git clone https://github.com/hanzel-sc/knapsack-of-sins.git
cd knapsack-of-sins

# Install pygame
pip install pygame

# Run game
python game.py
```

### Detailed Installation

#### Windows
```cmd
# Install Python from https://python.org/downloads/
# Ensure "Add Python to PATH" is checked

# Install pygame
pip install pygame

# Run game
python game.py
```

#### macOS
```bash
# Using Homebrew
brew install python
pip install pygame

# Run game
python game.py
```

#### Linux (Ubuntu/Debian)
```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Install pygame
pip3 install pygame

# Run game
python3 game.py
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv asylum_env

# Activate
# Windows:
asylum_env\Scripts\activate
# macOS/Linux:
source asylum_env/bin/activate

# Install dependencies
pip install pygame

# Run game
python game.py

# Deactivate when done
deactivate
```

## Controls

| Key | Action |
|-----|--------|
| Arrow Keys / WASD | Navigate menus and maze |
| SPACE | Select/deselect items, advance text |
| ENTER | Confirm selections, continue |
| R | Restart game (judgment screen) |

## Troubleshooting

### Common Issues

**Pygame Installation Error:**
```bash
# Upgrade pip first
pip install --upgrade pip
pip install pygame

# Linux: Install dependencies
sudo apt install python3-dev python3-setuptools
```

**Permission Errors:**
```bash
# Use --user flag
pip install --user pygame
```

**Display Issues:**
- Ensure 1400×900 resolution support
- Update graphics drivers
- Enable X11 forwarding for SSH connections

**Multiple Python Versions:**
```bash
# Use specific version
python3 -m pip install pygame
python3 game.py
```

## Technical Specifications

### Performance
- **Maze Generation**: ~0.1-0.5 seconds for 51×35 maze
- **Pathfinding**: ~0.01-0.1 seconds typical
- **Frame Rate**: 60 FPS target
- **Memory Usage**: ~10-20 MB during gameplay

### System Requirements

**Minimum:**
- OS: Windows 7+, macOS 10.9+, Linux
- RAM: 512 MB
- Display: 1400×900
- Python: 2.7+

**Recommended:**
- OS: Windows 10, macOS 10.15+, Ubuntu 18.04+
- RAM: 2 GB
- Display: 1920×1080
- Python: 3.7+

## Game Mechanics

### Moral Choice System

**Sins** (9 available):
- Wrath, Envy, Pride, Greed, Lust, Gluttony, Sloth, Despair, Hatred
- Each sin affects maze generation (adds complexity, loops, dead ends)

**Virtues** (7 available):
- Compassion, Humility, Forgiveness, Patience, Courage, Wisdom, Hope  
- Each virtue improves maze traversal (shortcuts, simplified paths)

### Maze Effects by Choice

| Choice | Maze Effect |
|--------|-------------|
| Wrath | Sharp turns and aggressive angles |
| Envy | Deceptive loops that circle back |
| Pride | Unnecessarily complex detours |
| Compassion | Helpful shortcuts between areas |
| Wisdom | Efficient path connections |
| Courage | Direct routes to goal |

### Judgment Criteria

Final fate determined by:
- **Moral Balance**: Virtue value - Sin value
- **Path Efficiency**: Player steps / Optimal steps
- **Combined Score**: Balance - (Efficiency penalty)

**Possible Destinations:**
- **Purgatory**: High virtue, efficient path
- **Gray Realm**: Balanced choices, moderate efficiency
- **Lower Circles**: More sins than virtues
- **The Abyss**: Overwhelming sin, poor navigation

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Acknowledgments

- Pygame community for excellent documentation
- Classic maze algorithms and their implementations
- Dante's Inferno for thematic inspiration