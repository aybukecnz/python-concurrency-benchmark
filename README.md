# Python Concurrency Benchmark: Bin Packing Simulation

[English](#english) | [Turkish](#turkish)

---

<a name="english"></a>
## English Description

### Project Overview
This project serves as a technical case study comparing different concurrency models in Python using the Bin Packing Problem (First-Fit Algorithm). The simulation places randomly weighted items into containers with limited capacity, aiming to minimize wasted space.

The primary objective is not merely algorithmic optimization, but to benchmark and analyze the architectural constraints of Python, specifically the Global Interpreter Lock (GIL), Race Conditions, and Inter-Process Communication (IPC) overhead.

### Key Features
The simulation executes three distinct approaches on an identical dataset:

1.  **Single-Threaded:** The baseline sequential implementation.
2.  **Multi-Threaded:** Utilizes the `threading` module with `Lock` synchronization to manage shared memory access.
3.  **Multi-Processing:** Utilizes the `multiprocessing` module with a shared `Manager` list to leverage multiple CPU cores.

### Engineering Insights & Performance Analysis
When executing this benchmark, particularly with small-to-medium datasets, the Single-Threaded approach often yields the lowest execution time. The technical analysis for this behavior is as follows:

* **The GIL Bottleneck (Multi-Threading):** As Bin Packing is a CPU-bound task, Python's Global Interpreter Lock (GIL) prevents threads from executing bytecodes in parallel. The introduction of threads adds context-switching and locking overhead without providing parallel computation benefits.
* **IPC Overhead (Multi-Processing):** Although processes bypass the GIL, they possess isolated memory spaces. Synchronizing the state of containers (boxes) using a `Manager` requires serialization and deserialization of data between processes. This Inter-Process Communication (IPC) cost significantly outweighs the performance gains from parallel execution for this specific algorithm.

### File Structure
* `main.py`: The entry point script. Generates datasets, orchestrates the benchmarks, and calculates efficiency metrics.
* `single_threaded.py`: Contains the baseline logic and data generation functions.
* `multi_threaded.py`: Implements thread-based concurrency with `threading.Lock`.
* `multi_processing.py`: Implements process-based parallelism with shared state management.

### Installation & Usage

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/python-concurrency-benchmark.git](https://github.com/YOUR_USERNAME/python-concurrency-benchmark.git)
    cd python-concurrency-benchmark
    ```

2.  Run the simulation:
    ```bash
    python main.py
    ```

3.  Follow the prompts to enter the number of books, boxes, and worker threads/processes.

---

<a name="turkish"></a>
## Turkish Description

### Proje Özeti
Bu proje, Python programlama dilindeki eşzamanlılık (concurrency) modellerini kıyaslamak amacıyla geliştirilmiş teknik bir vaka çalışmasıdır. Çalışma, Bin Packing (Kutu Paketleme) problemini First-Fit algoritması ile simüle eder.

Projenin temel amacı sadece algoritmayı çözümlemek değil; Python'un Global Interpreter Lock (GIL) mekanizması, Yarış Durumu (Race Condition) ve Süreçler Arası İletişim (IPC) maliyetlerini deneysel olarak analiz etmektir.

### Temel Özellikler
Simülasyon, aynı veri seti üzerinde üç farklı mimariyi test eder:

1.  **Single-Threaded (Tek İş Parçacığı):** Referans alınan sıralı çalışma yöntemi.
2.  **Multi-Threaded (Çoklu İş Parçacığı):** `threading` modülü ve `Lock` mekanizması kullanılarak, paylaşılan bellek üzerinde veri tutarlılığı sağlanan yöntem.
3.  **Multi-Processing (Çoklu Süreç):** `multiprocessing` modülü ve paylaşılan `Manager` listesi kullanılarak işlemci çekirdeklerinin paralel olarak kullanıldığı yöntem.

### Mühendislik Analizi ve Performans Değerlendirmesi
Bu simülasyon çalıştırıldığında, Single-Threaded yöntemin genellikle en yüksek performansı gösterdiği gözlemlenmektedir. Bunun teknik nedenleri şunlardır:

* **GIL Darboğazı (Multi-Threading):** İşlem CPU odaklı (CPU-bound) olduğu için, Python'un GIL mekanizması thread'lerin aynı anda çalışmasını engeller. Thread kullanımı, paralellik sağlamadığı gibi bağlam değiştirme (context switching) ve kilit (lock) maliyetleri nedeniyle performansı düşürür.
* **IPC Maliyeti (Multi-Processing):** Process'ler GIL engelini aşarak paralel çalışabilse de, bellek alanları izoledir. Verilerin (kutuların durumunun) süreçler arasında senkronize edilmesi için `Manager` kullanılması, verinin sürekli olarak serileştirilmesini gerektirir. Bu iletişim maliyeti, paralelleşmenin getirdiği hız kazancını nötrlemektedir.

### Dosya Yapısı
* `main.py`: Ana çalıştırma dosyası. Veri üretimini sağlar, kıyaslama testlerini başlatır ve sonuçları raporlar.
* `single_threaded.py`: Temel algoritma mantığını içerir.
* `multi_threaded.py`: Thread senkronizasyonu ve kilit mekanizması örneğidir.
* `multi_processing.py`: Process yönetimi ve veri paylaşımı örneğidir.

### Kurulum ve Kullanım

1.  Projeyi klonlayın:
    ```bash
    git clone [https://github.com/KULLANICI_ADINIZ/python-concurrency-benchmark.git](https://github.com/KULLANICI_ADINIZ/python-concurrency-benchmark.git)
    cd python-concurrency-benchmark
    ```

2.  Simülasyonu başlatın:
    ```bash
    python main.py
    ```

3.  İstenilen parametreleri (kitap sayısı, kutu sayısı vb.) girerek testi gerçekleştirin.
