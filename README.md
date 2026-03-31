# 🧬 MedVault Analytics

### Zero-Knowledge Medical Intelligence for Next-Gen Healthcare

## 🚨 Problem

Healthcare institutions generate massive amounts of sensitive clinical data.
Due to strict privacy laws like **HIPAA** and **GDPR**, hospitals cannot freely share patient data with researchers.

This leads to:

* 🔒 Data silos in hospitals
* 🧪 Slower medical research
* 🤖 Limited datasets for AI diagnostics

Researchers need insights from medical data, but **raw patient records cannot be exposed**.

---

## 💡 Solution – MedVault Analytics

**MedVault Analytics** is a privacy-preserving medical analytics platform that allows researchers to gain insights **without accessing raw patient data**.

Instead of sharing datasets, the system allows **secure statistical queries** on encrypted data.

Key idea:

> *Bring computation to the data, not the data to the researcher.*

---

## ⚙️ Core Features

### 🔐 AES-256 Encryption

All uploaded datasets are encrypted using **AES-256 symmetric encryption**, ensuring raw patient records remain protected.

### 📊 Differential Privacy

Statistical queries apply **Laplacian noise** to results, preventing patient re-identification attacks.

### 🧾 SHA-256 Shadow Ledger

Every action (upload, query, computation) is recorded in a **tamper-proof hash chain ledger**.

### 🤖 AI Clinical Insights

**Google Gemini 1.5 Flash** interprets privacy-safe results and provides medical insights for researchers.

---

## 🏗 System Architecture

1️⃣ **Secure Data Ingestion**

* Hospital uploads CSV dataset
* File is encrypted immediately
* Raw data is deleted

2️⃣ **Secure Query Execution**

* Researcher submits statistical query

3️⃣ **Zero-Knowledge Compute Engine**

* Data decrypted temporarily in memory
* Query executed with **Pandas**
* Differential privacy applied

4️⃣ **AI Interpretation**

* Safe result sent to **Gemini API**
* AI generates clinical explanation

5️⃣ **Audit Trail**

* All operations recorded using **SHA-256 hash chain**

---

## 🛠 Tech Stack

Frontend

* Streamlit

Backend

* Python

Data Processing

* Pandas

Security

* cryptography (AES-256 encryption)

Privacy Layer

* NumPy (Differential Privacy)

Audit System

* hashlib (SHA-256)

AI Intelligence

* Google Gemini 1.5 Flash

---

## 📂 Project Structure

```
MedVault-Analytics/
│
├── app.py                # Streamlit application
├── security_module.py     # Encryption + Ledger
├── privacy_module.py      # Differential Privacy
├── gemini_client.py       # Gemini API integration
├── requirements.txt
└── README.md
```

---

## 🚀 Running the Project Locally

### 1️⃣ Clone Repository

```
git clone https://github.com/ajaytilakvaiml2024-hub/CCP-PROJECT.git
cd CCP-PROJECT
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Set Gemini API Key

Create an environment variable:

```
GEMINI_API_KEY=your_api_key_here
```

### 4️⃣ Run Streamlit

```
streamlit run app.py
```

---

## 📊 Example Workflow

Hospital Admin:

* Upload encrypted patient dataset

Researcher:

* Query statistical insights

System:

* Applies differential privacy
* Generates AI interpretation

Auditor:

* Verifies immutable ledger logs

---

## 🎯 CCP - PROJECT

MedVault Analytics solves a real healthcare challenge:

✔ Protects patient privacy
✔ Enables medical research
✔ Prevents data misuse
✔ Provides AI-driven clinical insights

---

## 👨‍💻 Author

**Ajay Tilak V**
Student | AI & Data Enthusiast

GitHub:
https://github.com/ajaytilakvaiml2024-hub
