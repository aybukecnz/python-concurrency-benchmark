import multiprocessing
import time

def pack_subset_mp(books_subset, boxes, lock):
    """
    Worker function executed by each process.
    Attempts to pack a subset of books into the shared boxes.
    """
    for weight in books_subset:
        placed = False
        # We use a lock to ensure only one process updates the shared list at a time
        with lock:
            for i in range(len(boxes)):
                # In multiprocessing with a Manager, we must re-assign the object 
                # to the list to ensure the update propagates to shared memory.
                box = boxes[i]
                if box["used"] + weight <= box["capacity"]:
                    box["used"] += weight
                    boxes[i] = box  # Explicit update for Manager list
                    placed = True
                    break
        
        # Optional: verify placement logic or log failures here if needed
        if not placed:
            pass 

def pack_books_mp(num_processes, books, boxes_manager_list):
    """
    Orchestrates the multi-processing simulation.
    """
    start = time.perf_counter()
    
    total_book_weight = sum(books)
    # Calculate total capacity from the shared manager list
    total_capacity = sum(b["capacity"] for b in boxes_manager_list)

    # Divide books into chunks for each process
    chunk_size = len(books) // num_processes
    processes = []
    
    # Create a lock compatible with multiprocessing
    lock = multiprocessing.Lock()

    for i in range(num_processes):
        start_idx = i * chunk_size
        # Ensure the last process gets any remaining books
        end_idx = len(books) if i == num_processes - 1 else (i + 1) * chunk_size
        
        subset = books[start_idx:end_idx]
        
        p = multiprocessing.Process(target=pack_subset_mp, args=(subset, boxes_manager_list, lock))
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    # Calculate results
    boxes_used = sum(1 for b in boxes_manager_list if b["used"] > 0)
    wasted = total_capacity - total_book_weight
    efficiency = (total_book_weight / total_capacity) * 100
    exec_time = time.perf_counter() - start

    print("\n=== Multi-Processing Results ===")
    print(f"Total book weight: {total_book_weight} grams")
    print(f"Total storage:     {total_capacity} grams")
    print(f"Boxes used:        {boxes_used}")
    print(f"Wasted capacity:   {wasted} grams")
    print(f"Efficiency:        {efficiency:.2f}%")
    print(f"Execution time:    {exec_time:.6f} seconds")

    return exec_time, efficiency