from collections import deque

class Puzzle:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.n = 3  # 3x3 puzzle

    def find_blank(self, state):
        """Find the position of the blank space (0)."""
        for i in range(self.n):
            for j in range(self.n):
                if state[i][j] == 0:
                    return i, j

    def get_neighbors(self, state):
        """Return all possible moves from the current state."""
        moves = []
        x, y = self.find_blank(state)
        directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

        for move, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.n and 0 <= new_y < self.n:
                new_state = [row[:] for row in state]  # Copy state
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                moves.append((new_state, move))
        return moves

    def bfs(self):
        """Solve the puzzle using BFS."""
        queue = deque([(self.initial_state, [])])
        visited = set()

        while queue:
            state, path = queue.popleft()
            if state == self.goal_state:
                return path  # Return the sequence of moves

            visited.add(tuple(map(tuple, state)))
            for new_state, move in self.get_neighbors(state):
                if tuple(map(tuple, new_state)) not in visited:
                    queue.append((new_state, path + [move]))

        return None  # No solution found

    def dfs_limited(self, state, path, depth, visited):
        """Depth-limited DFS used in IDDFS."""
        if state == self.goal_state:
            return path

        if depth == 0:
            return None

        visited.add(tuple(map(tuple, state)))
        for new_state, move in self.get_neighbors(state):
            if tuple(map(tuple, new_state)) not in visited:
                result = self.dfs_limited(new_state, path + [move], depth - 1, visited)
                if result:
                    return result
        return None

    def iddfs(self, max_depth=50):
        """Solve the puzzle using IDDFS."""
        for depth in range(max_depth):
            visited = set()
            result = self.dfs_limited(self.initial_state, [], depth, visited)
            if result:
                return result
        return None  # No solution found


# Example Usage:
initial_state = [
    [1, 2, 3],
    [4, 0, 5],  # '0' represents the empty space
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

puzzle = Puzzle(initial_state, goal_state)

print("BFS Solution:", puzzle.bfs())
print("IDDFS Solution:", puzzle.iddfs())
