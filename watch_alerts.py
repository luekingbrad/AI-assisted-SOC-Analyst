import time
from pathlib import Path
from soc_ai import main

PROJECT_DIR = Path(__file__).parent

ALERT_FILE = PROJECT_DIR / "alerts.json"

def monitor():
    print("SOC Monitor Started...")
    print(f"Watching: {ALERT_FILE}")

    last_modified = ALERT_FILE.stat().st_mtime

    while True:
        try:
            current_modified = ALERT_FILE.stat().st_mtime

            if current_modified != last_modified:
                print("\nNew alert data detected!")
                print("Running AI analysis...\n")

                main()

                last_modified = current_modified

            time.sleep(5)

        except KeyboardInterrupt:
            print("\nSOC Monitor Stopped")
            break

        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor()
