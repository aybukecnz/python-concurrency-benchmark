import random
import time

def generate_books_and_boxes(num_books, num_boxes):
    books = [random.randint(100, 1000) for _ in range(num_books)]
    boxes = [{"capacity": random.randint(2000, 5000), "used": 0} for _ in range(num_boxes)]
    return books, boxes

def pack_books_single(books, boxes):
    start = time.perf_counter()
    total_book_weight = sum(books)
    total_capacity = sum(b["capacity"] for b in boxes)
    boxes_used = 0

    for weight in books:
        placed = False
        for box in boxes:
            if box["used"] + weight <= box["capacity"]:
                if box["used"] == 0:
                    boxes_used += 1
                box["used"] += weight
                placed = True
                break
        if not placed:
            pass  # kitap hiçbir kutuya sığmadıysa

    wasted = total_capacity - total_book_weight
    efficiency = (total_book_weight / total_capacity) * 100
    end = time.perf_counter()
    exec_time = end - start

    print("\n=== Single-threaded Results ===")
    print(f"Total book weight: {total_book_weight} grams")
    print(f"Total storage: {total_capacity} grams")
    print(f"Boxes used: {boxes_used}")
    print(f"Wasted capacity: {wasted} grams")
    print(f"Efficiency: {efficiency:.2f}%")
    print(f"Execution time: {exec_time:.6f} seconds")

    return exec_time, efficiency
