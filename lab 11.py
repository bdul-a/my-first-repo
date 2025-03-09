from collections import deque # double ended queue
def breadth_first_search(graph, start_node, target_node): #start a function
    if explored is None:
         queue = deque([[start_node]]) #enter a first node in list
    while queue:# loop run till empty
        current_path = queue.popleft() #remove from left
        current_node = current_path[-1]#remove from last

        if current_node == target_node:
            return current_path #path found code end

        if current_node not in explored:
            explored.add(current_node)#add a node in start of list
            for neighbor in graph.get(current_node, []):#search in near neighbors with the help of started node
                new_path = list(current_path)#assign a new path
                new_path.append(neighbor)
                queue.append(new_path)#at the end new neighbor in queue


    return None#otherwise return none

def depth_first_search(graph, start_node, target_node):
    explored = set()
    stack = [[start_node]]

    while stack:# star=ck with LIFO
        current_path = stack.pop() #same like upper case
        current_node = current_path[-1] #empty both path(first and end)

        if current_node == target_node:
            return current_path #shortest path in case goal achieved in first line

        if current_node not in explored:
            explored.add(current_node)
            for neighbor in reversed(graph.get(current_node, [])):#reverse case because not work like queue
                new_path = list(current_path)
                new_path.append(neighbor)
                stack.append(new_path)
    return None
def main():
    road_map = {
        0: [1, 3],
        1: [7],
        2: [],
        3: [],
        4: [1, 3, 6],
        5: [0, 3],
        6: [4],
        7: [5]
    }

    city_labels = {# labels for the city names
        0: "Lahore",
        1: "Kasur",
        2: "Jazira",
        3: "Bakhar",
        4: "Okara",
        5: "Jhang",
        6: "Khosab",
        7: "Sahiwal"
    }

    start_city = input("Enter the starting location: ").strip()#strip is used to avoid extra spaces
    destination_city = input("Enter the target location: ").strip()

    start_index = next((key for key, value in city_labels.items() if value.lower() == start_city.lower()), None)
    destination_index = next((key for key, value in city_labels.items() if value.lower() == destination_city.lower()), None)#nextr return first matching key and none

    if start_index is None or destination_index is None:
        print("Error: One or both of the entered city names are invalid. Please try again.")
        return

    bfs_result = breadth_first_search(road_map, start_index, destination_index)
    dfs_result = depth_first_search(road_map, start_index, destination_index)
    #convert it into labels
    bfs_path = [city_labels[node] for node in bfs_result] if bfs_result else None
    dfs_path = [city_labels[node] for node in dfs_result] if dfs_result else None

    print("Path using BFS:", " -> ".join(bfs_path) if bfs_path else "No path found")
    print("Path using DFS:", " -> ".join(dfs_path) if dfs_path else "No path found")
if __name__ == "__main__":
    main()







