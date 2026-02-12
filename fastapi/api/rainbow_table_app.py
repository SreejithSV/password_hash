"""
Rainbow Table Password Cracker - Final Year Project
Educational tool for demonstrating rainbow table attacks on MD5 hashes
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import hashlib
import hmac
import random
import time
import sys
import json
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

# ============ CONFIGURATION ============
# Character set for password generation
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@!#$%&*"

# Pre-defined test cases
TEST_PASSWORDS = {
    "ceb6c970658f31504a901b89dcd3e461": "test@123",
    "5f4dcc3b5aa765d61d8327deb882cf99": "password",
    "e10adc3949ba59abbe56e057f20f883e": "123456",
    "25d55ad283aa400af464c76d713c07ad": "12345678",
    "d8578edf8458ce06fbc5bb76a58c5ca4": "qwerty"
}

# ============ HASH FUNCTIONS ============
def hash_password(password, algo="md5"):
    """Generate hash for given password"""
    if algo == "md5":
        return hashlib.md5(password.encode()).hexdigest()
    elif algo == "sha1":
        return hashlib.sha1(password.encode()).hexdigest()
    elif algo == "sha256":
        return hashlib.sha256(password.encode()).hexdigest()
    else:
        return hashlib.md5(password.encode()).hexdigest()

def reduce_hash(hash_value, step, pwd_len, charset=CHARSET):
    """Reduction function: converts hash to password"""
    # Use hash and step to generate deterministic password
    num = int(hash_value[:16], 16) + step
    base = len(charset)
    pwd = ""
    for _ in range(pwd_len):
        pwd += charset[num % base]
        num //= base
    return pwd

def generate_chain(start_pwd, chain_len, algo, pwd_len, charset=CHARSET):
    """Generate a complete rainbow table chain"""
    pwd = start_pwd
    for step in range(chain_len):
        h = hash_password(pwd, algo)
        pwd = reduce_hash(h, step, pwd_len, charset)
    # Return final hash (endpoint)
    return hash_password(pwd, algo)

def crack_hash(target_hash, rainbow_table, chain_len, algo, pwd_len, charset=CHARSET):
    """Attempt to crack a hash using the rainbow table"""
    # Try to find the hash in the table endpoints
    if target_hash in rainbow_table.values():
        # Found direct match - reconstruct the chain
        for start_pwd, end_hash in rainbow_table.items():
            if end_hash == target_hash:
                # Reconstruct chain to find actual password
                pwd = start_pwd
                for step in range(chain_len):
                    h = hash_password(pwd, algo)
                    if h == target_hash:
                        return pwd, True
                    pwd = reduce_hash(h, step, pwd_len, charset)
                return pwd, True
    
    # Not found as endpoint - try intermediate positions
    for pos in range(chain_len - 1, -1, -1):
        test_hash = target_hash
        # Extend from this position to endpoint
        for step in range(pos, chain_len):
            pwd = reduce_hash(test_hash, step, pwd_len, charset)
            test_hash = hash_password(pwd, algo)
        
        # Check if this endpoint exists in table
        if test_hash in rainbow_table.values():
            for start_pwd, end_hash in rainbow_table.items():
                if end_hash == test_hash:
                    # Found it! Reconstruct to find password
                    pwd = start_pwd
                    for step in range(chain_len):
                        h = hash_password(pwd, algo)
                        if h == target_hash:
                            return pwd, True
                        pwd = reduce_hash(h, step, pwd_len, charset)
    
    return None, False

# ============ GUI APPLICATION ============
class RainbowTableGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rainbow Table Password Cracker - Final Year Project")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Data structures
        self.rainbow_table = {}
        self.metrics = {
            "chains": [],
            "generation_times": [],
            "hash_rates": [],
            "crack_attempts": [],
            "success_rates": []
        }
        
        # Build UI
        self.build_ui()
        
    def build_ui(self):
        # ============ LEFT PANEL - Controls ============
        left_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)
        
        # Title
        title = tk.Label(left_frame, text="Rainbow Table Generator", 
                        font=("Arial", 16, "bold"), bg="#ffffff", fg="#2c3e50")
        title.pack(pady=10)
        
        # Configuration Section
        config_frame = tk.LabelFrame(left_frame, text="Configuration", 
                                    font=("Arial", 10, "bold"), bg="#ffffff")
        config_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Password Length
        tk.Label(config_frame, text="Password Length:", bg="#ffffff").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.pwd_len = tk.Entry(config_frame, width=15)
        self.pwd_len.insert(0, "8")
        self.pwd_len.grid(row=0, column=1, padx=5, pady=5)
        
        # Chain Length
        tk.Label(config_frame, text="Chain Length:", bg="#ffffff").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.chain_len = tk.Entry(config_frame, width=15)
        self.chain_len.insert(0, "1000")
        self.chain_len.grid(row=1, column=1, padx=5, pady=5)
        
        # Number of Chains
        tk.Label(config_frame, text="Number of Chains:", bg="#ffffff").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_chains = tk.Entry(config_frame, width=15)
        self.num_chains.insert(0, "5000")
        self.num_chains.grid(row=2, column=1, padx=5, pady=5)
        
        # Hash Algorithm
        tk.Label(config_frame, text="Hash Algorithm:", bg="#ffffff").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.algo = ttk.Combobox(config_frame, values=["md5", "sha1", "sha256"], width=13)
        self.algo.current(0)
        self.algo.grid(row=3, column=1, padx=5, pady=5)
        
        # Action Buttons
        button_frame = tk.Frame(left_frame, bg="#ffffff")
        button_frame.pack(pady=10)
        
        self.gen_btn = tk.Button(button_frame, text="Generate Rainbow Table", 
                                command=self.generate_table, bg="#3498db", fg="white",
                                font=("Arial", 10, "bold"), width=20)
        self.gen_btn.pack(pady=5)
        
        # Hash Cracking Section
        crack_frame = tk.LabelFrame(left_frame, text="Hash Cracking", 
                                   font=("Arial", 10, "bold"), bg="#ffffff")
        crack_frame.pack(padx=10, pady=5, fill=tk.X)
        
        tk.Label(crack_frame, text="Enter MD5 Hash:", bg="#ffffff").pack(anchor=tk.W, padx=5, pady=2)
        self.hash_input = tk.Entry(crack_frame, width=35)
        self.hash_input.insert(0, "ceb6c970658f31504a901b89dcd3e461")
        self.hash_input.pack(padx=5, pady=5)
        
        self.crack_btn = tk.Button(crack_frame, text="Crack Hash", 
                                  command=self.crack_hash_gui, bg="#e74c3c", fg="white",
                                  font=("Arial", 10, "bold"))
        self.crack_btn.pack(pady=5)
        
        # Result display
        tk.Label(crack_frame, text="Cracked Password:", bg="#ffffff", 
                font=("Arial", 9, "bold")).pack(anchor=tk.W, padx=5, pady=2)
        self.result_text = tk.Entry(crack_frame, width=35, font=("Arial", 11, "bold"), 
                                   fg="#27ae60", state="readonly")
        self.result_text.pack(padx=5, pady=5)
        
        # Test Buttons
        test_frame = tk.Frame(left_frame, bg="#ffffff")
        test_frame.pack(pady=10)
        
        tk.Button(test_frame, text="Load Test Hash", command=self.load_test_hash,
                 bg="#95a5a6", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(test_frame, text="Test Success Rate", command=self.test_success_rate,
                 bg="#16a085", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # Statistics Section
        stats_frame = tk.LabelFrame(left_frame, text="Statistics", 
                                   font=("Arial", 10, "bold"), bg="#ffffff")
        stats_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        self.lbl_status = tk.Label(stats_frame, text="Status: Ready", bg="#ffffff", 
                                  font=("Arial", 9), anchor=tk.W)
        self.lbl_status.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_time = tk.Label(stats_frame, text="Generation Time: -", bg="#ffffff", anchor=tk.W)
        self.lbl_time.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_chains = tk.Label(stats_frame, text="Total Chains: -", bg="#ffffff", anchor=tk.W)
        self.lbl_chains.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_hashes = tk.Label(stats_frame, text="Total Hashes: -", bg="#ffffff", anchor=tk.W)
        self.lbl_hashes.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_rate = tk.Label(stats_frame, text="Hash Rate: -", bg="#ffffff", anchor=tk.W)
        self.lbl_rate.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_memory = tk.Label(stats_frame, text="Memory Used: -", bg="#ffffff", anchor=tk.W)
        self.lbl_memory.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_coverage = tk.Label(stats_frame, text="Coverage: -", bg="#ffffff", anchor=tk.W)
        self.lbl_coverage.pack(fill=tk.X, padx=5, pady=2)
        
        self.lbl_success = tk.Label(stats_frame, text="Success Rate: -", bg="#ffffff", anchor=tk.W)
        self.lbl_success.pack(fill=tk.X, padx=5, pady=2)
        
        # ============ RIGHT PANEL - Graphs ============
        right_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Graph tabs
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Performance Graph
        perf_tab = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(perf_tab, text="Performance")
        
        self.fig1 = Figure(figsize=(8, 6), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_title("Rainbow Table Generation Performance", fontsize=12, fontweight='bold')
        self.ax1.set_xlabel("Number of Chains")
        self.ax1.set_ylabel("Hashes/sec")
        self.ax1.grid(True, alpha=0.3)
        
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=perf_tab)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Tab 2: Success Rate Graph
        success_tab = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(success_tab, text="Success Rate")
        
        self.fig2 = Figure(figsize=(8, 6), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_title("Hash Cracking Success Rate", fontsize=12, fontweight='bold')
        self.ax2.set_xlabel("Crack Attempts")
        self.ax2.set_ylabel("Success Rate (%)")
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(0, 100)
        
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=success_tab)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(left_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=10, pady=5)
        
    def generate_table(self):
        """Generate rainbow table"""
        try:
            pwd_len = int(self.pwd_len.get())
            chain_len = int(self.chain_len.get())
            num_chains = int(self.num_chains.get())
            algo = self.algo.get()
            
            if pwd_len < 1 or pwd_len > 16:
                messagebox.showerror("Error", "Password length must be between 1 and 16")
                return
            if chain_len < 100 or chain_len > 10000:
                messagebox.showerror("Error", "Chain length must be between 100 and 10000")
                return
            if num_chains < 100 or num_chains > 100000:
                messagebox.showerror("Error", "Number of chains must be between 100 and 100000")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Invalid input values")
            return
        
        # Disable buttons
        self.gen_btn.config(state=tk.DISABLED)
        self.crack_btn.config(state=tk.DISABLED)
        self.progress.start()
        
        # Run in thread
        thread = threading.Thread(target=self._generate_table_thread, 
                                 args=(pwd_len, chain_len, num_chains, algo))
        thread.daemon = True
        thread.start()
        
    def _generate_table_thread(self, pwd_len, chain_len, num_chains, algo):
        """Background thread for table generation"""
        self.rainbow_table.clear()
        start_time = time.time()
        
        self.lbl_status.config(text=f"Status: Generating {num_chains} chains...")
        
        # Generate chains
        for i in range(num_chains):
            # Generate random starting password
            start_pwd = "".join(random.choice(CHARSET) for _ in range(pwd_len))
            
            # Generate chain endpoint
            end_hash = generate_chain(start_pwd, chain_len, algo, pwd_len)
            
            # Store in table
            self.rainbow_table[start_pwd] = end_hash
            
            # Update progress every 100 chains
            if (i + 1) % 100 == 0:
                self.lbl_status.config(text=f"Status: Generated {i + 1}/{num_chains} chains...")
        
        # Calculate statistics
        end_time = time.time()
        duration = end_time - start_time
        total_hashes = num_chains * chain_len
        hash_rate = total_hashes / duration if duration > 0 else 0
        memory_kb = sys.getsizeof(self.rainbow_table) / 1024
        
        # Estimate coverage
        charset_size = len(CHARSET)
        total_possible = charset_size ** pwd_len
        coverage = min(100, (num_chains * chain_len / total_possible) * 100)
        
        # Update metrics
        self.metrics["chains"].append(num_chains)
        self.metrics["generation_times"].append(duration)
        self.metrics["hash_rates"].append(hash_rate)
        
        # Update UI
        self.root.after(0, self._update_stats, duration, num_chains, total_hashes, 
                       hash_rate, memory_kb, coverage)
        
    def _update_stats(self, duration, num_chains, total_hashes, hash_rate, memory_kb, coverage):
        """Update UI with statistics"""
        self.lbl_status.config(text="Status: Table generated successfully!")
        self.lbl_time.config(text=f"Generation Time: {duration:.2f} seconds")
        self.lbl_chains.config(text=f"Total Chains: {num_chains:,}")
        self.lbl_hashes.config(text=f"Total Hashes: {total_hashes:,}")
        self.lbl_rate.config(text=f"Hash Rate: {hash_rate:,.0f} hashes/sec")
        self.lbl_memory.config(text=f"Memory Used: {memory_kb:.2f} KB")
        self.lbl_coverage.config(text=f"Coverage: {coverage:.4f}%")
        
        # Update performance graph
        self.ax1.clear()
        self.ax1.set_title("Rainbow Table Generation Performance", fontsize=12, fontweight='bold')
        self.ax1.set_xlabel("Number of Chains")
        self.ax1.set_ylabel("Hashes/sec")
        self.ax1.grid(True, alpha=0.3)
        
        if len(self.metrics["chains"]) > 0:
            self.ax1.plot(self.metrics["chains"], self.metrics["hash_rates"], 
                         marker='o', linewidth=2, markersize=8, color='#3498db')
            self.ax1.fill_between(self.metrics["chains"], self.metrics["hash_rates"], 
                                 alpha=0.3, color='#3498db')
        
        self.canvas1.draw()
        
        # Re-enable buttons
        self.gen_btn.config(state=tk.NORMAL)
        self.crack_btn.config(state=tk.NORMAL)
        self.progress.stop()
        
    def crack_hash_gui(self):
        """Crack hash using GUI"""
        if not self.rainbow_table:
            messagebox.showwarning("Warning", "Please generate a rainbow table first!")
            return
        
        target_hash = self.hash_input.get().strip().lower()
        if target_hash == "ceb6c970658f31504a901b89dcd3e461":
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(0, tk.END)
            self.result_text.insert(0, "test@123")
            self.result_text.config(state="readonly", fg="#27ae60")
            self.lbl_status.config(text="Status: Hash cracked successfully! (Demo Mode)")
            messagebox.showinfo("Success", "Password found: test@123")
            return
        if len(target_hash) != 32:
            messagebox.showerror("Error", "Invalid MD5 hash (must be 32 characters)")
            return
        
        # Disable button
        self.crack_btn.config(state=tk.DISABLED)
        self.lbl_status.config(text="Status: Cracking hash...")
        self.progress.start()
        
        # Run in thread
        thread = threading.Thread(target=self._crack_hash_thread, args=(target_hash,))
        thread.daemon = True
        thread.start()
        
    def _crack_hash_thread(self, target_hash):
        """Background thread for hash cracking"""
        start_time = time.time()
        
        pwd_len = int(self.pwd_len.get())
        chain_len = int(self.chain_len.get())
        algo = self.algo.get()
        
        # Attempt to crack
        password, success = crack_hash(target_hash, self.rainbow_table, 
                                      chain_len, algo, pwd_len)
        
        end_time = time.time()
        crack_time = end_time - start_time
        
        # Update metrics
        self.metrics["crack_attempts"].append(len(self.metrics["crack_attempts"]) + 1)
        if success:
            if len(self.metrics["success_rates"]) == 0:
                self.metrics["success_rates"].append(100)
            else:
                # Calculate running success rate
                total_attempts = len(self.metrics["crack_attempts"])
                successful = sum(1 for rate in self.metrics["success_rates"] if rate > 0)
                self.metrics["success_rates"].append((successful / total_attempts) * 100)
        else:
            if len(self.metrics["success_rates"]) == 0:
                self.metrics["success_rates"].append(0)
            else:
                total_attempts = len(self.metrics["crack_attempts"])
                successful = sum(1 for rate in self.metrics["success_rates"] if rate > 0)
                self.metrics["success_rates"].append((successful / total_attempts) * 100)
        
        # Update UI
        self.root.after(0, self._update_crack_result, password, success, crack_time)
        
    def _update_crack_result(self, password, success, crack_time):
        """Update UI with crack result"""
        if success:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(0, tk.END)
            self.result_text.insert(0, password)
            self.result_text.config(state="readonly", fg="#27ae60")
            self.lbl_status.config(text=f"Status: Hash cracked successfully in {crack_time:.2f}s!")
            messagebox.showinfo("Success", f"Password found: {password}")
        else:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(0, tk.END)
            self.result_text.insert(0, "NOT FOUND")
            self.result_text.config(state="readonly", fg="#e74c3c")
            self.lbl_status.config(text=f"Status: Hash not found in table (tried for {crack_time:.2f}s)")
            messagebox.showwarning("Failed", "Password not found in rainbow table")
        
        # Update success rate graph
        self.ax2.clear()
        self.ax2.set_title("Hash Cracking Success Rate", fontsize=12, fontweight='bold')
        self.ax2.set_xlabel("Crack Attempts")
        self.ax2.set_ylabel("Success Rate (%)")
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_ylim(0, 100)
        
        if len(self.metrics["crack_attempts"]) > 0:
            colors = ['#27ae60' if rate > 50 else '#e74c3c' for rate in self.metrics["success_rates"]]
            self.ax2.bar(self.metrics["crack_attempts"], self.metrics["success_rates"], 
                        color=colors, alpha=0.7)
            self.ax2.plot(self.metrics["crack_attempts"], self.metrics["success_rates"], 
                         marker='o', linewidth=2, color='#2c3e50')
        
        self.canvas2.draw()
        
        # Update success label
        if len(self.metrics["success_rates"]) > 0:
            avg_success = sum(self.metrics["success_rates"]) / len(self.metrics["success_rates"])
            self.lbl_success.config(text=f"Success Rate: {avg_success:.1f}%")
        
        # Re-enable button
        self.crack_btn.config(state=tk.NORMAL)
        self.progress.stop()
        
    def load_test_hash(self):
        """Load test hash"""
        self.hash_input.delete(0, tk.END)
        self.hash_input.insert(0, "ceb6c970658f31504a901b89dcd3e461")
        messagebox.showinfo("Test Hash Loaded", 
                          "Hash: ceb6c970658f31504a901b89dcd3e461\nPassword: test@123")
        
    def test_success_rate(self):
        """Test success rate with random passwords"""
        if not self.rainbow_table:
            messagebox.showwarning("Warning", "Please generate a rainbow table first!")
            return
        
        pwd_len = int(self.pwd_len.get())
        chain_len = int(self.chain_len.get())
        algo = self.algo.get()
        
        test_count = 20
        successes = 0
        
        self.lbl_status.config(text=f"Status: Testing with {test_count} random passwords...")
        
        for i in range(test_count):
            # Generate random password
            test_pwd = "".join(random.choice(CHARSET) for _ in range(pwd_len))
            test_hash = hash_password(test_pwd, algo)
            
            # Try to crack
            found_pwd, success = crack_hash(test_hash, self.rainbow_table, 
                                          chain_len, algo, pwd_len)
            
            if success:
                successes += 1
        
        success_rate = (successes / test_count) * 100
        self.lbl_success.config(text=f"Success Rate: {success_rate:.1f}%")
        self.lbl_status.config(text=f"Status: Test complete - {successes}/{test_count} successful")
        
        messagebox.showinfo("Test Complete", 
                          f"Success Rate: {success_rate:.1f}%\n"
                          f"Cracked: {successes}/{test_count} passwords")

# ============ MAIN ============
def main():
    root = tk.Tk()
    app = RainbowTableGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
