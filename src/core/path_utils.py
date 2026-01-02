import os


def get_data_path(relative_path: str) -> str:
    """
    Get the data path, using /app/data prefix if DEPLOYED=true, otherwise ./data
    
    Args:
        relative_path: The relative path within the data directory (e.g., "scrape_state.json")
    
    Returns:
        The full path to the data resource
    """
    if os.getenv("DEPLOYED", "false").lower() == "true":
        return f"/app/data/{relative_path}"
    else:
        return f"./data/{relative_path}"
