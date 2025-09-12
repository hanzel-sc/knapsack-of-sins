# Asylum of Sins

A dark, atmospheric CLI-based adventure game that combines **algorithmic problem-solving** with **narrative-driven gameplay**.  
Players navigate **moral choices (sins)** and **spatial challenges (mazes)** while the game compares their performance against algorithmic benchmarks.

---

## Table of Contents
1. [Game Overview](#game-overview)  
2. [Architecture & Design](#architecture--design)  
3. [Algorithm Implementations](#algorithm-implementations)  
4. [Game Mechanics](#game-mechanics)  
5. [Technical Features](#technical-features)  
6. [User Interface](#user-interface)  
7. [Ending System](#ending-system)  
8. [Installation & Usage](#installation--usage)  
9. [Code Structure](#code-structure)  
10. [Future Enhancements](#future-enhancements)  
11. [Performance Analysis](#performance-analysis)  
12. [Educational Value](#educational-value)  
13. [Technical Implementation Details](#technical-implementation-details)  
14. [Security and Data Privacy](#security-and-data-privacy)  
15. [Conclusion](#conclusion)  

---

## Game Overview

- **Theme**: Dark psychological horror with algorithmic judgment  
- **Genre**: CLI Adventure/Puzzle with Educational Elements  
- **Target Audience**: Programmers, algorithm enthusiasts, horror fans  
- **Unique Selling Point**: Real-time comparison of human decision-making vs algorithmic optimization  

---

## Architecture & Design

**Principles**:  
- Every choice has computational weight (sin weight in knapsack, path cost in maze).  
- Dual optimization:  
  - **Knapsack DP** for sin selection  
  - **Dijkstra** for pathfinding  
- Player choices → Algorithm analysis → Narrative consequences  

## Implementation

def fractional_knapsack_dp(self) -> List[Sin]:
    n = len(self.sins)
    W = self.max_weight
    
    # Create DP table: dp[i][w] = max value using first i items with weight limit w
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
    
    # Fill DP table using recurrence relation
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if self.sins[i-1].weight <= w:
                dp[i][w] = max(
                    dp[i-1][w],  # Don't take item i
                    dp[i-1][w - self.sins[i-1].weight] + self.sins[i-1].consequence_value  # Take item i
                )
            else:
                dp[i][w] = dp[i-1][w]  # Can't take item i
    
    # Backtrack to reconstruct solution
    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:  # Item i was selected
            selected.append(self.sins[i-1])
            w -= self.sins[i-1].weight
    
    return selected


---

## Algorithm Implementations

### 1. Dynamic Programming – Knapsack
- Optimizes sin selection within **weight constraint (15 units)**  
- **Complexity**: O(n × W), trivial for 7 sins  

### 2. Dijkstra’s Shortest Path
- Finds **optimal path** through maze  
- Compares player’s path vs optimal  
- **Complexity**: O(V log V + E), efficient for 15×15 mazes  

### 3. Recursive Backtracking – Maze Generation
- Generates unique solvable mazes  
- Randomized for variety  
- **Complexity**: O(n²)  

---

## Game Mechanics

- **Sins** act as weighted items with consequences:
  - *Greed*: 💰 heavy but high consequence  
  - *Wrath*: 🔥 adds costly obstacles  
  - *Despair*: 💀 triggers special ending conditions  

- **Navigation**:  
  - WASD movement  
  - Fog of war with limited vision (range = 2)  
  - Path length tracked for efficiency  

- **Performance Metrics**:  
  - Path efficiency  
  - Total consequence value  
  - Steps taken vs optimal  

---

## Technical Features

- **ASCII Art Engine** with typewriter text effect  
- **Fog of War** with ▒ and ∙ trail markers  
- **Symbols**: ☠ (player), ⚰ (exit), █ (walls), 🔥 👁 💀 💰 (obstacles)  
- Robust **error handling & input validation**  
- Cross-platform terminal support  

---

---

## Ending System

Three possible endings:  

1. **Hell (Damnation)** – heavy sins, poor optimization  
2. **Purgatory (Default)** – moderate outcome  
3. **Eternal Silence (Transcendence)** – optimal play, light burden  

---

## Installation & Usage

### Requirements
- Python 3.6+  
- keyboard==0.13.5
- colorama==0.4.6

