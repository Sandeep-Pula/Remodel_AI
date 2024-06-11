import pandas as pd
from textblob import TextBlob
import os
import datetime

# Load the historical sentiment data
historical_file = "sentiment_analysis_results.csv"
if os.path.exists(historical_file):
    historical_df = pd.read_csv(historical_file)
else:
    # Create an empty DataFrame with the required columns if the file doesn't exist
    historical_df = pd.DataFrame(columns=[
        'lead_id', 'lead_name', 'lead_email', 'lead_source', 'timestamp', 
        'chatbot_question', 'lead_message', 'cleaned_message', 'sentiment', 
        'sentiment_avg', 'potential_lead'
    ])

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

# Chatbot questions
questions = [
    "How can I assist you today?",
    "What product are you interested in?",
    "Can you provide more details about your requirements?",
    "Do you have any specific questions about our service?",
    "Is there anything else you need help with?",
    "Can you elaborate on your concerns?",
    "What are your expectations from our product?",
    "Do you need assistance with pricing?",
    "How soon are you looking to make a decision?",
    "Would you like to schedule a demo?"
]

# Collect responses
responses = []

print("Chatbot: Hi! I'm here to assist you with your queries. Please answer the following questions.")

for question in questions:
    response = input(f"Chatbot: {question}\nYou: ")
    responses.append(response)

# Determine the potentiality percentage of the current chatting lead
potentiality_percent, avg_sentiment = potentiality_percentage(responses)

print(f"\nPotentiality Percentage of the Lead: {potentiality_percent:.2f}%")
print(f"Average Sentiment Score: {avg_sentiment:.2f}")

# Append the conversation and results to the historical data
lead_id = historical_df['lead_id'].max() + 1 if not historical_df.empty else 1
lead_name = "Current Lead"  # Placeholder for lead name
lead_email = "lead@example.com"  # Placeholder for lead email
lead_source = "Chatbot Interaction"  # Placeholder for lead source
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

new_data = []

for question, response in zip(questions, responses):
    cleaned_message = preprocess_text(response)
    sentiment = get_sentiment(cleaned_message)
    new_data.append({
        'lead_id': lead_id,
        'lead_name': lead_name,
        'lead_email': lead_email,
        'lead_source': lead_source,
        'timestamp': timestamp,
        'chatbot_question': question,
        'lead_message': response,
        'cleaned_message': cleaned_message,
        'sentiment': sentiment,
        'sentiment_avg': avg_sentiment,
        'potential_lead': potentiality_percent > threshold
    })

new_df = pd.DataFrame(new_data)
historical_df = pd.concat([historical_df, new_df], ignore_index=True)

# Save the updated historical data to the CSV file
historical_df.to_csv(historical_file, index=False)

print("Conversation and results have been saved for continuous training.")
