import csv
import random
import sys
import os

# Add the parent directory to sys.path to import the function
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scirpt_locatie import get_closest_distance_time

# 20 creative question templates (distance-focused)
# QUESTION_TEMPLATES_DISTANCE = [
#     "Which is the closest {category} by distance? I'm currently on {street} in {city}.",
#     "Where can I find the nearest {category} around here? I'm located at {street} in {city}.",
#     "I need the closest {category} by distance, and I'm in {city} on {street}.",
#     "Which {category} is closest by distance if I'm at {street} in {city}?",
#     "Please tell me the nearest {category} by distance. My location is {city}, {street}.",
#     "From {city}, {street}, which is the closest {category} by distance?",
#     "I'm in {city} on {street}. Which {category} is nearest by distance?",
#     "Point me to the nearest {category} by distance if I'm on {street} in {city}.",
#     "Where's the nearest {category} by distance? I'm standing at {street} in {city}.",
#     "Which {category} is the closest by distance if I'm on {street}, {city}?",
#     "How do I find the nearest {category} by distance if I'm at {city}, {street}?",
#     "Please show me the closest {category} by distance from {city}, {street}.",
#     "Which {category} is nearest by distance from {city} on {street}?",
#     "In {city} on {street}, where's the nearest {category} by distance?",
#     "Guide me to the closest {category} by distance from {city}, {street}.",
#     "From {city}, {street}, which {category} is nearest by distance?",
#     "I'm here in {city} on {street}. Which {category} is the closest by distance?",
#     "Which {category} is closest by distance from {city}, {street}?",
#     "I'm located at {city}, {street}. Where's the nearest {category} by distance?",
#     "What's the nearest {category} by distance from {city}, {street}?"
# ]

QUESTION_TEMPLATES_DISTANCE = [
    "Hey, what's the closest {category} to {street} here in {city}, distance-wise?",
    "Do you know where the nearest {category} is located? I'm over on {street} in {city}.",
    "Could you help me find the closest {category}? I'm currently at {street}, {city}.",
    "If I'm on {street} in {city}, what's the nearest {category} by distance?",
    "Quick question—I'm at {city}, {street}. Where's the nearest {category} distance-wise?",
    "From here at {city} on {street}, which {category} is closest by distance?",
    "Could you direct me to the closest {category}? I'm currently on {street}, {city}.",
    "Any idea where the nearest {category} is from {street} here in {city}?",
    "What's the nearest {category} if I'm hanging out on {street} in {city}?",
    "Could you let me know how to find the closest {category} from {city}, {street}?",
    "Hey, I'm at {city}, {street}. Can you show me the closest {category} by distance?",
    "If I'm over here on {street} in {city}, which {category} is closest?",
    "Right now, I'm in {city} at {street}. Where's the nearest {category} around here?",
    "Could you guide me to the closest {category} from my spot on {street}, {city}?",
    "From {street} in {city}, what's the nearest {category} I can reach by distance?",
    "Here I am at {city} on {street}. Any clue where the closest {category} is?",
    "If I'm at {city}, {street}, which {category} is the nearest in terms of distance?",
    "Currently at {street}, {city}. Where can I find the closest {category} nearby?",
    "I'm at {city}, {street}. What's the closest {category} from here?"
]

# 20 creative question templates (time-focused)
QUESTION_TEMPLATES_TIME = [
    "I'm running late! What's the quickest {category} to get to from {street} in {city}?",
    "From where I am now at {street} in {city}, which {category} could I reach the fastest?",
    "Time's tight—what's the nearest {category} in minutes from {city}, {street}?",
    "If I'm short on time and at {street}, {city}, which {category} should I pick?",
    "I'm in a hurry at {city}, {street}. Which {category} is quickest to reach from here?",
    "Quick question: From {street} in {city}, what's the fastest {category} I can get to?",
    "From here at {city}, {street}, what's the closest {category} if I'm measuring by travel time?",
    "I've only got a few minutes—what {category} can I reach quickest from {street}, {city}?",
    "Stuck at {city}, {street}. What's the fastest-to-reach {category} near me?",
    "Can you point me to the quickest {category} from {street} in {city}?",
    "Short on time at {city}, {street}. Which {category} would I arrive at first?",
    "From {street}, {city}, which {category} is the shortest trip by time?",
    "I'm at {city}, {street}. What's the fastest nearby {category}?",
    "I need to save time—where's the nearest {category} from {street} in {city} based on minutes?",
    "If minutes count, what's the quickest {category} I can reach from {city}, {street}?",
    "From {city}, {street}, which {category} is closest in travel time?",
    "What's my quickest option for a {category} near {street} in {city}?",
    "I'm pressed for time on {street}, {city}. Which {category} should I choose?",
    "If I'm at {street} in {city}, what's the fastest {category} I can reach right now?",
    "In terms of time, what's the nearest {category} from my current spot at {city}, {street}?"
]

QUESTION_TEMPLATES_DISTANCE_WALK = [
    "Hey, what's the nearest {category} within walking distance from {street} here in {city}?",
    "I'm on foot at {street} in {city}, do you know where the closest {category} is?",
    "Could you point me to a {category} nearby? I'm walking around {street}, {city}.",
    "I'm walking around {street} in {city}. Any chance you know which {category} I can get to fastest?",
    "Quick question—I'm out walking near {street}, {city}. Where's the closest {category}?",
    "I'm at {street} in {city} right now, which {category} is closest if I'm walking?",
    "Standing on {street} in {city} and looking to walk—can you tell me where the nearest {category} is?",
    "Mind guiding me to the closest {category}? I'm currently walking near {street} in {city}.",
    "Any idea where the closest {category} is from my current spot at {street}, {city}? I'm on foot.",
    "Where can I find the nearest {category} from {street}, {city}, if I'm walking?",
    "Walking around {city} near {street}, could you recommend a close-by {category}?",
    "I'm walking near {street}, {city}. Any quick routes to the nearest {category}?",
    "Hey, while I'm out for a walk at {street} in {city}, where's the closest {category}?",
    "Taking a leisurely walk on {street}, {city}. Got a {category} nearby?",
    "If I'm exploring {city} on foot along {street}, where should I head for the nearest {category}?",
    "Could you suggest a nearby {category}? I'm wandering around {street}, {city}.",
    "Walking near {street}, {city}. Where's the best place to find a close {category}?",
    "Out for a walk at {city}, near {street}. Know where the closest {category} is?",
    "While on foot near {street} in {city}, where's my closest {category}?",
    "Could you point me toward the nearest {category}? I'm walking around {street}, {city}.",
]


QUESTION_TEMPLATES_DISTANCE_BIKE = [
    "Hey, any bike-friendly {category} close to {street} here in {city}?",
    "I'm cycling near {street}, {city}. Know where the nearest {category} might be?",
    "Riding my bike through {street} in {city}. Could you tell me the closest {category}?",
    "Quick one—where's the nearest {category} if I'm biking around {street} in {city}?",
    "Cycling around {city} near {street}. Any recommendations for the closest {category}?",
    "From my bike route at {street}, {city}, what's the nearest {category}?",
    "Out for a ride at {street}, {city}. Could you guide me to a nearby {category}?",
    "Can you point out the nearest {category}? I'm biking near {street}, {city} right now.",
    "I'm biking around {street} in {city}. Do you know which {category} is closest?",
    "Currently cycling through {city} at {street}. What's the nearest {category} along the way?",
    "Any suggestions for the closest {category} while I'm out cycling near {street}, {city}?",
    "I'm pedaling through {city}, near {street}. Can you tell me the closest {category}?",
    "Quick help—I'm biking at {street}, {city}, looking for a nearby {category}.",
    "Riding my bike along {street} in {city}. What's the nearest {category}?",
    "Cycling near {street}, {city}. Know any conveniently located {category}?",
    "If I'm out biking around {city}, near {street}, which {category} is closest?",
    "Got my bike on {street} in {city}. Could you steer me toward the nearest {category}?",
    "Bike ride in {city}, near {street}, could you recommend the nearest {category}?",
    "I'm cycling through {street}, {city}. Which {category} would be closest?",
    "Can you suggest the nearest {category}? I'm biking around {street} in {city}.",
]

QUESTION_TEMPLATES_TIME_WALK = [
    "I'm running late and walking from {street} in {city}—which {category} is quickest to reach on foot?",
    "Short on time while walking near {street}, {city}. What's the nearest {category} I can get to quickly?",
    "If I'm walking from {city}, {street} and in a hurry, which {category} should I choose?",
    "Walking fast from {street} in {city}, can you tell me the quickest {category} nearby?",
    "In a rush on foot at {city}, {street}. What's the fastest {category} to walk to?",
    "Got limited time, walking around {street}, {city}. Which {category} is quickest to reach?",
    "I'm pressed for time walking near {street}, {city}. What's my best bet for a quick {category}?",
    "Which {category} could I walk to fastest from {street} in {city}?",
    "In a hurry and on foot near {city}, {street}. Where's the quickest {category}?",
    "Quick question—I'm walking at {street}, {city}. Which {category} is quickest from here?",
    "I need something quick and nearby, walking from {street}, {city}, which {category} is closest time-wise?",
    "Fastest {category} I can reach on foot from {street} in {city}?",
    "I'm short on time and walking near {city}, {street}. What's the fastest reachable {category}?",
    "From {street}, {city}, what's the closest {category} I can reach quickly by walking?",
    "Walking near {street}, {city}—in terms of minutes, which {category} is closest?",
    "I'm walking and pressed for time at {street}, {city}. Which {category} should I head to?",
    "From my current walking location at {street}, {city}, what's the fastest-to-reach {category}?",
    "I'm rushing on foot near {city}, {street}, where's the quickest {category} to get to?",
    "Got a tight schedule, walking from {street} in {city}. Which {category} is closest by minutes?",
    "If every minute counts, what {category} should I walk to from {street}, {city}?",
]

QUESTION_TEMPLATES_TIME_BIKE = [
    "I'm running late—where's the quickest {category} I can reach by bike from {street} in {city}?",
    "Cycling from {street}, {city}, what's the fastest {category} nearby?",
    "On my bike and tight on time at {city}, {street}. What's my quickest option for a {category}?",
    "In a hurry cycling near {street} in {city}, can you tell me the fastest reachable {category}?",
    "Need a quick stop—what's the nearest {category} if I'm biking around {city}, {street}?",
    "Cycling quickly from {street} in {city}, which {category} is closest in minutes?",
    "Short on time and biking near {street}, {city}. What's the fastest {category} I can reach?",
    "Pressed for time, riding my bike through {city} at {street}. Where's the nearest quick {category}?",
    "Quick ride from {street}, {city}, what's my fastest {category} option?",
    "Cycling around {street}, {city}, need the quickest {category} available. Any suggestions?",
    "Racing against the clock on my bike near {city}, {street}. Which {category} is fastest to get to?",
    "From my current cycling spot at {street} in {city}, which {category} is quickest?",
    "I'm biking and short on time at {street}, {city}. Could you suggest the fastest {category}?",
    "On a tight schedule biking through {street}, {city}. What's the closest {category} I can reach quickly?",
    "Quickly biking from {city}, {street}, which nearby {category} saves me the most time?",
    "I'm pedaling fast around {street}, {city}. What's the quickest {category}?",
    "Cycling with limited time from {street}, {city}, which {category} can I get to fastest?",
    "Bike-riding and in a hurry at {city}, {street}, where's my nearest quick stop for a {category}?",
    "Fastest reachable {category} from my cycling route at {street}, {city}?",
    "Quick question—biking near {street}, {city}, what's the quickest {category} I can hit?",
]


def generate_all_qa(csv_input_path, csv_output_path="q_and_a_dataset.csv"):
    """
    Reads a CSV with 'City' and 'Street Name',
    uses every (city, street) pair for each question template,
    randomly picks category/distance/time, and saves Q&A pairs to output CSV.

    :param csv_input_path: str, path to input CSV with columns 'City','Street Name','Latitude','Longitude'
    :param csv_output_path: str, path to output CSV
    """
    categories = ["hospitals", "pharmacies", "supermarkets"]
    city_street_data = []
    
    # Counter variables
    total_iterations = 0
    city_street_counter = 0
    distance_questions_counter = 0
    time_questions_counter = 0
    distance_walk_questions_counter = 0
    distance_bike_questions_counter = 0
    time_walk_questions_counter = 0
    time_bike_questions_counter = 0

    # 1) Load city-street data
    with open(csv_input_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            city = row.get("City")
            street = row.get("Street Name")
            if city and street:
                city_street_data.append((city, street))
    
    if not city_street_data:
        print("No valid City,Street data found. Aborting.")
        return

    # 2) Generate Q&A for each (city,street) and each template
    results = []
    for city, street in city_street_data:
        city_street_counter += 1
        print(f"\nProcessing city/street pair {city_street_counter}: {city}, {street}")
        
        # Generate distance-focused questions (drive mode)
        for question_template in QUESTION_TEMPLATES_DISTANCE:
            distance_questions_counter += 1
            total_iterations += 1
            print(f"Iteration {total_iterations}: Distance question {distance_questions_counter}")
            
            # Pick a random category
            category = random.choice(categories)

            # Create question
            question = question_template.format(
                category=category, city=city, street=street
            )

            # Call the actual function to get real data
            mode_chosen = "drive"
            location = f"{city}, {street}"
            try:
                api_result = get_closest_distance_time(
                    category=f"{category}", 
                    mode=mode_chosen,
                    location=location,
                    metric_to_extract="distance"
                )
                
                if api_result and len(api_result) > 0:
                    distance_km = round(api_result[0]["distance"] / 1000, 3)
                    time_mins = round(api_result[0]["time"], 3)
                    
                    # Format the API call for the answer
                    answer_api_snippet = (
                        f'<API>get_closest_distance_time('
                        f'category="{category}", '
                        f'mode="{mode_chosen}", '
                        f'location="{location}", '
                        f'metric_to_extract="distance") -> '
                        f'{{"distance": {distance_km}, "time": {time_mins}}}</API>'
                    )

                    answer = (
                        f"The closest {category} you can find is "
                        f"{answer_api_snippet} "
                        f"{distance_km}km away."
                    )
                    
                    results.append((question, answer))
                else:
                    print(f"No results found for {location}, {category}")
            except Exception as e:
                print(f"Error processing {location}, {category}: {str(e)}")

        # Generate time-focused questions (drive mode)
        for question_template in QUESTION_TEMPLATES_TIME:
            time_questions_counter += 1
            total_iterations += 1
            print(f"Iteration {total_iterations}: Time question {time_questions_counter}")
            
            # Pick a random category
            category = random.choice(categories)

            # Create question
            question = question_template.format(
                category=category, city=city, street=street
            )

            # Call the actual function to get real data
            mode_chosen = "drive"
            location = f"{city}, {street}"
            try:
                api_result = get_closest_distance_time(
                    category=f"{category}", 
                    mode=mode_chosen,
                    location=location,
                    metric_to_extract="time"
                )
                
                if api_result and len(api_result) > 0:
                    distance_km = round(api_result[0]["distance"] / 1000, 3)
                    time_mins = round(api_result[0]["time"], 3)
                    
                    # Format the API call for the answer
                    answer_api_snippet = (
                        f'<API>get_closest_distance_time('
                        f'category="{category}", '
                        f'mode="{mode_chosen}", '
                        f'location="{location}", '
                        f'metric_to_extract="time") -> '
                        f'{{"distance": {distance_km}, "time": {time_mins}}}</API>'
                    )

                    answer = (
                        f"The quickest {category} you can reach is "
                        f"{answer_api_snippet} "
                        f"just {time_mins} minutes away."
                    )
                    
                    results.append((question, answer))
                else:
                    print(f"No results found for {location}, {category}")
            except Exception as e:
                print(f"Error processing {location}, {category}: {str(e)}")
                
        # Generate distance-focused questions (walking mode)
        for question_template in QUESTION_TEMPLATES_DISTANCE_WALK:
            distance_walk_questions_counter += 1
            total_iterations += 1
            print(f"Iteration {total_iterations}: Distance walk question {distance_walk_questions_counter}")
            
            category = random.choice(categories)
            question = question_template.format(
                category=category, city=city, street=street
            )

            mode_chosen = "walk"
            location = f"{city}, {street}"
            try:
                api_result = get_closest_distance_time(
                    category=f"{category}", 
                    mode=mode_chosen,
                    location=location,
                    metric_to_extract="distance"
                )
                
                if api_result and len(api_result) > 0:
                    distance_km = round(api_result[0]["distance"] / 1000, 3)
                    time_mins = round(api_result[0]["time"], 3)
                    
                    answer_api_snippet = (
                        f'<API>get_closest_distance_time('
                        f'category="{category}", '
                        f'mode="{mode_chosen}", '
                        f'location="{location}", '
                        f'metric_to_extract="distance") -> '
                        f'{{"distance": {distance_km}, "time": {time_mins}}}</API>'
                    )

                    answer = (
                        f"The closest {category} within walking distance is "
                        f"{answer_api_snippet} "
                        f"{distance_km}km away."
                    )
                    
                    results.append((question, answer))
                else:
                    print(f"No results found for {location}, {category} (walking)")
            except Exception as e:
                print(f"Error processing {location}, {category} (walking): {str(e)}")
                
        # Generate distance-focused questions (bicycling mode)
        for question_template in QUESTION_TEMPLATES_DISTANCE_BIKE:
            distance_bike_questions_counter += 1
            total_iterations += 1
            print(f"Iteration {total_iterations}: Distance bike question {distance_bike_questions_counter}")
            
            category = random.choice(categories)
            question = question_template.format(
                category=category, city=city, street=street
            )

            mode_chosen = "bike"
            location = f"{city}, {street}"
            try:
                api_result = get_closest_distance_time(
                    category=f"{category}", 
                    mode=mode_chosen,
                    location=location,
                    metric_to_extract="distance"
                )
                
                if api_result and len(api_result) > 0:
                    distance_km = round(api_result[0]["distance"] / 1000, 3)
                    time_mins = round(api_result[0]["time"], 3)
                    
                    answer_api_snippet = (
                        f'<API>get_closest_distance_time('
                        f'category="{category}", '
                        f'mode="{mode_chosen}", '
                        f'location="{location}", '
                        f'metric_to_extract="distance") -> '
                        f'{{"distance": {distance_km}, "time": {time_mins}}}</API>'
                    )

                    answer = (
                        f"The closest {category} by bike is "
                        f"{answer_api_snippet} "
                        f"{distance_km}km away."
                    )
                    
                    results.append((question, answer))
                else:
                    print(f"No results found for {location}, {category} (bicycling)")
            except Exception as e:
                print(f"Error processing {location}, {category} (bicycling): {str(e)}")
                
        # Generate time-focused questions (walking mode)
        for question_template in QUESTION_TEMPLATES_TIME_WALK:
            time_walk_questions_counter += 1
            total_iterations += 1
            print(f"Iteration {total_iterations}: Time walk question {time_walk_questions_counter}")
            
            category = random.choice(categories)
            question = question_template.format(
                category=category, city=city, street=street
            )

            mode_chosen = "walk"
            location = f"{city}, {street}"
            try:
                api_result = get_closest_distance_time(
                    category=f"{category}", 
                    mode=mode_chosen,
                    location=location,
                    metric_to_extract="time"
                )
                
                if api_result and len(api_result) > 0:
                    distance_km = round(api_result[0]["distance"] / 1000, 3)
                    time_mins = round(api_result[0]["time"], 3)
                    
                    answer_api_snippet = (
                        f'<API>get_closest_distance_time('
                        f'category="{category}", '
                        f'mode="{mode_chosen}", '
                        f'location="{location}", '
                        f'metric_to_extract="time") -> '
                        f'{{"distance": {distance_km}, "time": {time_mins}}}</API>'
                    )

                    answer = (
                        f"The quickest {category} you can walk to is "
                        f"{answer_api_snippet} "
                        f"just {time_mins} minutes away on foot."
                    )
                    
                    results.append((question, answer))
                else:
                    print(f"No results found for {location}, {category} (walking time)")
            except Exception as e:
                print(f"Error processing {location}, {category} (walking time): {str(e)}")
                
        # Generate time-focused questions (bicycling mode)
        for question_template in QUESTION_TEMPLATES_TIME_BIKE:
            time_bike_questions_counter += 1
            total_iterations += 1
            print(f"Iteration {total_iterations}: Time bike question {time_bike_questions_counter}")
            
            category = random.choice(categories)
            question = question_template.format(
                category=category, city=city, street=street
            )

            mode_chosen = "bike"
            location = f"{city}, {street}"
            try:
                api_result = get_closest_distance_time(
                    category=f"{category}", 
                    mode=mode_chosen,
                    location=location,
                    metric_to_extract="time"
                )
                
                if api_result and len(api_result) > 0:
                    distance_km = round(api_result[0]["distance"] / 1000, 3)
                    time_mins = round(api_result[0]["time"], 3)
                    
                    answer_api_snippet = (
                        f'<API>get_closest_distance_time('
                        f'category="{category}", '
                        f'mode="{mode_chosen}", '
                        f'location="{location}", '
                        f'metric_to_extract="time") -> '
                        f'{{"distance": {distance_km}, "time": {time_mins}}}</API>'
                    )

                    answer = (
                        f"The quickest {category} you can reach by bike is "
                        f"{answer_api_snippet} "
                        f"just {time_mins} minutes away cycling."
                    )
                    
                    results.append((question, answer))
                else:
                    print(f"No results found for {location}, {category} (bicycling time)")
            except Exception as e:
                print(f"Error processing {location}, {category} (bicycling time): {str(e)}")

    # 3) Write results to CSV
    with open(csv_output_path, mode="w", encoding="utf-8", newline="") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["question", "answer"])
        for q, a in results:
            writer.writerow([q, a])

    print(f"Dataset created: {csv_output_path} with {len(results)} rows.")
    print(f"Total iterations: {total_iterations}")
    print(f"City/street pairs processed: {city_street_counter}")
    print(f"Distance questions generated: {distance_questions_counter}")
    print(f"Time questions generated: {time_questions_counter}")
    print(f"Distance walking questions generated: {distance_walk_questions_counter}")
    print(f"Distance biking questions generated: {distance_bike_questions_counter}")
    print(f"Time walking questions generated: {time_walk_questions_counter}")
    print(f"Time biking questions generated: {time_bike_questions_counter}")


if __name__ == "__main__":
    # Example usage
    input_file = "durangaldea_streets.csv"  # Your input CSV path
    output_file = "DATASET_FINAL_INTRB_1.csv"

    generate_all_qa(
        csv_input_path=input_file,
        csv_output_path=output_file
    )
    # print(len(QUESTION_TEMPLATES_DISTANCE))
    test_category = "hospital"
    test_mode = "drive"
    test_location = "Bilbao, Gran Vía"  # Replace with your test location

    # Make the API call
    try:
        api_result = get_closest_distance_time(
            category=f"{test_category}s", 
            mode=test_mode,
            location=test_location,
            metric_to_extract="distance"
        )
        
        if api_result and len(api_result) > 0:
            print("API call successful! Result:")
            print(api_result)
        else:
            print("No results found for the test location.")
    except Exception as e:
        print(f"Error during API call: {str(e)}")