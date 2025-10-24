import pandas as pd
from phoenix.evals import llm_classify, OpenAIModel
from phoenix.client import Client
from textwrap import dedent
import os


JUDGE_PROMPT_TEMPLATE = dedent("""
    You are a judge that evaluates the relevance of responses given input queries.
    For each input query and its corresponding output response, rate the response on a scale of 1 to 5,
    where 5 is an excellent response that fully addresses the query, and 1 is a poor response that fails to address the query.
    
    Provide a brief explanation for your rating.
    Input: {input.value}
    AI Response: {output.value}
    Format your response as:
    Rating: <1-5>
    Explanation: <your explanation here>
""")

JUDGE_RAILS = [str(i) for i in range(1, 6)]

async def evaluate_relevance(data: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluate spans data using an LLM evaluator.
    
    Args:
        data: DataFrame containing spans data with 'input.value' and 'output.value' columns
        
    Returns:
        DataFrame with evaluation results
    """
    
    llm_judge_model = OpenAIModel(
        model = "gpt-4.1",
        default_concurrency=10,
        base_url=os.getenv("OPENAI_API_ENDPOINT")
    )

    eval_results = llm_classify(
        data = data,
        template=JUDGE_PROMPT_TEMPLATE,
        model=llm_judge_model,
        provide_explanation=True,
        rails = JUDGE_RAILS
    )

    # Handle case where eval_results might be a list or other type
    if isinstance(eval_results, pd.DataFrame):
        eval_df = pd.concat([data, eval_results], axis=1).set_index("context.span_id")
    else:
        # If eval_results is not a DataFrame, convert it
        if isinstance(eval_results, list):
            eval_results_df = pd.DataFrame(eval_results)
        else:
            eval_results_df = pd.DataFrame([eval_results])
        eval_df = pd.concat([data, eval_results_df], axis=1).set_index("context.span_id")
    
    return eval_df


def annotate_span_evals(evaluation_results: pd.DataFrame) -> None:
    """
    Annotate spans with evaluation results in Phoenix.
    """
    try:
        client = Client(
            base_url = os.getenv("PHOENIX_COLLECTOR_ENDPOINT"),
            api_key = os.getenv("PHOENIX_API_KEY")
        )
        
        annotation_ids = client.spans.log_span_annotations_dataframe(
            dataframe = evaluation_results,
            annotation_name="relevance",
            annotator_kind="LLM",
            sync = True
        )
        
        print(f"Successfully annotated {len(annotation_ids)} spans")
        return annotation_ids
    except Exception as e:
        print(f"Warning: Could not annotate spans in Phoenix: {e}")
        print("Evaluation completed but annotation skipped")
        return None
