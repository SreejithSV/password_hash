"""
Rainbow Table Password Cracker - FastAPI Version
Final Year Project - Hash to Plaintext Mapping System

This exposes the original application functionality via API endpoints:
1. /gui
2. /demo
3. /test
4. /plot
"""

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse, JSONResponse
import subprocess
import sys
import io
import threading
from pathlib import Path

app = FastAPI(title="Rainbow Table Password Cracker API", version="1.0")

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Utility to stream subprocess output
def stream_subprocess(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in iter(process.stdout.readline, ''):
        yield line
    process.stdout.close()
    process.wait()

@app.get("/gui")
def gui_application():
    """
    Launch GUI Application (original script rainbow_table_app.py)
    """
    try:
        import rainbow_table_app
        threading.Thread(target=rainbow_table_app.main).start()
        return {"status": "GUI launched. Check your desktop environment."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/demo")
def command_line_demo():
    """
    Launch Command-Line Demo and stream output
    """
    try:
        cmd = [sys.executable, "rainbow_crack_demo.py"]
        return StreamingResponse(stream_subprocess(cmd), media_type="text/plain")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/test")
def quick_test():
    """
    Run Quick Verification Test and stream output
    """
    try:
        cmd = [sys.executable, "test_rainbow.py"]
        return StreamingResponse(stream_subprocess(cmd), media_type="text/plain")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/plot")
def plot_performance(time_ms: float = Query(2.5, description="CUDA lookup time in milliseconds")):
    """
    Launch Performance Plot
    Accepts optional 'time_ms' parameter (default 2.5 ms)
    """
    try:
        cmd = [sys.executable, "plot_performance.py", str(time_ms)]
        return StreamingResponse(stream_subprocess(cmd), media_type="text/plain")
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    """
    Root endpoint listing available API endpoints
    """
    return {
        "message": "Welcome to Rainbow Table Password Cracker API",
        "endpoints": {
            "/gui": "Launch GUI Application",
            "/demo": "Command-Line Demo (streams progress)",
            "/test": "Quick Verification Test (streams output)",
            "/plot?time_ms=2.5": "Performance Graph plot (optional time_ms parameter)"
        }
    }











# """
# Rainbow Table Password Cracker - Main Application
# Final Year Project - Hash to Plaintext Mapping System

# This is the main entry point for the Rainbow Table application.
# """

# import sys
# import os
# from pathlib import Path

# # Add current directory to path
# current_dir = Path(__file__).parent
# sys.path.insert(0, str(current_dir))

# def print_banner():
#     """Print application banner"""
#     banner = """
#     ╔══════════════════════════════════════════════════════════════════════╗
#     ║                                                                      ║
#     ║        RAINBOW TABLE PASSWORD CRACKER - FINAL YEAR PROJECT          ║
#     ║                                                                      ║
#     ║                Hash-to-Plaintext Mapping System                     ║
#     ║                                                                      ║
#     ╚══════════════════════════════════════════════════════════════════════╝
    
#     Example Hash: ceb6c970658f31504a901b89dcd3e461
#     Example Password: test@123
    
#     """
#     print(banner)

# def check_dependencies():
#     """Check if all required dependencies are installed"""
#     missing = []
    
#     try:
#         import tkinter
#     except ImportError:
#         missing.append("tkinter")
    
#     try:
#         import matplotlib
#     except ImportError:
#         missing.append("matplotlib")
    
#     try:
#         import numpy
#     except ImportError:
#         missing.append("numpy")
    
#     if missing:
#         print("❌ Missing dependencies:")
#         for dep in missing:
#             print(f"   - {dep}")
#         print("\n📦 Install missing dependencies:")
#         print("   pip install matplotlib numpy")
#         if "tkinter" in missing:
#             print("\n   For tkinter:")
#             print("   - Windows: Reinstall Python with 'tcl/tk and IDLE' option")
#             print("   - Linux: sudo apt-get install python3-tk")
#             print("   - macOS: brew install python-tk")
#         return False
    
#     print("✓ All dependencies installed!")
#     return True

# def show_menu():
#     """Display main menu"""
#     print("\n┌─────────────────────────────────────┐")
#     print("│         SELECT APPLICATION          │")
#     print("├─────────────────────────────────────┤")
#     print("│ 1. GUI Application (Recommended)    │")
#     print("│ 2. Command-Line Demo                │")
#     print("│ 3. Quick Test                       │")
#     print("│ 4. Plot Performance Graph           │")
#     print("│ 5. Exit                             │")
#     print("└─────────────────────────────────────┘")
#     print()

# def run_gui():
#     """Launch the GUI application"""
#     print("\n🚀 Launching GUI Application...")
#     print("   Please wait while the interface loads...\n")
#     try:
#         import rainbow_table_app
#         rainbow_table_app.main()
#     except Exception as e:
#         print(f"❌ Error launching GUI: {e}")
#         print("\nTroubleshooting:")
#         print("1. Ensure all dependencies are installed")
#         print("2. Check the INSTALLATION_GUIDE.md")
#         print("3. Try running: python rainbow_table_app.py")

# def run_demo():
#     """Launch the command-line demo"""
#     print("\n🚀 Launching Command-Line Demo...")
#     print("   This will demonstrate the rainbow table cracking process.\n")
#     try:
#         import rainbow_crack_demo
#         rainbow_crack_demo.main()
#     except Exception as e:
#         print(f"❌ Error launching demo: {e}")
#         print("\nTry running: python rainbow_crack_demo.py")

# def run_test():
#     """Run quick verification test"""
#     print("\n🧪 Running Quick Test...")
#     print("   Verifying rainbow table functionality...\n")
#     try:
#         import subprocess
#         result = subprocess.run([sys.executable, "test_rainbow.py"], 
#                               capture_output=False, text=True)
#         if result.returncode == 0:
#             print("\n✓ Test completed successfully!")
#         else:
#             print("\n❌ Test failed. Check error messages above.")
#     except Exception as e:
#         print(f"❌ Error running test: {e}")
#         print("\nTry running: python test_rainbow.py")

# def run_plot():
#     """Launch performance plot"""
#     print("\n📊 Launching Performance Graph...")
#     print("   Enter CUDA lookup time in milliseconds (or press Enter for demo):")
    
#     time_input = input("   Time (ms): ").strip()
    
#     if time_input:
#         try:
#             time_ms = float(time_input)
#         except ValueError:
#             print("   Invalid input. Using demo value: 2.5 ms")
#             time_ms = 2.5
#     else:
#         time_ms = 2.5
    
#     try:
#         import subprocess
#         subprocess.run([sys.executable, "plot_performance.py", str(time_ms)])
#     except Exception as e:
#         print(f"❌ Error launching plot: {e}")

# def main():
#     """Main application entry point"""
#     print_banner()
    
#     # Check dependencies
#     print("🔍 Checking dependencies...")
#     if not check_dependencies():
#         print("\n❌ Please install missing dependencies before continuing.")
#         print("   See INSTALLATION_GUIDE.md for detailed instructions.")
#         return
    
#     # Main loop
#     while True:
#         show_menu()
#         choice = input("Enter your choice (1-5): ").strip()
        
#         if choice == '1':
#             run_gui()
#             break  # Exit after GUI closes
#         elif choice == '2':
#             run_demo()
#             input("\nPress Enter to return to menu...")
#         elif choice == '3':
#             run_test()
#             input("\nPress Enter to return to menu...")
#         elif choice == '4':
#             run_plot()
#             input("\nPress Enter to return to menu...")
#         elif choice == '5':
#             print("\n👋 Thank you for using Rainbow Table Password Cracker!")
#             print("   Good luck with your final year project! 🎓\n")
#             break
#         else:
#             print("\n❌ Invalid choice. Please select 1-5.")

# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\n👋 Application terminated by user.")
#     except Exception as e:
#         print(f"\n❌ Unexpected error: {e}")
#         print("   Please check the documentation or try running individual scripts.")
