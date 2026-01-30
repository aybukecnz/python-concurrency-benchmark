import threading
import time

lock = threading.Lock()

def pack_subset(books_subset, boxes):
    for weight in books_subset:
        with lock:
            for box in boxes:
                if box["used"] + weight <= box["capacity"]:
                    box["used"] += weight
                    break

def pack_books_multi(num_threads, books, boxes):
    start = time.perf_counter()
    total_book_weight = sum(books)
    total_capacity = sum(b["capacity"] for b in boxes)

    # Kitapları thread'lere böl
    chunk_size = len(books) // num_threads
    threads = []

    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = len(books) if i == num_threads - 1 else (i + 1) * chunk_size
        t = threading.Thread(target=pack_subset, args=(books[start_idx:end_idx], boxes))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    boxes_used = sum(1 for b in boxes if b["used"] > 0)
    wasted = total_capacity - total_book_weight
    efficiency = (total_book_weight / total_capacity) * 100
    end = time.perf_counter()
    exec_time = end - start

    print("\n=== Multi-threaded Results ===")
    print(f"Total book weight: {total_book_weight} grams")
    print(f"Total storage: {total_capacity} grams")
    print(f"Boxes used: {boxes_used}")
    print(f"Wasted capacity: {wasted} grams")
    print(f"Efficiency: {efficiency:.2f}%")
    print(f"Execution time: {exec_time:.6f} seconds")

    return exec_time, efficiency
