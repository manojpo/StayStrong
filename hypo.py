# Import necessary libraries
import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np

# Load the dataset
file_path = 'cleaned_data_Semester2.xlsx'  # Replace with the correct path to your dataset
data = pd.read_excel(file_path)

# Step 1: Data Cleaning
# Drop duplicates based on Client ID and clean key columns
cleaned_data = data.drop_duplicates(subset=['Client ID'])

# Clean and handle missing values (drop rows where K10 score or key variables are missing)
cleaned_data = cleaned_data.dropna(subset=['K10 Score'])

# Identifying relevant columns for analysis
goal_columns = [col for col in cleaned_data.columns if 'Goal' in col and 'What' in col]
worry_columns = [col for col in cleaned_data.columns if 'Worry' in col]

# Step 2: Create aggregated columns for goals and worries
cleaned_data['Total Goals'] = cleaned_data[goal_columns].notna().sum(axis=1)
cleaned_data['Total Worries'] = cleaned_data[worry_columns].notna().sum(axis=1)

# Clean data by handling potential missing 'Strengths'
cleaned_data['No. of Strengths'] = cleaned_data['No. of Strengths'].fillna(0)

# Step 3: Define clients in need of support as those with a high K10 score (threshold: 20)
cleaned_data['Needs Support'] = cleaned_data['K10 Score'] > 20

# Step 4: Hypothesis Testing (t-tests) for Total Goals, Total Worries, and Number of Strengths
# Split data into high K10 and low K10 groups
high_k10 = cleaned_data[cleaned_data['K10 Score'] > 20]
low_k10 = cleaned_data[cleaned_data['K10 Score'] <= 20]

# Perform t-tests
t_stat_goals, p_value_goals = ttest_ind(high_k10['Total Goals'], low_k10['Total Goals'], equal_var=False)
t_stat_strengths, p_value_strengths = ttest_ind(high_k10['No. of Strengths'], low_k10['No. of Strengths'], equal_var=False)
t_stat_worries, p_value_worries = ttest_ind(high_k10['Total Worries'], low_k10['Total Worries'], equal_var=False)

# Step 5: Logistic Regression to predict clients in need of support
# Define features (independent variables) and target (dependent variable)
features = cleaned_data[['Total Goals', 'No. of Strengths', 'Total Worries']]
target = cleaned_data['Needs Support']

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

# Initialize and fit logistic regression model
log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

# Make predictions and generate a classification report
y_pred = log_reg.predict(X_test)
classification_rep = classification_report(y_test, y_pred)

# Step 6: Chi-square test to check the relationship between organization/training and needing support
contingency_table = pd.crosstab(cleaned_data['Organisation'], cleaned_data['Needs Support'])
chi2, p_chi2, dof, expected = chi2_contingency(contingency_table)

# Step 7: Identify the clients who need help (K10 score > 20)
clients_needing_help = cleaned_data[cleaned_data['Needs Support'] == True][['Client ID', 'K10 Score', 'Total Goals', 'No. of Strengths', 'Total Worries']]

# Print the results
print(f"T-test for Total Goals: T-statistic = {t_stat_goals}, P-value = {p_value_goals}")
print(f"T-test for No. of Strengths: T-statistic = {t_stat_strengths}, P-value = {p_value_strengths}")
print(f"T-test for Total Worries: T-statistic = {t_stat_worries}, P-value = {p_value_worries}")
print(f"\nLogistic Regression Classification Report:\n{classification_rep}")
print(f"\nChi-square test for Organisation and Needs Support: Chi2 = {chi2}, P-value = {p_chi2}")

# Display the list of clients who need help
print("\nClients Needing Help Based on K10 Scores:\n")
print(clients_needing_help)

# Optionally save the clients needing help to a CSV file
clients_needing_help.to_csv('hypohelpneed.csv', index=False)

# Step 8: Visualization of Clients Needing Support based on K10 scores
plt.figure(figsize=(10, 6))
sns.histplot(cleaned_data['K10 Score'], bins=30, kde=True, color='blue')
plt.axvline(20, color='red', linestyle='--', label='K10 Threshold (20)')
plt.title('Distribution of K10 Scores with Clients Needing Support')
plt.xlabel('K10 Score')
plt.ylabel('Frequency')
plt.legend()
plt.show()

# Step 9: Box Plots for Total Goals, Strengths, and Worries for High and Low K10 groups
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
sns.boxplot(x='Needs Support', y='Total Goals', data=cleaned_data, ax=axes[0])
axes[0].set_title('Total Goals by Clients Needing Support')
axes[0].set_xlabel('Needs Support')
axes[0].set_ylabel('Total Goals')

sns.boxplot(x='Needs Support', y='No. of Strengths', data=cleaned_data, ax=axes[1])
axes[1].set_title('Number of Strengths by Clients Needing Support')
axes[1].set_xlabel('Needs Support')
axes[1].set_ylabel('No. of Strengths')

sns.boxplot(x='Needs Support', y='Total Worries', data=cleaned_data, ax=axes[2])
axes[2].set_title('Total Worries by Clients Needing Support')
axes[2].set_xlabel('Needs Support')
axes[2].set_ylabel('Total Worries')

plt.tight_layout()
plt.show()
