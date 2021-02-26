# Purwadhika Jakarta Batch 11 - William Andreas

## HR Analytics: Job Change Prediction

A predictive machine learning project uses a classification algorithm to predict whether or not candidates change their jobs after they have completed their training.

## Dataset

Dataset was taken from [Kaggle](https://www.kaggle.com/arashnic/hr-analytics-job-change-of-data-scientists)

The data is related to an anonymous company that's dynamic in Big Data and Data Science that needs to enlist data scientists among individuals who effectively pass a few courses which conduct by the company. The said company needs to know which of these candidates are really wants to work for the company after training or seeking out new employment because it makes a difference to reduce the cost and time as well as the quality of preparing or arranging the courses and categorization of candidates.

The classification objectives are:
1. To predict whether or not candidates alter their occupations after they have completed their training.
2. Help out the said company to reduce the cost and time as well as the quality of the courses and categorization of candidates by sorting out candidates that are false predicted (predicted not change their jobs while actually they are seeking out new employment).

## Cleaning and Pre-Processing

1. Drop rows containing ID and training hours of candidates.
2. Impute missing values using their most frequent values.
3. Encode categorical columns of data to numerical using Binary Encoder, and ordinal columns of data to numerical using Ordinal Encoder.
4. Scale numerical column of data using RobustScaler.
5. Generate polynomial and interaction features using PolynomialFeatures for numerical column of data after it's scaled.

## Modeling

### Handling Imbalance Target

|  Target  | Percentage of Data |
|:-:|:-:|
| Not Changed | 75.07% |
| Job Changed | 24.93% |

The target was imbalance. There are 2 ways of technique was used to balance the target:

1. Setting the parameter "(class_weight='balanced')" for models which have it and their "random_state" parameter respectively.
2. Using SMOTE oversampling method and setting the "random_state" parameter for models that don't have "class_weight" parameter.

### Features Selection

Using SelectPercentile in sklearn, the features of the data is automatically selected based on the percentile parameter.

### Base, Tune and Hyperparameter Tuning Model

Using RepeatedStratifiedKFold and GridSearchCV to search over specified parameter values for an estimator. The "scoring" parameter used is 'recall'.

| Model |  Before  | After |
|:-:|:-:|:-:|
| Logistic Regression | 0.656 | 0.652 |
| Decision Tree Classifier | 0.496 | 0.697 |
| Random Forest Classifier | 0.454 | 0.658 |
| Support Vector Classifier | 0.641 | 0.714 |
| Ada Boost Classifier | 0.576 | 0.580 |
| Gradient Boosting Classifier | 0.582 | 0.607 |
| XGBoost Classifier | 0.584 | 0.612 |
| K Nearest Classifier | 0.650 | 0.521 |

Based on the 'recall' score, and speed performance of models, the best model is the Decision Tree Classifier. After said model undergo hyperparameter tuning, the 'recall' score of said model is increasing dramatically, which became 0.81 when gets predicted to the X_test.

#### Decision Tree Classifier Confusion Matrix

##### Before Hyperparameter Tuning 

![DTC Default Confusion Matrix](https://raw.githubusercontent.com/W1lly-Wonka/Prediction-Final-Project/main/Visualizations/DTC%20Default%20Confusion%20Matrix.png "DTC Default Confusion Matrix")

##### After Hyperparameter Tuning

![DTC Hyperparameter Tuning Confusion Matrix](https://raw.githubusercontent.com/W1lly-Wonka/Prediction-Final-Project/main/Visualizations/DTC%20Hyperparameter%20Tuniing%20Confusion%20Matrix.png "DTC Hyperparameter Tuning Confusion Matrix")

### Conclusions:

1. The machine learning model is able to help the company to reduce the cost and save time by reducing candidates who are going to alter their occupations.
2. The result might be able to be improved by having more data on candidates who are going to alter their occupations.

### Business Insights:

1. The company.
2. The company.
