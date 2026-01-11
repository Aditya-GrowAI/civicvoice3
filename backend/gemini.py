from dotenv import load_dotenv
import os
from google import genai
from google.genai import errors
from PIL import Image
import io
import time

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set")

client = genai.Client(api_key=API_KEY)

PROMPT = """
Return ONLY one label:
pothole
garbage
water_leak
street_light
unknown
"""


def detect_issue(image_bytes: bytes, max_retries: int = 3) -> str:
    """
    Detect the type of civic issue from an image using Gemini AI.
    
    Args:
        image_bytes: Image data as bytes
        max_retries: Maximum number of retry attempts for rate limiting
        
    Returns:
        str: One of 'pothole', 'garbage', 'water_leak', 'street_light', or 'unknown'
        
    Raises:
        RuntimeError: If API call fails after all retries
    """
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        print(f"Error opening image: {e}")
        return "unknown"

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="models/gemini-2.0-flash-exp",  # Using correct model name format
                contents=[PROMPT, image]
            )

            text = ""

            # Parse response with better error handling
            if hasattr(response, 'text'):
                text = response.text.lower()
            elif response.candidates:
                parts = response.candidates[0].content.parts
                if parts and hasattr(parts[0], "text"):
                    text = parts[0].text.lower()

            # Extract issue type from response
            if "pothole" in text:
                return "pothole"
            elif "garbage" in text:
                return "garbage"
            elif "water" in text:
                return "water_leak"
            elif "light" in text:
                return "street_light"
            else:
                return "unknown"

        except errors.ClientError as e:
            error_msg = str(e)
            # Handle rate limiting (429 errors)
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # Exponential backoff: 2s, 4s, 8s
                    print(f"Rate limit hit. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                else:
                    print(f"Rate limit exceeded after {max_retries} attempts")
                    return "unknown"
            else:
                print(f"Gemini API error: {error_msg}")
                return "unknown"
                
        except Exception as e:
            print(f"Unexpected error in detect_issue: {type(e).__name__}: {e}")
            return "unknown"

    return "unknown"
