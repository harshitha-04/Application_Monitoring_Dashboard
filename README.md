
# Application-Monitoring-Dashboard

This repository contains the code and setup for the **Application Monitoring Dashboard** project, including API generation, Kafka-based logging, MySQL integration, and Grafana-based visualization.

---

## 🗓️ Week 1: Setup and Initial Configuration

---

### 📦 Prerequisites

Before running the project, ensure you have the following installed:

```bash
sudo apt update 
sudo apt install python3 python3-pip python3-venv -y 
```

To install FastAPI and Kafka Python client:

```bash
python3 -m venv env 
source env/bin/activate 
pip install fastapi uvicorn kafka-python 
```

---

### 🚀 Running the Week 1 Setup

1. **Clone the repository:**

```bash
git clone https://github.com/HannahAlex004/Application-Monitoring-Dashboard.git
cd Application-Monitoring-Dashboard
```

2. **Install dependencies:**  
   (Already covered in prerequisites)

3. **Start FastAPI Server:**

```bash
python3 -m uvicorn app:app --reload
```

Open `http://localhost:8000/docs` to test endpoints like `/users/1` and `/error-test`.

4. **Run Load Testing Script:**

```bash
python3 load_test.py
```

Expected log output:
```
Hit /users/1 → Status: 200 
Hit /error-test → Status: 500 
```

5. **Kafka Setup in Docker:**
- Ensure Kafka and Zookeeper are up via Docker.
- Topics (`api-logs`, `error-logs`) should be created.

```bash
docker ps
docker exec -it kafka_kafka_1 bash
kafka-topics --list --bootstrap-server localhost:9092
exit
```

6. **View Logs via Kafka Console Consumer:**

```bash
docker exec -it kafka_kafka_1 bash
kafka-console-consumer --topic api-logs --bootstrap-server localhost:9092
```

7. **Dockerized Setup:**

```bash
cat docker-compose.yml
docker-compose down && docker-compose up -d
curl http://localhost:8000/
docker-compose logs
```

---

## 🗓️ Week 2: Kafka Consumer and MySQL Integration

---

### 📦 Prerequisites

- Docker installed
- Kafka and MySQL running via Docker Compose
- Python Kafka Consumer script (`consumer.py`)

---

### 🚀 Steps to Run Week 2

1. **Start Docker Services:**

```bash
docker-compose up -d
docker ps
```

2. **Create MySQL Database and Table:**

Use **MySQL Workbench** or login via **terminal** to the MySQL container and run the following SQL code to set up the `logdb` database and `logs` table:

```sql
CREATE DATABASE IF NOT EXISTS logdb;
USE logdb;

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    method VARCHAR(10),
    url TEXT,
    status INT,
    duration FLOAT,
    error BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT ALL PRIVILEGES ON logdb.* TO 'root'@'localhost';
FLUSH PRIVILEGES;

INSERT INTO logs (method, url, status, duration, error)
VALUES ('GET', 'https://example.com/api', 200, 0.15, false);

SELECT * FROM logs;
```

3. **Run load testing script:**
   
(Run this script only if Week 2 is being done separately. Otherwise, skip it.)

Terminal 1
```bash
python3 -m venv env 
source env/bin/activate
python3 -m uvicorn app:app --reload
```
Terminal 2
```bash
python3 load_test.py
```

Expected log output:
```
Hit /users/1 → Status: 200 
Hit /error-test → Status: 500 
```

4. **Run Kafka Consumer Script:**
In new Terminal
```bash
python3 consumer.py
```

Expected Output:
```
MySQL connection successful.
Starting consumer...
```

5. **Check Logs in MySQL:**

```sql
USE logdb;
SELECT * FROM logs;
```

---

## 🗓️ Week 3: Grafana Dashboard for Visualization

---

### 1. Add Grafana to Docker Compose

Update `docker-compose.yml` or create `docker-consumer.yml` with:

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.3.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181

  kafka:
    image: confluentinc/cp-kafka:7.3.0
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1

  mysql:
    image: mysql:8.4.4
    environment:
      MYSQL_ROOT_PASSWORD: xxx
      MYSQL_DATABASE: logdb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - kafka

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    depends_on:
      - mysql
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  mysql_data:
  grafana_data:
```

---

### 2. Start All Services:

```bash
docker-compose -f docker-consumer.yml up -d
```

---

### 3. Configure Grafana

- Access Grafana at: [http://localhost:3000](http://localhost:3000)
- Login: `admin/admin`
- Change password if prompted

**Add MySQL as Data Source:**

- Go to ⚙️ Configuration > Data Sources
- Add data source → Select **MySQL**
- Configure:
  - Name: `MySQL`
  - Host: `mysql:3306`
  - Database: `logdb`
  - User: `root`
  - Password: `xxx` (your MySQL password)
  - TLS/SSL: Disabled
- Click **Save & Test**

---

### 4. Create Dashboard Panels

#### Panel 1: Request Count per Endpoint

```sql
SELECT
  url AS metric,
  COUNT(*) AS count
FROM logs
GROUP BY url
ORDER BY count DESC
```

Visualization: **Bar chart**  
Panel Title: `Request Count by Endpoint`

---

#### Panel 2: Response Time Trends

```sql
SELECT
  timestamp AS time,
  duration AS value,
  url AS metric
FROM logs
```

Visualization: **Time Series**

---

#### Panel 3: Most Frequent Errors

```sql
SELECT
  url AS metric,
  COUNT(*) AS error_count
FROM logs
WHERE error = 1
GROUP BY url
ORDER BY error_count DESC
```

Visualization: **Bar chart or Table**

---

#### Panel 4: Real-Time Logs Feed

```sql
SELECT
  timestamp,
  method,
  url,
  status,
  duration,
  error
FROM logs
ORDER BY timestamp DESC
LIMIT 100
```

Visualization: **Table**

---

### ✅ You can add more panels as needed based on log data!
