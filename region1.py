import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'cleaned_data_Semester2.xlsx'
data = pd.read_excel(file_path)

# Define Australian state ranges by postcode
postcode_ranges = {
    'NSW': range(1000, 2600),
    'VIC': range(3000, 4000),
    'QLD': range(4000, 5000),
    'SA': range(5000, 5800),
    'WA': range(6000, 6800),
    'TAS': range(7000, 7800),
    'ACT': range(2600, 2620),
    'NT': range(800, 1000),
}

# Function to map postcodes to regions
def get_region(postcode):
    try:
        postcode = int(postcode)
        for state, p_range in postcode_ranges.items():
            if postcode in p_range:
                return state
        return 'Other'
    except:
        return 'Unknown'

# Apply the function to create a Region column
data['Region'] = data['Post Code'].apply(get_region)

# Cross-tabulation on the region and specific metrics
crosstab_data = pd.pivot_table(
    data,
    values=['Client ID', 'Session Number', 'K10 Score', 'K5 Score', 'PhQ2 Score', 'No. of Goals', 'No. of Strengths', 'Organisation'],
    index='Region',
    aggfunc={
        'Client ID': 'nunique', 
        'Session Number': 'count', 
        'K10 Score': 'mean', 
        'K5 Score': 'mean', 
        'PhQ2 Score': 'mean', 
        'No. of Goals': 'mean', 
        'No. of Strengths': 'mean', 
        'Organisation': 'nunique'
    }
)

# Create a total row with the number of states and the averages for each metric
total_row = pd.DataFrame(crosstab_data.mean()).T
total_row.index = ['Total']
total_row['Client ID'] = crosstab_data['Client ID'].sum()  # Sum of total clients across states
total_row['Session Number'] = crosstab_data['Session Number'].sum()  # Sum of practice sessions across states
crosstab_data_with_total = pd.concat([crosstab_data, total_row])

# Save cross-tab data with averages in the total row to Excel
output_path = 'region_crosstab_analysis.xlsx'
crosstab_data_with_total.to_excel(output_path)
print(f"Cross-tab data saved to {output_path}")

# Display cross-tab data with totals in console
print("Cross-tabulated data by Region with Totals (Averages for Metrics, Totals for Clients/Sessions):")
print(crosstab_data_with_total)

# First Figure: Main Visualization with Metrics (Leave this figure as it was)
fig1, axes = plt.subplots(2, 3, figsize=(18, 10))
fig1.suptitle("Regional Analysis of Mental Health Metrics", fontsize=16)

# Plot each metric in the main visualization figure
axes[0, 0].bar(crosstab_data.index, crosstab_data['Client ID'], color='skyblue')
axes[0, 0].set_title('Total Clients per State')
axes[0, 0].set_xlabel('Region')
axes[0, 0].set_ylabel('Total Clients')

axes[0, 1].bar(crosstab_data.index, crosstab_data['Session Number'], color='orange')
axes[0, 1].set_title('Practice Sessions per State')
axes[0, 1].set_xlabel('Region')
axes[0, 1].set_ylabel('Practice Sessions')

axes[0, 2].bar(crosstab_data.index, crosstab_data['K10 Score'], color='green')
axes[0, 2].set_title('Average K10 Score by State')
axes[0, 2].set_xlabel('Region')
axes[0, 2].set_ylabel('K10 Score')

axes[1, 0].bar(crosstab_data.index, crosstab_data['K5 Score'], color='purple')
axes[1, 0].set_title('Average K5 Score by State')
axes[1, 0].set_xlabel('Region')
axes[1, 0].set_ylabel('K5 Score')

axes[1, 1].bar(crosstab_data.index, crosstab_data['PhQ2 Score'], color='red')
axes[1, 1].set_title('Average PhQ2 Score by State')
axes[1, 1].set_xlabel('Region')
axes[1, 1].set_ylabel('PhQ2 Score')

width = 0.35  # width of the bars
index = range(len(crosstab_data.index))
axes[1, 2].bar(index, crosstab_data['No. of Goals'], width, color='lightblue', label='Goals')
axes[1, 2].bar([i + width for i in index], crosstab_data['No. of Strengths'], width, color='pink', label='Strengths')
axes[1, 2].set_xticks([i + width / 2 for i in index])
axes[1, 2].set_xticklabels(crosstab_data.index)
axes[1, 2].set_title('Average Goals and Strengths per State')
axes[1, 2].set_xlabel('Region')
axes[1, 2].set_ylabel('Average Count')
axes[1, 2].legend()

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Second Figure: Data Table
fig2, ax2 = plt.subplots(figsize=(12, 8))
ax2.axis('tight')
ax2.axis('off')
table_data = crosstab_data_with_total.round(2)  # Round data for clarity
table = ax2.table(cellText=table_data.values,
                  colLabels=table_data.columns,
                  rowLabels=table_data.index,
                  cellLoc='center',
                  loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)
ax2.set_title("Cross-Tab Stats of Regional Analysis", pad=20)

# Third Figure: Unique Organizations per State
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.bar(crosstab_data.index, crosstab_data['Organisation'], color='lightblue')
ax3.set_title('Number of Unique Organizations by State')
ax3.set_xlabel('State')
ax3.set_ylabel('Number of Organizations')

# Display all figures
plt.show()
