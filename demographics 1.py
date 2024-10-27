import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
file_path = 'E:/IT Thesis/cln_data_cleaned.xlsx' 
data = pd.read_excel(file_path)

# Function to map Australian postcodes to states
def map_postcode_to_state(postcode):
    try:
        postcode = int(postcode)
        if 200 <= postcode <= 299:
            return 'ACT'
        elif 800 <= postcode <= 999:
            return 'NT'
        elif 1000 <= postcode <= 2599 or 2619 <= postcode <= 2899 or 2921 <= postcode <= 2999:
            return 'NSW'
        elif 3000 <= postcode <= 3999 or 8000 <= postcode <= 8999:
            return 'VIC'
        elif 4000 <= postcode <= 4999 or 9000 <= postcode <= 9999:
            return 'QLD'
        elif 5000 <= postcode <= 5799 or 5800 <= postcode <= 5999:
            return 'SA'
        elif 6000 <= postcode <= 6797 or 6800 <= postcode <= 6999:
            return 'WA'
        elif 7000 <= postcode <= 7799 or 7800 <= postcode <= 7999:
            return 'TAS'
        else:
            return 'Unknown'
    except:
        return 'Unknown'

# Apply the mapping function to create 'State' column
data['State'] = data['Post Code'].apply(map_postcode_to_state)

# Ensure 'Gender' is treated as a categorical variable
data['Gender'] = data['Gender'].astype('category')

# Create age groups for cross-tabulation analysis
data['Age Group'] = pd.cut(data['Age'], bins=[0, 18, 30, 50, 70, 100], labels=['0-18', '19-30', '31-50', '51-70', '71+'])

# 1. Age Group Analysis

# Crosstab for Age Group vs. Number of People Chosen
age_people_crosstab = pd.crosstab(data['Age Group'], data['No. of People Chosen'])
print("Age Group vs. Number of People Chosen:\n", age_people_crosstab)

# Crosstab for Age Group vs. Number of Strengths
age_strengths_crosstab = pd.crosstab(data['Age Group'], data['No. of Strengths'])
print("\nAge Group vs. Number of Strengths:\n", age_strengths_crosstab)

# Crosstab for Age Group vs. Number of Worries
age_worries_crosstab = pd.crosstab(data['Age Group'], data['No. of Worries'])
print("\nAge Group vs. Number of Worries:\n", age_worries_crosstab)

# Crosstab for Age Group vs. Number of Goals
age_goals_crosstab = pd.crosstab(data['Age Group'], data['No. of Goals'])
print("\nAge Group vs. Number of Goals:\n", age_goals_crosstab)

# Crosstab for Age Group vs. K5 Score
age_k5_crosstab = pd.crosstab(data['Age Group'], data['K5 Score'])
print("\nAge Group vs. K5 Score:\n", age_k5_crosstab)

# Crosstab for Age Group vs. K10 Score
age_k10_crosstab = pd.crosstab(data['Age Group'], data['K10 Score'])
print("\nAge Group vs. K10 Score:\n", age_k10_crosstab)

# Crosstab for Age Group vs. PHQ2 Score
age_phq2_crosstab = pd.crosstab(data['Age Group'], data['PhQ2 Score'])
print("\nAge Group vs. PHQ2 Score:\n", age_phq2_crosstab)

# 2. Gender Analysis

# Crosstab for Gender vs. Number of People Chosen
gender_people_crosstab = pd.crosstab(data['Gender'], data['No. of People Chosen'])
print("\nGender vs. Number of People Chosen:\n", gender_people_crosstab)

# Crosstab for Gender vs. Number of Strengths
gender_strengths_crosstab = pd.crosstab(data['Gender'], data['No. of Strengths'])
print("\nGender vs. Number of Strengths:\n", gender_strengths_crosstab)

# Crosstab for Gender vs. Number of Worries
gender_worries_crosstab = pd.crosstab(data['Gender'], data['No. of Worries'])
print("\nGender vs. Number of Worries:\n", gender_worries_crosstab)

# Crosstab for Gender vs. Number of Goals
gender_goals_crosstab = pd.crosstab(data['Gender'], data['No. of Goals'])
print("\nGender vs. Number of Goals:\n", gender_goals_crosstab)

# Crosstab for Gender vs. K5 Score
gender_k5_crosstab = pd.crosstab(data['Gender'], data['K5 Score'])
print("\nGender vs. K5 Score:\n", gender_k5_crosstab)

# Crosstab for Gender vs. K10 Score
gender_k10_crosstab = pd.crosstab(data['Gender'], data['K10 Score'])
print("\nGender vs. K10 Score:\n", gender_k10_crosstab)

# Crosstab for Gender vs. PHQ2 Score
gender_phq2_crosstab = pd.crosstab(data['Gender'], data['PhQ2 Score'])
print("\nGender vs. PHQ2 Score:\n", gender_phq2_crosstab)

# 3. State Analysis

# Crosstab for State vs. Number of People Chosen
state_people_crosstab = pd.crosstab(data['State'], data['No. of People Chosen'])
print("\nState vs. Number of People Chosen:\n", state_people_crosstab)

# Crosstab for State vs. Number of Strengths
state_strengths_crosstab = pd.crosstab(data['State'], data['No. of Strengths'])
print("\nState vs. Number of Strengths:\n", state_strengths_crosstab)

# Crosstab for State vs. Number of Worries
state_worries_crosstab = pd.crosstab(data['State'], data['No. of Worries'])
print("\nState vs. Number of Worries:\n", state_worries_crosstab)

# Crosstab for State vs. Number of Goals
state_goals_crosstab = pd.crosstab(data['State'], data['No. of Goals'])
print("\nState vs. Number of Goals:\n", state_goals_crosstab)

# Crosstab for State vs. K5 Score
state_k5_crosstab = pd.crosstab(data['State'], data['K5 Score'])
print("\nState vs. K5 Score:\n", state_k5_crosstab)

# Crosstab for State vs. K10 Score
state_k10_crosstab = pd.crosstab(data['State'], data['K10 Score'])
print("\nState vs. K10 Score:\n", state_k10_crosstab)

# Crosstab for State vs. PHQ2 Score
state_phq2_crosstab = pd.crosstab(data['State'], data['PhQ2 Score'])
print("\nState vs. PHQ2 Score:\n", state_phq2_crosstab)\

# Visualization Functions

# Heatmap for Age Group vs. Number of People Chosen
plt.figure(figsize=(10, 6))
sns.heatmap(age_people_crosstab, annot=True, fmt='d', cmap='Blues')
plt.title('Heatmap of Age Group vs. Number of People Chosen')
plt.xlabel('Number of People Chosen')
plt.ylabel('Age Group')
plt.show()

# Heatmap for Age Group vs. Number of Strengths
plt.figure(figsize=(12, 6))
sns.heatmap(age_strengths_crosstab, annot=True, fmt='d', cmap='Greens')
plt.title('Heatmap of Age Group vs. Number of Strengths')
plt.xlabel('Number of Strengths')
plt.ylabel('Age Group')
plt.show()

# Heatmap for Gender vs. Number of Worries
plt.figure(figsize=(10, 6))
sns.heatmap(gender_worries_crosstab, annot=True, fmt='d', cmap='Purples')
plt.title('Heatmap of Gender vs. Number of Worries')
plt.xlabel('Number of Worries')
plt.ylabel('Gender')
plt.show()

# Heatmap for State vs. Number of Goals
plt.figure(figsize=(14, 7))
sns.heatmap(state_goals_crosstab, annot=True, fmt='d', cmap='Oranges')
plt.title('Heatmap of State vs. Number of Goals')
plt.xlabel('Number of Goals')
plt.ylabel('State')
plt.show()

# Stacked Bar Chart for Age Group vs. K5 Score
age_k5_crosstab.plot(kind='bar', stacked=True, figsize=(12, 6), colormap='coolwarm')
plt.title('Stacked Bar Chart of Age Group vs. K5 Score')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.legend(title='K5 Score')
plt.show()

# Stacked Bar Chart for Gender vs. K10 Score
gender_k10_crosstab.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='viridis')
plt.title('Stacked Bar Chart of Gender vs. K10 Score')
plt.xlabel('Gender')
plt.ylabel('Count')
plt.legend(title='K10 Score')
plt.show()

# Stacked Bar Chart for State vs. PHQ2 Score
state_phq2_crosstab.plot(kind='bar', stacked=True, figsize=(14, 7), colormap='plasma')
plt.title('Stacked Bar Chart of State vs. PHQ2 Score')
plt.xlabel('State')
plt.ylabel('Count')
plt.legend(title='PHQ2 Score')
plt.show()
