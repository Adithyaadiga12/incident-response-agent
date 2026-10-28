import time
import random
import logging 
from fastapi import FastAPI

app = FastAPI()

STATE = {"fault": "none"}

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.get('/health')
def health():
    return {"status": "OK"}

@app.get('/data')
def data():
    fault = STATE["fault"]
    logging.info("GET /data called, fault=%s", fault)
    
    if fault == "slow":
        time.sleep(3)
        logging.warning("GET /data served slowly (3s)")
        return {"data":"finally done"}
    
    if fault == "crash":
        logging.error("GET /data failed: database connection failed")
        raise Exception("DB Connection failed")
    
    if fault == "errors" and random.random() < 0.5:
        logging.error("GET /data failed: random upstream error")
        raise Exception("Random failure occurred")
    
    return {"data": "here is your data"}

@app.post("/fault/{mode}")
def set_fault(mode : str):
    STATE["fault"] = mode
    logging.info("fault set to %s", mode)
    return {"fault_now": mode}
