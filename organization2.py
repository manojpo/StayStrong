import pandas as pd
from scipy import stats

# Load the dataset
file_path = 'organization_merged_full_analysis.xlsx'  # Update this path if necessary
data = pd.read_excel(file_path)

# Separate the data by training status
trained_data = data[data['Trained'] > 0]
untrained_data = data[data['Not Trained'] > 0]

# Define the metrics for analysis
metrics = ['Total Clients', 'Total', 'K10 Score', 'K5 Score', 'PhQ2 Score', 'No. of Goals', 'No. of Strengths']

# Dictionary to store F-values and p-values for each metric
anova_results = {}

# Perform ANOVA for each metric comparing trained and untrained organizations
for metric in metrics:
    # Extract metric values for trained and untrained organizations
    trained_values = trained_data[metric].dropna()
    untrained_values = untrained_data[metric].dropna()
    
    # Perform one-way ANOVA
    f_value, p_value = stats.f_oneway(trained_values, untrained_values)
    
    # Store the results
    anova_results[metric] = {'F-value': f_value, 'p-value': p_value}

# Convert results to a DataFrame for better readability
anova_df = pd.DataFrame(anova_results).T

# Display the F-values and p-values for each metric
print(anova_df)
