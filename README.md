# 🧩 Rush Hour Puzzle Solver

A Python implementation of the **Rush Hour Puzzle**, featuring:
- **Breadth-First Search (BFS)**
- **A\*** Search Algorithm with three different heuristics (h1, h2, h3)
- A **Graphical User Interface (GUI)** built with **Pygame** for visualizing the solutions.

---

## 🚗 Project Overview

The **Rush Hour puzzle** consists of a 6×6 grid containing vehicles that block the red car ("X").  
The goal is to **move the red car to the exit** on the right side of the grid by moving other cars up, down, left, or right.

This project implements:
- **Search algorithms** to automatically solve the puzzle.
- A **graphical interface** to visualize each step of the solution.

---

## 🧠 Algorithms Implemented

### 1️⃣ Breadth-First Search (BFS)
- Explores all states level by level.
- Guarantees the shortest solution.
- Can be slow for large puzzles due to the high number of explored states.

### 2️⃣ A\* Search Algorithm
A more efficient search that uses heuristics to guide the exploration.

**Heuristics used:**
- **h1:** Distance from the red car to the exit.
- **h2:** h1 + number of blocking vehicles in the path.
- **h3:** h1 + total length of blocking vehicles.

**Performance comparison (example):**
| Algorithm | Time (s) | Explored States |
|------------|-----------|----------------|
| BFS        | 1.07      | 486            |
| A\* (h1)   | 0.71      | 399            |
| A\* (h2)   | 0.48      | 319            |
| A\* (h3)   | 0.46      | 304            |

---

## 🖥️ Graphical Interface (Pygame)

The GUI allows you to:
- Choose the algorithm (BFS, A\* h1, h2, h3).
- Watch the solution animate step by step.
- Reset the board after solving.
- Quit the application.

**Controls:**
- 🟦 **BFS**
- 🟢 **A\* h1/h2/h3**
- 🔄 **Reset**
- ❌ **Quit**

---

## 📁 Project Structure

```
📂 Rush-Hour-Puzzle/
├── Rush.py              # Core logic
├── gui.py               # Pygame interface
├── 1.csv                # Example puzzle
├── 2-c.csv              # Another puzzle
├── README.md            # Documentation
```

---

## ⚙️ Installation

```bash
git clone https://github.com/yourusername/Rush-Hour-Puzzle.git
cd Rush-Hour-Puzzle
pip install pygame
python gui.py
```

---

## 🧩 Example of a CSV File

```csv
6,6
X,1,2,H,2
A,0,0,V,3
B,3,0,H,2
C,2,3,V,3
#,4,5
```

**Format:**
```
ID, x, y, orientation(H/V), length
# = wall or blocked cell
```

---

## 📊 Results & Observations

- BFS always finds the optimal path but explores many states.  
- A\* significantly reduces search time using heuristics.  
- h3 performs best among the heuristics.  
- The GUI makes it easy to visualize how each algorithm behaves differently.

---

## 👨‍💻 Technologies Used

- **Python 3**
- **Pygame**
- **CSV**
- **A\* & BFS Search**

---

## ✨ Author

**Abderrahmane Ferhat**  
📧 abderrahmaneferhat93@gmail.com  
🧠 Final-year computer science student passionate about AI & algorithms.
