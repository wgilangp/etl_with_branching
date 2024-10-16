# ETL with Airflow: Kaggle Dataset Extraction and Loading into SQLite

This repository contains a simple ETL (Extract, Transform, Load) process using Apache Airflow. The workflow extracts data from Kaggle datasets and loads them into an SQLite database. The ETL pipeline is orchestrated using Airflow and Docker. 

Special thanks to my mentor, [Galuhrama Ditya](https://github.com/galuhramaditya), for the guidance and support throughout this project.

## Project Overview

The main goal of this project is to demonstrate an Extract-Load (EL) process where data is extracted from Kaggle datasets using `kagglehub`, stored as CSV files in a staging area, and finally loaded into SQLite databases.

### DAG Features

- **Branching Logic**: A BranchPythonOperator selects which dataset to extract based on parameters.
- **Dataset Source**: Two datasets are downloaded from Kaggle using `kagglehub`:
  - Walmart Stock Data (`wmt_data.csv`)
  - Instagram Marketing Data (`Instagram-Data.csv`)
- **Data Loading**: After extraction, data is loaded into separate SQLite databases using `pandas` and `SQLAlchemy`.

## Getting Started

### Prerequisites

Before running this project, ensure you have the following installed:

- Docker
- Docker Compose
- Apache Airflow 2.6.2+
- Python 3.8+
- Kaggle account (though not using the Kaggle API directly)

### Installation

1. **Install Docker and Docker Compose**:

   Follow these steps to install Docker and Docker Compose:

   - **For Windows and macOS**:
     - Download the Docker Desktop installer from [Docker's official website](https://www.docker.com/products/docker-desktop).
     - Run the installer and follow the on-screen instructions.

   - **For Linux**:
     ```bash
     # Update your package index
     sudo apt-get update
     
     # Install Docker
     sudo apt-get install -y docker.io
     
     # Start Docker and enable it to run on startup
     sudo systemctl start docker
     sudo systemctl enable docker
     
     # Add your user to the Docker group (you might need to log out and back in)
     sudo usermod -aG docker $USER

     # Install Docker Compose
     sudo apt-get install -y docker-compose
     ```

2. **Clone the Airflow Docker repository**:

   Clone the repository that sets up Docker for Apache Airflow:

   ```bash
   git clone https://github.com/galuhramaditya/docker-airflow-jdk.git airflow
   cd airflow
   ```

3. **Install dependencies**:

   In your Dockerfile, ensure `kagglehub` is installed:

   ```Dockerfile
   FROM apache/airflow:2.6.2

   # Install dependencies
   RUN pip install kagglehub
   ```

4. **Download Datasets**:

   The DAG automatically downloads the datasets using `kagglehub`. No additional setup for Kaggle API keys is required.

### Configuration

This project uses `docker-compose.yaml` to orchestrate Airflow and other services. Ensure your Airflow instance is properly configured.

### Running the DAG

1. **Start Airflow**:

   Make sure you are in the project directory, then start the Airflow services:

   ```bash
   docker-compose up
   ```

2. **Trigger the DAG**:

   Access the Airflow web UI at `http://localhost:8080` and trigger the `etl_with_branching_kaggle` DAG. The DAG will download the Kaggle datasets and load them into SQLite databases.

## DAG Structure

- **Branching Logic**: The DAG uses a `BranchPythonOperator` to choose between the Walmart stock data and Instagram marketing data.
- **Extraction Tasks**:
  - `extract_walmart_data`: Downloads the Walmart stock data.
  - `extract_instagram_data`: Downloads the Instagram marketing data.
- **Loading Tasks**:
  - `load_walmart_to_sqlite`: Loads Walmart stock data into an SQLite database.
  - `load_instagram_to_sqlite`: Loads Instagram marketing data into an SQLite database.

## Files

- `Dockerfile`: Defines the Airflow environment and installs necessary dependencies like `kagglehub`.
- `dags/etl_with_branching_kaggle.py`: The main DAG definition.
- `docker-compose.yaml`: The Docker Compose setup for running Airflow.

## Troubleshooting

- Ensure that your Docker environment is properly set up and running.
- If dataset downloads fail, ensure that the `kagglehub` package is installed correctly in the Docker container.

### Contributions and Feedback

I welcome and appreciate contributions to this project. If you have any suggestions or improvements, feel free to submit a pull request or contact me directly with any questions or feedback.

#### Thank you for your interest in this project!