import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk
from autocorrect import Speller
from spellchecker import SpellChecker

# Function to download required NLTK resources
def download_nltk_resources():
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('vader_lexicon')

# Function to initialize NLTK tools and Spellers
def initialize_tools():
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    sia = SentimentIntensityAnalyzer()
    autocorrect_speller = Speller()
    spell_checker = SpellChecker()
    return stop_words, lemmatizer, sia, autocorrect_speller, spell_checker

# Function to load the dataset
def load_dataset(filepath):
    return pd.read_csv(filepath)

# Function to preprocess text
def preprocess_text(text, autocorrect_speller, spell_checker, lemmatizer, stop_words):
    # Initial autocorrect
    text = autocorrect_speller(text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize
    words = word_tokenize(text)
    # Spell check and correct
    misspelled = spell_checker.unknown(words)
    words = [spell_checker.correction(word) if word in misspelled else word for word in words]
    # Remove stop words and lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]
    # Reconstruct text
    return ' '.join(words)

# Function to get sentiment polarity using VADER
def get_sentiment_vader(text, sia):
    return sia.polarity_scores(text)['compound']

# Function to get polarity and subjectivity using TextBlob
def get_sentiment_textblob(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity, analysis.sentiment.subjectivity

# Function to apply preprocessing and sentiment analysis
def apply_sentiment_analysis(df, stop_words, lemmatizer, sia, autocorrect_speller, spell_checker):
    df['cleaned_message'] = df['lead_message'].apply(lambda text: preprocess_text(text, autocorrect_speller, spell_checker, lemmatizer, stop_words))
    df['vader_sentiment'] = df['cleaned_message'].apply(lambda text: get_sentiment_vader(text, sia))
    df[['textblob_polarity', 'textblob_subjectivity']] = df['cleaned_message'].apply(lambda text: pd.Series(get_sentiment_textblob(text)))
    return df

# Function to aggregate sentiment scores for each lead
def aggregate_sentiment_scores(df):
    lead_sentiment = df.groupby('lead_id').agg({
        'vader_sentiment': 'mean',
        'textblob_polarity': 'mean',
        'textblob_subjectivity': 'mean'
    }).reset_index()
    return lead_sentiment

# Function to normalize VADER sentiment to a 0-1 scale for potential lead score
def normalize_vader_sentiment(lead_sentiment):
    lead_sentiment['potential_lead_score'] = (lead_sentiment['vader_sentiment'] + 1) / 2
    return lead_sentiment

# Function to merge sentiment analysis results back to the original dataframe
def merge_sentiment_results(df, lead_sentiment):
    df = df.merge(lead_sentiment[['lead_id', 'vader_sentiment', 'textblob_polarity', 'textblob_subjectivity', 'potential_lead_score']], on='lead_id', suffixes=('', '_avg'))
    return df

# Function to save the results to a new CSV file
def save_results(df, output_file_path):
    df.to_csv(output_file_path, index=False)
    print(f"Sentiment analysis completed and results saved as {output_file_path}")

# Main function to call all other functions
def main():
    download_nltk_resources()
    stop_words, lemmatizer, sia, autocorrect_speller, spell_checker = initialize_tools()
    
    # Load the dataset
    df = load_dataset('Remodel_AI.csv')

    # Apply preprocessing and sentiment analysis
    df = apply_sentiment_analysis(df, stop_words, lemmatizer, sia, autocorrect_speller, spell_checker)

    # Aggregate sentiment scores for each lead
    lead_sentiment = aggregate_sentiment_scores(df)

    # Normalize VADER sentiment to a 0-1 scale for potential lead score
    lead_sentiment = normalize_vader_sentiment(lead_sentiment)

    # Merge sentiment analysis results back to the original dataframe
    df = merge_sentiment_results(df, lead_sentiment)

    # Save the results to a new CSV file
    save_results(df, "sentiment_analysis_results.csv")

# Run the main function
if __name__ == "__main__":
    main()
