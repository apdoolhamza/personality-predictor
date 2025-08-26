# Personality Predictor AI (ML + Flask)

A simple yet powerful smart **AI Personality Predictor** that guesses your MBTI type just by analyzing your writing.

[![Watch the video](https://img.youtube.com/vi/cDToQKIc67M/maxresdefault.jpg)](https://youtu.be/cDToQKIc67M)
[![Watch on YouTube](https://img.shields.io/badge/Watch%20on-YouTube-red?logo=youtube&logoColor=white)](https://youtu.be/cDToQKIc67M)

## What does it do?

It predicts your **MBTI Personality Type** (like INTJ, ENFP, ISTP, etc.) based on what you write.
It also shows an easy-to-understand explanation of:
- Your type
- What it means
- A famous quote ...

## Technologies Used
- **Python**: Core language for data processing and machine learning.
- **Scikit-learn**: For building and evaluating machine learning models.
- **NLTK**: For NLP tasks like sentiment analysis and text preprocessing.
- **Pandas & NumPy**: For data manipulation and analysis.
- **Flask, HTML5, & Bootstrap 5**: For deploying the model as a web application.
- **Jupyter Notebook**: For exploratory data analysis and model development.

## How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/apdoolhamza/customer-feedback-sentiment-checker.git
```
### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Run the project
```bash
python app.py
```

## Usage
1. Launch the application using the instructions above.
2. Input data (e.g., text responses or survey data) into the interface.
3. Receive a personality prediction (e.g., “Extroverted” or “INTP”).

## Dataset
This AI was trained on a public dataset made from over 8,000+ people’s writings, where each person’s MBTI type is known.
The writings were collected from [Kaggle](https://www.kaggle.com/datasets/datasnaek/mbti-type) a popular dataset repository, so the model learned how people with different personality types express themselves through text.

## Contact
Apdoolmajeed Hamza - [LinkedIn Profile](https://www.linkedin.com/in/apdoolhamza/) | [GitHub Profile](https://github.com/apdoolhamza/)

##  License
This project is licensed under the [MIT License](https://github.com/apdoolhamza/personality-predictor/blob/main/LICENSE)
