# 📂 Spam Detection Using Artificial Intelligence

## ✨ Project Overview

This project is a **production-grade, containerized microservice** that classifies text-based inputs (such as posts or comments) as **"spam" or "not\_spam"** with a confidence score. The microservice is fully offline, built with FastAPI, and follows strict REST API standards.

It is specifically trained on **Indian context data**, including WhatsApp-style text, Hinglish, and regional scam patterns.

---

## 📋 Table of Contents

* [Project Overview](#-project-overview)
* [Project Pipeline](#-project-pipeline)
* [Tech Stack](#-tech-stack)
* [Data Collection](#-data-collection)
* [Data Preprocessing](#-data-preprocessing)
* [Functional Requirements](#-functional-requirements)
* [Model Selection](#-model-selection)
* [Model Training & Evaluation](#-model-training--evaluation)
* [Microservice Design](#-microservice-design)
* [Dockerization](#-dockerization)
* [Configuration Management](#-configuration-management)
* [Testing & Validation](#-testing--validation)
* [Project Structure](#-project-structure)
* [Installation](#-installation)
* [Usage](#-usage)
* [Contributors](#-contributors)

---

## 🔗 Project Pipeline

```text
Dataset Collection → Preprocessing → Model Training → Model Evaluation → API Development → Dockerization → Testing → Deployment
```

---

## 🛠️ Tech Stack

* **Programming Language:** Python 3.x
* **Machine Learning:** scikit-learn
* **Vectorization:** TF-IDF
* **Classifier:** Logistic Regression
* **API Framework:** FastAPI
* **Containerization:** Docker
* **Testing:** FastAPI TestClient, unittest
* **Configuration:** config.json

---

## 📅️ Data Collection

* **Sources:**

  * Real-world spam and ham messages collected from the [India Spam SMS Classification Dataset](https://github.com/junioralive/india-spam-sms-classification/tree/main/dataset).
  * Synthetic data generated using ChatGPT to simulate Indian context messages, including WhatsApp-style spam, scam offers, and Hinglish content.
* **Dataset Size:**

  * Total: Approximately 3,500 labeled entries
  * Combination of original and synthetic data to ensure diversity and balance.

---

## 🧹 Data Preprocessing

* Lowercasing
* Punctuation and URL removal
* Stopword filtering
* Tokenization
* Vectorization using TF-IDF

---

## ✅ Functional Requirements

* **Input:**

  * Method: `POST /predict`
  * Payload:

    ```json
    {
      "post": "Win a free recharge now! Click this link!"
    }
    ```

* **Output:**

  * JSON response:

    ```json
    {
      "label": "spam",
      "confidence": 0.93
    }
    ```
  * Confidence: A float between 0.0 and 1.0.

* **API Endpoints:**

  * `POST /predict` - Classify input text.
  * `GET /health` - Return system health status.
  * `GET /version` - Return model version and configuration metadata.

---

## 🧐 Model Selection

### Model Chosen:

* **Vectorizer:** TF-IDF
* **Classifier:** Logistic Regression

### Why This Model?

* Logistic Regression is **robust, interpretable, and effective** for binary classification tasks.
* TF-IDF efficiently transforms text into a numerical form suited for Logistic Regression.
* Logistic Regression provides **probabilistic outputs (confidence scores)**, which meet project requirements.
* Logistic Regression performed better in terms of precision and recall compared to Naive Bayes for this dataset.

---

## 📈 Model Training & Evaluation

* Trained using 3,500 labeled entries balanced between "spam" and "not\_spam".
* Dataset focused on **Indian context**: INR-specific scams, Hinglish, WhatsApp-like messages.
* **Evaluation Metrics:**

  * Accuracy
  * Confusion Matrix
* **Output Artifacts:**

  * Trained model pipeline (preprocessor, vectorizer, and classifier bundled together): `model/model.joblib`

---

## 🖥️ Microservice Design

* **Framework:** FastAPI
* **Input Format:** JSON only
* **Endpoints:**

  * `POST /predict`: Classifies the input post.
  * `GET /health`: Checks service health.
  * `GET /version`: Returns model version and config settings.
* **Output Schema:** Defined by `schema.json`
* **Response Time:** <1 second per request

---

## 🐳 Dockerization

* Production-ready Dockerfile.
* Runs entirely offline inside the container.
* Exposes port 8000.
* Commands:

  ```bash
  docker build -t spam-detector .
  docker run -p 8000:8000 spam-detector
  ```

---

## ⚙️ Configuration Management

* Uses a **runtime `config.json` file.**
* App must terminate if `config.json` is missing or invalid.
* Configuration drives runtime behavior like thresholds and logging.

---

## 🤮 Testing & Validation

* Validates response structure and confidence score.
* All endpoints tested for proper response.
* Service must follow the structure defined in `schema.json`.

---

## 📂 Project Structure

```text
SpamDetector/
│
├── app/
│   ├── __init__.py                 # Marks app as a Python package
│   ├── main.py                     # FastAPI app (API routes and server logic)
│   ├── generator.py                # Model loading, config loading, prediction logic
│   ├── logger.py                   # Logging configuration and prediction logging
│   ├── preprocessor.py             # Custom text preprocessing class
│   ├── config_validator.py         # Pydantic schema validation for config.json
│   └── model/
│       └── model.joblib            # Trained model pipeline (saved with joblib)
│
├── data/
│   └── dataset_updated.csv         # Dataset used for training
│
├── tests/
│   ├── test_api.py                 # API endpoint tests using pytest
│   ├── test_unittest.py            # Unittest class for preprocessor and API testing
│   ├── test3.py                    # Additional tests: invalid input, missing keys, config schema validation
│   └── __init__.py                 # Marks tests as a Python package
│
├── config.json                     # Runtime configuration (thresholds, labels, logging)
├── schema.json                     # Input validation schema for API requests
├── requirements.txt                # Project dependencies
├── Dockerfile                      # Docker setup to containerize the API
├── .dockerignore                   # Files and folders to exclude from Docker image
├── train_model.py                  # Model training script
├── README.md                       # Project documentation (optional but recommended)
```

---

## 🛠️ Installation

```bash
git clone <https://github.com/PBS-Alekhya/SpamDetectionUsingAI>
cd spam-detector
pip install -r requirements.txt
```

---

## ▶️ Usage

### Running the App Locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker Run

```bash
docker build -t spam-detector .
docker run -p 8000:8000 spam-detector
```

### Example API Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"post": "Win free recharge now!"}'
```

### Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## 👥 Contributors

* Alekhya Pepakayala – [GitHub Profile](https://github.com/)
