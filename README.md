# 🧠 Diabetes ML App – CI/CD with Docker & KIND (Beginner Guide)

This project demonstrates how to **automatically test, build, and deploy** a **Machine Learning FastAPI app** to **Kubernetes** using **GitHub Actions** and **KIND (Kubernetes IN Docker)**.

> ✅ Designed for **beginners**
>
> ✅ Uses **local-style Kubernetes deployment**
>
> ✅ No cloud account required

---

## 📌 What You Will Learn

By the end of this project, you will understand:

* What **CI/CD** means for ML applications
* How to **test ML models automatically**
* How to **containerize an ML API using Docker**
* How to **deploy to Kubernetes locally using KIND**
* How GitHub Actions automates everything

---

## 🏗️ Architecture Overview

```
Developer pushes code to GitHub
        ↓
GitHub Actions (CI/CD)
        ↓
1. Run ML & API tests
2. Build Docker image
3. Create KIND Kubernetes cluster
4. Load Docker image into KIND
5. Deploy app to Kubernetes
```

---

## 📁 Project Structure

```
diabetes-ml-app/
│
├── api/                  # FastAPI application
│   └── main.py
│
├── model/                # ML model logic
│   └── predict.py
│
├── tests/                # Unit & API tests
│   └── test_api.py
│
├── k8s/                  # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   └── namespace.yaml
│
├── Dockerfile             # Docker image definition
├── requirements.txt       # Python dependencies
└── .github/workflows/
    └── ci-cd.yml          # CI/CD pipeline
```

---

## 🔑 Key Concepts (Simple Explanation)

### 🔹 CI (Continuous Integration)

* Automatically runs tests when code is pushed
* Ensures model & API are not broken

### 🔹 CD (Continuous Deployment)

* Automatically deploys app if tests pass
* Uses Kubernetes for deployment

### 🔹 Docker

* Packages the ML app + dependencies into one image

### 🔹 Kubernetes

* Runs and manages the app container
* Handles restarts, scaling, networking

### 🔹 KIND

* Runs Kubernetes **inside Docker**
* Perfect for learning & CI pipelines

---

## ⚙️ Step-by-Step CI/CD Process

### **Step 1: Push Code to GitHub**

You push code to the `main` branch.

```bash
git push origin main
```

---

### **Step 2: GitHub Actions Starts Automatically**

GitHub detects the push and triggers:

```
.github/workflows/ci-cd.yml
```

---

### **Step 3: Install Dependencies**

GitHub Actions installs Python packages:

```bash
pip install -r requirements.txt
```

---

### **Step 4: Run Tests**

Runs:

* ML tests
* FastAPI endpoint tests

```bash
pytest tests/
```

❌ Pipeline fails if tests fail
✅ Pipeline continues if tests pass

---

### **Step 5: Build Docker Image**

Creates a container image for the ML API:

```bash
docker build -t diabetes-ml-api:cicd .
```

Runs API locally:(Optional)

```bash
docker run -p 8000:8000 diabetes-ml-api:cicd
```

---

### **Step 6: Create KIND Kubernetes Cluster**

KIND creates a Kubernetes cluster **inside GitHub Actions**:

```bash
kind create cluster --name ml-cluster
```

---

### **Step 7: Load Image into KIND**

Instead of pushing to Docker Hub, the image is **loaded locally**:

```bash
kind load docker-image diabetes-ml-api:cicd --name ml-cluster
```

✔ No registry needed
✔ Faster for local-style deployments

---

### **Step 8: Deploy to Kubernetes**

Kubernetes manifests are applied:

```bash
kubectl apply -n ml-app -f k8s/
```

This creates:

* Deployment (runs the app)
* Service (exposes the app)

---

### **Step 9: Verify Deployment**

GitHub Actions waits until the app is running:

```bash
kubectl rollout status deployment/diabetes-ml-api -n ml-app
```

❌ Pipeline fails if deployment fails
✅ Pipeline succeeds if app is healthy

---

## 🧪 How to Run Locally (Optional)

### 1️⃣ Install tools

```bash
brew install docker kubectl kind
```

### 2️⃣ Create KIND cluster

```bash
kind create cluster
```

### 3️⃣ Build & load image

```bash
docker build -t diabetes-ml-api .
kind load docker-image diabetes-ml-api
```

### 4️⃣ Deploy

```bash
kubectl apply -f k8s/
```

### 5️⃣ Access API

```bash
kubectl port-forward svc/diabetes-ml-api 8000:80 -n ml-app
```

Test:

```bash
curl http://localhost:8000/health
```

---

## 🚀 Why This Approach Is Good for Beginners

| Benefit            | Reason                     |
| ------------------ | -------------------------- |
| No cloud           | Runs fully locally         |
| Same as production | Kubernetes YAML stays same |
| Fast feedback      | CI fails early             |
| Safe               | No secrets required        |
| Scalable           | Easy to move to EKS/GKE    |

---

## 🏁 Summary

✔ You built an ML CI/CD pipeline
✔ You deployed to Kubernetes
✔ You used industry tools
✔ You learned real MLOps foundations

