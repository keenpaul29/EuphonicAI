import os
import pandas as pd
import numpy as np
import requests
from io import StringIO

def download_dataset():
    """
    Download a subset of the Million Song Dataset
    """
    # URL for a preprocessed subset of the Million Song Dataset
    dataset_url = "https://raw.githubusercontent.com/urinieto/msaf/master/data/sample_msd.csv"
    
    try:
        # Download the dataset
        response = requests.get(dataset_url)
        response.raise_for_status()
        
        # Save the dataset
        dataset_path = os.path.join('D:/my-projects/moodify/backend/datasets', 'million_song_subset.csv')
        
        with open(dataset_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        return dataset_path
    
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

def preprocess_dataset(input_path):
    """
    Preprocess the dataset for mood-based playlist generation
    """
    try:
        # Read the dataset
        df = pd.read_csv(input_path)
        
        # Select and rename columns
        columns_to_keep = [
            'track_id', 
            'title', 
            'artist_name', 
            'tempo', 
            'time_signature', 
            'key', 
            'mode'
        ]
        
        # Validate columns
        available_columns = set(df.columns)
        columns_to_keep = [col for col in columns_to_keep if col in available_columns]
        
        # Create mood features
        df['valence'] = np.random.uniform(0, 1, len(df))  # Random valence
        df['energy'] = np.abs(np.sin(df['tempo'] / 100))  # Energy derived from tempo
        df['danceability'] = np.abs(np.cos(df['time_signature'] / 10))  # Danceability from time signature
        
        # Normalize features
        for feature in ['valence', 'energy', 'danceability']:
            df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())
        
        # Select final columns
        processed_df = df[columns_to_keep + ['valence', 'energy', 'danceability']]
        
        # Save processed dataset
        output_path = os.path.join('D:/my-projects/moodify/backend/datasets', 'processed_million_song_dataset.csv')
        processed_df.to_csv(output_path, index=False)
        
        print(f"Processed dataset saved to {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error preprocessing dataset: {e}")
        return None

def main():
    # Download dataset
    downloaded_path = download_dataset()
    
    if downloaded_path:
        # Preprocess dataset
        preprocess_dataset(downloaded_path)
    else:
        print("Failed to download dataset")

if __name__ == "__main__":
    main()
