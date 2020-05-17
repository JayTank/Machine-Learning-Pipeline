# Machine-Learning-Pipeline
Creating a Machine Learning Pipeline to transform, process and analyze a large National Patient Database. The results obtained with the proposed method can be used for tailored health communication.

System Requiremens:\
Programming Language - Python 3.x\
Database - PostgreSQL\
Libraries - psycopg2, pandas, numpy, scikit-learn


Background: I present a method to create a Big Data pipeline utilizing Healthcare Cost and Utilization Project (HCUP) dataset for
predicting disease risk of individuals based on their medical diagnosis history. The presented methodology may be incorporated in a
variety of applications such as risk management, tailored health communication and decision support systems in healthcare.

Methods: I employed the National Inpatient Sample (NIS) data, which is available through Healthcare Cost and Utilization Project (HCUP),
to train various machine learning models for breast cancer prediction. Since the HCUP data is categorical in nature and highly imbalanced,
I employed an ensemble learning approach of data cleaning and data pre-processing before feeding the data into machine learning algorithms.
I compared the performance of Logistic Regression, Decision Tree and Naive Bayes Classifier to predict the risk of breast cancer.

Results: I trained 3 different Machine Learning models on the dataset and after comparing the results I observed that Decision tree was
able to outperform the other models 97% of the time to predict breast cancer among the patients with a higher accuracy.

Conclusion: I was able to overcome the class imbalance problem and achieve promising results. Using the national HCUP data set and
leveraging the data science technologies I was successfully able to build a predictive model which gives an average AUC of 85%.
