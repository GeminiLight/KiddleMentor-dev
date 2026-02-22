"""Integration tests for tutoring agents."""

import pytest
from unittest.mock import MagicMock, patch

from gen_mentor.agents.tutoring import chat_with_tutor_with_llm


class TestTutoringAgents:
    """Integration tests for tutoring agents."""

    @pytest.mark.integration
    def test_chat_with_tutor_basic(self, mock_llm, sample_learner_profile):
        """Test basic chatbot interaction."""
        with patch('gen_mentor.agents.tutoring.chatbot.AITutorChatbot') as mock_chatbot_class:
            mock_chatbot = MagicMock()
            mock_chatbot.chat.return_value = "Python is a programming language."
            mock_chatbot_class.return_value = mock_chatbot

            messages = [{"role": "user", "content": "What is Python?"}]

            result = chat_with_tutor_with_llm(
                llm=mock_llm,
                messages=messages,
                learner_profile=sample_learner_profile,
                use_search=False,
            )

            assert result is not None
            mock_chatbot.chat.assert_called_once()

    @pytest.mark.integration
    def test_chat_with_tutor_with_search(self, mock_llm, sample_learner_profile):
        """Test chatbot with search enabled."""
        with patch('gen_mentor.agents.tutoring.chatbot.AITutorChatbot') as mock_chatbot_class:
            mock_chatbot = MagicMock()
            mock_chatbot.chat.return_value = "Python is a high-level programming language..."
            mock_chatbot_class.return_value = mock_chatbot

            # Mock SearchRagManager
            mock_search_rag = MagicMock()
            mock_search_rag.invoke.return_value = [
                {"content": "Python documentation", "source": "python.org"}
            ]

            messages = [{"role": "user", "content": "Tell me about Python decorators"}]

            result = chat_with_tutor_with_llm(
                llm=mock_llm,
                messages=messages,
                learner_profile=sample_learner_profile,
                search_rag_manager=mock_search_rag,
                use_search=True,
            )

            assert result is not None
            mock_chatbot.chat.assert_called_once()

    @pytest.mark.integration
    def test_chat_with_conversation_history(self, mock_llm, sample_learner_profile):
        """Test chatbot with conversation history."""
        with patch('gen_mentor.agents.tutoring.chatbot.AITutorChatbot') as mock_chatbot_class:
            mock_chatbot = MagicMock()
            mock_chatbot.chat.return_value = "Functions help organize code into reusable blocks."
            mock_chatbot_class.return_value = mock_chatbot

            messages = [
                {"role": "user", "content": "What is Python?"},
                {"role": "assistant", "content": "Python is a programming language."},
                {"role": "user", "content": "Tell me about functions."},
            ]

            result = chat_with_tutor_with_llm(
                llm=mock_llm,
                messages=messages,
                learner_profile=sample_learner_profile,
            )

            assert result is not None
            mock_chatbot.chat.assert_called_once()
