import heapq
import time
import itertools

class PuzzleNode:
    def __init__(self, state, parent, move, g_cost, h_cost):
        """Initialize the puzzle node"""
        self.state = state
        self.parent = parent
        self.move = move
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost

    def generate_children(self):
        """Generate new states by moving the empty tile"""
        children = []
        x, y = [(i, row.index(0)) for i, row in enumerate(self.state) if 0 in row][0]  # Find empty tile position
        moves = {"up": (x - 1, y), "down": (x + 1, y), "left": (x, y - 1), "right": (x, y + 1)}

        for move, (new_x, new_y) in moves.items():
            if 0 <= new_x < 3 and 0 <= new_y < 3:  # Ensure move is within bounds
                new_state = [row[:] for row in self.state]
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                child_node = PuzzleNode(new_state, self, move, self.g_cost + 1, 0)
                children.append(child_node)

        return children

    @staticmethod
    def calculate_heuristic(state, goal_state, heuristic_type="manhattan"):
        """Calculate Manhattan Distance or Misplaced Tiles heuristic"""
        if heuristic_type == "manhattan":
            return sum(abs(x - gx) + abs(y - gy)
                       for num in range(1, 9)
                       for x, row in enumerate(state) for y, val in enumerate(row) if val == num
                       for gx, grow in enumerate(goal_state) for gy, gval in enumerate(grow) if gval == num)

        elif heuristic_type == "misplaced_tiles":
            return sum(1 for x, row in enumerate(state) for y, val in enumerate(row)
                       if val != 0 and val != goal_state[x][y])
        return 0

    def __lt__(self, other):
        """Ensures nodes are compared by f_cost in heapq"""
        return self.f_cost < other.f_cost


class PuzzleSolver:
    def __init__(self, start_state, goal_state):
        """Initialize with start and goal state"""
        self.start_state = start_state
        self.goal_state = goal_state

    def is_solvable(self, state):
        """Count inversions in the 1D representation of the puzzle.
           If inversions are even, the puzzle is solvable.
           Otherwise, the puzzle is unsolvable.
        """
        flattened = list(itertools.chain(*state))
        flattened.remove(0)  # Remove the empty tile (0)
        inversions = sum(1 for i in range(len(flattened)) for j in range(i + 1, len(flattened)) if flattened[i] > flattened[j])
        return inversions % 2 == 0

    def astar_search(self, heuristic_type="manhattan"):
        """Implement A* algorithm"""
        open_list = []
        closed_set = set()
        start_node = PuzzleNode(self.start_state, None, None, 0,
                                PuzzleNode.calculate_heuristic(self.start_state, self.goal_state, heuristic_type))
        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            if current_node.state == self.goal_state:
                return current_node  # Goal reached

            closed_set.add(tuple(map(tuple, current_node.state)))

            for child in current_node.generate_children():
                if tuple(map(tuple, child.state)) in closed_set:
                    continue

                child.h_cost = PuzzleNode.calculate_heuristic(child.state, self.goal_state, heuristic_type)
                child.f_cost = child.g_cost + child.h_cost
                heapq.heappush(open_list, child)

        return None  # No solution found

    def trace_solution(self, node):
        """Trace back the solution path"""
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()

        for step, state in enumerate(path):
            print(f"Step {step}:")
            for row in state:
                print(row)
            print()


# Sample initial and goal states
initial_state = [
    [1, 2, 3],
    [4, 0, 6],  # '0' represents the empty tile
    [7, 5, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Create PuzzleSolver object
solver = PuzzleSolver(initial_state, goal_state)

# Check if the puzzle is solvable
if solver.is_solvable(initial_state):
    print("The puzzle is solvable. Proceeding with A* Search...\n")

    # Run A* Search with Manhattan Distance heuristic
    print("Running A* Search (Manhattan Distance)...")
    start_time = time.time()
    astar_solution_manhattan = solver.astar_search(heuristic_type="manhattan")
    end_time = time.time()

    if astar_solution_manhattan:
        print("\nSolution (Manhattan Distance):")
        solver.trace_solution(astar_solution_manhattan)
        print(f"Execution Time: {end_time - start_time:.5f} seconds\n")

    # Run A* Search with Misplaced Tiles heuristic
    print("Running A* Search (Misplaced Tiles)...")
    start_time = time.time()
    astar_solution_misplaced = solver.astar_search(heuristic_type="misplaced_tiles")
    end_time = time.time()

    if astar_solution_misplaced:
        print("\nSolution (Misplaced Tiles):")
        solver.trace_solution(astar_solution_misplaced)
        print(f"Execution Time: {end_time - start_time:.5f} seconds\n")

else:
    print("The puzzle is NOT solvable.")
