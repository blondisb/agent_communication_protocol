import pytest
import unittest.mock as mock
from unittest.mock import Mock, MagicMock, patch
import warnings

# Assuming these imports exist in your codebase
# You may need to adjust the import paths based on your project structure
from smolagents import LiteLLMModel, ChatMessage, Tool, TokenUsage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

class TestLiteLLMModelGenerate:
    """Test suite for LiteLLMModel generate method."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Mock the litellm import to avoid dependency issues
        self.mock_litellm = Mock()
        self.mock_client = Mock()
        self.mock_litellm.completion.return_value = self._create_mock_response()
        
        # Create a LiteLLMModel instance with mocked client
        with patch('smolagents.models', self.mock_litellm):
            self.model = LiteLLMModel(
                model_id="groq/deepseek-r1-distill-llama-70b"
                # api_base="https://api.test.com",
                # api_key=""
            )
        
        # Mock the client property
        self.model.client = self.mock_litellm
        
        # Mock the _prepare_completion_kwargs method
        self.model._prepare_completion_kwargs = Mock(return_value={
            'model': 'test-model',
            'messages': [{'role': 'user', 'content': 'Hello'}, {'role': 'system', 'content': 'Hi, how can i help u?'}],
            # 'api_base': 'https://api.test.com',
            'api_key': 'test-key'
        })

    def _create_mock_response(self):
        """Create a mock response object."""
        mock_response = Mock()
        mock_response.usage.prompt_tokens = 10
        mock_response.usage.completion_tokens = 20
        
        mock_choice = Mock()
        mock_choice.message.model_dump.return_value = {
            'role': 'assistant',
            'content': 'Hello! How can I help you?',
            'tool_calls': None
        }
        mock_response.choices = [mock_choice]
        
        return mock_response

    def test_generate_basic_functionality(self):
        """Test basic generate method functionality."""
        # Prepare test data
        messages = [ChatMessage(role="user", content="Hello, world!")]
        
        # Mock ChatMessage.from_dict
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message) as mock_from_dict:
            # Call the method
            result = self.model.generate(messages=messages)
            
            # Assertions
            assert result == mock_chat_message
            self.model._prepare_completion_kwargs.assert_called_once()
            self.mock_litellm.completion.assert_called_once()
            
            # Verify token counts were set
            assert self.model._last_input_token_count == 10
            assert self.model._last_output_token_count == 20
            
            # Verify ChatMessage.from_dict was called correctly
            mock_from_dict.assert_called_once()
            call_args = mock_from_dict.call_args
            assert call_args[0][0] == {
                'role': 'assistant',
                'content': 'Hello! How can I help you?',
                'tool_calls': None
            }

    def test_generate_with_stop_sequences(self):
        """Test generate method with stop sequences."""
        messages = [ChatMessage(role="user", content="Generate text")]
        stop_sequences = ["STOP", "END"]
        
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message):
            result = self.model.generate(
                messages=messages,
                stop_sequences=stop_sequences
            )
            
            # Verify _prepare_completion_kwargs was called with stop_sequences
            call_args = self.model._prepare_completion_kwargs.call_args
            assert call_args[1]['stop_sequences'] == stop_sequences

    def test_generate_with_response_format(self):
        """Test generate method with response format."""
        messages = [ChatMessage(role="user", content="Generate JSON")]
        response_format = {"type": "json_object"}
        
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message):
            result = self.model.generate(
                messages=messages,
                response_format=response_format
            )
            
            # Verify _prepare_completion_kwargs was called with response_format
            call_args = self.model._prepare_completion_kwargs.call_args
            assert call_args[1]['response_format'] == response_format

    def test_generate_with_tools(self):
        """Test generate method with tools."""
        messages = [ChatMessage(role="user", content="Use tools")]
        tools = [Mock(spec=Tool)]
        
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message):
            result = self.model.generate(
                messages=messages,
                tools_to_call_from=tools
            )
            
            # Verify _prepare_completion_kwargs was called with tools
            call_args = self.model._prepare_completion_kwargs.call_args
            assert call_args[1]['tools_to_call_from'] == tools

    def test_generate_with_additional_kwargs(self):
        """Test generate method with additional keyword arguments."""
        messages = [ChatMessage(role="user", content="Test")]
        additional_kwargs = {"temperature": 0.7, "max_tokens": 100}
        
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message):
            result = self.model.generate(
                messages=messages,
                **additional_kwargs
            )
            
            # Verify additional kwargs were passed through
            call_args = self.model._prepare_completion_kwargs.call_args
            assert call_args[1]['temperature'] == 0.7
            assert call_args[1]['max_tokens'] == 100

    def test_generate_completion_kwargs_parameters(self):
        """Test that generate passes correct parameters to _prepare_completion_kwargs."""
        messages = [ChatMessage(role="user", content="Test")]
        
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message):
            self.model.generate(messages=messages)
            
            call_args = self.model._prepare_completion_kwargs.call_args
            
            # Verify all expected parameters are passed
            assert call_args[1]['model'] == self.model.model_id
            assert call_args[1]['api_base'] == self.model.api_base
            assert call_args[1]['api_key'] == self.model.api_key
            assert call_args[1]['convert_images_to_image_urls'] is True
            assert call_args[1]['custom_role_conversions'] == self.model.custom_role_conversions

    def test_generate_api_call_failure(self):
        """Test generate method when API call fails."""
        messages = [ChatMessage(role="user", content="Test")]
        
        # Make the completion call raise an exception
        self.mock_litellm.completion.side_effect = Exception("API Error")
        
        # Verify the exception is propagated
        with pytest.raises(Exception, match="API Error"):
            self.model.generate(messages=messages)

    def test_generate_token_usage_in_chat_message(self):
        """Test that token usage is correctly included in the returned ChatMessage."""
        messages = [ChatMessage(role="user", content="Test")]
        
        mock_chat_message = Mock(spec=ChatMessage)
        with patch.object(ChatMessage, 'from_dict', return_value=mock_chat_message) as mock_from_dict:
            result = self.model.generate(messages=messages)
            
            # Check that TokenUsage was created and passed to ChatMessage.from_dict
            call_args = mock_from_dict.call_args
            assert 'token_usage' in call_args[1]
            token_usage = call_args[1]['token_usage']
            assert token_usage.input_tokens == 10
            assert token_usage.output_tokens == 20


# Additional test for integration testing (if you want to test with real API)
@pytest.mark.integration
class TestLiteLLMModelIntegration:
    """Integration tests for LiteLLMModel - requires actual API access."""
    
    # @pytest.mark.skip(reason="Requires actual API key and credits")
    def test_generate_real_api_call(self):
        """Test generate with a real API call (uncomment and configure for integration testing)."""
        
        # This test requires actual API credentials and should be run separately
        model = LiteLLMModel(
            model_id="groq/deepseek-r1-distill-llama-70b"
            # api_key=""
        )
       
        messages = [ChatMessage(
            role="user",
            content=[{
                    "type": "text",
                    "text": "You are a supervisory agent that can delegate tasks to specialized ACP agents.\nAvailable agents:\n- function_engineer_agent: This is an agent that determines whether an agent is secure or not, depending on the use case.\nIt uses a RAG pattern to find answers in a PDF document and provides a secure communication protocol for agents to communicate with each other and with humans.\nUse it to help answer questions on designing secure communication protocols for AI agents.\n- designer_agent: This agent is designed to help with the design of a communication protocol for agents.\nIt can generate code based on a given prompt and can also search the web for information.\nUse it to help answer questions on designing communication protocols for AI agents.\n\nYour task is to:\n1. Analyze the user's request\n2. Call the appropriate agent(s) to gather information\n3. When you have a complete answer, ALWAYS call the final_answer tool with your response\n4. Do not provide answers directly in your messages - always use the final_answer tool\n5. If you have sufficient information to complete a task do not call out to another agent unless required\n\nRemember:\n- Always use the final_answer tool when you have a complete answer\n- Do not provide answers in your regular messages\n- Chain multiple agent calls if needed to gather all required information\n- The final_answer tool is the only way to return results to the user\n"
            }]
        )]
        
        result = model.generate(messages=messages)
        print("\n\n\n---------------------------------------",result)
        assert isinstance(result, ChatMessage)
        assert result.content
        # pass


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])