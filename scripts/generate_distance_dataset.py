import csv
import random
import sys
import os

# Add the parent directory to sys.path to import the function
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scirpt_locatie import get_closest_distance_time

# Walking mode templates
QUESTION_TEMPLATES_WALK = [
    "Could you show me some streets where I can walk to a {category} in under {max_distance} km?",
    "I want to walk only—can you list {num_locations} places where a {category} is within {max_distance} km?",
    "If I'm on foot, which {num_locations} spots let me reach a {category} in under {max_distance} km?",
    "Any suggestions for {num_locations} places where a {category} is a quick walk, under {max_distance} km?",
    "Which {num_locations} streets have a {category} close enough to walk in under {max_distance} km?",
    "Please share {num_locations} locations where I could easily walk to a {category} within {max_distance} km.",
    "Looking for a short walk—what are {num_locations} areas with a {category} under {max_distance} km away?",
    "I'll be on foot. Can you name {num_locations} places that keep a {category} within {max_distance} km?",
    "Give me {num_locations} spots where it's less than {max_distance} km to walk to a {category}.",
    "I'd like a walkable {category}. Which {num_locations} places would put it under {max_distance} km away?"
]

# Biking mode templates
QUESTION_TEMPLATES_BIKE = [
    "Give me {num_locations} locations where I can reach a {category} in under {max_distance} km by bike.",
    "If I hop on a bike, what are {num_locations} streets that put me within {max_distance} km of a {category}?",
    "Cycling options only: list {num_locations} places where a {category} is under {max_distance} km away.",
    "I want to bike—what {num_locations} areas make it easy to get to a {category} within {max_distance} km?",
    "Show me {num_locations} zones where biking to a {category} is less than {max_distance} km.",
    "Can you point out {num_locations} streets where a {category} is reachable by bike in under {max_distance} km?",
    "Give me {num_locations} spots where cycling to a {category} won't go over {max_distance} km.",
    "Let's stick to biking—what are {num_locations} locations where a {category} is within {max_distance} km ride?",
    "Imagine I'm cycling—where can I start from to reach a {category} in {max_distance} km tops?",
    "Which {num_locations} places are perfect for reaching a {category} by bike in less than {max_distance} km?"
]

# Driving mode (explicit) templates
QUESTION_TEMPLATES_DRIVE = [
    "Give me {num_locations} places I can drive from to reach a {category} under {max_distance} km away.",
    "What are {num_locations} streets where driving to a {category} takes less than {max_distance} km?",
    "I'm looking to drive—got {num_locations} locations where a {category} is that close?",
    "List {num_locations} areas where driving puts me within {max_distance} km of a {category}.",
    "Can you find {num_locations} starting points where I can drive to a {category} in under {max_distance} km?",
    "Let's say I'm driving—what {num_locations} streets will get me to a {category} fast, under {max_distance} km?",
    "Driving-focused: show me {num_locations} locations where a {category} is nearby—within {max_distance} km.",
    "Tell me {num_locations} places where driving to a {category} is quick, under {max_distance} km.",
    "Give me {num_locations} neighborhoods I could drive from and hit a {category} before {max_distance} km.",
    "Imagine I'm behind the wheel—what {num_locations} spots let me reach a {category} fast, under {max_distance} km?"
]

# Driving assumed (no mode) templates
QUESTION_TEMPLATES_DEFAULT = [
    "What are {num_locations} locations where I could easily get to a {category} in under {max_distance} km?",
    "Give me {num_locations} streets from which a {category} is less than {max_distance} km away.",
    "I need {num_locations} spots where reaching a {category} takes no more than {max_distance} km.",
    "What are {num_locations} areas where getting to a {category} doesn't exceed {max_distance} km?",
    "Can you show me {num_locations} locations where I'd find a {category} nearby—under {max_distance} km?",
    "Suggest {num_locations} places where a {category} is reachable within {max_distance} km, no hassle.",
    "I'm trying to keep it under {max_distance} km—what {num_locations} streets have a {category} that close?",
    "What are {num_locations} zones where getting to a {category} is super quick—under {max_distance} km?",
    "I'm trying to stay within {max_distance} km. Got {num_locations} suggestions for where to start from?",
    "Give me {num_locations} places that make a {category} easy to reach without going over {max_distance} km."
]

def generate_distance_qa(csv_output_path="q_and_a_dataset_distances.csv"):
    """
    Generates Q&A pairs for distance-based questions with varying number of locations and maximum distances.
    Uses predefined distance and time limits for each category and mode.
    
    :param csv_output_path: str, path to output CSV
    """
    categories = ["hospitals", "pharmacies", "supermarkets"]
    possible_num_locations = [2, 3, 4, 5]  # Increased number of locations to request
    
    # Define distance limits (in meters) for each category and mode
    distance_limits = {
        "hospitals": {
            "bike": (798.277, 21445.788),
            "drive": (1644.832, 29346.516),
            "walk": (798.277, 21218.417)
        },
        "pharmacies": {
            "bike": (42.143, 11714.097),
            "drive": (11.947, 21090.353),
            "walk": (22.987, 11596.903)
        },
        "supermarkets": {
            "bike": (13.463, 14841.709),
            "drive": (40.778, 21274.942),
            "walk": (8.369, 14783.599)
        }
    }
    
    # Counter variables
    total_iterations = 0
    walk_questions_counter = 0
    bike_questions_counter = 0
    drive_questions_counter = 0
    default_questions_counter = 0
    
    results = []

    # Repeat the process to generate more questions
    for _ in range(10):  # Repeat the process 10 times to reach around 1000 questions
        for mode, templates, counter_name in [
            ("walk", QUESTION_TEMPLATES_WALK, "walk_questions_counter"),
            ("bike", QUESTION_TEMPLATES_BIKE, "bike_questions_counter"),
            ("drive", QUESTION_TEMPLATES_DRIVE, "drive_questions_counter"),
            ("drive", QUESTION_TEMPLATES_DEFAULT, "default_questions_counter")
        ]:
            for template in templates:
                for category in categories:
                    total_iterations += 1
                    locals()[counter_name] = locals().get(counter_name, 0) + 1
                    
                    # Randomly select parameters
                    num_locations = random.choice(possible_num_locations)
                    
                    # Get distance limits for this category and mode
                    min_dist, max_dist = distance_limits[category][mode]
                    
                    # Generate a random max_distance between min and max (in km)
                    max_distance = round(random.uniform(min_dist/1000, max_dist/1000), 2)
                    
                    # Create question
                    question = template.format(
                        category=category,
                        num_locations=num_locations,
                        max_distance=max_distance
                    )
                    
                    # Get real data
                    try:
                        api_result = get_closest_distance_time(
                            category=category,
                            mode=mode,
                            metric_to_extract="distance",
                            max_metric=max_distance * 1000,  # Convert km to meters
                            nr_locations=num_locations
                        )
                        
                        # Print the API result for debugging
                        print(f"API result for {category} with mode {mode}: {api_result}")

                        if isinstance(api_result, list) and len(api_result) > 0:
                            # Format API call for answer
                            
                            # Create answer with all locations
                            locations_info = "; ".join(api_result)
                            
                            answer_api_snippet = (
                                f'<API>get_closest_distance_time('
                                f'category="{category}", '
                                f'mode="{mode}", '
                                f'metric_to_extract="distance", '
                                f'max_metric={max_distance * 1000}, '
                                f'nr_locations={num_locations}) -> '
                                f'{{"addresses": {locations_info}}}</API>'
                            )
                            
                            
                            answer = (
                                f"Here are {len(api_result)} locations with a {category} within {max_distance}km: {answer_api_snippet} "
                                f"{locations_info}."
                            )
                            
                            results.append((question, answer))
                        else:
                            print(f"No results found for {category} with mode {mode}")
                    except Exception as e:
                        print(f"Error processing {category} with mode {mode}: {str(e)}")
    
    # Write results to CSV
    with open(csv_output_path, mode="w", encoding="utf-8", newline="") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["question", "answer"])
        for q, a in results:
            writer.writerow([q, a])
    
    print(f"\nDataset created: {csv_output_path}")
    print(f"Total iterations: {total_iterations}")
    print(f"Walking questions: {walk_questions_counter}")
    print(f"Biking questions: {bike_questions_counter}")
    print(f"Driving questions: {drive_questions_counter}")
    print(f"Default (assumed driving) questions: {default_questions_counter}")
    print(f"Total Q&A pairs generated: {len(results)}")

if __name__ == "__main__":
    output_file = "q_and_a_dataset_INTREBARE2_MULTE_LAST.csv"
    generate_distance_qa(csv_output_path=output_file) 