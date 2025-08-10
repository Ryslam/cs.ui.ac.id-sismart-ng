import sys
from sympy import isprime, nextprime
from dataclasses import dataclass

@dataclass
class Barang:
    id: str
    kuantitas: int
    harga: int

class DoubleHashTable:
    def __init__(self, initial_capacity):
        self.initial_capacity = initial_capacity

    def _hash_1():
        pass
    
    def _hash_2():
        pass

@dataclass
class gudang:
    id: int
    double_hash_table: DoubleHashTable

def process_query(query):
    match (query[0]):
        case "M":
            pass
        case "O":
            pass
        case "A":
            pass
        case "D":
            pass
        case "S":
            pass
        case "T":
            pass
        case "U":
            pass
        case "B":
            pass

def main():
    M = int(input()) # Ukuran awal dari hash table
    if not isprime(M): # Kalo M tidak prime
        M = nextprime(M)

    # TODO: Inisialisasi DoubleHashTable

    V, E = map(int, input().split()) # V  = jumlah vertex/node/gudang, E = jumlah edge/rute

    # TODO: Inisialisasi Graph

    for warehouse_id in range (1, V + 1): # Input barang masing-masing gudang
        input_line = input().split()
        if input_line[0] == "0":
            continue

        i = 1
        while i < len(input_line): # Add setiap barang
            barang = Barang(id = input_line[i], kuantitas = input_line[i + 1], harga = input_line[i + 2])

            # TODO: Tambahkan barang ke DoubleHashTable // add

            i += 3
    
    for edge in range(1, E + 1): # Input rute-rute antar gudang
        pass
        # TODO: Tambahkan edge ke Graph

    S = int(input()) # Gudang posisi awal keberadaan Sofita

    Q = int(input()) # Jumlah query yang akan dilakukan oleh Sofita/user

    for query in range(1, Q + 1): # Input query yang akan dilakukan oleh Sofita/user
        process_query(query)

if __name__ == "__main__":
    main()
