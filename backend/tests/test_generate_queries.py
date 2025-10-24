from src.evals.generate_spans import generate_input_queries, pipeline
import asyncio
import pytest

MAX_SYNTHETIC_QUERIES = 20

@pytest.fixture
def input_queries():
    """Test that generate_input_queries function generates queries"""
    queries = asyncio.run(generate_input_queries(max_queries=MAX_SYNTHETIC_QUERIES))
    print(f"Generated {len(queries)} queries:")
    for q in queries:
        print(f"- {q}")

    assert len(queries) == MAX_SYNTHETIC_QUERIES
    return queries


def test_pipeline(input_queries):

    """Test the full pipeline with generated queries"""
    queries = input_queries
    responses = asyncio.run(pipeline(queries=queries))
    
    print(f"Pipeline returned {len(responses)} responses:")
    for r in responses:
        print(f"- {r}")

    assert len(responses) == MAX_SYNTHETIC_QUERIES
    for r in responses:
        assert len(r) > 0


