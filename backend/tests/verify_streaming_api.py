import asyncio
import httpx
import json
import io
from PIL import Image

async def test_streaming_analyze():
    url = "http://127.0.0.1:8000/api/v1/inbound/analyze"
    
    # 1. Create a dummy image (100x100 white)
    img = Image.new('RGB', (100, 100), color = 'white')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
    
    print(f"🚀 Sending request to {url}...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            async with client.stream("POST", url, files=files) as response:
                print(f"Response Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"Error: {await response.aread()}")
                    return

                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        if data.get("status") == "progress":
                            print(f"🔄 PROGRESS: {data.get('message')}")
                        elif data.get("status") == "complete":
                            print(f"✅ COMPLETE: Data received (keys: {list(data.get('data', {}).keys())})")
                        elif data.get("status") == "error":
                            print(f"❌ ERROR: {data.get('message')}")
                        else:
                            print(f"Unknown status: {line}")
                    except json.JSONDecodeError:
                        print(f"Raw Line: {line}")
        except httpx.ConnectError:
             print("❌ Connection failed. Is the server running on port 8000?")
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_streaming_analyze())
