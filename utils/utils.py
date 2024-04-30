import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def explicit_content_check_from_text(result: str) -> bool:
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

