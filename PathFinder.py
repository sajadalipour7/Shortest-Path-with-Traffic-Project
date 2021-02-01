import math

class Node:
    def __init__(self, id, latitude, longitude):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.adjacency_list = {}
        self.prev=None
        self.dist=math.inf
        self.is_explored=False

    def add_neighbour(self, neighbour, length,traffic):
        self.adjacency_list[neighbour] = length*(1+0.3*traffic)

    def get_neighbours(self):
        return self.adjacency_list

class MinHeap:
    def __init__(self):
        self.heap = [0]*1000
        self.size = 0
        self.index_hash_table={}

    def get_min(self):
        return self.heap[0]
    def left(self,i):
        return 2*i+1
    def right(self,i):
        return 2*i+2
    def parent(self,i):
        return (i-1)//2
    def swap(self, a, b):
        self.index_hash_table[self.heap[a]]=b
        self.index_hash_table[self.heap[b]]=a
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]
    def insert(self,x):
        self.size+=1
        self.heap[self.size-1]=x
        self.index_hash_table[x]=self.size-1
        i=self.size-1
        while i!=0 and self.heap[self.parent(i)].dist>self.heap[i].dist:
            self.swap(i,self.parent(i))
            i=self.parent(i)
    def decrease_key(self,index,new_val):
        tmp_node=Node(0,0,0)
        tmp_node.dist=new_val
        self.heap[index]=tmp_node
        while index != 0 and self.heap[self.parent(index)].dist > self.heap[index].dist:
            self.swap(index, self.parent(index))
            index = self.parent(index)
    def heapify(self,i):
        left=self.left(i)
        right=self.right(i)
        ans=i
        if left<self.size and self.heap[left].dist<self.heap[i].dist:
            ans=left
        if right<self.size and self.heap[right].dist<self.heap[ans].dist:
            ans=right
        if ans!=i:
            self.swap(i,ans)
            self.heapify(ans)
    def extract_min(self):
        if self.size==1:
            self.size-=1
            return self.heap[0]
        ans=self.heap[0]
        self.heap[0]=self.heap[self.size-1]
        self.index_hash_table[self.heap[0]]=0
        self.size-=1
        self.heapify(0)
        return ans
    def remove(self,index):
        self.decrease_key(index,-math.inf)
        self.extract_min()

    def show_details(self):
        for i in range(0,self.size):
            print("(",self.heap[i].id,",",self.heap[i].dist,")",end=" ")
        print()
        for i,j in self.index_hash_table.items():
            print("(",i.id,",",j,")",end=" ")
        print()
        print("------------------------------------------")

def all_visited(arr):
    for dummy,node in arr.items():
        if node.is_explored==False:
            return False
    return True
def dijkstra(vertices,start):
    heap=MinHeap()
    for dummy,node in vertices.items():
        heap.insert(node)
    start.dist=0
    # heap.show_details()
    heap.remove(heap.index_hash_table[start])
    # heap.show_details()
    heap.insert(start)
    # heap.show_details()
    while not all_visited(vertices):
        current_vertex=heap.extract_min()
        current_vertex.is_explored=True

        # update estimates
        for neighbour, weight in current_vertex.get_neighbours().items():
            if neighbour.is_explored == False:
                if current_vertex.dist + weight < neighbour.dist:
                    neighbour.dist = current_vertex.dist + weight
                    neighbour.prev = current_vertex
                    heap.remove(heap.index_hash_table[neighbour])
                    heap.insert(neighbour)




# Start
vertices = {}
file_input = open("Maps/1/m1.txt", "r")
first_line = list(map(int, (file_input.readline()).split()))
number_of_vertices = first_line[0]
number_of_edges = first_line[1]
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
    length = math.sqrt(
        (first_vertex.latitude - second_vertex.latitude) ** 2 + (first_vertex.longitude - second_vertex.longitude) ** 2)
    first_vertex.add_neighbour(second_vertex, length,0)
    second_vertex.add_neighbour(first_vertex, length,0)




# heap=MinHeap()
# heap.insert(50)
# heap.insert(10)
# heap.insert(7)
# heap.insert(3)
# heap.insert(4)
# heap.insert(49)
# heap.insert(20)
# print(heap.heap)