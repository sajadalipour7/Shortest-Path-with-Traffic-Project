import math
import matplotlib.pyplot as plt


class Node:
    """
    This is a class for vertex and it's details
    """

    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.adjacency_list = {}
        self.length_list = {}
        self.prev = None
        self.dist = math.inf
        self.is_explored = False

    def add_neighbour(self, neighbour, length, traffic):
        self.adjacency_list[neighbour] = length * (1 + 0.3 * traffic)
        self.length_list[neighbour] = length

    def get_neighbours(self):
        return self.adjacency_list


class MinHeap:
    """
    This is a min heap to store distances in it .
    """

    def __init__(self):
        self.heap = [0] * 1000000
        self.size = 0
        self.index_hash_table = {}

    def get_min(self):
        return self.heap[0]

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def parent(self, i):
        return (i - 1) // 2

    def swap(self, a, b):
        self.index_hash_table[self.heap[a]] = b
        self.index_hash_table[self.heap[b]] = a
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def insert(self, x):
        self.size += 1
        self.heap[self.size - 1] = x
        self.index_hash_table[x] = self.size - 1
        i = self.size - 1
        while i != 0 and self.heap[self.parent(i)].dist > self.heap[i].dist:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def decrease_key(self, index, new_val):
        tmp_node = Node(0, 0, 0)
        tmp_node.dist = new_val
        self.heap[index] = tmp_node
        while index != 0 and self.heap[self.parent(index)].dist > self.heap[index].dist:
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def heapify(self, i):
        left = self.left(i)
        right = self.right(i)
        ans = i
        if left < self.size and self.heap[left].dist < self.heap[i].dist:
            ans = left
        if right < self.size and self.heap[right].dist < self.heap[ans].dist:
            ans = right
        if ans != i:
            self.swap(i, ans)
            self.heapify(ans)

    def extract_min(self):
        if self.size == 1:
            self.size -= 1
            return self.heap[0]
        ans = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.index_hash_table[self.heap[0]] = 0
        self.size -= 1
        self.heapify(0)
        return ans

    def remove(self, index):
        self.decrease_key(index, -math.inf)
        self.extract_min()

    def show_details(self):
        for i in range(0, self.size):
            print("(", self.heap[i].id, ",", self.heap[i].dist, ")", end=" ")
        print()
        for i, j in self.index_hash_table.items():
            print("(", i.id, ",", j, ")", end=" ")
        print()
        print("------------------------------------------")


def all_visited(arr):
    """
    This is a function to check if all vertices are explored
    """
    for dummy, node in arr.items():
        if node.is_explored == False:
            return False
    return True


def dijkstra(vertices, start):
    """
    This is a function to perform Dijkstra algorithm on a graph
    """
    heap = MinHeap()
    for dummy, node in vertices.items():
        heap.insert(node)
    start.dist = 0
    heap.remove(heap.index_hash_table[start])
    heap.insert(start)
    while not all_visited(vertices):
        current_vertex = heap.extract_min()
        current_vertex.is_explored = True

        # update estimates
        for neighbour, weight in current_vertex.get_neighbours().items():
            if neighbour.is_explored == False:
                if current_vertex.dist + weight < neighbour.dist:
                    neighbour.dist = current_vertex.dist + weight
                    neighbour.prev = current_vertex
                    heap.remove(heap.index_hash_table[neighbour])
                    heap.insert(neighbour)


# Start
# Getting Inputs
vertices = {}
file_input = open("Maps/1/m1.txt", "r")
first_line = list(map(int, (file_input.readline()).split()))
number_of_vertices = first_line[0]
number_of_edges = first_line[1]
edges = []
for i in range(number_of_vertices):
    str_line = list(map(float, (file_input.readline()).split()))
    id = int(str_line[0])
    latitude = str_line[1]
    longitude = str_line[2]
    vertices[id] = Node(id, latitude, longitude)
for i in range(number_of_edges):
    str_line = list(map(int, (file_input.readline()).split()))
    first_vertex = vertices[str_line[0]]
    second_vertex = vertices[str_line[1]]
    edges.append((first_vertex, second_vertex))
    length = math.sqrt(
        (first_vertex.latitude - second_vertex.latitude) ** 2 + (first_vertex.longitude - second_vertex.longitude) ** 2)
    first_vertex.add_neighbour(second_vertex, length, 0)
    second_vertex.add_neighbour(first_vertex, length, 0)


def calculate_and_perform_traffic_from_point_a_and_b(vertices, start, destination, time):
    """
    This is a function to calculate the time and perform traffic
    """
    time_ans = 0
    path = []
    current = vertices[destination]
    while current.id != start:
        path.append(current.id)
        time_ans += current.adjacency_list[current.prev]
        current.adjacency_list[current.prev] += current.length_list[current.prev] * 0.3 * 1
        current.prev.adjacency_list[current] += current.prev.length_list[current] * 0.3 * 1
        current = current.prev
    path.append(current.id)
    path.reverse()
    return (time + time_ans * 120, path)


def reset_vertices(vertices):
    """
    This is a function to reset vertices to get them ready for dijkstra algorithm
    """
    for id, vertex in vertices.items():
        vertices[id].dist = math.inf
        vertices[id].is_explored = False
        vertices[id].prev = None


def check_if_traffic_will_be_finish_in_any_path(vertices, paths, req_time):
    """
    This is a function to check if traffic will be finish for the paths
    """
    for path in paths:
        time_path = path[0]
        the_path = path[1]
        if req_time - time_path >= 0:
            for i in range(0, len(the_path) - 1):
                first = vertices[the_path[i]]
                second = vertices[the_path[i + 1]]
                if first.adjacency_list[second] > first.length_list[second]:
                    first.adjacency_list[second] -= first.length_list[second] * 0.3 * 1
                    second.adjacency_list[first] -= second.length_list[first] * 0.3 * 1


def show_path(vertices, edges, path, t):
    """
    This is a function to show the results graphically with matplotlib library
    """
    for i, j in edges:
        x = [i.longitude, j.longitude]
        y = [i.latitude, j.latitude]
        names = [i.id, j.id]
        plt.plot(x, y, '-o', color='r')
        for ii, txt in enumerate(names):
            plt.annotate(txt, (x[ii], y[ii]))

    for i in range(len(path) - 1):
        v1 = vertices[path[i]]
        v2 = vertices[path[i + 1]]
        x = [v1.longitude, v2.longitude]
        y = [v1.latitude, v2.latitude]
        plt.plot(x, y, '-o', color='b')
    plt.title(t)
    plt.show()

# Getting sources and destinations
paths = []
dummy_first_time = True
while True:
    command = input()
    commands = list(map(float, command.split()))
    req_time = commands[0]
    start = int(commands[1])
    destination = int(commands[2])
    if dummy_first_time:
        dummy_first_time = False
        dijkstra(vertices, vertices[start])
        details = calculate_and_perform_traffic_from_point_a_and_b(vertices, start, destination, req_time)
        paths.append(details)
        print("The best path is : ", details[1])
        print("Estimated time to arrive : ", details[0] - req_time, " minutes")
        show_path(vertices, edges, details[1], str(details[0] - req_time) + " minutes")
        reset_vertices(vertices)
    else:
        check_if_traffic_will_be_finish_in_any_path(vertices, paths, req_time)
        dijkstra(vertices, vertices[start])
        details = calculate_and_perform_traffic_from_point_a_and_b(vertices, start, destination, req_time)
        paths.append(details)
        print("The best path is : ", details[1])
        print("Estimated time to arrive : ", details[0] - req_time, " minutes")
        show_path(vertices, edges, details[1], str(details[0] - req_time) + " minutes")
        reset_vertices(vertices)
