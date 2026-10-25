"""Create synthetic South African personal-finance demo records."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from app.services.demo_data import seed_demo_data

def main():
    app = create_app()
    with app.app_context():
        if seed_demo_data():
            print("Created synthetic demo data for 2026.")
        else:
            print("Database already contains transactions; no demo data added.")

if __name__ == "__main__": main()
