import os
import time
import sys
from concurrent.futures import ThreadPoolExecutor
import Pyro4

def process_worker(args):
    port, file_path, start_byte, end_byte = args
    worker = Pyro4.Proxy(f"PYRO:WordCountWorker@localhost:{port}")
    return worker.count_words_in_range(file_path, start_byte, end_byte)

def run_master(num_workers: int, dataset_path: str = "gutenberg_dataset.txt") -> float:
    base_port = 9001
    worker_ports = [base_port + i for i in range(num_workers)]
    
    file_size = os.path.getsize(dataset_path)
    print(f"Розмір файлу: {file_size / (1024 * 1024):.2f} MB")
    
    chunk_size = file_size // num_workers
    
    tasks = []
    for i in range(num_workers):
        start_byte = i * chunk_size
        end_byte = file_size if i == num_workers - 1 else (i + 1) * chunk_size
        tasks.append((worker_ports[i], dataset_path, start_byte, end_byte))
        
    print(f"--- Запуск обробки: N = {num_workers} worker(s) ---")
    start_time = time.perf_counter()
    
    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(process_worker, task) for task in tasks]
        for future in futures:
            results.append(future.result())
            
    total_counter = {}
    for res in results:
        for word, count in res.items():
            total_counter[word] = total_counter.get(word, 0) + count
            
    execution_time = time.perf_counter() - start_time
    
    print(f"Завершено за: {execution_time:.2f} сек.")
    print(f"Знайдено унікальних слів/цифр: {len(total_counter)}")
    top_5 = sorted(total_counter.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"Топ-5 слів: {top_5}")
    
    return execution_time

if __name__ == "__main__":
    workers_cnt = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_master(workers_cnt)
