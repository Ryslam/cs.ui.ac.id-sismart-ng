import heapq
from dataclasses import dataclass

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_next_prime(n):
    if is_prime(n):
        return n
    num = n + 1
    while True:
        if is_prime(num):
            return num
        num += 1

def merge_sort(arr, key, reverse=False, tie_breaker_key=None):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid], key, reverse, tie_breaker_key)
    right_half = merge_sort(arr[mid:], key, reverse, tie_breaker_key)

    return merge(left_half, right_half, key, reverse, tie_breaker_key)

def merge(left, right, key, reverse, tie_breaker_key):
    sorted_list = []
    i = j = 0
    while i < len(left) and j < len(right):
        left_val = key(left[i])
        right_val = key(right[j])

        should_move_left = False
        if left_val == right_val:
            if tie_breaker_key:
                left_tie = tie_breaker_key(left[i])
                right_tie = tie_breaker_key(right[j])
                if reverse:  # Descending main sort (S H), ascending tie-break
                    should_move_left = left_tie < right_tie
                else:  # Ascending main sort (S L), descending tie-break
                    should_move_left = left_tie > right_tie
            else:
                should_move_left = True # stable sort behavior
        elif reverse:
            should_move_left = left_val > right_val
        else:
            should_move_left = left_val < right_val

        if should_move_left:
            sorted_list.append(left[i])
            i += 1
        else:
            sorted_list.append(right[j])
            j += 1
            
    sorted_list.extend(left[i:])
    sorted_list.extend(right[j:])
    return sorted_list

@dataclass
class Barang:
    id: str
    kuantitas: int
    harga: int

class DoubleHashTable:
    _DELETED = object()

    def __init__(self, capacity, warehouse_id):
        self.warehouse_id = str(warehouse_id)
        self.capacity = get_next_prime(capacity)
        self.slots = [None] * self.capacity
        self.active_count = 0
        self.size = 0 # active_count + tombstones
        self.total_value = 0
    
    def _get_raw_key(self, id_barang):
        return self.warehouse_id + str(id_barang)

    def _string_to_int(self, key: str) -> int:
        return sum(ord(char) for char in key)

    def _h1(self, key_int: int) -> int:
        return 1 + (key_int % (self.capacity - 1)) if self.capacity > 1 else 1

    def _h2(self, key_int: int) -> int:
        res = 7 - (key_int % 7)
        return res if res != 0 else 1

    def _probe_indices(self, key_str: str):
        key_int = self._string_to_int(key_str)
        h1 = self._h1(key_int)
        h2 = self._h2(key_int)
        for i in range(self.capacity):
            yield (h1 + i * h2) % self.capacity

    def _find_index(self, id_barang: str):
        raw_key = self._get_raw_key(id_barang)
        for idx in self._probe_indices(raw_key):
            slot = self.slots[idx]
            if slot is None:
                return None
            if slot is self._DELETED:
                continue
            if isinstance(slot, Barang) and slot.id == id_barang:
                return idx
        return None
    
    def _resize(self):
        old_slots = [slot for slot in self.slots if isinstance(slot, Barang)]
        new_capacity = get_next_prime(self.capacity * 2)
        
        self.capacity = new_capacity
        self.slots = [None] * self.capacity
        self.active_count = 0
        self.size = 0
        self.total_value = 0
        
        for barang in old_slots:
            self.add_barang(barang)

    def add_barang(self, barang: Barang):
        if (self.size + 1) / self.capacity > 0.8:
            self._resize()

        raw_key = self._get_raw_key(barang.id)
        
        insertion_idx = -1
        
        # Probe the table
        for idx in self._probe_indices(raw_key):
            slot = self.slots[idx]

            # Check for active duplicate
            if isinstance(slot, Barang) and slot.id == barang.id:
                return -1 # Item already exists and is active.

            # Find the first available insertion spot (tombstone or empty)
            if (slot is None or slot is self._DELETED) and insertion_idx == -1:
                insertion_idx = idx

            # If we hit an empty slot, the probe chain ends.
            # We can be sure no active duplicate exists.
            if slot is None:
                break

        # If after probing, we haven't found an insertion spot, the table is full.
        if insertion_idx == -1:
            return -1

        # Perform the insertion
        if self.slots[insertion_idx] is None:
            self.size += 1 # A truly empty slot is being filled.
        
        self.slots[insertion_idx] = barang
        self.active_count += 1
        self.total_value += barang.kuantitas * barang.harga
        return insertion_idx
    
    def update_harga(self, id_barang, harga_baru):
        idx = self._find_index(id_barang)
        if idx is None:
            return -1
        
        slot = self.slots[idx]
        old_total_item_value = slot.kuantitas * slot.harga
        slot.harga = harga_baru
        new_total_item_value = slot.kuantitas * slot.harga
        
        self.total_value = self.total_value - old_total_item_value + new_total_item_value
        return new_total_item_value

    def audit(self, stok_minimal):
        if self.active_count == 0:
            return -1
        
        deleted_count = 0
        for i, slot in enumerate(self.slots):
            if isinstance(slot, Barang) and slot.kuantitas < stok_minimal:
                self.total_value -= slot.kuantitas * slot.harga
                self.slots[i] = self._DELETED
                self.active_count -= 1
                deleted_count += 1
        return deleted_count
    
class Graph:
    def __init__(self, num_vertices):
        self.v = num_vertices
        self.adj = {i: {} for i in range(1, num_vertices + 1)}
        self.vertices = set(range(1, num_vertices + 1))

    def add_edge(self, u, v, weight):
        if u not in self.vertices or v not in self.vertices:
            return -1
        if v in self.adj[u]:
            return -1
        self.adj[u][v] = weight
        self.adj[v][u] = weight
        return len(self.adj[u])

    def remove_edge(self, u, v):
        if u not in self.vertices or v not in self.vertices:
            return -1
        if v not in self.adj[u]:
            return -1
        del self.adj[u][v]
        del self.adj[v][u]
        return len(self.adj[u])
    
    def dijkstra(self, start_node):
        if start_node not in self.vertices:
            return {node: float('inf') for node in self.vertices}
            
        distances = {node: float('inf') for node in self.vertices}
        distances[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.adj[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        return distances

    def prim_mst(self, start_node):
        if start_node not in self.vertices or not self.adj[start_node]:
            return -1

        q = [start_node]
        visited_component = {start_node}
        head = 0
        while head < len(q):
            u = q[head]
            head += 1
            for v_neighbor in self.adj[u]:
                if v_neighbor not in visited_component:
                    visited_component.add(v_neighbor)
                    q.append(v_neighbor)
        
        mst_cost = 0
        pq = [(0, start_node)]
        visited_prim = set()
        
        while pq and len(visited_prim) < len(visited_component):
            weight, u = heapq.heappop(pq)

            if u in visited_prim:
                continue
                
            visited_prim.add(u)
            mst_cost += weight
            
            for v, w in self.adj[u].items():
                if v in visited_component and v not in visited_prim:
                    heapq.heappush(pq, (w, v))

        return mst_cost

def main():
    M = int(input())
    V, E = map(int, input().split())

    warehouses = {i: DoubleHashTable(M, i) for i in range(1, V + 1)}
    graph = Graph(V)

    for i in range(1, V + 1):
        line = input().split()
        if not line: continue
        num_items = int(line[0])
        if num_items > 0:
            items_data = line[1:]
            for j in range(0, len(items_data), 3):
                id_barang = items_data[j]
                kuantitas = int(items_data[j+1])
                harga = int(items_data[j+2])
                barang = Barang(id=id_barang, kuantitas=kuantitas, harga=harga)
                warehouses[i].add_barang(barang)

    for _ in range(E):
        u, v, w = map(int, input().split())
        graph.add_edge(u, v, w)

    sofita_at = int(input())
    

    Q = int(input())
    for _ in range(Q):
        query = input().split()
        cmd = query[0]
        args = query[1:]
        
        if cmd == "M":
            dest = int(args[0])
            if dest not in graph.vertices:
                print(-1)
                continue

            if dest == sofita_at:
                print(0)
                continue

            distances = graph.dijkstra(sofita_at)
            cost = distances.get(dest, float('inf'))
            
            if cost == float('inf'):
                print(-1)
            else:
                sofita_at = dest
                print(cost)

        elif cmd == "O":
            start_node = int(args[0])
            print(graph.prim_mst(start_node))

        elif cmd == "A":
            u, v, w = map(int, args)
            print(graph.add_edge(u, v, w))

        elif cmd == "D":
            u, v = map(int, args)
            print(graph.remove_edge(u, v))
            
        elif cmd == "S":
            order = args[0]
            if len(warehouses) < 2:
                print(-1)
                continue

            wh_list = list(warehouses.values())
            
            sorted_warehouses = merge_sort(
                wh_list, 
                key=lambda wh: wh.total_value, 
                reverse=(order == 'H'),
                tie_breaker_key=lambda wh: int(wh.warehouse_id)
            )

            sofita_at = int(sorted_warehouses[0].warehouse_id)
            
            top_warehouses = [wh.warehouse_id for wh in sorted_warehouses[:3]]
            print(" ".join(top_warehouses))

        elif cmd == "T":
            id_barang, kuantitas, harga = args
            barang = Barang(id=id_barang, kuantitas=int(kuantitas), harga=int(harga))
            print(warehouses[sofita_at].add_barang(barang))

        elif cmd == "U":
            id_barang, harga_baru = args
            print(warehouses[sofita_at].update_harga(id_barang, int(harga_baru)))
            
        elif cmd == "B":
            stok_minimal = int(args[0])
            print(warehouses[sofita_at].audit(stok_minimal))

if __name__ == "__main__":
    main()