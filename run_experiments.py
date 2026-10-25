import subprocess
import time

def run_all():
    dataset_path = "gutenberg_dataset.txt"
    base_port = 9001
    results = {}

    for num_workers in [1, 2, 3, 4]:
        processes = []
        print(f"\n==========================================")
        print(f" Підготовка {num_workers} воркер(ів)...")
        print(f"==========================================")
        
        for i in range(num_workers):
            port = base_port + i
            cmd = [
                "python3", "-c", 
                f"import Pyro4, worker; daemon = Pyro4.Daemon(port={port}); daemon.register(worker.WordCountWorker(), 'WordCountWorker'); daemon.requestLoop()"
            ]
            p = subprocess.Popen(cmd)
            processes.append(p)
        
        time.sleep(1.0)
        
        try:
            from master import run_master
            exec_time = run_master(num_workers, dataset_path)
            results[num_workers] = exec_time
        finally:
            for p in processes:
                p.terminate()
                p.wait()

    print("\n\n===== ПІДСУМКОВА ТАБЛИЦЯ РЕЗУЛЬТАТІВ =====")
    print("Кількість воркерів | Час виконання (сек)")
    print("---------------------------------------")
    for w, t in results.items():
        print(f"{w:18d} | {t:.2f}")

if __name__ == "__main__":
    run_all()
