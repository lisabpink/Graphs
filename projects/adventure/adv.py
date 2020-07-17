from room import Room
from player import Player
from world import World
from utils import Queue, Stack

import random
from ast import literal_eval

import time
import sys

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
my_graph = {
    0: {'n': '?', 's': '?', 'e': '?', 'w': '?'}
}

backpath = []


# ATTEMPT 2
def get_opp(direction):
    if direction == 'n':
        return 's'
    if direction == 'e':
        return 'w'
    if direction == 's':
        return 'n'
    if direction == 'w':
        return 'e'


def log_path(direction, prev_room, prev_exits):
    # if room already in own graph, assign exit just used, leave everything else alone
    if player.current_room.id in my_graph:
        for x in player.current_room.get_exits():
            if get_opp(direction) == x:
                my_graph[player.current_room.id][x] = prev_room

    # otherwise, create room, assign exit just used, fill other exits with '?'
    else:
        my_graph[player.current_room.id] = {}
        for x in player.current_room.get_exits():
            if get_opp(direction) == x:
                my_graph[player.current_room.id][x] = prev_room
            else:
                my_graph[player.current_room.id][x] = '?'

    # assign exit just used to previous room
    for x in prev_exits:
        if x == direction:
            my_graph[prev_room][x] = player.current_room.id


def get_unexplored(unexplored):
    # if any exits in current room == '?', add to unexplored list
    for x in player.current_room.get_exits():
        if my_graph[player.current_room.id][x] == '?':
            unexplored.append(x)


def travel(direction):
    player.travel(direction)
    traversal_path.append(direction)


def dft():

    while len(my_graph) < len(room_graph):
        prev_room = player.current_room.id
        prev_exits = player.current_room.get_exits()
        # loop through current room exits, if exit == '?', then add to unexplored list
        unexplored = []
        get_unexplored(unexplored)

        # choose random direction from unexplored
        if len(unexplored) > 0:
            direction = random.choice(unexplored)
            travel(direction)
            backpath.append(get_opp(direction))
        else:
            # if dead-end reached
            while len(unexplored) == 0:
                direction = backpath.pop()
                travel(direction)
                get_unexplored(unexplored)

        # after traveling, log
        log_path(direction, prev_room, prev_exits)


start = time.time()
dft()
end = time.time()
print("my_graph = ", my_graph)
print("traversal_path = ", traversal_path)
print("len(my_graph) = ", len(my_graph))
print("len(room_graph) = ", len(room_graph))
print("length of traversal path (number of steps): ", len(traversal_path))
print("Time: ", end - start)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisitned rooms")


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
