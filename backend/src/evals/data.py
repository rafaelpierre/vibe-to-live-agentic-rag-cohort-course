# Export spans and traces from Phoenix Arize

from phoenix.client import Client
from phoenix.client.types.spans import SpanQuery
import os
import logging
from httpx import HTTPStatusError

logger = logging.getLogger(__name__)

client = Client(
    base_url = os.getenv("PHOENIX_COLLECTOR_ENDPOINT"),
    api_key = os.getenv("PHOENIX_API_KEY")
)

def get_data(project_name: str = "fast_api_agent", span_kind: str = "CHAIN", debug: bool = False):
    """
    Retrieve spans data from Phoenix/Arize for a given project.
    
    Args:
        project_name: Name of the project to retrieve data from
        debug: If True, return all spans without filtering
        
    Returns:
        DataFrame containing spans data
        
    Raises:
        HTTPStatusError: If the API request fails
        ValueError: If the project doesn't exist or query is invalid
    """
    try:
        query = (
            SpanQuery()
            .select("input.value", "output.value")
            .where(f"span_kind == '{span_kind}'")
        )
        
        data = client.spans.get_spans_dataframe(
            query = query,
            project_name=project_name,
            root_spans_only=True
        ).dropna()
        
        return data
        
    except HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving data: {e}")
        raise


def create_dataset():
    """
    Create a dataset from spans data for evaluation.
    
    Returns:
        DataFrame containing spans data
    """
    data = get_data()
    return data