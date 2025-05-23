import os
import pandas as pd
import numpy as np
import requests
from io import StringIO

def generate_synthetic_dataset():
    """
    Generate a synthetic dataset mimicking the Million Song Dataset
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate synthetic data
    n_tracks = 10000
    
    data = {
        'track_id': [f'track_{i}' for i in range(n_tracks)],
        'title': [f'Song {i}' for i in range(n_tracks)],
        'artist_name': [f'Artist {np.random.randint(1, 500)}' for _ in range(n_tracks)],
        'tempo': np.random.uniform(60, 200, n_tracks),
        'time_signature': np.random.choice([3, 4, 6], n_tracks),
        'key': np.random.randint(0, 12, n_tracks),
        'mode': np.random.choice([0, 1], n_tracks)
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Create mood features
    df['valence'] = np.random.uniform(0, 1, n_tracks)  # Random valence
    df['energy'] = np.abs(np.sin(df['tempo'] / 100))  # Energy derived from tempo
    df['danceability'] = np.abs(np.cos(df['time_signature'] / 10))  # Danceability from time signature
    
    # Normalize features
    for feature in ['valence', 'energy', 'danceability']:
        df[feature] = (df[feature] - df[feature].min()) / (df[feature].max() - df[feature].min())
    
    return df

def save_dataset(df, output_path):
    """
    Save the dataset to a CSV file
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save processed dataset
        df.to_csv(output_path, index=False)
        
        print(f"Dataset saved to {output_path}")
        return output_path
    
    except Exception as e:
        print(f"Error saving dataset: {e}")
        return None

def main():
    # Generate synthetic dataset
    synthetic_dataset = generate_synthetic_dataset()
    
    # Save dataset
    output_path = os.path.join('D:/my-projects/moodify/backend/datasets', 'processed_million_song_dataset.csv')
    save_dataset(synthetic_dataset, output_path)

if __name__ == "__main__":
    main()
