import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt

# Define function to clean and tokenize text
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

# Define function to clean, tokenize, and remove stopwords and blank entries
def clean_and_filter_text_no_blanks(text, stop_words):
    words = clean_text(text)
    # Filter out stop words and blank entries
    return [word for word in words if word not in stop_words and word.strip() != '']

# Load the dataset
data = pd.read_excel('cleaned_data_Semester2.xlsx', sheet_name='in')

# Define stop words to remove (conjunctions, common words)
stop_words = {'and', 'or', 'to', '00', 'too', 'being'}

# Get 'strength' and 'worry' columns
strength_columns = [col for col in data.columns if 'Strength' in col]
worry_columns = [col for col in data.columns if 'Worry' in col]

# Concatenate and clean text data
strength_data = data[strength_columns].fillna('').astype(str).apply(lambda x: ' '.join(x), axis=1)
worry_data = data[worry_columns].fillna('').astype(str).apply(lambda x: ' '.join(x), axis=1)

# Count word frequencies excluding stopwords and blank entries
strength_words = strength_data.apply(lambda x: clean_and_filter_text_no_blanks(x, stop_words)).explode()
worry_words = worry_data.apply(lambda x: clean_and_filter_text_no_blanks(x, stop_words)).explode()

strength_word_counts = Counter(strength_words)
worry_word_counts = Counter(worry_words)

# Remove any blank entries from the word counts
filtered_strength_word_counts_no_blanks = {k: v for k, v in strength_word_counts.items() if k and pd.notna(k)}
filtered_worry_word_counts_no_blanks = {k: v for k, v in worry_word_counts.items() if k and pd.notna(k)}

# Convert filtered word counts to DataFrames and sort by frequency
strengths_df_no_blanks = pd.DataFrame(filtered_strength_word_counts_no_blanks.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)
worries_df_no_blanks = pd.DataFrame(filtered_worry_word_counts_no_blanks.items(), columns=['Word', 'Frequency']).sort_values(by='Frequency', ascending=False)

# Save the sorted data to Excel
output_file_path_sorted = 'Freetextanalysisfreq.xlsx'

with pd.ExcelWriter(output_file_path_sorted) as writer:
    strengths_df_no_blanks.to_excel(writer, sheet_name='Strengths Word Frequency', index=False)
    worries_df_no_blanks.to_excel(writer, sheet_name='Worries Word Frequency', index=False)

# Function to create bar plots with indexed frequency values for word frequencies
def plot_word_frequencies_with_value_labels(df, title):
    plt.figure(figsize=(10, 6))
    bars = plt.barh(df['Word'], df['Frequency'], color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(title)
    plt.gca().invert_yaxis()  # To display the highest frequency at the top
    
    # Add frequency values next to each bar
    for bar in bars:
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{int(bar.get_width())}', va='center')
    
    plt.show()

# Visualize the top 10 strengths and worries with indexed frequency labels
plot_word_frequencies_with_value_labels(strengths_df_no_blanks.head(10), 'Strengths Word Frequency (With Values)')
plot_word_frequencies_with_value_labels(worries_df_no_blanks.head(10), 'Worries Word Frequency (With Values)')

print(f"Analysis saved to {output_file_path_sorted}")
