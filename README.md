# Network-Intrusion-Detection-System

Project Overview
This project develops a Network Intrusion Detection System (NIDS) capable of identifying whether a network connection is Normal or an Attack using supervised machine learning.
The model is trained on the NSL-KDD dataset, a widely used benchmark dataset for intrusion detection research. The complete pipeline includes data preprocessing, feature selection, hyperparameter tuning, model evaluation, and prediction on unseen network traffic.


📌 Problem Statement
Modern computer networks are continuously exposed to cyber threats such as Denial of Service (DoS), Probe attacks, User-to-Root (U2R), and Remote-to-Local (R2L) attacks.
Traditional rule-based intrusion detection systems struggle to identify new or evolving attacks.
The objective of this project is to build a machine learning model capable of classifying network traffic as:
Normal
Attack
allowing suspicious traffic to be detected automatically.


📊 Dataset
Dataset: NSL-KDD
The dataset contains 41 network traffic features including:
Duration
Protocol Type
Service
Flag
Source Bytes
Destination Bytes
Count
Serror Rate
Same Service Rate
Host Statistics
Network Behavior Features


Target Variable:
Attack
0 → Normal
1 → Attack


Project Workflow
Dataset
↓
Data Cleaning
↓
Feature Engineering
↓
Encoding & Scaling
↓
Decision Tree Pipeline
↓
GridSearchCV
↓
Feature Importance
↓
Top Feature Selection
↓
Model Retraining
↓
Evaluation
↓
Prediction on New Data


Technologies Used:
Python
Pandas
NumPy
Matplotlib
Scikit-learn
Joblib
Machine Learning Pipeline

The project uses :
Pipeline
ColumnTransformer
StandardScaler
OneHotEncoder
DecisionTreeClassifier
GridSearchCV

Hyperparameter tuning is performed using 5-Fold Cross Validation with Recall as the optimization metric to reduce missed attacks.


Feature Selection :
The model extracts feature importance from the trained Decision Tree.
The top-performing features are selected and used to retrain the final model, improving efficiency while maintaining predictive performance.


Model Evaluation :
The final model is evaluated using:
Accuracy
Confusion Matrix
Classification Report
ROC Curve
ROC-AUC Score
Precision-Recall Curve
Average Precision Score


Output
The trained model can classify unseen network traffic.
Input.csv
↓
Prediction
↓
Output.csv


Predictions are generated as:
Attack
or
Normal


Project Structure : 
Network-Intrusion-Detection-System/
│
├── Data/
├── Graph/
│   ├── Correlation.png
│   ├── Important_Feature.png
│   ├── ROC_Curve.png
│   └── Precision_Recall.png
│
├── model.pkl
├── feature.pkl
├── training.log
├── main.py
├── Input.csv
├── Output.csv
├── requirements.txt
├── .gitignore
└── README.md


Future Improvements : 
Compare multiple machine learning algorithms.
Experiment with XGBoost and LightGBM.
Perform multiclass attack classification.
Deploy the model as a web application.
Integrate real-time packet capture. 


Author
Siddesh Kuppast
B.Tech – Artificial Intelligence & Machine Learning