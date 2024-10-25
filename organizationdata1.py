import pandas as pd
# organization.........................s
# Load the dataset
file_path = 'cleaned_data_Semester2.xlsx'  # Update this path
data = pd.read_excel(file_path)

# Define the mapping of specific organization names for consistent naming
organization_mapping = {
    'det': 'Department of Education',
    'dept of edu': 'Department of Education',
    'department of edu': 'Department of Education',
    'Departmemt Of Education Nsw': 'Department of Education',
    'Department For Education': 'Department of Education',
    'Department For Education Nsw': 'Department of Education',
    'Department Of Education': 'Department of Education',
    'Department Of Education ': 'Department of Education',
    'Department Of Education Nsw': 'Department of Education',
    'NSW Department Of Education': 'Department of Education',
    'NT DoE': 'Department of Education',
    'Nsw Department Of Education': 'Department of Education',
    'Nsw Dept Of Education ': 'Department of Education',
    'department of education': 'Department of Education',
    'NSW Department of Education': 'Department of Education',
    'camhs ': 'Camhs',
    'Camhs': 'Camhs',
    'Camhs orange': 'Camhs',
    'Camhsresources@sa.gov.au': 'Camhs',
    'Catholic Care NT': 'Catholic Care',
    'Catholiccare ': 'Catholic Care',
    'catholiccare nt ': 'Catholic Care',
    'Headspace Adelaide': 'Headspace',
    'Headspace ': 'Headspace',
    'headspace': 'Headspace',
    'headspace Adelaide': 'Headspace',
    'headspace Darwin ': 'Headspace',
    'Life Without Barriers': 'Life Without Barriers',
    'life without barriers ': 'Life Without Barriers',
    'Life Without Barriers ': 'Life Without Barriers',
    'curtin': 'University',
    'Curtin': 'University',
    'Curtin University': 'University',
    'Curtin University ': 'University',
    'Charles Darwin University': 'University'
}

# Replace specific names with standardized names
data['Organisation'] = data['Organisation'].replace(organization_mapping)

# Set all organizations containing "education" to "Department of Education"
data['Organisation'] = data['Organisation'].apply(lambda x: 'Department of Education' if isinstance(x, str) and 'education' in x.lower() else x)

# Aggregating basic metrics: total clients, trained/not trained counts
org_client_counts = data.groupby('Organisation')['Client ID'].nunique().reset_index()
org_client_counts.columns = ['Organisation', 'Total Clients']

# Count of trained and not trained per organization
org_training_counts = data.groupby(['Organisation', 'Trained']).size().unstack(fill_value=0).reset_index()
org_training_counts.columns = ['Organisation', 'Not Trained', 'Trained']

# Merge client and training counts
org_analysis = pd.merge(org_client_counts, org_training_counts, on='Organisation')

# Additional metrics columns to aggregate
metrics_columns = ['Total', 'No. of Worries', 'No. of Goals', 'No. of Strengths', 'K5 Score', 'K10 Score', 'PhQ2 Score']

# Sum of the additional metrics per organization
org_metrics = data.groupby('Organisation')[metrics_columns].sum().reset_index()

# Merge all data into one DataFrame
org_full_analysis = pd.merge(org_analysis, org_metrics, on='Organisation')

# Save the final result to an Excel file
output_path = 'organization_merged_full_analysis.xlsx'  # Update with your desired output path
org_full_analysis.to_excel(output_path, index=False)

print(f"Analysis complete. File saved as: {output_path}")
