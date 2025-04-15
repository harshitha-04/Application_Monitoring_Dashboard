
from fastapi import FastAPI, HTTPException 
import logging 
import random 
import time 
from pydantic import BaseModel 
 
from kafka import KafkaProducer 
import json 
 
producer = KafkaProducer( 
    bootstrap_servers='localhost:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8') 
) 
 
app = FastAPI() 
 
# Mock Database 
users_db = {"1": "Alice", "2": "Bob"} 
products_db = {"101": "Laptop", "102": "Phone"} 
 
# --- API Endpoints --- 
@app.get("/") 
def home(): 
    return {"message": "Welcome to the API!"} 
 
@app.get("/users/{user_id}") 
def get_user(user_id: str): 
    if user_id not in users_db: 
        raise HTTPException(status_code=404, detail="User not found") 
    return {"user_id": user_id, "name": users_db[user_id]} 
 
@app.get("/products/{product_id}") 
def get_product(product_id: str): 
    if product_id not in products_db: 
        raise HTTPException(status_code=404, detail="Product not found") 
    return {"product_id": product_id, "name": products_db[product_id]} 
 
@app.post("/users") 
def create_user(name: str): 
    user_id = str(random.randint(3, 100)) 
    users_db[user_id] = name 
    return {"user_id": user_id, "name": name} 
 
@app.get("/slow-endpoint") 
def slow_endpoint(): 
    time.sleep(2)  # Simulate slow response 
    return {"message": "This was slow!"} 
 
@app.get("/error-test") 
def error_test(): 
    if random.random() > 0.5: 
        raise HTTPException(status_code=500, detail="Random error occurred!") 
    return {"message": "Success!"} 
 
# --- Logging Setup --- 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
 
@app.middleware("http") 
async def log_requests(request, call_next): 
    start_time = time.time() 
    response = await call_next(request) 
    duration = time.time() - start_time 
 
    log_data = { 
        "method": request.method, 
        "url": str(request.url), 
        "status": response.status_code, 
        "duration": duration, 
        "error": response.status_code >= 400 
    } 
 
    producer.send("api-logs", log_data) 
    if log_data["error"]: 
        producer.send("error-logs", log_data) 
    return response