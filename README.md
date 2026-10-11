\# 🛡️ PhishGuard — Phishing Website Detection



PhishGuard is a machine learning-based web application that helps identify potentially phishing websites by analyzing URL-related features. It provides a simple interface for users to check URLs and view prediction results.



\## 🎯 Project Objective



The main objective of PhishGuard is to demonstrate how machine learning can help detect suspicious URLs and support safer browsing.



\## ✨ Features



\- 🔍 URL scanning interface

\- 🤖 Machine learning-based classification

\- 📊 Prediction confidence display

\- 📈 Model evaluation and feature importance visualization

\- 🖥️ Interactive dashboard built with Streamlit

\- 🧪 Model training script included



\## 🛠️ Technologies Used



\- Python

\- Pandas

\- NumPy

\- Scikit-learn

\- Streamlit

\- Matplotlib



\## 📂 Project Structure



```text

PhishGuard/

├── app.py

├── train\_url\_model.py

├── README.md

├── data/

│   └── phishing.csv

├── model/

│   └── url\_only\_phishing\_model.pkl

├── dataset/

└── notebook/

```



\*The exact files in `dataset/` and `notebook/` may vary.\*



\## ⚙️ Requirements



\- Python 3.12 or a compatible Python version

\- pip

\- The project dataset and trained model files



\## 🚀 Installation and Setup



\### 1. Clone the repository



```bash

git clone https://github.com/rushikeshkamble34381-arch/phishing-website-detection.git

```



\### 2. Open the project folder



```bash

cd phishing-website-detection

```



\### 3. Install dependencies



```bash

python -m pip install streamlit pandas numpy scikit-learn matplotlib

```



\### 4. Run the application



```bash

python -m streamlit run app.py

```



Open the local URL shown in your terminal, usually:



`http://localhost:8501`



\## 🧠 How It Works



1\. The user enters a URL into the application.

2\. The application extracts URL-related features.

3\. The trained machine learning model analyzes those features.

4\. The application displays its prediction and related information.



\## 📊 Model Information



The project uses a Random Forest classifier trained on URL-related features from a phishing website dataset.



The selected features include URL length, IP address usage, URL shortening services, the `@` symbol, subdomains, and HTTPS-related indicators.



Model performance should be evaluated using appropriate metrics such as accuracy, precision, recall, F1-score, and a confusion matrix.



\## 🔒 Limitations



\- A prediction is not a guarantee that a website is safe or malicious.

\- Model accuracy depends on the training data and feature extraction.

\- A website's legitimacy cannot be determined reliably from a URL alone.

\- This project is an educational demonstration, not a replacement for professional security tools.



\## 🔮 Future Scope



\- Improve the dataset and feature engineering.

\- Evaluate additional machine learning algorithms.

\- Add real-time threat intelligence checks.

\- Improve URL parsing and model calibration.

\- Deploy the application online.



\## ⚠️ Disclaimer



PhishGuard is an educational project intended to demonstrate machine learning for phishing website detection. Always verify suspicious links independently. Do not enter passwords or sensitive information on websites you do not trust.



\## 👨‍💻 Author



\*\*Rushikesh Kamble\*\*



GitHub: \[rushikeshkamble34381-arch](https://github.com/rushikeshkamble34381-arch)



\---



⭐ If you find this project useful, consider starring the repository.

