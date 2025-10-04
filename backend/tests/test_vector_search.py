"""
Tests for the vector search tool.

These tests use mocking to avoid making actual API calls to Qdrant.
"""

import os
from unittest.mock import MagicMock, Mock, patch

import pytest

from tools.vector_search import VectorSearchTool, search_knowledge_base


# Fixtures
@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set up mock environment variables."""
    monkeypatch.setenv("QDRANT_URL", "https://mock-qdrant.example.com")
    monkeypatch.setenv("QDRANT_API_KEY", "mock-api-key-12345")


@pytest.fixture
def mock_qdrant_client():
    """Create a mock Qdrant client."""
    with patch("tools.vector_search.QdrantClient") as mock_client:
        yield mock_client


@pytest.fixture
def mock_collection_info():
    """Create mock collection info response."""
    mock_info = Mock()
    mock_info.points_count = 100
    mock_info.config.params.vectors.size = 384
    mock_info.config.params.vectors.distance = "COSINE"
    return mock_info


@pytest.fixture
def mock_search_results():
    """Create mock search results."""
    results = []
    for i in range(3):
        result = Mock()
        result.score = 0.95 - (i * 0.1)
        result.payload = {
            "document": f"This is the content of document {i+1}. It contains information about monetary policy and interest rates.",
            "title": f"Fed Speech {i+1}",
            "speaker": f"Speaker {i+1}",
            "pub_date": "2024-01-15",
            "category": "Monetary Policy",
            "url": f"https://example.com/speech{i+1}",
            "description": f"Description {i+1}",
        }
        results.append(result)
    
    mock_response = Mock()
    mock_response.points = results
    return mock_response


# Tests for VectorSearchTool.__init__
class TestVectorSearchToolInit:
    """Tests for VectorSearchTool initialization."""
    
    def test_init_with_env_vars(self, mock_env_vars, mock_qdrant_client):
        """Test initialization with environment variables."""
        tool = VectorSearchTool()
        
        assert tool.qdrant_url == "https://mock-qdrant.example.com"
        assert tool.qdrant_api_key == "mock-api-key-12345"
        assert tool.collection_name == "fed_speeches"
        assert tool.model_name == "BAAI/bge-small-en"
        
        mock_qdrant_client.assert_called_once_with(
            url="https://mock-qdrant.example.com",
            api_key="mock-api-key-12345",
        )
    
    def test_init_with_parameters(self, mock_qdrant_client):
        """Test initialization with explicit parameters."""
        tool = VectorSearchTool(
            qdrant_url="https://custom.qdrant.com",
            qdrant_api_key="custom-key",
            collection_name="custom_collection",
            model_name="custom-model"
        )
        
        assert tool.qdrant_url == "https://custom.qdrant.com"
        assert tool.qdrant_api_key == "custom-key"
        assert tool.collection_name == "custom_collection"
        assert tool.model_name == "custom-model"
        
        mock_qdrant_client.assert_called_once_with(
            url="https://custom.qdrant.com",
            api_key="custom-key",
        )
    
    def test_init_missing_url(self, monkeypatch, mock_qdrant_client):
        """Test initialization fails when QDRANT_URL is missing."""
        monkeypatch.delenv("QDRANT_URL", raising=False)
        monkeypatch.setenv("QDRANT_API_KEY", "test-key")
        
        with pytest.raises(ValueError, match="QDRANT_URL and QDRANT_API_KEY must be provided"):
            VectorSearchTool()
    
    def test_init_missing_api_key(self, monkeypatch, mock_qdrant_client):
        """Test initialization fails when QDRANT_API_KEY is missing."""
        monkeypatch.setenv("QDRANT_URL", "https://test.com")
        monkeypatch.delenv("QDRANT_API_KEY", raising=False)
        
        with pytest.raises(ValueError, match="QDRANT_URL and QDRANT_API_KEY must be provided"):
            VectorSearchTool()
    
    def test_init_parameters_override_env(self, mock_env_vars, mock_qdrant_client):
        """Test that explicit parameters override environment variables."""
        tool = VectorSearchTool(
            qdrant_url="https://override.com",
            qdrant_api_key="override-key"
        )
        
        assert tool.qdrant_url == "https://override.com"
        assert tool.qdrant_api_key == "override-key"


# Tests for VectorSearchTool.search
class TestVectorSearchToolSearch:
    """Tests for the search method."""
    
    def test_search_returns_formatted_results(
        self, mock_env_vars, mock_qdrant_client, mock_search_results
    ):
        """Test that search returns properly formatted results."""
        # Setup mock
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        # Execute
        tool = VectorSearchTool()
        results = tool.search("test query", limit=3)
        
        # Verify
        assert len(results) == 3
        assert all("content" in r for r in results)
        assert all("metadata" in r for r in results)
        assert all("score" in r for r in results)
        
        # Check first result structure
        first_result = results[0]
        assert first_result["score"] == 0.95
        assert "monetary policy" in first_result["content"]
        assert first_result["metadata"]["title"] == "Fed Speech 1"
        assert first_result["metadata"]["speaker"] == "Speaker 1"
        assert first_result["metadata"]["pub_date"] == "2024-01-15"
        assert first_result["metadata"]["category"] == "Monetary Policy"
        assert first_result["metadata"]["url"] == "https://example.com/speech1"
    
    def test_search_calls_query_points_with_correct_params(
        self, mock_env_vars, mock_qdrant_client, mock_search_results
    ):
        """Test that search calls query_points with correct parameters."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        tool = VectorSearchTool()
        tool.search("monetary policy and interest rates", limit=5)
        
        # Verify the call was made
        mock_client_instance.query_points.assert_called_once()
        call_args = mock_client_instance.query_points.call_args
        
        assert call_args.kwargs["collection_name"] == "fed_speeches"
        assert call_args.kwargs["limit"] == 5
        assert hasattr(call_args.kwargs["query"], "text")
    
    def test_search_with_custom_limit(
        self, mock_env_vars, mock_qdrant_client, mock_search_results
    ):
        """Test search with custom limit parameter."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        tool = VectorSearchTool()
        results = tool.search("test query", limit=10)
        
        call_args = mock_client_instance.query_points.call_args
        assert call_args.kwargs["limit"] == 10
    
    def test_search_handles_empty_results(self, mock_env_vars, mock_qdrant_client):
        """Test search handles empty results gracefully."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_response = Mock()
        mock_response.points = []
        mock_client_instance.query_points.return_value = mock_response
        
        tool = VectorSearchTool()
        results = tool.search("test query")
        
        assert results == []
    
    def test_search_handles_missing_payload_fields(
        self, mock_env_vars, mock_qdrant_client
    ):
        """Test search handles missing payload fields gracefully."""
        mock_client_instance = mock_qdrant_client.return_value
        
        # Create result with minimal payload
        result = Mock()
        result.score = 0.85
        result.payload = {}  # Empty payload
        
        mock_response = Mock()
        mock_response.points = [result]
        mock_client_instance.query_points.return_value = mock_response
        
        tool = VectorSearchTool()
        results = tool.search("test query")
        
        assert len(results) == 1
        assert results[0]["content"] == ""
        assert results[0]["metadata"]["title"] == ""
        assert results[0]["metadata"]["speaker"] == ""
        assert results[0]["score"] == 0.85


# Tests for VectorSearchTool.verify_collection
class TestVectorSearchToolVerifyCollection:
    """Tests for the verify_collection method."""
    
    def test_verify_collection_exists(
        self, mock_env_vars, mock_qdrant_client, mock_collection_info
    ):
        """Test verify_collection when collection exists."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.get_collection.return_value = mock_collection_info
        
        tool = VectorSearchTool()
        result = tool.verify_collection()
        
        assert result["exists"] is True
        assert result["points_count"] == 100
        assert result["vector_size"] == 384
        assert result["distance"] == "COSINE"
        assert "error" not in result
    
    def test_verify_collection_does_not_exist(
        self, mock_env_vars, mock_qdrant_client
    ):
        """Test verify_collection when collection does not exist."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.get_collection.side_effect = Exception("Collection not found")
        
        tool = VectorSearchTool()
        result = tool.verify_collection()
        
        assert result["exists"] is False
        assert "error" in result
        assert "Collection not found" in result["error"]
    
    def test_verify_collection_calls_get_collection(
        self, mock_env_vars, mock_qdrant_client, mock_collection_info
    ):
        """Test that verify_collection calls get_collection with correct name."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.get_collection.return_value = mock_collection_info
        
        tool = VectorSearchTool()
        tool.verify_collection()
        
        mock_client_instance.get_collection.assert_called_once_with("fed_speeches")


# Tests for search_knowledge_base function
class TestSearchKnowledgeBase:
    """Tests for the search_knowledge_base function."""
    
    def test_search_knowledge_base_returns_formatted_string(
        self, mock_env_vars, mock_qdrant_client, mock_search_results
    ):
        """Test that search_knowledge_base returns a formatted string."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        result = search_knowledge_base("monetary policy")
        
        assert isinstance(result, str)
        assert "Found 3 relevant documents" in result
        assert "Fed Speech 1" in result
        assert "Speaker 1" in result
        assert "Score: 0.95" in result
    
    def test_search_knowledge_base_with_custom_limit(
        self, mock_env_vars, mock_qdrant_client, mock_search_results
    ):
        """Test search_knowledge_base with custom limit."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        result = search_knowledge_base("test query", limit=2)
        
        # Should still return all 3 from mock, but the limit should be passed
        call_args = mock_client_instance.query_points.call_args
        assert call_args.kwargs["limit"] == 2
    
    def test_search_knowledge_base_no_results(
        self, mock_env_vars, mock_qdrant_client
    ):
        """Test search_knowledge_base with no results."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_response = Mock()
        mock_response.points = []
        mock_client_instance.query_points.return_value = mock_response
        
        result = search_knowledge_base("test query")
        
        assert "No results found" in result
        assert "test query" in result
    
    def test_search_knowledge_base_handles_errors(
        self, mock_env_vars, mock_qdrant_client
    ):
        """Test that search_knowledge_base handles errors gracefully."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.side_effect = Exception("Connection error")
        
        result = search_knowledge_base("test query")
        
        assert "Error searching knowledge base" in result
        assert "Connection error" in result
    
    def test_search_knowledge_base_truncates_long_content(
        self, mock_env_vars, mock_qdrant_client
    ):
        """Test that search_knowledge_base truncates long content."""
        mock_client_instance = mock_qdrant_client.return_value
        
        # Create result with long content
        result = Mock()
        result.score = 0.95
        result.payload = {
            "document": "A" * 500,  # Long content
            "title": "Test",
            "speaker": "Speaker",
            "pub_date": "2024-01-01",
            "category": "Test",
            "url": "https://test.com",
            "description": "Test",
        }
        
        mock_response = Mock()
        mock_response.points = [result]
        mock_client_instance.query_points.return_value = mock_response
        
        output = search_knowledge_base("test")
        
        # Should be truncated to 300 chars + "..."
        assert "A" * 300 + "..." in output
        assert "A" * 301 not in output


# Integration-style tests
class TestVectorSearchIntegration:
    """Integration-style tests that verify the complete flow."""
    
    def test_complete_search_workflow(
        self, mock_env_vars, mock_qdrant_client, mock_search_results
    ):
        """Test the complete search workflow from initialization to results."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        # Initialize tool
        tool = VectorSearchTool()
        
        # Perform search
        results = tool.search("monetary policy and interest rates", limit=3)
        
        # Verify we got results
        assert len(results) == 3
        
        # Verify result structure and content
        for i, result in enumerate(results):
            assert result["score"] == 0.95 - (i * 0.1)
            assert result["content"]
            assert result["metadata"]["title"] == f"Fed Speech {i+1}"
            assert result["metadata"]["speaker"] == f"Speaker {i+1}"
    
    def test_custom_collection_and_model(
        self, mock_qdrant_client, mock_search_results
    ):
        """Test using custom collection and model names."""
        mock_client_instance = mock_qdrant_client.return_value
        mock_client_instance.query_points.return_value = mock_search_results
        
        tool = VectorSearchTool(
            qdrant_url="https://test.com",
            qdrant_api_key="test-key",
            collection_name="custom_docs",
            model_name="custom-model"
        )
        
        tool.search("test query")
        
        call_args = mock_client_instance.query_points.call_args
        assert call_args.kwargs["collection_name"] == "custom_docs"
