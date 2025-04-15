# Application-Monitoring-Dashboard

This repository contains the code and setup for the **Application Monitoring Dashboard** project. 

---

## 🗓️ Week 1: Setup and Initial Configuration


---

### 📦 Prerequisites

Before running the project, ensure you have pip installed, if not then follow the below 2 commands:
```bash
sudo apt update 
sudo apt install python3 python3-pip python3-venv -y 
```
To install Kafka and fastapi, run the below in your root directory:
```bash
python3 -m venv env 
source env/bin/activate 
pip install fastapi uvicorn kafka-python 
```
---

### 🚀 Running the Week 1 Setup

Follow these steps to get the project running:

1. **Clone the repository:**

    First, clone the repository to your local machine:

    ```bash
    git clone https://github.com/HannahAlex004/Application-Monitoring-Dashboard.git
    cd Application-Monitoring-Dashboard
    ```

2. **Install dependencies:**

   Mentioned in prequisites.

3. **Check the setup:**

    1. Successsful API Responses and Errors [200 OK nand 404/500]
    ```bash
    python3 -m uvicorn app:app --reload
    ```
    Open http://localhost:8000/docs in a browser. 
    Click on endpoints like /users/1, /error-test, etc, to see if they work. 
    
    2. Continuous random API calls with status codes
    ```bash
    python3 load_test.py
    ```
    Show real-time logs: 
            Hit /users/1 → Status: 200 
            Hit /error-test → Status: 500 
    
    3. Kafka running in Docker
    Kafka and Zookeeper containers running. 
    Topics (api-logs, error-logs) created.
    Check running containers:
     ```bash
    docker ps
    ```
    List Kafka topics:
     ```bash
    docker exec -it kafka_kafka_1 bash 
    kafka-topics --list --bootstrap-server localhost:9092 
    exit 
    ```

    4. Kafka Producer Logging API Requests
    ```bash
    docker exec -it kafka_kafka_1 bash 
    kafka-console-consumer --topic api-logs --bootstrap-server localhost:9092
    ```

    5. Dockerized setup
    ```bash
    cat docker-compose.yml
    docker-compose down && docker-compose up-d
    curl http://localhost:8000/
    docker-compose logs
    ```

## 🗓️ Week 2: Kafka Consumer and MySQL Integration
---

### 📦 Prerequisites
You should have the following prerequisites installed and set up:

- **Docker**: For running MySQL and Kafka.
- **Kafka Consumer**: Python script to read from Kafka and insert logs into MySQL.
- **MySQL Database**: For storing the logs.
---
### 🚀 Steps to Run Week 2

#### 1. Ensure MySQL is Running in Docker

Make sure your **MySQL database** is set up and running using Docker. You can start it using:

```bash
docker-compose up -d
```
Check the containers are running by listing active containers:
```bash
docker ps
```
#### 2. Create the logdb Database in MySQL

Make sure your **MySQL database** is set up and running using Docker. 

### 3. Run the Kafka Consumer Script
```bash
python3 consumer.py
```
Expected Output:
```bash
MySQL connection successful.
Starting consumer...
```
### 4. Verify logs in MySQL
```bash
USE logdb;
SELECT * FROM logs;
```
