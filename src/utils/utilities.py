import pandas as pd
import re



def load_column_from_csv(path_map: dict, source: str, column: str, dropna: bool = True) -> list[str]:
    """
    Load a specific column from a CSV file based on a source-to-path mapping.

    Parameters:
        path_map (dict): A dictionary mapping source names to CSV file paths.
                         Example: {"raw": "data/raw.csv", "generated": "data/gen.csv"}
        source (str): The key to select which file path to use.
        column (str): Name of the column to load from the CSV.
        dropna (bool): Whether to drop rows where the column is NaN.

    Returns:
        list[str]: A list of values (as strings) from the specified column.
    """
    if source not in path_map:
        raise ValueError(f"❌ Unknown source: '{source}'. Available sources: {list(path_map.keys())}")

    csv_path = path_map[source]

    try:
        df = pd.read_csv(csv_path)
        if column not in df.columns:
            raise ValueError(f"❌ Column '{column}' not found in file: {csv_path}")

        series = df[column]
        if dropna:
            series = series.dropna()

        return series.astype(str).tolist()

    except FileNotFoundError:
        print(f"❌ File not found: {csv_path}")
        return []
    except Exception as e:
        print(f"❌ Error reading CSV file '{csv_path}': {e}")
        return []






def clean_text(text: str) -> str:
    """
    Clean a single text string by applying:
    - Lowercasing
    - URL removal
    - Mention (@user) removal
    - Hashtag symbol removal (but keep the word)
    - Emoji and special character removal
    - Extra whitespace normalization
    """
    text = text.lower()
    text = re.sub(r'http\S+|www\S+', '', text)  # Remove URLs
    text = re.sub(r'@\w+', '', text)            # Remove mentions
    text = re.sub(r'#(\w+)', r'\1', text)       # Keep hashtag word
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove emojis and punctuation
    text = re.sub(r'\s+', ' ', text).strip()    # Normalize whitespace
    return text





def preprocess_text_list(texts: list[str]) -> list[str]:
    """
    Apply `clean_text` to a list of strings.
    """
    return [clean_text(t) for t in texts]



import json

def load_json_data(path: str) -> list:
    """
    Load a JSON file containing either a list of dictionaries or a list of strings.

    Parameters:
        path (str): Path to the JSON file.

    Returns:
        List: The loaded data, either as list[dict] or list[str].
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON content must be a list.")
        return data
    except Exception as e:
        print(f"❌ Error loading JSON file '{path}': {e}")
        return []
