import os
from core import logger


def get_data_path(relative_path: str) -> str:
    """
    Get the data path, using /app/data prefix if DEPLOYED=true, otherwise ./data
    
    Args:
        relative_path: The relative path within the data directory (e.g., "scrape_state.json")
    
    Returns:
        The full path to the data resource
    """
    deployed = os.getenv("DEPLOYED", "false").lower() == "true"
    logger.info(f"get_data_path('{relative_path}'): DEPLOYED={deployed}, env value={os.getenv('DEPLOYED', 'NOT SET')}")
    
    if deployed:
        path = f"/app/data/{relative_path}"
    else:
        path = f"./data/{relative_path}"
    
    logger.info(f"  -> returning: {path}")
    return path
