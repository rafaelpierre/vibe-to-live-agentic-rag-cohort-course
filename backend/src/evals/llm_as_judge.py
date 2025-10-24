import pandas as pd
from phoenix.evals import llm_classify, OpenAIModel
from phoenix.evals.llm import LLM
from textwrap import dedent

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

def evaluate_relevance(data: pd.DataFrame) -> pd.DataFrame:
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
        base_url="https://api.hexflow.ai"
    )

    eval_results = llm_classify(
        data = data,
        template=JUDGE_PROMPT_TEMPLATE,
        model=llm_judge_model,
        provide_explanation=True,
        rails = JUDGE_RAILS
    )

    return {
        "labels": eval_results["label"].tolist(),
        "data": eval_results["explanation"].tolist()
    }