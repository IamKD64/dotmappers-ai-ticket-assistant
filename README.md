# AI Support Ticket Assistant

## Project Overview

For this assessment, I developed an AI-powered Support Ticket Assistant that enables users to analyze customer support tickets using natural language queries.

The application loads support ticket data from a CSV file, processes user questions using a Large Language Model (LLM), detects anomalies, and presents results through both a FastAPI backend and a Streamlit dashboard.

The objective of this project was to combine natural language understanding, data analytics, anomaly detection, and interactive visualization into a single end-to-end AI application.

---

## Features

### Natural Language Querying

Users can ask questions in plain English, including:

* How many tickets are open?
* How many tickets are resolved?
* Which agent has the highest rating?
* Which agent has the lowest rating?
* Which category has the most tickets?
* What is the average resolution time?
* Are there any unresolved critical tickets?
* Show tickets requiring immediate attention.

### AI-Powered Responses

The system uses Groq's Llama 3.3 70B model to:

* Interpret user intent
* Understand different phrasings of the same question
* Generate business-friendly explanations
* Improve overall user experience

### Anomaly Detection

The application automatically identifies:

* Tickets with unusually long resolution times
* Critical unresolved tickets
* Operational issues requiring immediate attention

### Interactive Dashboard

The Streamlit dashboard provides:

* Ticket statistics
* Anomaly metrics
* Natural language query interface
* Dataset exploration

### REST API

The FastAPI backend exposes endpoints for:

* Health checks
* Natural language querying
* Dataset schema inspection
* Anomaly detection

---

## System Architecture

```text
User Question
      │
      ▼
Streamlit Dashboard
      │
      ▼
FastAPI Backend
      │
      ├── Data Loader
      ├── Query Engine
      ├── LLM Service
      └── Anomaly Detector
      │
      ▼
Support Tickets Dataset
      │
      ▼
Analytics Results
```

### Components

#### Data Loader

Loads and validates the support ticket dataset from the CSV file.

#### Query Engine

Processes analytical questions and executes data operations using Pandas.

#### LLM Service

Uses Groq's Llama 3.3 70B model to understand user intent and generate explanations.

#### Anomaly Detector

Identifies abnormal ticket behavior such as long resolution times and unresolved critical issues.

---

## Technology Stack

### Backend

* Python
* FastAPI
* Pandas
* NumPy

### Frontend

* Streamlit

### AI / LLM

* Groq API
* Llama 3.3 70B Versatile

### Data Source

* CSV Dataset (support_tickets.csv)

---

## Project Structure

```text
DotMappers/
│
├── app/
│   ├── main.py
│   ├── data_loader.py
│   ├── query_engine.py
│   ├── llm_service.py
│   ├── anomaly_detector.py
│   └── config.py
│
├── data/
│   └── support_tickets.csv
│
├── ui/
│   └── dotai_app.py
│
├── requirements.txt
├── README.md
└── .env.example
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd DotMappers
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Quick Start

### Start FastAPI Backend

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

### Start Streamlit Dashboard

```bash
streamlit run ui/dotai_app.py
```

Dashboard URL:

```text
http://localhost:8501
```

---

## API Endpoints

### Health Check

```http
GET /health
```

Returns application status and dataset information.

### Natural Language Query

```http
POST /query
```

Example Request:

```json
{
  "question": "Which agent has the highest rating?"
}
```

### Dataset Schema

```http
GET /schema
```

Returns dataset column information and metadata.

### Anomaly Detection

```http
GET /anomalies
```

Returns anomaly statistics and ticket details.

---

## Example Queries

### Agent Performance

* Which agent has the highest rating?
* Which support representative performs best?
* Who receives the worst customer feedback?
* Which agent resolves tickets fastest?

### Ticket Analytics

* How many tickets are open?
* How many tickets are resolved?
* Which category has the most tickets?
* Which category has the least tickets?

### Customer Satisfaction

* Which category has the highest customer satisfaction?
* Which agent has the lowest customer rating?

### Operational Monitoring

* Show unresolved critical tickets.
* How many anomalies are present?
* Show tickets requiring immediate attention.

### Business Insights

* What trends do you observe in the support data?
* Summarize the health of the support operation.

---

## Anomaly Detection Logic

The system currently identifies two major anomaly types:

### Long Resolution Time Tickets

Tickets whose resolution time exceeds the normal operational threshold.

### Critical Unresolved Tickets

Tickets that:

* Have Critical priority
* Are not resolved
* Require immediate attention

Current dataset results:

* Total Anomalies: 48
* Long Resolution Tickets: 17
* Critical Unresolved Tickets: 31

---

## Challenges Faced

One challenge was handling multiple ways users could ask the same question.

For example:

* Which agent has the highest rating?
* Who performs best?
* Who gets the best customer feedback?

Although phrased differently, these questions should produce the same result.

To address this challenge, I combined LLM-based intent understanding with structured data analysis using Pandas.

Another challenge was presenting analytical results in a way that remains easy for non-technical users to understand.

---

## Limitations

* The dataset is static and CSV-based.
* No authentication or user management has been implemented.
* Multi-turn conversation support is limited.
* Query accuracy depends on LLM-generated interpretations.
* Historical trend analysis is limited to the available dataset.

---

## Future Improvements

Given additional time, I would:

* Add conversational memory.
* Implement semantic search using vector databases.
* Integrate with live ticketing systems.
* Add advanced machine learning-based anomaly detection.
* Containerize the application using Docker.
* Deploy the system on a cloud platform.

---

## Conclusion

This project demonstrates how Large Language Models can be combined with traditional data analytics to create a natural language interface for business data. The system allows users to explore support ticket information conversationally while identifying operational risks through anomaly detection.

---

## Author

**Dhanushkumar K**

AI Engineer Assessment Submission

DOTMappers IT Pvt. Ltd.
