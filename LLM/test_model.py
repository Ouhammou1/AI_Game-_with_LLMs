# from huggingface_hub import InferenceClient
# import os
# from dotenv import load_dotenv
# load_dotenv()

# client = InferenceClient(provider="hf-inference", api_key=os.getenv("HF_API_KEY"))

# models = [
#     "CompVis/stable-diffusion-v1-4",
#     "runwayml/stable-diffusion-v1-5",
#     "stabilityai/stable-diffusion-xl-base-1.0",
#     "Lykon/dreamshaper-8",
#     "prompthero/openjourney",
# ]

# for model in models:
#     try:
#         print(f"Testing {model}...")
#         image = client.text_to_image("a cat", model=model)
#         image.save(f"test_output.jpg")
#         print(f"✅ SUCCESS: {model}")
#         break
#     except Exception as e:
#         print(f"❌ FAILED: {e}")