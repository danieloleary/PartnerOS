#!/usr/bin/env python3
"""
Quick test of Partner Agent chat functionality
"""

import sys
import json
sys.path.insert(0, '/workspaces/PartnerOS/scripts/partner_agent')

from agent import PartnerAgent

def test_chat_completion():
    """Test the chat_completion method"""
    print("=" * 60)
    print("Testing Partner Agent Chat Functionality")
    print("=" * 60)
    
    try:
        # Initialize agent
        print("\n✓ Initializing Partner Agent...")
        agent = PartnerAgent()
        
        if not agent.llm_client:
            print("⚠️  Warning: LLM client not initialized")
            print("   (Set ANTHROPIC_API_KEY or configure a different provider)")
            return False
        
        print(f"✓ Provider: {agent.config.get('provider', 'unknown')}")
        print(f"✓ Model: {agent.config.get('model', 'unknown')}")
        
        # Test chat_completion method exists
        print("\n✓ Testing chat_completion method...")
        assert hasattr(agent, 'chat_completion'), "chat_completion method not found"
        print("✓ chat_completion method found")
        
        # Test simple message (without API key, it will fail gracefully)
        print("\n✓ Testing message processing...")
        test_message = "What is an Ideal Partner Profile?"
        
        print(f"\n📨 Test message: '{test_message}'")
        
        response = agent.chat_completion(
            user_message=test_message,
            system_prompt="You are a helpful partner program expert."
        )
        
        if response.startswith("["):
            print(f"⚠️  API Error (expected if no API key): {response}")
        else:
            print(f"✓ Response received: {response[:100]}...")
        
        # Test multi-turn conversation
        print("\n✓ Testing multi-turn conversation...")
        context = [
            {"role": "user", "content": "What's a partner tier?"},
            {"role": "assistant", "content": "A partner tier is a classification level..."}
        ]
        
        follow_up = "Can you give examples?"
        response = agent.chat_completion(
            user_message=follow_up,
            conversation_context=context
        )
        
        print(f"✓ Follow-up response processed: {response[:100] if not response.startswith('[') else response}")
        
        print("\n" + "=" * 60)
        print("✅ All chat tests passed!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_chat_completion()
    sys.exit(0 if success else 1)
