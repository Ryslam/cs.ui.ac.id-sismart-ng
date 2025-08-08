import sys
from sympy import isprime, nextprime

class DoubleHashTable:
    def __init__(self, warehouse_id: int, initial_capacity: int):
        self.warehouse_id: int = warehouse_id


def main():
    M = int(input())
    if not isprime(M): # Kalo M tidak prime
        M = nextprime(M)

    # TODO: Inisialisasi DoubleHashTable

    V, E = map(int, input().split())

    # TODO: Inisialisasi Graph
    for warehouse_id in range (1, V + 1):
        input_line = input().split()
        N = input_line[0]

        for info_barang_input in range(1, N):
            index_id = 
            index_kuantitas = 
            index_harga = 
            print(f"ID: {input_line[info_barang_input]}")
            print(f"Kuantitas: {input_line[info_barang_input]}")
            print(f": {input_line[info_barang_input]}")


if __name__ == "__main__":
    main()
