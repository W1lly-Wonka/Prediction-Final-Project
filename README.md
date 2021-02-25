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
2. Impute missing values using their most frequent values
3. Encode categorical columns of data to numerical using Binary Encoder, and ordinal columns of data to numerical using Ordinal Encoder
4. Scale numerical column of data using RobustScaler.
5. Generate polynomial and interaction features using PolynomialFeatures for numerical column of data after it's scaled

## Handling Imbalance Target

|  Target  | Percentage of Data |
|:-:|:-:|
| Not Changed | 75.07% |
| Job Changed | 24.93% |

The target was imbalance. There are 2 ways of technique was used to balance the target:

1. Setting the parameter "(class_weight='balanced')" for models which have it and their "random_state" parameter respectively.
2. Using SMOTE oversampling method and setting the "random_state" parameter for models that don't have "class_weight" parameter

## Features Selection

1. Using SelectPercentile in sklearn, the features of the data is automatically selected based on the percentile parameter.

