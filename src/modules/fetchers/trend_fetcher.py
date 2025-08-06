from src.utils.utilities import load_column_from_csv, preprocess_text_list


def load_trends(source="generated",column="text" , preprocess=False) -> list[str]:
    """
    Load trend texts from a selected source.

    Parameters:
        source (str): "raw" or "generated" or any dataset's name
        column (str): name of the column to extract from CSV
        preprocess (bool): Whether to apply preprocessing to the texts

    Returns:
        list[str]: List of text entries (raw or cleaned)
    """
    path_map = {
        "raw": "data/trends.csv",
        "generated": "data/trends_generated.csv"
    }

    texts = load_column_from_csv(path_map, source=source, column=column)

    if preprocess:
        texts = preprocess_text_list(texts)

    return texts
