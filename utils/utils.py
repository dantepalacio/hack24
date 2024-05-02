import sys
import os
import random
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def add_to_csv(post_dict,action):
    fieldnames = ["text", "image", "video"]

    
    filename = 'like_humanfeedback.csv' if action == 'like' else 'dislike_humanfeedback.csv'
    


    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if csvfile.tell() == 0:
            writer.writeheader()
        
        writer.writerow(post_dict)

def generate_random_int_id(length=4):
    min_value = 10**(length - 1)
    max_value = (10**length) - 1
    return random.randint(min_value, max_value)

def explicit_content_check_from_text(result: dict) -> bool:
    explicit = 'publish'
    reasons = []

    for key in result.keys():
        if result[key] == 1:
            explicit = 'ban'
            reasons.append(key)
    
    return {'is_explicit': explicit, 'reasons': reasons}
    

def explicit_content_check_from_image(result: dict) -> bool:
    explicit = 'publish'
    reasons = []

    for key in result.keys():
        if float(result[key]) == 0.6:
            explicit = 'same'
            reasons.append(key)
        elif float(result[key]) > 0.6:
            explicit = 'ban'
            reasons.append(key)
 
    return {'is_explicit': explicit, 'reasons': reasons}

