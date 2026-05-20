import math
from typing import List, Optional
from collections import deque

# =============================================================================
# STRUKTUR DATA & MODUL 1: ADVANCED SORTER (SORTING LANJUTAN)
# =============================================================================

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class AdvancedSorter:
    def __init__(self):
        pass

    # ---- 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray) ----
    def sort_array(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1: 
            return arr
        tmp_array = [0] * len(arr)  # Alokasi tunggal di awal: O(1) memori tambahan setelah ini
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        if first >= last: 
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        # Menyalin bagian virtual sublist yang relevan ke array sementara
        for idx in range(left_start, right_end + 1):
            tmp_array[idx] = arr[idx]
            
        a = left_start      # Penanda sublist kiri
        b = mid + 1         # Penanda sublist kanan
        curr = left_start   # Penanda posisi pengisian kembali ke arr
        
        # Penggabungan secara STABLE menggunakan operator <=
        while a <= mid and b <= right_end:
            if tmp_array[a] <= tmp_array[b]:
                arr[curr] = tmp_array[a]
                a += 1
            else:
                arr[curr] = tmp_array[b]
                b += 1
            curr += 1
            
        # Menyalin sisa elemen sublist kiri jika masih ada
        while a <= mid:
            arr[curr] = tmp_array[a]
            a += 1
            curr += 1
            
        # Elemen sisa sublist kanan otomatis berada di posisi yang benar

    # ---- 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge) ----
    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
            
        # Pemisahan list menggunakan teknik Fast-Slow pointer
        right_head = self._split_linked_list(head)
        left_head = head
        
        # Rekursi untuk masing-masing bagian sublist
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)
        
        # Penggabungan kembali secara stabil tanpa node baru
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        midPoint = head
        curNode = head.next
        
        # Fast pointer (curNode) melompat 2 langkah, Slow pointer (midPoint) melompat 1 langkah
        while curNode and curNode.next:
            midPoint = midPoint.next
            curNode = curNode.next.next
            
        right_head = midPoint.next
        midPoint.next = None  # Memutus jembatan list menjadi dua sublist independen
        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)  # Dummy node statis untuk mempermudah referensi head awal
        tail = dummy
        
        # Penggabungan secara STABLE, mengutamakan listA jika nilainya sama besar
        while listA and listB:
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next
            
        # Menyambungkan sisa node yang belum habis terproses
        if listA:
            tail.next = listA
        else:
            tail.next = listB
            
        return dummy.next

    # ---- 3. QUICK SORT PARTITION & FALLBACK LIMITER ----
    def quick_sort(self, arr: List[int]) -> List[int]:
        n = len(arr)
        if n <= 1:
            return arr
        self._quick_sort_recursive(arr, 0, n - 1, 0, n)
        return arr

    def _quick_sort_recursive(self, arr, first, last, depth, n):
        if first >= last:
            return
            
        # Fallback Limiter: Menghindari skenario terburuk O(n^2) jika kedalaman > 2 * log2(n)
        if depth > 2 * math.log2(n):
            # Menggunakan virtual merge sort yang stabil dan aman dari overhead memori
            tmp_array = [0] * len(arr)
            self._rec_merge_sort(arr, first, last, tmp_array)
            return

        pivot_idx = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pivot_idx - 1, depth + 1, n)
        self._quick_sort_recursive(arr, pivot_idx + 1, last, depth + 1, n)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        mid = (first + last) // 2
        
        # Strategi Pemilihan Pivot Robust: Median-of-Three (first, mid, last)
        # Melakukan sorting kecil pada 3 elemen tersebut
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
            
        # Pindahkan median (yang berada di posisi 'mid') ke posisi 'first' sebagai pivot resmi
        arr[first], arr[mid] = arr[mid], arr[first]
        pivot = arr[first]
        
        # Logika Partisi Standar Hoare/Lomuto (In-Place)
        left = first + 1
        right = last
        
        while True:
            while left <= right and arr[left] <= pivot:
                left += 1
            while left <= right and arr[right] >= pivot:
                right -= 1
            if left <= right:
                arr[left], arr[right] = arr[right], arr[left]
                left += 1
                right -= 1
            else:
                break
                
        # Tempatkan kembali pivot ke posisi akhir semestinya
        arr[first], arr[right] = arr[right], arr[first]
        return right  # Mengembalikan indeks posisi pivot akhir


# =============================================================================
# MODUL 2: EXPRESSION-DRIVEN IN-PLACE HEAPSORT (POHON BINER & HEAP)
# =============================================================================

class ExprHeapSorter:
    def __init__(self, expr_str: str):
        # Membersihkan spasi pada ekspresi string agar parsing konsisten
        self.expr = expr_str.replace(" ", "")
        self.values = []

    # ---- 1. Expression Tree Builder & Evaluator ----
    def parse_and_evaluate(self) -> List[int]:
        tokens = deque(self.expr)
        root = self._build_tree(tokens)
        
        # List penampung hasil evaluasi urutan postorder
        evaluated_list = []
        self._eval_tree(root, evaluated_list)
        self.values = evaluated_list
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        if not tokens:
            return None
            
        token = tokens.popleft()
        
        # Jika menemukan kurung buka '(', berarti sub-ekspresi baru dimulai
        if token == '(':
            left_node = self._build_tree(tokens)    # Parsing operand/operasi kiri
            operator = tokens.popleft()            # Ambil token operator (+, -, *, /)
            right_node = self._build_tree(tokens)   # Parsing operand/operasi kanan
            
            # Buang tanda penutup kurung ')' yang bersesuaian
            if tokens and tokens[0] == ')':
                tokens.popleft()
                
            return {'val': operator, 'left': left_node, 'right': right_node}
            
        # Jika berupa angka (operand tunggal)
        elif token.isdigit():
            # Mengantisipasi jika bilangan memiliki lebih dari 1 digit
            val_accum = token
            while tokens and tokens[0].isdigit():
                val_accum += tokens.popleft()
            return {'val': int(val_accum), 'left': None, 'right': None}
            
        return None

    def _eval_tree(self, node: Optional[dict], result_list: List[int]) -> int:
        if node is None:
            return 0
            
        # Base case: jika merupakan daun (operand), langsung masukkan nilai numeriknya
        if node['left'] is None and node['right'] is None:
            val = node['val']
            result_list.append(val)
            return val
            
        # Evaluasi secara Postorder (Kiri, Kanan, Root)
        left_val = self._eval_tree(node['left'], result_list)
        right_val = self._eval_tree(node['right'], result_list)
        
        op = node['val']
        if op == '+':
            res = left_val + right_val
        elif op == '-':
            res = left_val - right_val
        elif op == '*':
            res = left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Division by zero error!")
            res = left_val // right_val  # Menggunakan pembagian bilangan bulat (integer division)
        else:
            raise ValueError(f"Token operator tidak valid: {op}")
            
        result_list.append(res)
        return res

    # ---- 2 & 3. In-Place Max-Heap Construction & Heapsort ----
    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        n = len(arr)
        if n <= 1: 
            return arr
            
        # Fase 1: Build Max-Heap secara In-Place dari bawah (bottom-up)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)
            
        # Fase 2: Ekstraksi Root (Elemen Terbesar) & Sift-Down
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]  # Menukar elemen root ke ujung belakang array
            self._sift_down(arr, end, 0)         # Memulihkan sifat heap pada porsi depan yang tersisa
            
        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            largest = idx
            
            # Membandingkan dengan anak kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left
            # Membandingkan dengan anak kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right
                
            # Jika elemen saat ini sudah yang terbesar, struktur heap telah pulih
            if largest == idx:
                break
                
            # Jika tidak, tukar nilai dan turun ke level berikutnya
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    # ---- 4. Complete Tree Validator ----
    def is_complete_tree(self, arr: List[int]) -> bool:
        n = len(arr)
        # Mengecek representasi indeks array 0..n-1
        # Dalam struktur sekuensial kontigu seperti Python List, 
        # asalkan semua elemen terisi dari indeks 0 hingga n-1, ia secara definisi 
        # tidak memiliki "lubang" kosong (no missing child intermediate nodes) di tengah.
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            
            # Validasi aturan sekuensial kontigu: jika indeks anak melebihi ukuran n, 
            # itu legal (berarti node i adalah leaf), namun tidak boleh ada anak yang valid 
            # berada melompati batasan kapasitas array.
            if left >= n and right < n:
                return False  # Tidak valid jika punya anak kanan tapi tidak punya anak kiri
        return True


# =============================================================================
# CONTOH TESTING EKSEKUSI PROGRAM
# =============================================================================
if __name__ == "__main__":
    print("--- [TESTING MODUL 1: AdvancedSorter] ---")
    sorter = AdvancedSorter()
    
    # Test Array Merge Sort
    arr_test = [38, 27, 43, 3, 9, 82, 10]
    print("Awal Array :", arr_test)
    print("Hasil Sort :", sorter.sort_array(arr_test))
    
    # Test Linked List Merge Sort
    # Membuat list: 4 -> 2 -> 1 -> 3
    head = ListNode(4, ListNode(2, ListNode(1, ListNode(3))))
    print("\nAwal Linked List: 4 -> 2 -> 1 -> 3")
    sorted_head = sorter.sort_linked_list(head)
    print("Hasil Linked List:", end=" ")
    curr = sorted_head
    while curr:
        print(curr.data, end=" -> " if curr.next else "\n")
        curr = curr.next

    print("\n--- [TESTING MODUL 2: ExprHeapSorter] ---")
    # Menggunakan contoh dari soal: ((8*5)+(9/(7-4)))
    ekspresi = "((8*5)+(9/(7-4)))"
    print("Ekspresi Arismatika:", ekspresi)
    
    heap_sorter = ExprHeapSorter(ekspresi)
    hasil_evaluasi = heap_sorter.parse_and_evaluate()
    print("Hasil Evaluasi (Postorder List Intermediet):", hasil_evaluasi)
    
    # Duplikasi data untuk pembuktian stabilitas penanganan elemen ganda
    hasil_evaluasi.extend([15, 40, 2, 7])
    print("Array Gabungan Tambahan (Sebelum Heapsort):", hasil_evaluasi)
    
    terurut = heap_sorter.heapsort_inplace(hasil_evaluasi)
    print("Array Setelah Di-Heapsort (Ascending)     :", terurut)
    print("Apakah Valid Melambangkan Complete Tree?   :", heap_sorter.is_complete_tree(terurut))