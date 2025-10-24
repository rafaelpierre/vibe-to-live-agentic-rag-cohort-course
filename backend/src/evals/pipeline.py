from src.evals.generate_spans import generate_input_queries, generate_responses
from src.evals.llm_as_judge import evaluate_relevance, annotate_span_evals
from src.evals.data import get_data
import asyncio
import time
from typing import List
import pandas as pd


def run_synthetic_relevance_pipeline(max_queries: int = 20) -> List[str]:
    """Runs the full pipeline of generating synthetic queries and getting responses.

    Args:
        max_queries: Maximum number of synthetic queries to generate
    """

    async def pipeline() -> List[str]:
        # Step 1: Generate queries and responses (creates spans in Phoenix)
        queries = await generate_input_queries(max_queries=max_queries)
        responses = []
        for query in queries:
            from src.web.services import get_chat_response
            response = await get_chat_response(prompt=query)
            responses.append(str(response))
        
        # Step 2: Wait for spans to be available in Phoenix
        print("Waiting for spans to be available in Phoenix...")
        time.sleep(3)  # Give Phoenix time to process the spans
        
        # Step 3: Fetch real spans from Phoenix
        try:
            spans_df = get_data(project_name='fast_api_agent', debug=True)
            # Get the most recent spans (assuming they're the ones we just created)
            recent_spans = spans_df.tail(len(queries)).reset_index()
            
            # Step 4: Evaluate relevance using real spans
            evaluation_df = await evaluate_relevance(data=recent_spans)
            
            # Step 5: Annotate spans in Phoenix
            annotate_span_evals(evaluation_results=evaluation_df)
            
            return responses
        except Exception as e:
            print(f"Warning: Could not fetch spans from Phoenix: {e}")
            print("Returning responses without evaluation")
            return responses

    return asyncio.run(pipeline())