import pandas as pd
from textblob import TextBlob

# Load the dataset
df = pd.read_csv("enhanced_sample_chat_data.csv")

# Function to preprocess text (if necessary)
def preprocess_text(text):
    # Add any preprocessing steps if needed (e.g., removing special characters, stop words)
    return text

# Function to get sentiment polarity
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Apply sentiment analysis to each lead message
df['cleaned_message'] = df['lead_message'].apply(preprocess_text)
df['sentiment'] = df['cleaned_message'].apply(get_sentiment)

# Aggregate sentiment scores for each lead
lead_sentiment = df.groupby('lead_id')['sentiment'].mean().reset_index()

# Determine potential leads based on sentiment score threshold
threshold = 0.2
lead_sentiment['potential_lead'] = lead_sentiment['sentiment'] > threshold

# Merge sentiment analysis results back to the original dataframe
df = df.merge(lead_sentiment[['lead_id', 'sentiment', 'potential_lead']], on='lead_id', suffixes=('', '_avg'))

# Save the results to a new CSV file
df.to_csv("sentiment_analysis_results.csv", index=False)

print("Sentiment analysis completed and results saved as sentiment_analysis_results.csv")
