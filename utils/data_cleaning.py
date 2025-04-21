import re

def clean_text(text):
    # Convert to lowercase
    text = text.lower()
    
    # Remove digits and punctuation
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text
