import math

index_in_heap_hashtable = {}
class MinHeap:
    def __init__(self):
        self.heap = []
        self.size = 0

    def get_min(self):
        return self.heap[0]
    def left(self,i):
        return 2*i+1
    def right(self,i):
        return 2*i+2
    def parent(self,i):
        return (i-1)//2
    def swap(self, a, b):
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]
    def insert(self,x):
        self.size+=1
        self.heap.append(x)
        i=self.size-1
        while i!=0 and self.heap[self.parent(i)]>self.heap[i]:
            self.swap(i,self.parent(i))
            i=self.parent(i)
    def decrease_key(self,index,new_val):
        self.heap[index]=new_val
        while index != 0 and self.heap[self.parent(index)] > self.heap[index]:
            self.swap(index, self.parent(index))
            index = self.parent(index)
    def heapify(self,i):
        left=self.left(i)
        right=self.right(i)
        ans=i
        if left<self.size and self.heap[left]<self.heap[i]:
            ans=left
        if right<self.size and self.heap[right]<self.heap[ans]:
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
        self.size-=1
        self.heapify(0)
        return ans
    def remove(self,index):
        self.decrease_key(index,-math.inf)
        self.extract_min()


heap=MinHeap()
heap.insert(50)
heap.insert(10)
heap.insert(7)
heap.insert(3)
heap.insert(4)
heap.insert(49)
heap.insert(20)
print(heap.heap)
heap.remove(1)
print(heap.heap)