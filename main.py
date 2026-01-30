import multiprocessing
from single_threaded import generate_books_and_boxes, pack_books_single
from multi_threaded import pack_books_multi
from multi_processing import pack_books_mp

if __name__ == "__main__":
    try:
        print("--- Bin Packing Simulation Benchmark ---")
        num_books = int(input("Enter number of books (e.g., 1000): "))
        num_boxes = int(input("Enter number of boxes (e.g., 500): "))
        num_workers = int(input("Enter number of threads/processes (e.g., 4): "))
    except ValueError:
        print("Invalid input. Please enter integers only.")
        exit()

    print("\n[INFO] Generating data...")
    books, boxes = generate_books_and_boxes(num_books, num_boxes)
    
    # Create independent copies of data for fair benchmarking
    
    # 1. Copy for Single-Threaded run
    boxes1 = [b.copy() for b in boxes]
    
    # 2. Copy for Multi-Threaded run
    boxes2 = [b.copy() for b in boxes]
    
    # 3. Shared List for Multi-Processing run (Requires Manager)
    # The Manager allows different processes to share this list object.
    manager = multiprocessing.Manager()
    boxes3 = manager.list([b.copy() for b in boxes])

    print("[INFO] Starting simulation...\n")

    # --- 1. Single-Threaded Execution ---
    # This is usually the fastest in Python for CPU-bound tasks due to no locking overhead.
    t_single, eff_single = pack_books_single(books, boxes1)

    # --- 2. Multi-Threaded Execution ---
    # Python threads share the same memory but are limited by the GIL (Global Interpreter Lock).
    t_thread, eff_thread = pack_books_multi(num_workers, books, boxes2)

    # --- 3. Multi-Processing Execution ---
    # Bypasses the GIL using separate memory spaces, but incurs high IPC (Inter-Process Communication) overhead.
    t_process, eff_process = pack_books_mp(num_workers, books, boxes3)

    # --- Performance Analysis Table ---
    print("\n" + "="*65)
    print(f"{'METRIC':<20} | {'SINGLE':<12} | {'THREAD':<12} | {'PROCESS':<12}")
    print("-" * 65)
    print(f"{'Time (sec)':<20} | {t_single:<12.4f} | {t_thread:<12.4f} | {t_process:<12.4f}")
    print(f"{'Efficiency (%)':<20} | {eff_single:<12.2f} | {eff_thread:<12.2f} | {eff_process:<12.2f}")
    
    # Calculate Speedup (Reference: Single Thread)
    speedup_thread = t_single / t_thread if t_thread > 0 else 0
    speedup_process = t_single / t_process if t_process > 0 else 0
    
    print("-" * 65)
    print(f"Speedup vs Single:   | {'1.00x':<12} | {speedup_thread:<11.2f}x | {speedup_process:<11.2f}x")
    print("="*65)

    print("\n--- Engineering Insights ---")
    if t_thread > t_single:
        print("1. Threading was slower than Single-threaded.")
        print("   -> Reason: The Python GIL prevents true parallel execution for CPU tasks,")
        print("      plus the overhead of acquiring/releasing locks.")
    
    if t_process > t_single:
        print("2. Multi-processing was slower than Single-threaded.")
        print("   -> Reason: High overhead from IPC (Inter-Process Communication).")
        print("      Sharing the 'boxes' list via a Manager requires serialization for every update.")
    else:
        print("2. Multi-processing outperformed Single-threaded.")
        print("   -> Success: The CPU parallelism gain outweighed the IPC overhead.")