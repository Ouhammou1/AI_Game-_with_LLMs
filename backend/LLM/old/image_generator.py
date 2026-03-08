import os
import uuid
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
from .rate_limiter import check_rate_limit
from .error_handler import handle_error

load_dotenv()

STATIC_IMG_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'generated')
os.makedirs(STATIC_IMG_DIR, exist_ok=True)

client = InferenceClient(
    provider="hf-inference",
    api_key=os.getenv("HF_API_KEY")
)

def generate_image(prompt):
    try:
        check_rate_limit()

        image = client.text_to_image(
            prompt,
            model="stabilityai/stable-diffusion-xl-base-1.0"


        )

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(STATIC_IMG_DIR, filename)
        image.save(filepath)

        return f"/static/generated/{filename}"

    except Exception as e:
        return handle_error(e)
