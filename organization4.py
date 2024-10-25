import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'm1crosstab.xlsx'  
data = pd.read_excel(file_path)

# Rename the first column to 'Organisation' for clarity
data.rename(columns={'Unnamed: 0': 'Organisation'}, inplace=True)

# Calculate per-client values
data['K10 Score per Client'] = data['K10 Score'] / data['Total Clients']
data['K5 Score per Client'] = data['K5 Score'] / data['Total Clients']
data['PHQ2 Score per Client'] = data['PhQ2 Score'] / data['Total Clients']
data['Goals per Client'] = data['No. of Goals'] / data['Total Clients']
data['Strengths per Client'] = data['No. of Strengths'] / data['Total Clients']

# Display the updated dataset in the console
print("Updated dataset with per-client values:")
print(data)

# Save the data to an Excel file
output_path = 'm5.xlsx'
data.to_excel(output_path, index=False)
print(f"Data for visualization saved to {output_path}")

# Setting up the figure for multiple subplots (2 rows, 3 columns)
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.tight_layout(pad=6.0)

# Plot 1: Total Clients per Organization
axes[0, 0].barh(data['Organisation'], data['Total Clients'], color='skyblue')
axes[0, 0].set_title('Total Clients per Organization')
axes[0, 0].set_xlabel('Number of Clients')
axes[0, 0].set_ylabel('Organization')

# Plot 2: Total Worries per Organization
axes[0, 1].barh(data['Organisation'], data['No. of Worries'], color='orange')
axes[0, 1].set_title('Total Worries per Organization')
axes[0, 1].set_xlabel('Number of Worries')
axes[0, 1].set_ylabel('Organization')

# Plot 3: K10 Score per Client per Organization
axes[0, 2].barh(data['Organisation'], data['K10 Score per Client'], color='green')
axes[0, 2].set_title('K10 Score per Client per Organization')
axes[0, 2].set_xlabel('K10 Score per Client')
axes[0, 2].set_ylabel('Organization')

# Plot 4: K5 Score per Client per Organization
axes[1, 0].barh(data['Organisation'], data['K5 Score per Client'], color='purple')
axes[1, 0].set_title('K5 Score per Client per Organization')
axes[1, 0].set_xlabel('K5 Score per Client')
axes[1, 0].set_ylabel('Organization')

# Plot 5: PHQ2 Score per Client per Organization
axes[1, 1].barh(data['Organisation'], data['PHQ2 Score per Client'], color='red')
axes[1, 1].set_title('PHQ2 Score per Client per Organization')
axes[1, 1].set_xlabel('PHQ2 Score per Client')
axes[1, 1].set_ylabel('Organization')

# Plot 6: Goals and Strengths per Client per Organization
axes[1, 2].barh(data['Organisation'], data['Goals per Client'], color='lightblue', label='Goals per Client')
axes[1, 2].barh(data['Organisation'], data['Strengths per Client'], color='pink', alpha=0.7, label='Strengths per Client')
axes[1, 2].set_title('Goals and Strengths per Client per Organization')
axes[1, 2].set_xlabel('Goals and Strengths per Client')
axes[1, 2].set_ylabel('Organization')
axes[1, 2].legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
