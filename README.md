
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
source env/bin/activate 
python3 -m uvicorn app:app --reload
```

Open `http://localhost:8000/docs` to test endpoints like `/users/1` and `/error-test`.

4. **Run Load Testing Script:**
 `New terminal`
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

 `New terminal`
```bash
docker ps
docker exec -it kafka_kafka_1 bash
kafka-topics --list --bootstrap-server localhost:9092
exit
```

6. **View Logs via Kafka Console Consumer:**

 `New terminal`
```bash
docker exec -it kafka_kafka_1 bash
kafka-console-consumer --topic api-logs --bootstrap-server localhost:9092
```

7. **Dockerized Setup:**

 `New terminal`
```bash
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
   
(Run this script only if Week 2 is being done separately. Otherwise, no need to run again!)

Terminal 1
```bash
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

Update `docker-compose.yml` to have grafana:

---

### 2. Start All Services to update grafana:

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


## 📊 Creating a Dashboard in Grafana (Updated UI)

### 1. Create a New Dashboard
- Look for the "Dashboards" icon (four squares) in the left menu.
- Click **"New"** (button on the top-right).
- Select **"New Dashboard"**.
   **or**
- Click on " + " and click on new dashboards
  
### 3. Add a Panel
You'll see an empty dashboard.
- Click **"Add visualization"** (or "Add panel").

**Adding Your First Panel (Example: Request Count)**
- Select Data Source:
- Choose **MySQL** (the one you configured earlier).
- Switch to **Code** Mode (SQL):
- Click the **"Edit SQL"** button (or select "SQL" from the query type dropdown).
- Paste the SQL Query.

### 4. Visualization Settings
- Under **"Visualization"** (right sidebar), select **"Bar chart"**.
- Set a Panel title (e.g., "Request Count by Endpoint").
- Save the Panel: Click **"Apply"** (top-right).

## SQL Queries to Use (Create Panels)

#### 1. Request Count per Endpoint(Panel 1)
```sql
SELECT
  url AS metric,
  COUNT(*) AS count
FROM logs
GROUP BY url
ORDER BY count DESC;
```
Visualization: **Bar chart**   

Panel Title: `Request Count by Endpoint`

#### 2. Response Time Trends(Panel 2)
```sql
SELECT
  timestamp AS time,
  duration AS value,
  url AS metric
FROM logs;
```
Visualization: **Time Series**

Panel Title: `Response Time Trends`

#### 3. Most Frequent Errors(Panel 3)
```sql
SELECT
  url AS metric,
  COUNT(*) AS error_count
FROM logs
WHERE error = 1
GROUP BY url
ORDER BY error_count DESC;
```
Visualization: **Bar chart or Table**

Panel Title: `Most Frequent Errors`

#### 4. Real-Time Logs Feed(Panel 4)
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
LIMIT 100;
```
Visualization: **Table**

Panel Title: `Real-Time Logs Feed`

---

### 5. ✅ Add more panels if needed!


