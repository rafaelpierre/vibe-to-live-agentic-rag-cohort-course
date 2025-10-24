from src.evals.llm_as_judge import evaluate_relevance


def test_evaluate_relevance():
    """Test the evaluate_relevance function with sample data"""
    import pandas as pd

    # Sample data
    data = pd.DataFrame({
        "input.value": [
            "What is the capital of France?",
            "Explain the theory of relativity."
        ],
        "output.value": [
            "The capital of France is Sao Paulo.",
            "The theory of relativity, developed by Albert Einstein, encompasses two interrelated theories: special relativity and general relativity."
        ]
    })

    # Evaluate relevance
    results = evaluate_relevance(data)

    print("Evaluation Results:")
    print(results)

    # Basic assertions
    assert len(results) == len(data)
    assert False