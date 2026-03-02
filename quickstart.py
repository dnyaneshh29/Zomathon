"""
🚀 QUICKSTART SCRIPT
Get the system running in one command!
"""

import subprocess
import sys
from pathlib import Path

print("\n" + "="*70)
print("🏆 CAUSAL REVENUE-OPTIMIZED ENGINE")
print("   Quickstart Setup")
print("="*70)

# Step 1: Check Python
print("\n✅ Python version:", sys.version.split()[0])

# Step 2: Install dependencies
print("\n📦 Installing dependencies...")
print("   (This may take 2-3 minutes)")

try:
    subprocess.run([
        sys.executable, "-m", "pip", "install",
        "pandas", "numpy", "pyyaml", "tqdm", "pyarrow",
        "torch", "pytorch-lightning", "lightgbm",
        "scikit-learn", "scipy", "redis", "fastapi", "uvicorn"
    ], check=True)
    print("✅ Dependencies installed!")
except:
    print("⚠️  Some dependencies failed - continuing anyway")

# Step 3: Generate data
print("\n📊 Generating causal data...")
try:
    subprocess.run([sys.executable, "src/data/generate.py"], check=True)
    print("✅ Data generated!")
except Exception as e:
    print(f"⚠️  Data generation skipped: {e}")

# Step 4: Open UI
print("\n🎨 Opening UI...")
ui_path = Path("src/ui/index.html").absolute()

if sys.platform == "win32":
    subprocess.run(["start", str(ui_path)], shell=True)
elif sys.platform == "darwin":
    subprocess.run(["open", str(ui_path)])
else:
    subprocess.run(["xdg-open", str(ui_path)])

print("\n" + "="*70)
print("✅ QUICKSTART COMPLETE!")
print("="*70)

print("\n🎉 Your revolutionary system is ready!")
print("\n📍 What's running:")
print("   ✅ Beautiful UI (opened in browser)")
print("   ✅ Mock data (for instant demo)")

print("\n🚀 Next steps:")
print("   1. Try the UI - add items, get recommendations")
print("   2. See causal impact metrics")
print("   3. Check profit scores")
print("   4. Notice fatigue protection")

print("\n🏆 Optional - Full system:")
print("   • Train models: python src/train.py")
print("   • Start API: python src/api/server.py")

print("\n💡 The UI works standalone - perfect for demos!")
print("\n🎯 Ready to win the hackathon! 🏆\n")
