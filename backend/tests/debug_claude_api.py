
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add backend directory to sys.path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

# Load environment variables from project root
load_dotenv(str(backend_dir.parent / ".env"))

from anthropic import AsyncAnthropic

async def debug_claude():
    print("------- Claude API Debugger -------")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY is not found in environment variables.")
        return

    print(f"🔑 API Key found: {api_key[:10]}...{api_key[-5:]}")
    
    client = AsyncAnthropic(api_key=api_key)
    print("Authenticated Client created.")
    
    # Try listing models to see what is available
    print("\nAttempting to list available models...")
    try:
        models = await client.models.list()
        print(f"✅ Successfully listed {len(models.data)} models.")
        for m in models.data:
            print(f" - {m.id} ({m.created_at})")
    except Exception as e:
        print(f"❌ Failed to list models: {e}")

    print("\nAttempting to send a simple 'Hello' message to Claude Sonnet 4.5 (Alias Check)...")
    try:
        message = await client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=10,
            messages=[
                {"role": "user", "content": "Hello, are you active?"}
            ]
        )
        print("✅ Success! Response received:")
        print(message.content[0].text)
        print("\nConclusion: The API Key is valid and working.")
        
    except Exception as e:
        print("\n❌ API Call Failed!")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        
        if "credit" in str(e).lower() or "balance" in str(e).lower():
            print("\n💡 Diagnosis: This looks like a credit/balance issue.")
            print("   Even if you charged $5, it might take a few minutes to propagate,")
            print("   or you might need to check your billing limits in the Anthropic Console.")
        elif "api_key" in str(e).lower() or "authentication" in str(e).lower():
             print("\n💡 Diagnosis: The API Key itself might be invalid or copied incorrectly.")

if __name__ == "__main__":
    asyncio.run(debug_claude())
