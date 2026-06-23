
# Retail Sales Lakehouse Pipeline

## Project Overview

Retail Sales Lakehouse Pipeline is an end-to-end Data Engineering project that simulates a real-world retail analytics workflow. The project demonstrates how raw retail transaction data can be processed through a Medallion Architecture (Bronze, Silver, and Gold layers) using Databricks and PySpark, and then visualized through an interactive Streamlit dashboard.

The project was developed to strengthen practical skills in Data Engineering, ETL pipelines, Databricks, Apache Spark, Data Analytics, and Data Visualization.

---

## Project Objectives

* Generate synthetic retail sales data using Python
* Build an ETL pipeline using Databricks and PySpark
* Implement Medallion Architecture (Bronze, Silver, Gold)
* Create business-ready aggregated datasets
* Visualize insights using Streamlit and Plotly
* Apply Data Engineering concepts learned through IBM Data Engineering coursework
* Maintain professional version control using Git and GitHub

---

## Dataset

The project uses a synthetic retail sales dataset generated programmatically using Python.

### Dataset Fields

| Column     | Description               |
| ---------- | ------------------------- |
| OrderID    | Unique order identifier   |
| Product    | Product name              |
| CustomerID | Customer identifier       |
| Date       | Transaction date          |
| Price      | Unit price                |
| Quantity   | Number of units purchased |
| City       | Customer city             |
| Region     | Geographic region         |

---

## Architecture

```text
Synthetic Retail Dataset
          │
          ▼
     Bronze Layer
 (Raw Ingested Data)
          │
          ▼
     Silver Layer
(Cleaned & Enriched Data)
          │
          ▼
      Gold Layer
(Business Aggregations)
          │
          ▼
 Streamlit Dashboard
```

---

## Medallion Architecture

### Bronze Layer

Stores raw retail transaction data exactly as ingested.

Activities:

* Data ingestion
* Schema validation
* Raw data storage

Output:

```text
bronze_sales
```

---

### Silver Layer

Transforms and cleans the Bronze data.

Activities:

* Data type conversion
* Null value handling
* Revenue calculation

Derived Column:

```text
Revenue = Price × Quantity
```

Output:

```text
silver_sales
```

---

### Gold Layer

Creates business-level aggregated tables for reporting and analytics.

Generated Tables:

### Daily Revenue

```text
gold_daily_revenue
```

### Revenue by Product

```text
gold_product_revenue
```

### Revenue by Region

```text
gold_region_revenue
```

---

## Dashboard

An interactive Streamlit dashboard was developed to visualize the Gold Layer data.

### Dashboard Features

* Revenue by Product Analysis
* Revenue by Region Analysis
* Daily Revenue Trends
* Interactive Charts using Plotly
* Data Exploration Tables

---

## Technologies Used

### Programming

* Python
* sql

### Data Processing

* Pandas
* NumPy
* PySpark

### Data Engineering

* Databricks

### Visualization

* Streamlit
* Plotly

### Version Control

* Git
* GitHub

---

## Project Structure

```text
retail_sales_pipeline/
│
├── dashboard.py
├── generate_data.py
├── State_01.py
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── silver/
│   └── gold/
│
└── databricks/
    └── notebooks/
```

---

## Learning Outcomes

This project demonstrates practical experience in:

* ETL Pipeline Development
* Data Cleaning and Transformation
* Databricks Lakehouse Architecture
* Apache Spark (PySpark)
* Medallion Architecture
* Streamlit Dashboard Development
* Git and GitHub Workflow
* Data Engineering Best Practices

---

## Future Improvements

* Airflow Pipeline Automation
* AWS S3 Integration
* MLflow Experiment Tracking
* Real-Time Data Streaming
* Docker Containerization
* Cloud Deployment
* Advanced Analytics Layer

---

## Author

**Dahamya**

Data Science Undergraduate

Areas of Interest:

* Data Engineering
* Machine Learning
* MLOps
* Data Analytics
* Lakehouse Architecture

---
