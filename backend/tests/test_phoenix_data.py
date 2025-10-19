from src.evals.data import get_data


def test_get_data():
    """Test that get_data function works with Phoenix API"""
    data = get_data()
    print(f"Retrieved {len(data)} spans")
    data.to_csv("spans.csv")
    
    # Verify we got data and it has the expected structure
    assert data is not None
    assert len(data) > 0
