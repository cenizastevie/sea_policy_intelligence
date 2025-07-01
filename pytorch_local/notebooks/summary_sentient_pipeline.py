import os
import sys
from pathlib import Path
from transformers import (
    AutoModelForSequenceClassification,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline
)
import torch
import pandas as pd
from tqdm import tqdm

# Check if CUDA is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Set up paths to local models
base_path = Path("hf_models")  # Adjust path as needed
sentiment_path = base_path / "sentiment"
summarization_path = base_path / "summarization"

print(f"Looking for models in: {base_path.absolute()}")
print(f"Sentiment model path: {sentiment_path.exists()}")
print(f"Summarization model path: {summarization_path.exists()}")

# Load Sentiment Analysis Model
print("Loading sentiment analysis model...")
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    sentiment_path,
    local_files_only=True
)
sentiment_tokenizer = AutoTokenizer.from_pretrained(
    sentiment_path,
    local_files_only=True
)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=sentiment_model,
    tokenizer=sentiment_tokenizer,
    device=0 if device == "cuda" else -1
)
print("✅ Sentiment analysis model loaded successfully!")

# Load Summarization Model
print("Loading summarization model...")
summarization_model = AutoModelForSeq2SeqLM.from_pretrained(
    summarization_path,
    local_files_only=True
)
summarization_tokenizer = AutoTokenizer.from_pretrained(
    summarization_path,
    local_files_only=True
)
summarization_pipeline = pipeline(
    "summarization",
    model=summarization_model,
    tokenizer=summarization_tokenizer,
    device=0 if device == "cuda" else -1
)
print("✅ Summarization model loaded successfully!")

# Load CSV file
def load_dataframe(csv_file):
    df = pd.read_csv(csv_file)
    df.info()
    return df

# Batch processing function
def process_text_batch(texts, batch_size=8):
    """Process texts in batches for better performance"""
    summaries = []
    sentiments = []
    for i in tqdm(range(0, len(texts), batch_size), desc="Processing batches"):
        batch_texts = texts[i:i+batch_size]
        try:
            batch_summaries = summarization_pipeline(
                batch_texts,
                max_length=100,
                min_length=80,
                do_sample=False,
                truncation=True
            )
            batch_summary_texts = [s['summary_text'] for s in batch_summaries]
            summaries.extend(batch_summary_texts)
            batch_sentiments = sentiment_pipeline(batch_summary_texts)
            sentiments.extend(batch_sentiments)
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
            for _ in batch_texts:
                summaries.append("Error generating summary")
                sentiments.append({"label": "UNKNOWN", "score": 0.0})
    return summaries, sentiments

if __name__ == "__main__":
    csv_file = "channelnewsasia_com.csv"
    df = load_dataframe(csv_file)
    text_column = 'content'
    print(f"Processing {len(df)} articles...")
    texts = df[text_column].fillna("").tolist()
    titles = df['title'].fillna("").tolist()
    # Remove the test_size limit to process all articles
    print(f"Processing all {len(texts)} articles...")
    summaries, sentiments = process_text_batch(texts)
    results_df = pd.DataFrame({
        'original_text': texts,
        'title': titles,
        'summary': summaries,
        'sentiment_label': [s['label'] for s in sentiments],
        'sentiment_score': [s['score'] for s in sentiments]
    })
    print("✅ Processing complete!")
    print(f"Results DataFrame shape: {results_df.shape}")
    print("\nFirst few results:")
    print(results_df.head())
    # Output the results to a CSV file
    output_csv = "summarized_sentiment_results.csv"
    results_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")
