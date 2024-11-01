import urllib.request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk


    
def download_text(url):
    with urllib.request.urlopen(url) as f:
        text = f.read().decode('utf-8')
    return text
    
def clean_gutenberg_text(text): # find the main content
    """Remove project gutenberg boilerplate and clean the text"""
    start_markers = ["*** START OF THE PROJECT GUTENBERG EBOOK THE GREAT GATSBY ***"]
    end_markers = ["*** END OF THE PROJECT GUTENBERG EBOOK THE GREAT GATSBY ***"]
    start_position = len(text)
    for marker in start_markers: # start of main content
        position = text.find(marker)
        if position != -1:
            end_of_line = text.find("\n", position)
            if end_of_line != -1 and end_of_line < start_position:
                start_position = end_of_line
    
    end_position = 0 # end of main content
    for marker in end_markers:
        position = text.find(marker)
        if position != -1 and position > end_position:
            end_position = position
    
    if start_position < len(text) and end_position > 0: # extract main content if positions are valid
        main_text = text[start_position:end_position].strip()
    else:
        main_text = text # fallback to original text if markers not found
    
    return main_text

def calculate_word_frequency(text):
    """
    calculate frequency of each word in the text
    """
    words = text.lower().split()
    punctuation = ".,!?()[]{}:;"
    cleaned_words = []
    for word in words:
        for char in punctuation:
            word =word.replace(char,"")
        if word:
            cleaned_words.append(word)
    
    word_freq = {}
    for word in cleaned_words:
        if word:
            word_freq[word] = word_freq.get(word, 0) + 1
    return word_freq

def sort_by_frequency(item):
    """
    help function to sort
    """
    return item[1]
    
def generate_summary_statistics(word_frequency):
    """
    generate summary statistics from word frequency
    """
    total_words = sum(word_frequency.values())
    unique_words = len(word_frequency)
    average_frequency = total_words / unique_words if unique_words > 0 else 0
    sorted_words = sorted(word_frequency.items(),key=lambda x:x[1], reverse=True)
    
    statistics = {
        "total_words":total_words,
        "unique_words":unique_words,
        "average_frequency": average_frequency,
        "most_common_words":sorted_words[:10]
    }
    return statistics

def remove_stop_words(words_frequency):
    """
    remover stop words and recalculate frequency
    """
    stop_words = {"a", "of", "on", "i", "for", "with", "the", "at", "from", "in" , "to" } 
    filtered_frequency = {word: freq for word, freq in words_frequency.items() if word not in stop_words}
    return filtered_frequency

def perform_sentiment_analysis(text):
    """
    perform sentiment analysis using both vader and text blob
    """
    try:
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            nltk.download('vader_lexicon')
    
        vader_analyzer = SentimentIntensityAnalyzer()
        vader_scores = vader_analyzer.polarity_scores(text)
    
        blob = TextBlob(text)
        textblob_scores = {
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
        
        return {
            'vader': vader_scores,
            'textblob': textblob_scores
        }
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        return None
        
def analyze_text(text):
    """
    show the analyze
    """
    clean_text = clean_gutenberg_text(text)
    
    print("\n=== Initial Word Frequency Analysis ===")
    word_frequency = calculate_word_frequency(clean_text)
    stats = generate_summary_statistics(word_frequency)
    
    print(f"\nTotal words: {stats['total_words']}")
    print(f"Unique words: {stats['unique_words']}")
    print(f"Average word frequency: {stats['average_frequency']:.2f}")
    print("\nTop 10 most frequent words (including stop words):")
    for word, freq in stats['most_common_words']:
        print(f"'{word}': {freq} times")
    
    # Remove stop words and reanalyze
    print("\n=== Analysis After Removing Stop Words ===")
    filtered_frequency = remove_stop_words(word_frequency)
    filtered_stats = generate_summary_statistics(filtered_frequency)
    
    print(f"\nUnique words (excluding stop words): {filtered_stats['unique_words']}")
    print("\nTop 10 most frequent words (excluding stop words):")
    for word, freq in filtered_stats['most_common_words']:
        print(f"'{word}': {freq} times")
    print("\n=== Sentiment Analysis ===")
    sentiment_scores = perform_sentiment_analysis(clean_text)
    if sentiment_scores:
        print("\nVADER Sentiment Scores:")
        for key, value in sentiment_scores['vader'].items():
            print(f"{key}: {value:.3f}")
        print("\nTextBlob Sentiment Scores:")
        print(f"Polarity: {sentiment_scores['textblob']['polarity']:.3f}")
        print(f"Subjectivity: {sentiment_scores['textblob']['subjectivity']:.3f}")

def main():
    url = 'https://www.gutenberg.org/cache/epub/64317/pg64317.txt'
    try:
        text = download_text(url)
        analyze_text(text)
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Please ensure you have internet connection and have installed required packages:")
        print("pip install nltk textblob")
        

if __name__ == "__main__":
    main()