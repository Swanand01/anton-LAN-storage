import os
import subprocess
import sys


def main():
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

    print("🚀 Starting Anton LAN Storage...")
    os.execvp("python", ["python", "app.py"])


if __name__ == "__main__":
    main()
