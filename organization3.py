import pandas as pd

# Load the dataset
file_path = 'organization_merged_full_analysis.xlsx'
organization_data = pd.read_excel(file_path)

# Specify the organizations of interest
selected_orgs = [
    'Department of Education', 
    'University', 
    'Queensland Health', 
    'Menzies School Of Health Research',  
    'Cdu Ot Masters Students',
    'Headspace',
    'Camhs',
    'Caaps Aboriginal Corporation'
]

# Filter the dataset for these specific organizations
selected_org_data = organization_data[organization_data['Organisation'].isin(selected_orgs)]

# Select the relevant columns and reset the index for easier handling
selected_org_metrics = selected_org_data[
    ['Organisation', 'Total Clients', 'No. of Worries', 'No. of Goals', 'No. of Strengths', 'K5 Score', 'K10 Score', 'PhQ2 Score']
].set_index('Organisation')

# Calculate the totals for each metric across selected organizations
totals = selected_org_metrics.sum(axis=0).to_frame().T
totals.index = ['Total']

# Append the totals row at the end of the dataframe
selected_org_metrics_with_totals = pd.concat([selected_org_metrics, totals])

# Output the final dataframe
print(selected_org_metrics_with_totals)

# Optionally, save the output to an Excel file
output_path = 'm1crosstab.xlsx'
selected_org_metrics_with_totals.to_excel(output_path)
