"""
Austin Kingsland

In this project, I aimed to demonstrate high-level computer science and machine learning skills by building, 
evaluating, and comparing multiple machine learning models using the Iris dataset. The Iris dataset, 
a well-known dataset in the field of machine learning, contains measurements of iris flowers from three different species: setosa, versicolor, and virginica. 
The primary goal was to classify the species of iris flowers based on these measurements.

We began by loading the Iris dataset and convert it to a Pandas DataFrame for easier manipulation and analysis. 
Initial exploratory data analysis was performed, which included viewing the first few rows of the dataset, 
its statistical description, and class distribution. 

To visualize the relationships between the features, we used Seaborn's pair plot, which helped in understanding the data distribution and feature interactions.

Next, we split the dataset into training and testing sets to evaluate the model's performance on unseen data. 
We created pipelines for three different machine learning algorithms: Random Forest, Gradient Boosting, and Support Vector Classifier (SVC). 
These pipelines streamlined preprocessing, specifically standardization, and model training.

To optimize model performance, we performed hyperparameter tuning using Grid Search with cross-validation, 
identifying the best hyperparameters for each model. Subsequently, each model was trained on the training set 
with the best hyperparameters and evaluated on the test set. 
Key performance metrics such as accuracy, precision, recall, and F1-score were computed.

We also conducted a ROC (Receiver Operating Characteristic) analysis, computing and plotting ROC curves and AUC (Area Under the Curve) 
scores for each class in the multi-class classification scenario. This provided insights into the models' ability to distinguish between different classes. 
For the Random Forest model, we computed and visualized feature importance scores, helping us understand which features contributed most to the model's predictions.

The results were accurate, with all models achieving a test set accuracy of 1.0. The best parameters for Random Forest 
were `{'clf__n_estimators': 100, 'clf__max_depth': None, 'clf__min_samples_split': 2}`, yielding a cross-validation score of 0.9733. 
Gradient Boosting had best parameters `{'clf__learning_rate': 0.1, 'clf__max_depth': 3, 'clf__n_estimators': 100}`, with a cross-validation score of 0.9667. 
The SVC model's best parameters were `{'clf__C': 1, 'clf__gamma': 0.1, 'clf__kernel': 'rbf'}`, and it achieved a cross-validation score of 0.9733. 
ROC curves indicated excellent model performance across all classes, and the Random Forest model's feature importance analysis highlighted petal length and 
petal width as the most significant features.

This project demonstrates a complete machine learning pipeline, from data loading and exploration to model training, evaluation, and analysis. 
The use of multiple models and hyperparameter tuning showcased advanced techniques for optimizing and comparing different algorithms. Additionally, 
the inclusion of ROC AUC analysis and feature importance provided deeper insights into model performance and interpretability. 
The comprehensive analyses conducted in this project underscore the importance of thorough model evaluation and understanding, 
which are crucial in real-world applications where model performance and interpretability can significantly impact decision-making processes.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve, auc

# Load Iris dataset from sklearn
# The Iris dataset contains 150 samples of iris flowers, with 4 features (float) and a target label (integer)
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)  # Feature data (float)
y = iris.target  # Target labels (integer)

# Exploratory Data Analysis (EDA)
# Displaying the first few rows of the dataset to understand its structure
print("Dataset Head:")
print(X.head())
print("\nDataset Description:")
# Descriptive statistics to summarize the central tendency, dispersion, and shape of the dataset’s distribution
print(X.describe())
print("\nClass Distribution:")
# Displaying the class distribution to see how the target labels are distributed
print(y)

# Data Visualization
# Visualizing the pair-wise relationships in the dataset to identify patterns or correlations
sns.pairplot(pd.concat([X, pd.Series(y, name='target')], axis=1), hue='target')
plt.show()

# Split dataset into training and testing sets
# X_train, X_test (float): Feature data split into training and testing sets
# y_train, y_test (integer): Target labels split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define a function to plot ROC curve
def plot_roc_curve(fpr, tpr, label=None):
    plt.plot(fpr, tpr, linewidth=2, label=label)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')

# Create pipelines for each model to streamline preprocessing and model training
pipeline_rf = Pipeline([
    ('scaler', StandardScaler()),  # Standardize features (float) by removing the mean and scaling to unit variance
    ('clf', RandomForestClassifier(random_state=42))  # Random Forest Classifier
])

pipeline_gb = Pipeline([
    ('scaler', StandardScaler()),  # Standardization
    ('clf', GradientBoostingClassifier(random_state=42))  # Gradient Boosting Classifier
])

pipeline_svc = Pipeline([
    ('scaler', StandardScaler()),  # Standardization
    ('clf', SVC(probability=True, random_state=42))  # Support Vector Classifier
])

# Parameter grid for Grid Search
# These are the hyperparameters we will tune for each model using Grid Search with Cross-Validation
param_grid_rf = {
    'clf__n_estimators': [50, 100, 200],  # Number of trees in the forest (integer)
    'clf__max_depth': [None, 10, 20, 30],  # Maximum depth of the tree (integer or None)
    'clf__min_samples_split': [2, 5, 10]  # Minimum number of samples required to split an internal node (integer)
}

param_grid_gb = {
    'clf__n_estimators': [50, 100, 200],  # Number of boosting stages (integer)
    'clf__learning_rate': [0.01, 0.1, 0.2],  # Learning rate shrinks the contribution of each tree (float)
    'clf__max_depth': [3, 5, 10]  # Maximum depth of the individual estimators (integer)
}

param_grid_svc = {
    'clf__C': [0.1, 1, 10],  # Regularization parameter (float)
    'clf__gamma': [0.01, 0.1, 1],  # Kernel coefficient (float)
    'clf__kernel': ['rbf', 'linear']  # Specifies the kernel type to be used in the algorithm (string)
}

# Grid Search with Cross-Validation
# This step involves finding the best hyperparameters for each model by evaluating different combinations using cross-validation
grid_search_rf = GridSearchCV(pipeline_rf, param_grid_rf, cv=5, n_jobs=-1, verbose=1)
grid_search_rf.fit(X_train, y_train)

grid_search_gb = GridSearchCV(pipeline_gb, param_grid_gb, cv=5, n_jobs=-1, verbose=1)
grid_search_gb.fit(X_train, y_train)

grid_search_svc = GridSearchCV(pipeline_svc, param_grid_svc, cv=5, n_jobs=-1, verbose=1)
grid_search_svc.fit(X_train, y_train)

# Best parameters and best score from Grid Search
print(f"Random Forest - Best parameters: {grid_search_rf.best_params_}")
print(f"Random Forest - Best cross-validation score: {grid_search_rf.best_score_}")

print(f"Gradient Boosting - Best parameters: {grid_search_gb.best_params_}")
print(f"Gradient Boosting - Best cross-validation score: {grid_search_gb.best_score_}")

print(f"SVC - Best parameters: {grid_search_svc.best_params_}")
print(f"SVC - Best cross-validation score: {grid_search_svc.best_score_}")

# Evaluate the best model on the test set
models = {
    'Random Forest': grid_search_rf.best_estimator_,
    'Gradient Boosting': grid_search_gb.best_estimator_,
    'SVC': grid_search_svc.best_estimator_
}

# Function to calculate and plot ROC AUC for multi-class classification
def plot_multiclass_roc(clf, X_test, y_test, n_classes, class_names):
    y_score = clf.predict_proba(X_test)  # Predict probabilities for each class (float)
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test, y_score[:, i], pos_label=i)  # Compute ROC curve
        roc_auc[i] = auc(fpr[i], tpr[i])  # Compute AUC

    # Plot all ROC curves
    plt.figure()
    colors = ['aqua', 'darkorange', 'cornflowerblue']
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                       ''.format(class_names[i], roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic for Multi-Class')
    plt.legend(loc="lower right")
    plt.show()

# Evaluate each model and plot ROC curves
for name, model in models.items():
    y_pred = model.predict(X_test)  # Predict on test set (integer)
    y_prob = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None  # Predict probabilities if applicable (float)

    accuracy = accuracy_score(y_test, y_pred)  # Calculate accuracy (float)
    report = classification_report(y_test, y_pred, target_names=iris.target_names)  # Generate classification report (string)
    conf_matrix = confusion_matrix(y_test, y_pred)  # Compute confusion matrix (integer)

    print(f"\n{name} Model - Test set accuracy: {accuracy}")
    print("Classification Report:")
    print(report)
    print("Confusion Matrix:")
    print(conf_matrix)

    if y_prob is not None:
        plot_multiclass_roc(model, X_test, y_test, n_classes=3, class_names=iris.target_names)

# Feature Importance for Random Forest
# This step is specific to the Random Forest model to understand which features contribute the most to the predictions
feature_importances = grid_search_rf.best_estimator_.named_steps['clf'].feature_importances_  # Feature importance scores (float)
features = X.columns  # Feature names (string)
importances = pd.Series(feature_importances, index=features).sort_values(ascending=False)  # Sorted feature importance scores (float)

plt.figure(figsize=(10, 6))
sns.barplot(x=importances, y=importances.index)
plt.title("Feature Importance (Random Forest)")
plt.xlabel("Importance Score")
plt.ylabel("Feature")
plt.show()