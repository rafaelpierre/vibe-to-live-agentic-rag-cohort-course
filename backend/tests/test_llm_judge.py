from src.evals.llm_as_judge import evaluate_relevance
from src.evals.llm_as_judge import annotate_span_evals
import pytest

@pytest.fixture
def sample_data():
    """Get real span data from Phoenix for testing"""
    from src.evals.data import get_data
    
    # Get real spans from the fast_api_agent project
    # get_data already returns a DataFrame with 'input.value', 'output.value' columns
    # and 'context.span_id' in the index
    spans_df = get_data(project_name='fast_api_agent', debug=True)
    
    # Take just one span for testing
    sample_df = spans_df.head(1)
    
    # Reset index to make context.span_id a column for the evaluation
    sample_df = sample_df.reset_index()
    
    return sample_df

@pytest.fixture
def relevance_evaluation(sample_data):
    """Test the evaluate_relevance function with sample data"""

    # Evaluate relevance
    results = evaluate_relevance(sample_data)

    print("Evaluation Results:")
    print(results)

    # Basic assertions
    assert len(results) > 0

    return results


def test_create_span_annotation(relevance_evaluation):

    """Test the upload function with relevance evaluation results"""

    # Upload evaluation results
    ids = annotate_span_evals(relevance_evaluation)

    print("Annotation IDs:", ids)
    
    # Verify that annotations were created successfully
    assert ids is not None
    assert len(ids) > 0
    
    # Each annotation should have an ID
    for annotation in ids:
        assert 'id' in annotation
        assert annotation['id'] is not None