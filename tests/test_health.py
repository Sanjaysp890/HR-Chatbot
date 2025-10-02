import subprocess, time, requests, sys

def test_health():
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "api:app", "--port", "8000"])
    try:
        for _ in range(40):
            try:
                r = requests.get("http://127.0.0.1:8000/health", timeout=1)
                if r.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(0.25)
        else:
            raise AssertionError("health endpoint not ready")
        assert r.status_code == 200
    finally:
        proc.terminate()
