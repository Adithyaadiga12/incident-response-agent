import logging
import requests


def reset_logs():
    """Reset the log file by clearing its contents."""
    logging.shutdown()
    open("app.log","w").close()
    
def trigger_fault(mode:str,hits : int = 3):
    """Set a fault on the running app and hit /data a few times to generate logs."""
    requests.post(f"http://localhost:8000/fault/{mode}")
    for _ in range(hits):
        try:
            requests.get("http://localhost:8000/data")
        except Exception:
            pass


if __name__ == "__main__":
    reset_logs()
    trigger_fault("crash")
    print("Done. Check app.log for crash errors.")
        