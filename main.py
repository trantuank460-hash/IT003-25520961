import time
import sys
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""
có tham khảo từ AI các thư viện sau: 
time        : đo thời gian thực thi
sys         : thao tác hệ thống, tăng giới hạn đệ quy
random      : sinh số ngẫu nhiên
numpy       : xử lý mảng số lớn
pandas      : lưu trữ và xuất bảng CSV
matplotlib  : vẽ biểu đồ
"""
sys.setrecursionlimit(2000000) #cho phép hàm gọi lại chính nó tối đa 2 triệu tầng

# xây dựng thuật toán quick sort : Thuật toán Quick Sort hoạt động bằng cách chọn một phần tử làm pivot, chia mảng thành các phần nhỏ hơn, bằng và lớn hơn mốc, sau đó đệ quy sắp xếp các phần và ghép lại để thu được mảng đã sắp xếp.
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    moc = random.choice(arr)
    left = [x for x in arr if x < moc]
    mid = [x for x in arr if x == moc]
    right = [x for x in arr if x > moc]
    return quick_sort(left) + mid + quick_sort(right)
# xây dựng thuật toán merge sort : Dựa vào chia để trị 
def merge_sort(a):
    # Nếu mảng có hơn 1 phần tử thì mới cần sắp xếp
    if len(a) > 1:
        # Chia mảng làm 2 nửa
        m = len(a) // 2
        L = a[:m]      # nửa trái
        R = a[m:]      # nửa phải

        # Đệ quy sắp xếp từng nửa
        merge_sort(L)
        merge_sort(R)

        # i: duyệt L, j: duyệt R, k: vị trí ghi vào mảng a
        i = j = k = 0

        # Trộn 2 mảng L và R đã được sắp xếp
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                a[k] = L[i]
                i += 1
            else:
                a[k] = R[j]
                j += 1
            k += 1

        # Nếu L còn phần tử thì copy nốt
        while i < len(L):
            a[k] = L[i]
            i += 1
            k += 1

        # Nếu R còn phần tử thì copy nốt
        while j < len(R):
            a[k] = R[j]
            j += 1
            k += 1

# xây dựng thuật toán heap sort: Heap Sort sắp xếp dữ liệu bằng cách xây dựng max-heap, sau đó liên tục đưa phần tử lớn nhất về cuối mảng và duy trì lại cấu trúc heap cho đến khi mảng được sắp xếp hoàn toàn.
def heap_sort(arr):
    def heapify(arr, size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2

        if left < size and arr[left] > arr[largest]:
            largest = left
        if right < size and arr[right] > arr[largest]:
            largest = right
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(arr, size, largest)

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

DATA_SIZE = 1_000_000
data_sets = {}

data_sets["1. Float Asc"] = np.sort(np.random.uniform(-1000, 1000, DATA_SIZE))
data_sets["2. Float Desc"] = np.sort(np.random.uniform(-1000, 1000, DATA_SIZE))[::-1]

for idx in range(3, 6):
    data_sets[f"{idx}. Float Rand"] = np.random.uniform(-1000, 1000, DATA_SIZE)

for idx in range(6, 11):
    data_sets[f"{idx}. Int Rand"] = np.random.randint(-10000, 10000, DATA_SIZE)

result_table = {
    "Dữ liệu": [],
    "QuickSort": [],
    "HeapSort": [],
    "MergeSort": [],
    "sort (C++)": [],
    "sort (numpy)": []
}

TEST_SIZE = 10000

for data_name, data_array in data_sets.items():
    sample_data = data_array[:TEST_SIZE]
    row_data = {"Dữ liệu": data_name}

    algo_list = [
        ("QuickSort", quick_sort),
        ("HeapSort", heap_sort),
        ("MergeSort", merge_sort),
        ("sort (C++)", sorted),
        ("sort (numpy)", np.sort)
    ]

    for algo_label, algo_func in algo_list:
        work_arr = np.array(sample_data) if algo_label == "sort (numpy)" else list(sample_data)

        start_time = time.time()
        if algo_label == "HeapSort":
            algo_func(work_arr)
        else:
            _ = algo_func(work_arr)
        end_time = time.time()

        row_data[algo_label] = round((end_time - start_time) * 1000, 2)

    for col in result_table:
        if col != "Dữ liệu":
            result_table[col].append(row_data[col])
    result_table["Dữ liệu"].append(data_name)

df = pd.DataFrame(result_table)

print("\n===== BẢNG KẾT QUẢ =====\n")
print(df)

print("\n===== CSV OUTPUT =====\n")
print(df.to_csv(index=False))

df.to_csv("ket_qua.csv", index=False)

plt.style.use("ggplot")
df.set_index("Dữ liệu").plot(kind="bar", figsize=(12, 6))

plt.title("So sánh thời gian thực hiện các thuật toán sắp xếp")
plt.ylabel("Thời gian (ms)")
plt.xlabel("Bảng thống kê")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("thongke.png")
plt.show()
