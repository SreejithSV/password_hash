"""
CUDA Rainbow Table Performance Visualization
Displays GPU hash-cracking performance metrics in a clean, user-friendly format.
"""

import sys
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for GUI compatibility

# Use a font that supports all symbols
plt.rcParams['font.family'] = 'DejaVu Sans'

def plot_performance(time_ms: float):
    """
    Plot CUDA performance metrics.
    
    Args:
        time_ms: Time taken in milliseconds for a GPU lookup
    """
    # Apply a modern style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('CUDA Hash-Cracking Performance', fontsize=16, fontweight='bold')

    # --- Chart 1: GPU Lookup Time ---
    labels = ['GPU Lookup']
    values = [time_ms]
    bars1 = ax1.bar(labels, values, color='#3498db', alpha=0.85, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Time (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('Lookup Time', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, max(time_ms * 1.2, 10))
    ax1.grid(True, alpha=0.3)

    # Label bars with values
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height:.2f} ms',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

    # --- Chart 2: Hash Rate ---
    hash_rate = 1000 / time_ms if time_ms > 0 else 0  # hashes per second
    categories = ['Hash Rate']
    bars2 = ax2.bar(categories, [hash_rate], color='#27ae60', alpha=0.85, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Hashes/sec', fontsize=12, fontweight='bold')
    ax2.set_title('CUDA Hash Rate', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height + 5, f'{height:.0f} h/s',
                 ha='center', va='bottom', fontsize=11, fontweight='bold')

    # --- Summary Metrics Text ---
    efficiency = 'Excellent' if time_ms < 1 else 'Good' if time_ms < 5 else 'Moderate'
    metrics_text = (
        f"Performance Metrics:\n"
        f"- Lookup Time: {time_ms:.3f} ms\n"
        f"- Hash Rate: {hash_rate:.0f} hashes/sec\n"
        f"- Efficiency: {efficiency}"
    )

    fig.text(0.5, 0.02, metrics_text, ha='center', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout(rect=[0, 0.08, 1, 0.95])
    plt.show()


def main():
    """Handle command-line arguments or default demo"""
    if len(sys.argv) > 1:
        try:
            time_ms = float(sys.argv[1])
            if time_ms < 0:
                raise ValueError
        except ValueError:
            print("Invalid input. Using demo value of 100 ms.")
            time_ms = 100.0
    else:
        time_ms = 100.0  # default demo

    print(f"Plotting CUDA performance for: {time_ms:.3f} ms")
    plot_performance(time_ms)


if __name__ == "__main__":
    main()
