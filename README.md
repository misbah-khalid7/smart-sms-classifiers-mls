# Smart SMS Classifier

A simple **Machine Learning Web App** that detects spam messages in real-time.
Built using **Flask (Backend)**, **Logistic Regression (ML Model)**, and **CountVectorizer (Text Vectorization)**.

This project demonstrates a complete pipeline of **NLP + ML + Web Deployment**.

---

## 🔹 Features

* ✅ Spam / Ham classification
* ✅ Real-time web predictions
* ✅ Confidence score display
* ✅ User login & registration system
* ✅ Clean and responsive UI
* ✅ Lightweight and easy to deploy

---

## ⚙️ How It Works

1. User enters an SMS message in the web app.
2. The message is preprocessed (lowercasing, cleaning special characters).
3. Text is converted into numerical features using **CountVectorizer**.
4. The trained **Logistic Regression** model predicts whether it is Spam or Ham.
5. The result and confidence score are displayed instantly.

---

## 📊 Model Performance

* Algorithm: Logistic Regression
* Text Vectorization: CountVectorizer
* Dataset: SMS Spam Collection
* Accuracy: ~97–99% (depending on train/test split)

---

## 📁 Project Structure

```
smart-sms-classifier/
│
├── app.py              # Main Flask application
├── train.py            # Model training script
├── requirements.txt
│
├── models/
│   ├── classifier.pkl
│   └── vectorizer.pkl
│
├── data/
│   └── spam.csv
│
├── static/
│   ├── style.css
│   └── script.js
│
└── templates/
    ├── login.html
    ├── register.html
    └── home.html
```
