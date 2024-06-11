import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download required NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('vader_lexicon')

# Load the dataset
df = pd.read_csv("enhanced_sample_chat_data.csv")

# Initialize NLTK tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()

# Function to preprocess text
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    words = word_tokenize(text)
    # Remove stop words and lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]
    # Reconstruct text
    return ' '.join(words)

# Function to get sentiment polarity using VADER
def get_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Apply preprocessing and sentiment analysis
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
