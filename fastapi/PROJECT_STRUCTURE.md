# Rainbow Table Project - Complete File Structure

## 📁 Project Organization

```
D:\Final year\rainbow-table-project\
│
├── main.py                          # Main entry point (run this!)
├── rainbow_table_app.py             # GUI application
├── rainbow_crack_demo.py            # CLI demonstration
├── test_rainbow.py                  # Quick verification test
├── plot_performance.py              # Performance graph plotter
├── requirements.txt                 # Python dependencies
│
├── docs/
│   ├── README.md                    # Complete documentation
│   ├── QUICK_START.md               # 3-minute setup guide
│   ├── INSTALLATION_GUIDE.md        # Detailed installation
│   └── PRESENTATION_GUIDE.md        # Presentation slides
│
├── api/                             # API structure (optional)
│   └── utils.py                     # Utility functions
│
├── python/                          # Python scripts (optional)
│   └── plot_performance.py          # Alternative location for plot
│
└── cuda_core/                       # CUDA simulation (optional)
    └── src/
        └── cuda_rainbow.exe         # Simulated CUDA binary

```

## 🚀 How to Set Up

### Option 1: Simple Setup (Recommended)

Create a single folder with all main files:

```
D:\Final year\rainbow-project\
├── main.py
├── rainbow_table_app.py
├── rainbow_crack_demo.py
├── test_rainbow.py
├── plot_performance.py
├── requirements.txt
├── README.md
├── QUICK_START.md
├── INSTALLATION_GUIDE.md
└── PRESENTATION_GUIDE.md
```

**Steps:**
1. Create folder: `D:\Final year\rainbow-project`
2. Copy all downloaded files into this folder
3. Open Command Prompt in this folder
4. Run: `pip install -r requirements.txt`
5. Run: `python main.py`

### Option 2: Organized Structure

If you want the organized structure with folders:

```
D:\Final year\rainbow-table-project\
├── main.py
├── rainbow_table_app.py
├── rainbow_crack_demo.py
├── test_rainbow.py
├── plot_performance.py
├── requirements.txt
└── docs\
    ├── README.md
    ├── QUICK_START.md
    ├── INSTALLATION_GUIDE.md
    └── PRESENTATION_GUIDE.md
```

**Steps:**
1. Create main folder: `D:\Final year\rainbow-table-project`
2. Create subfolder: `docs`
3. Place Python files (*.py) in main folder
4. Place documentation (*.md) in docs folder
5. Place requirements.txt in main folder

## 📝 File Descriptions

### Core Application Files

| File | Description | When to Use |
|------|-------------|-------------|
| **main.py** | Main menu launcher | Run this first! |
| **rainbow_table_app.py** | Full GUI application | For demo/presentation |
| **rainbow_crack_demo.py** | Command-line version | For automated testing |
| **test_rainbow.py** | Quick verification | To test setup |
| **plot_performance.py** | Graph plotter | For performance visualization |
| **requirements.txt** | Dependencies list | For pip install |

### Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete project overview |
| **QUICK_START.md** | Fast 3-minute setup |
| **INSTALLATION_GUIDE.md** | Detailed installation help |
| **PRESENTATION_GUIDE.md** | Presentation slides & script |

## 🎯 Quick Start Commands

### Windows:

```cmd
# Navigate to project folder
cd D:\Final year\rainbow-project

# Install dependencies
pip install -r requirements.txt

# Run main application
python main.py

# Or run GUI directly
python rainbow_table_app.py

# Or run demo
python rainbow_crack_demo.py
```

### macOS/Linux:

```bash
# Navigate to project folder
cd ~/FinalYear/rainbow-project

# Install dependencies
pip3 install -r requirements.txt

# Run main application
python3 main.py

# Or run GUI directly
python3 rainbow_table_app.py
```

## 🔧 What Each File Does

### 1. main.py
- Entry point with menu
- Checks dependencies
- Launches other applications
- **Run this to start!**

### 2. rainbow_table_app.py
- Full graphical interface
- Rainbow table generation
- Hash cracking
- Real-time graphs
- Performance metrics
- **Best for demonstrations!**

### 3. rainbow_crack_demo.py
- Command-line version
- Automated demonstration
- Shows statistics
- No GUI required
- **Good for testing!**

### 4. test_rainbow.py
- Quick verification
- Tests hash cracking
- Validates setup
- **Run to verify installation!**

### 5. plot_performance.py
- Creates performance graphs
- Visualizes CUDA metrics
- Standalone plotting
- **For graph generation!**

## 📊 Workflow

```
1. Setup
   ↓
   Install Python → Install dependencies → Verify with test

2. Development
   ↓
   Run main.py → Choose GUI → Generate table → Crack hash

3. Presentation
   ↓
   Prepare slides → Practice demo → Run live demonstration

4. Testing
   ↓
   test_rainbow.py → rainbow_crack_demo.py → Success tests
```

## 🎓 For Your Final Year Project

### Minimal Setup (Fastest):

```
rainbow-project\
├── main.py
├── rainbow_table_app.py
├── requirements.txt
└── README.md
```

This is enough to demonstrate the project!

### Complete Setup (Best):

```
rainbow-table-project\
├── main.py
├── rainbow_table_app.py
├── rainbow_crack_demo.py
├── test_rainbow.py
├── plot_performance.py
├── requirements.txt
├── README.md
├── QUICK_START.md
├── INSTALLATION_GUIDE.md
└── PRESENTATION_GUIDE.md
```

This includes everything for a professional submission!

## 💡 Tips

1. **Keep it simple**: Start with Option 1 (flat structure)
2. **Test first**: Run `test_rainbow.py` to verify
3. **Use main.py**: It provides a nice menu
4. **For demo**: Use `rainbow_table_app.py` directly
5. **Have backups**: Keep copies of all files

## ✅ Verification Checklist

- [ ] All files in correct folder
- [ ] Python installed (3.7+)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Test passes (`python test_rainbow.py`)
- [ ] GUI launches (`python rainbow_table_app.py`)
- [ ] Hash cracks successfully (test@123)
- [ ] Graphs display correctly

## 🆘 If You Get Lost

**Just remember these 3 files are essential:**

1. `rainbow_table_app.py` - The main program
2. `requirements.txt` - Dependencies
3. `README.md` - Instructions

Everything else is optional but helpful!

---

**Created**: All files ready to use
**Location**: Save to `D:\Final year\rainbow-project\`
**Next Step**: Run `python main.py`

Good luck! 🎓✨
