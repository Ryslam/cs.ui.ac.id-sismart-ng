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
        if input_line[0] == "0":
            continue

        i = 1
        print(f"Berikut barang yang berhasil dinput ke Warehouse ID {warehouse_id}:")
        while i < len(input_line):
            print()
            print(f"ID: {input_line[i]}")
            print(f"Kuantitas: {input_line[i + 1]}")
            print(f"Harga: {input_line[i + 2]}")
            print()
            i += 3
    print()

if __name__ == "__main__":
    main()
