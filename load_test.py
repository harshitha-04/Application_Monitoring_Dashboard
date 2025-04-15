import requests 
import time 
import random 
 
API_BASE = "http://localhost:8000" 
ENDPOINTS = [ 
    "/", 
    "/users/1", 
    "/products/101", 
    "/slow-endpoint", 
    "/error-test" 
] 
 
def simulate_traffic(): 
    while True: 
        endpoint = random.choice(ENDPOINTS) 
        try: 
            response = requests.get(f"{API_BASE}{endpoint}") 
            print(f"Hit {endpoint} → Status: {response.status_code}") 
        except Exception as e: 
            print(f"Error on {endpoint}: {e}") 
        time.sleep(random.uniform(0.1, 1.0)) 
 
if __name__ == "__main__": 
    simulate_traffic()
