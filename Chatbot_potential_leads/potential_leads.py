import pandas as pd
from textblob import TextBlob

# Load the historical sentiment data
historical_df = pd.read_csv("sentiment_analysis_results.csv")

# Define the threshold based on historical analysis
threshold = 0.2

# Function to preprocess text (if necessary)
def preprocess_text(text):
    # Add any preprocessing steps if needed (e.g., removing special characters, stop words)
    return text

# Function to get sentiment polarity
def get_sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

# Function to determine the potentiality percentage of a lead based on current chat messages
def potentiality_percentage(current_messages):
    # Preprocess and analyze sentiment for each message
    sentiments = [get_sentiment(preprocess_text(message)) for message in current_messages]
    
    # Aggregate sentiment scores
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    
    # Scale the average sentiment to a percentage (0% to 100%)
    potentiality_percent = min(max(avg_sentiment / threshold * 100, 0), 100)
    
    return potentiality_percent, avg_sentiment

# Example of current chat messages from a lead
current_chat_messages = [
    "I need some time to decide.",
    "No, I dont want your offer.",
    "Shall we discuss this later?",
    "I need to speak with my manager first.",
    "Alright then, I'll speak with you later."
]

# Determine the potentiality percentage of the current chatting lead
potentiality_percent, avg_sentiment = potentiality_percentage(current_chat_messages)

print(f"Potentiality Percentage of the Lead: {potentiality_percent:.2f}%")
print(f"Average Sentiment Score: {avg_sentiment:.2f}")
