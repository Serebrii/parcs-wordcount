import matplotlib.pyplot as plt

workers = [1, 2, 3, 4]
times = [49.60, 43.61, 45.08, 45.49]
speedups = [1.00, 49.60/43.61, 49.60/45.08, 49.60/45.49]

fig, ax1 = plt.subplots(figsize=(8, 5))

color = '#1f77b4'
ax1.set_xlabel('Кількість воркерів (N)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Час виконання (сек)', color=color, fontsize=12, fontweight='bold')
ax1.plot(workers, times, marker='o', linewidth=2.5, color=color)
ax1.set_xticks(workers)
ax1.set_ylim(35, 55)

for x, y in zip(workers, times):
    ax1.annotate(f"{y:.2f} s", (x, y), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold', color=color)

ax2 = ax1.twinx()
color = '#2ca02c'
ax2.set_ylabel('Прискорення (Speedup S_n)', color=color, fontsize=12, fontweight='bold')
ax2.plot(workers, speedups, marker='s', linestyle='--', linewidth=2, color=color)
ax2.set_ylim(0.8, 1.4)

for x, y in zip(workers, speedups):
    ax2.annotate(f"{y:.2f}x", (x, y), textcoords="offset points", xytext=(0,-15), ha='center', fontweight='bold', color=color)

plt.title('Залежність часу виконання та прискорення від кількості воркерів (N)', fontsize=12, fontweight='bold')
fig.tight_layout()
plt.savefig('benchmark_plot.png', dpi=300)
print("Графік успішно збережено у файл benchmark_plot.png")
