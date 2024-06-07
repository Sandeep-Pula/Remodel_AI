import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Generate unique lead IDs
num_leads = 50  # Number of unique leads
messages_per_lead = 10  # Minimum messages per lead
total_messages = num_leads * messages_per_lead

lead_ids = np.repeat(np.arange(1, num_leads + 1), messages_per_lead)
messages = [
    "I'm interested in your product.",
    "Can you give me more details?",
    "Not really satisfied with the information.",
    "Looks promising!",
    "I have some doubts.",
    "I'm happy with the service.",
    "I need more time to decide.",
    "This is not what I expected.",
    "Could you help me with the pricing?",
    "Great, let's move forward.",
    "I'm not interested.",
    "Thanks for the information.",
    "I'll get back to you.",
    "This sounds good.",
    "I need a demo before making a decision."
]

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

# Randomly select messages and assign to leads
messages_sample = np.random.choice(messages, size=total_messages, replace=True)
questions_sample = np.random.choice(questions, size=total_messages, replace=True)

# Generate additional attributes
timestamps = [fake.date_time_this_year() for _ in range(total_messages)]
lead_names = [fake.name() for _ in range(num_leads)]
lead_emails = [fake.email() for _ in range(num_leads)]
lead_sources = np.random.choice(['Website', 'Referral', 'Social Media', 'Advertisement'], size=num_leads, replace=True)

# Expand lead names and emails to match the number of messages
lead_names_expanded = np.repeat(lead_names, messages_per_lead)
lead_emails_expanded = np.repeat(lead_emails, messages_per_lead)
lead_sources_expanded = np.repeat(lead_sources, messages_per_lead)

# Create DataFrame
data = {
    'lead_id': lead_ids,
    'lead_name': lead_names_expanded,
    'lead_email': lead_emails_expanded,
    'lead_source': lead_sources_expanded,
    'timestamp': timestamps,
    'chatbot_question': questions_sample,
    'lead_message': messages_sample
}

df = pd.DataFrame(data)

# Save DataFrame to CSV
df.to_csv("enhanced_sample_chat_data.csv", index=False)

print("Dataset saved as enhanced_sample_chat_data.csv")
