# Export spans and traces from Phoenix Arize

from phoenix.client import Client
from phoenix.client.types.spans import SpanQuery
import os
import logging
from httpx import HTTPStatusError

logger = logging.getLogger(__name__)

client = Client(
    base_url=os.getenv("PHOENIX_COLLECTOR_ENDPOINT"),
    api_key=os.getenv("PHOENIX_API_KEY"),
)


def get_data(
    project_name: str = "fast_api_agent", span_kind: str = "CHAIN", debug: bool = False
):
    """Retrieve spans data from Phoenix/Arize for evaluation purposes.

    This function connects to the Phoenix observability platform and retrieves
    span data for a specific project. Spans represent individual operations or
    steps in a trace, and this function filters for root spans only (top-level
    operations) of a specific kind.

    The function uses the Phoenix Client SDK to query spans and returns them
    as a pandas DataFrame with null values removed, making it ready for
    downstream evaluation tasks.

    Args:
        project_name (str): The name of the Phoenix project to retrieve data from.
            Defaults to "fast_api_agent".
        span_kind (str): The type of span to filter for (e.g., "CHAIN", "TOOL", "LLM").
            This corresponds to the span_kind attribute in Phoenix. Defaults to "CHAIN".
        debug (bool): If True, returns all spans without filtering. Currently unused
            in the implementation but reserved for future debugging capabilities.
            Defaults to False.

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved spans with columns:
            - 'input.value': The input data for each span
            - 'output.value': The output data for each span
            - Additional metadata columns from Phoenix
            Rows with null values in any column are automatically removed.

    Raises:
        HTTPStatusError: If the Phoenix API request fails due to network issues,
            authentication problems, or invalid endpoints.
        ValueError: If the project doesn't exist in Phoenix or if the query
            parameters are invalid.
        Exception: For any other unexpected errors during data retrieval.

    Example:
        >>> data = get_data(project_name="my_agent", span_kind="LLM")
        >>> print(data.columns)
        Index(['input.value', 'output.value', ...])

    Note:
        - Requires PHOENIX_COLLECTOR_ENDPOINT and PHOENIX_API_KEY environment variables
        - Only retrieves root spans (not nested child spans)
        - Automatically drops rows with null values
    """
    try:
        query = (
            SpanQuery()
            .select("input.value", "output.value")
            .where(f"span_kind == '{span_kind}'")
        )

        data = client.spans.get_spans_dataframe(
            query=query, project_name=project_name, root_spans_only=True
        ).dropna()

        return data

    except HTTPStatusError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving data: {e}")
        raise
