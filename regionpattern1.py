import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_excel('cleaned_data_Semester2.xlsx')

# Define Australian states with their postcodes based on the provided link
state_postcodes = {
    'NSW': range(1000, 2599),
    'ACT': range(2600, 2619),
    'VIC': range(3000, 3999),
    'QLD': range(4000, 4999),
    'SA': range(5000, 5799),
    'WA': range(6000, 6797),
    'TAS': range(7000, 7799),
    'NT': range(800, 899) 
}

# Clean the 'Post Code' column by removing NaN values and converting to integer
data['Post Code'] = pd.to_numeric(data['Post Code'], errors='coerce')  # Coerce non-numeric values to NaN
data.dropna(subset=['Post Code'], inplace=True)  # Removing rows with NaN postcodes
data['Post Code'] = data['Post Code'].astype(int)  # Converting postcodes to integers

# Add a new 'State' column based on the 'Post Code' column
def classify_state(postcode):
    for state, postcode_range in state_postcodes.items():
        if int(postcode) in postcode_range:
            return state
    return 'Unknown'

data['State'] = data['Post Code'].apply(classify_state)

# Group by state and get counts and averages
state_analysis = data.groupby('State').agg({
    'Client ID': 'nunique',
    'Practice Session': 'sum',
    'K10 Score': 'mean',
    'K5 Score': 'mean',
    'PhQ2 Score': 'mean',
    'No. of Goals': 'mean',
    'No. of Strengths': 'mean'
}).reset_index()

# Rename columns for better clarity
state_analysis.columns = [
    'State', 'Number of Clients', 'Practice Sessions',
    'K10 Score', 'K5 Score',
    'PHQ2 Score', 'Goals Set',
    'Strengths Input'
]

# Save the state analysis to Excel
output_file = 'mr.xlsx'
with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
    state_analysis.to_excel(writer, sheet_name='Regional Analysis', index=False)

# Plot the analysis
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('State-based Mental Health Analysis')

# Plot number of clients per state
axes[0, 0].barh(state_analysis['State'], state_analysis['Number of Clients'], color='skyblue')
axes[0, 0].set_title('Clients per State')
axes[0, 0].set_xlabel('Number of Clients')

# Plot practice sessions per state
axes[0, 1].barh(state_analysis['State'], state_analysis['Practice Sessions'], color='orange')
axes[0, 1].set_title('Practice Sessions per State')
axes[0, 1].set_xlabel('Practice Sessions')

# Plot average K10 score per state
axes[0, 2].barh(state_analysis['State'], state_analysis['K10 Score'], color='green')
axes[0, 2].set_title('K10 Score per State')
axes[0, 2].set_xlabel('K10 Score')

# Plot average K5 score per state
axes[1, 0].barh(state_analysis['State'], state_analysis['K5 Score'], color='purple')
axes[1, 0].set_title('K5 Score per State')
axes[1, 0].set_xlabel('K5 Score')

# Plot average PHQ2 score per state
axes[1, 1].barh(state_analysis['State'], state_analysis['PHQ2 Score'], color='red')
axes[1, 1].set_title('PHQ2 Score per State')
axes[1, 1].set_xlabel('PHQ2 Score')

# Plot goals and strengths input per state
axes[1, 2].barh(state_analysis['State'], state_analysis['Goals Set'], color='cyan', label='Goals Set')
axes[1, 2].barh(state_analysis['State'], state_analysis['Strengths Input'], color='pink', alpha=0.5, label='Strengths Input')
axes[1, 2].set_title('Goals and Strengths per State')
axes[1, 2].set_xlabel('Goals and Strengths')
axes[1, 2].legend()

plt.tight_layout()
plt.subplots_adjust(top=0.88)
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')

# Create the table from state_analysis DataFrame
table = ax.table(cellText=state_analysis.values,
                 colLabels=state_analysis.columns,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.5, 1.5)  # Adjust the scale of the table

plt.title('Data Table for Regional Analysis')
plt.show()
# Map each postcode to a state using the classify_state function
data['State'] = data['Post Code'].apply(classify_state)

# Group the data by 'State' and 'Organisation' and count unique organizations per state
state_org_usage = data.groupby('State')['Organisation'].nunique()

# Display the result
print("Number of unique organizations being used by clients per state:")
print(state_org_usage)

# Visualize the results
plt.figure(figsize=(10, 6))
state_org_usage.plot(kind='bar', color='skyblue')
plt.title("Number of Unique Organizations by State")
plt.xlabel("State")
plt.ylabel("Number of Organizations")
plt.xticks(rotation=45)
plt.show()
