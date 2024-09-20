import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import nltk

# Download the 'punkt' resource if not already downloaded
nltk.download('punkt')


start_time = time.time()
# Read the Excel file
df = pd.read_excel('C:/Users/DELL/Documents/20211030 Test Assignment/Input.xlsx')

# Extract all URLs from the 'URL' column
urls = df['URL'].tolist()

# Positive words file path
positive_words_file = 'C:/Users/DELL/Documents/20211030 Test Assignment/MasterDictionary/positive-words.txt'
# Negative words file path
negative_words_file = 'C:/Users/DELL/Documents/20211030 Test Assignment/MasterDictionary/negative-words.txt'

# Read positive words from file
with open(positive_words_file, 'r') as file:
    positive_words = file.read().splitlines()

# Read negative words from file
with open(negative_words_file, 'r') as file:
    negative_words = file.read().splitlines()

# Initialize dictionaries to store positive and negative word counts for each URL
positive_word_counts = {}
negative_word_counts = {}

# Process each URL
for url in urls:
    # Fetch data from URL
    response = requests.get(url)
    html_content = response.text
    
    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Count positive words
    positive_count = sum(1 for word in tokens if word in positive_words)
    # Store positive word count for the URL
    positive_word_counts[url] = positive_count
    
    # Count negative words
    negative_count = sum(1 for word in tokens if word in negative_words)
    # Store negative word count for the URL
    negative_word_counts[url] = negative_count

# Calculate polarity score for each URL
polarity_scores = {}
for url in urls:
    positive_count = positive_word_counts[url]
    negative_count = negative_word_counts[url]
    polarity_score = (positive_count - negative_count) / ((positive_count + negative_count) + 0.000001)
    polarity_scores[url] = polarity_score

# Print results for each URL

for url in urls:
    print(f"URL: {url}")
    print(f"Positive words count: {positive_word_counts[url]}")
    print(f"Negative words count: {negative_word_counts[url]}")
    print(f"Polarity score: {polarity_scores[url]}\n")
end_time = time.time()

total = end_time - start_time
print(f"total time taken is: {total}")