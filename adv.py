from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)

traversal_path = []


# move player helper function
def move_player(direction):
    player.travel(direction)
    traversal_path.append(direction)

# * Recursive DFT


def find_path_rec(visited=None, previous=None, move=None):
    # visited dict starts as none, previous room starts as none, move input starts as none
    curr_id = player.current_room.id
    connected_rooms = player.current_room.get_exits()
    # * enable easily determining what room the player came from -- previous room is the room opposite Move
    reverse_dirs = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e'
    }

    # * instantiates visited set at first
    if visited == None:
        visited = {}

    # * create empty set in visited when curr_id not in visited
    if curr_id not in visited:
        visited[curr_id] = {}

    # * handles movement command -- if the function recieves a move, the curr_id is assigned to the move applied to the previous room
    if move is not None:
        visited[previous][move] = curr_id

    # * the previous room is the room at the opposite-provided direction
    # ! handle after checking move
    if previous is not None:
        visited[curr_id][reverse_dirs[move]] = previous

    # * determines if there are remaining neighbors to be visited and recursively visits
    if len(visited[curr_id]) < len(connected_rooms):
        for direction in connected_rooms:
            if direction not in visited[curr_id]:
                move_player(direction)
                find_path_rec(visited, previous=curr_id, move=direction)

    # * If the player has visited fewer than total rooms move the player backwards
    if len(visited) < len(room_graph):
        move_player(reverse_dirs[move])


# ! executes recursive function to determine path
find_path_rec()

visited_rooms = set()
player.current_room = world.starting_room


# * Allows player to be controlled by dft function
# Moves player according to traversal_path
for direction in traversal_path:
    player.travel(direction)
    current_room = player.current_room
    visited_rooms.add(current_room)

print('traversal_path: ', traversal_path)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
