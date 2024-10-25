# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'cleaned_data_Semester2.xlsx'  
data = pd.read_excel(file_path)

# Step 1: Filter the dataset for necessary columns
time_series_data = data[['Client ID', 'Session Number', 'K10 Score']]

# Drop rows with missing K10 scores
time_series_data = time_series_data.dropna(subset=['K10 Score'])

# Step 2: Calculate moving average for K10 scores (window of 2 sessions for simplicity)
time_series_data = time_series_data.sort_values(by=['Client ID', 'Session Number'])
time_series_data['K10_Moving_Avg'] = time_series_data.groupby('Client ID')['K10 Score'].rolling(window=2).mean().reset_index(level=0, drop=True)

# Step 3: Visualize the K10 Score trends with moving averages
plt.figure(figsize=(12, 6))
sample_clients = time_series_data['Client ID'].unique()[:1000]  #  sample clients

for client in sample_clients:
    client_data = time_series_data[time_series_data['Client ID'] == client]
    plt.plot(client_data['Session Number'], client_data['K10_Moving_Avg'], label=f'Client {client}')

plt.title('K10 Score Moving Average Trends (Sample Clients)')
plt.xlabel('Session Number')
plt.ylabel('K10 Score Moving Average')
plt.legend()
plt.show()
