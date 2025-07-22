#REPARARE ULTIM FISIER
import os
import re
import torch
import time
from fastapi import FastAPI
from pydantic import BaseModel
from unsloth import FastLanguageModel
from transformers import AutoTokenizer
from scirpt_locatie import get_closest_distance_time
from fastapi.middleware.cors import CORSMiddleware


# Set cache
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface/transformers"

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set to ["http://localhost:5173"] or your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load model and tokenizer ---
# Use base model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="/tmp/DeepSeek-R1-Distill-Llama-8B",
    max_seq_length=1024,
    dtype=torch.float16,
    load_in_4bit=True,
    device_map="auto", # Optional if private
    use_safetensors=True,        # ✅ this forces loading safetensors
)

# Load your adapter
model.load_adapter("./durangaldea-assistantFinalPD")
FastLanguageModel.for_inference(model)

# Helper functions
def extract_api_call_from_answer(response_text):
    parts = response_text.split("### Answer:", 1)
    answer_text = parts[1] if len(parts) == 2 else response_text
    match = re.search(r"<API>(.*?)</API>", answer_text, re.DOTALL)
    return match.group(1).strip() if match else None

def parse_api_call(call_str):
    # Matches: key="value" or key=123.45
    pattern = r'(\w+)\s*=\s*(?:"([^"]+)"|([\d.]+))'
    matches = re.findall(pattern, call_str)

    kwargs = {}
    for match in matches:
        key, str_value, num_value = match
        kwargs[key] = str_value if str_value else float(num_value) if '.' in num_value else int(num_value)

    return kwargs

def extract_answer_only(response_text):
    parts = response_text.split("### Answer:", 1)
    return parts[1].strip() if len(parts) == 2 else response_text.strip()
# Request model
class QuestionRequest(BaseModel):
    question: str

# Response model
class AnswerResponse(BaseModel):
    original_response: str
    api_result: dict | list | None
    paraphrased_response: str

@app.get("/")
def read_root():
    return {"message": "🚀 API is running successfully!"}

@app.post("/ask", response_model=AnswerResponse)
def answer_question(request: QuestionRequest):
    start_route_time = time.perf_counter()
    # Intent verification prompt
    intent_prompt = f"""
    Classify the intent of this question as either "location_travel" or "other":

    Question: "{request.question}"

    Intent:
    """

    inputs_intent = tokenizer([intent_prompt], return_tensors="pt").to("cuda")
    intent_ids = model.generate(**inputs_intent, max_new_tokens=10, do_sample=False)
    intent_result = tokenizer.decode(intent_ids[0], skip_special_tokens=True).strip().lower()

    # Debugging intent (can print to logs)
    print("Intent detected:", intent_result)

    # Guard condition
    if "location_travel" not in intent_result:
        return AnswerResponse(
            original_response="Your question seems unrelated to locations or travel in Durangaldea. Please ask a question related to locations, distances, travel modes, or nearby amenities.",
            api_result=None,
            paraphrased_response="I'm here to help with questions about locations, distances, and travel. Please rephrase your question accordingly!"
        )

    # (your original logic continues here)
    prompt = f"""Below is a question about locations in Durangaldea. Your task is to provide a clear and accurate answer using the <API> call whenever necessary. There are two types of questions you may encounter, each with a specific API call format.

    Type 1: Closest Location
    Use this API format to find the closest place of a given category from a specific location:

    <API>get_closest_distance_time(category, mode, location, metric_to_extract) -> result</API>

    Parameters:
    - category: One of ["hospitals", "pharmacies", "supermarkets"]
    - mode: Transportation mode, one of ["drive", "walk", "bike"]
    - location: City and street name in Durangaldea (e.g., "Durango, Artekalea Kalea")
    - metric_to_extract: "distance" or "time"

    The result is returned as a JSON object with:
    {{ "distance": <float km>, "time": <float minutes> }}

    Type 2: Filtered Location List
    Use this API format when the question asks for [X] locations within [Y] km or minutes:
    Example:
    "Give me 3 locations where I can reach a supermarket in under 2 km using walk."
    <API>get_closest_distance_time(category, mode, metric_to_extract, max_metric, nr_locations) -> result</API>

    Parameters:
    - category: One of ["hospitals", "pharmacies", "supermarkets"]
    - mode: One of ["drive", "walk", "bike"]
    - metric_to_extract: "distance" or "time"
    - max_metric: Maximum allowed metric (e.g., 2000 for 2 km)
    - nr_locations: Number of locations to return (e.g., 3)

    Result JSON:
    {{
      "addresses": [
        "Street 1, City",
        "Street 2, City",
        …
      ]
    }}

    Instructions:
    Before answering, identify the question type and build a logical response. Use plain language to explain API call results.

    ### Question:
    {request.question}

    ### Answer:
    """
    start_model_time = time.perf_counter()
    inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
    output_ids = model.generate(**inputs, max_new_tokens=256)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    end_model_time = time.perf_counter()
    print(f"⏱️ Model generation time: {end_model_time - start_model_time:.3f} seconds")
    
    api_call = extract_api_call_from_answer(response)
    api_result = None

    if api_call:
        try:
            kwargs = parse_api_call(api_call.split(")", 1)[0] + ")")
            print("\n" + "="*50)
            print("DEBUG - API CALL KWARGS:")
            for key, value in kwargs.items():
                print(f"{key}: {value} ({type(value)})")
            print("="*50 + "\n")
            start_api_time = time.perf_counter()
            api_result = get_closest_distance_time(**kwargs)
            end_api_time = time.perf_counter()
            print(f"🌐 API call time: {end_api_time - start_api_time:.3f} seconds")
            print("API CALL DUPA APEL:", api_result)
            # Ensure api_result is always a list for consistent processing
            if not isinstance(api_result, list):
                api_result = [api_result] if api_result else []

        except Exception as e:
            api_result = {"error": str(e)}

    print("API CALL:", api_call)
    print("API RESULT:", api_result)
    # first extract the answer only, then remove the <API> tags and what is after.
    #cleaned = re.sub(r"<API>.*?</API>", "", response, flags=re.DOTALL).strip()
    #answer_only = extract_answer_only(cleaned)

    answer_only = extract_answer_only(response)
    cleaned = re.sub(r"(?s)(.*?)<API>.*", r"\1", answer_only).strip()

    answer_with_api_data = cleaned

    if api_result and isinstance(api_result, list) and len(api_result) > 0:
        first_result = api_result[0]  # Take the first item (assuming single-item lists for distance/time)
        if isinstance(first_result, dict):
            if "distance" in first_result:
                distance = float(first_result["distance"])
                distance_km = distance / 1000  # Convert meters to kilometers
                answer_with_api_data = f"{cleaned} {distance_km:.2f}km away"
            elif "time" in first_result:
                time_value = float(first_result["time"])
                answer_with_api_data = f"{cleaned} {time_value:.1f} minutes away"
            elif "addresses" in first_result:
                addresses_str = "; ".join(first_result["addresses"])  # Join addresses with "; "
                answer_with_api_data = f"{cleaned} {addresses_str}"
            else:
                answer_with_api_data = cleaned  # Fallback if no matching key
        else:
            answer_with_api_data = cleaned  # Fallback if not a dict
    else:
        answer_with_api_data = cleaned  # Fallback if no API result

    end_route_time = time.perf_counter()
    print(f"WHOLE ROUTE call time: {end_route_time - start_route_time:.3f} seconds")
    return AnswerResponse(
        original_response=api_call, #era cleaned
        api_result=api_result[0] if isinstance(api_result, list) and len(api_result) > 0 else api_result,
        paraphrased_response=answer_with_api_data,
    )
