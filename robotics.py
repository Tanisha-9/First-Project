import random
import matplotlib
matplotlib.use("Agg")   # IMPORTANT: disables slow GUI backend
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ------------------ GRID GRAPH ------------------

class GridGraph:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.nodes = [(i, j) for i in range(rows + 1)
                             for j in range(cols + 1)]

# ------------------ ROBOT ------------------

class Robot:
    def __init__(self, robot_id, position):
        self.robot_id = robot_id
        self.position = position
        self.rank = None

    def __repr__(self):
        return f"Robot {self.robot_id} at {self.position} (rank={self.rank})"

# ------------------ SYMMETRY CHECK ------------------

def reflect_horizontal(positions, rows):
    return {(rows - x, y) for (x, y) in positions}

def reflect_vertical(positions, cols):
    return {(x, cols - y) for (x, y) in positions}

def rotate_180(positions, rows, cols):
    return {(rows - x, cols - y) for (x, y) in positions}

def is_symmetric(positions, rows, cols):
    pos_set = set(positions)
    return (
        pos_set == reflect_horizontal(pos_set, rows)
        or pos_set == reflect_vertical(pos_set, cols)
        or pos_set == rotate_180(pos_set, rows, cols)
    )

# ------------------ ASYMMETRIC PLACEMENT ------------------

def place_robots_asymmetric(grid, num_robots):
    if num_robots > len(grid.nodes):
        raise ValueError("Too many robots for grid")

    anchor = (0, 0)

    for _ in range(500):
        remaining = list(set(grid.nodes) - {anchor})
        sampled = random.sample(remaining, num_robots - 1)
        positions = [anchor] + sampled

        if not is_symmetric(positions, grid.rows, grid.cols):
            return [Robot(i + 1, pos) for i, pos in enumerate(positions)]

    raise RuntimeError("Failed to find asymmetric placement")

# ------------------ RANK COMPUTATION ------------------

def traversal_orders(grid):
    R, C = grid.rows, grid.cols
    return [
        [(x, y) for x in range(0, R + 1) for y in range(0, C + 1)],
        [(x, y) for x in range(0, R + 1) for y in range(C, -1, -1)],
        [(x, y) for x in range(R, -1, -1) for y in range(0, C + 1)],
        [(x, y) for x in range(R, -1, -1) for y in range(C, -1, -1)]
    ]

def compute_ranks(grid, robots):
    positions = {r.position for r in robots}
    robot_map = {r.position: r for r in robots}

    best_string = ""
    best_order = None

    for order in traversal_orders(grid):
        s = ''.join('1' if n in positions else '0' for n in order)
        rs = s[::-1]

        if s > best_string:
            best_string = s
            best_order = order
        if rs > best_string:
            best_string = rs
            best_order = list(reversed(order))

    rank = 1
    for node in best_order:
        if node in robot_map:
            robot_map[node].rank = rank
            rank += 1

# ------------------ VISUALIZATION ------------------

def plot_grid(grid, robots, show_ranks=False, filename="output.png", title=""):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Grid lines
    for x in range(grid.rows + 1):
        ax.plot([0, grid.cols], [x, x], linewidth=1)
    for y in range(grid.cols + 1):
        ax.plot([y, y], [0, grid.rows], linewidth=1)

    robot_positions = {r.position: r for r in robots}

    # Squares at ALL nodes
    for (x, y) in grid.nodes:
        px = y
        py = grid.rows - x

        size = 0.28
        square = Rectangle(
            (px + 0.12, py - 0.12),
            size,
            size,
            linewidth=0.8,
            edgecolor='black',
            facecolor='white',
            zorder=2
        )
        ax.add_patch(square)

        if show_ranks and (x, y) in robot_positions:
            ax.text(
                px + 0.12 + size / 2,
                py - 0.12 + size / 2,
                str(robot_positions[(x, y)].rank),
                ha='center',
                va='center',
                fontsize=9,
                fontweight='bold',
                zorder=4
            )

    # Robots
    for r in robots:
        ax.scatter(
            r.position[1],
            grid.rows - r.position[0],
            s=350,
            edgecolors='black',
            linewidths=1.5,
            zorder=5
        )

    ax.set_xlim(-0.3, grid.cols + 0.6)
    ax.set_ylim(-0.3, grid.rows + 0.6)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

    plt.savefig(filename, dpi=200, bbox_inches="tight")
    plt.close()

# ------------------ MAIN ------------------

if __name__ == "__main__":

    rows = int(input("Enter number of rows (cells): "))
    cols = int(input("Enter number of columns (cells): "))
    num_robots = int(input("Enter number of robots: "))

    grid = GridGraph(rows, cols)
    robots = place_robots_asymmetric(grid, num_robots)

    print("\nInitial positions:")
    for r in robots:
        print(r)

    # IMAGE 1
    plot_grid(
        grid,
        robots,
        show_ranks=False,
        filename="before_ranking.png",
        title="Initial Configuration"
    )

    compute_ranks(grid, robots)

    print("\nAfter ranking:")
    for r in robots:
        print(r)

    # IMAGE 2
    plot_grid(
        grid,
        robots,
        show_ranks=True,
        filename="after_ranking.png",
        title="After Symmetry Breaking"
    )

    print("\nImages generated:")
    print(" - before_ranking.png")
    print(" - after_ranking.png")
