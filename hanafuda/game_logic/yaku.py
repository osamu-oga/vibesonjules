# hanafuda/game_logic/yaku.py
from .cards import BRIGHT, ANIMAL, RIBBON, PLAIN, SAKE_CUP, RAINMAN, PHOENIX, CURTAIN, MOON, CRANE
from .cards import BOAR, DEER, BUTTERFLIES # Ino-Shika-Cho
from .cards import WARBLER, CUCKOO, GEESE # For specific combinations if needed, though not standard yaku on their own.

# Yaku Definitions
# Each yaku could be a dictionary or a small class with a check method.
# For simplicity, let's use dictionaries with a 'checker' function or specific card names/types.

YAKU_DEFINITIONS = [] # This will be populated below

# Helper function to count cards of a specific type or name
def count_cards(cards, card_property, value):
    return sum(1 for card in cards if card[card_property] == value)

def count_specific_cards(cards, card_names):
    return sum(1 for card in cards if card['name'] in card_names)

def has_card(cards, card_name):
    return any(card['name'] == card_name for card in cards)

# --- Bright Yaku ---
YAKU_DEFINITIONS.extend([
    {
        "name": "Goko", "points": 10, "type": "Bright",
        "condition": lambda cards: count_specific_cards(cards, [CRANE, CURTAIN, MOON, RAINMAN, PHOENIX]) == 5
    },
    {
        "name": "Shiko", "points": 8, "type": "Bright", # Four Brights (excluding Rainman)
        "condition": lambda cards: count_specific_cards(cards, [CRANE, CURTAIN, MOON, PHOENIX]) == 4 and not has_card(cards, RAINMAN)
    },
    {
        "name": "Ame-Shiko", "points": 7, "type": "Bright", # Four Brights (including Rainman)
        "condition": lambda cards: count_specific_cards(cards, [CRANE, CURTAIN, MOON, PHOENIX, RAINMAN]) == 4 and has_card(cards, RAINMAN)
    },
    # { # Original Sanko, potentially problematic due to Rainman inclusion
    #     "name": "Sanko", "points": 5, "type": "Bright", # Any Three Brights (excluding Rainman)
    #     "condition": lambda cards: count_cards(cards, 'type', BRIGHT) == 3 and not has_card(cards, RAINMAN) and not (count_specific_cards(cards, [CRANE, CURTAIN, MOON, PHOENIX]) == 3) 
    # },
    { # More precise Sanko
         "name": "Sanko (No Rain)", "points": 5, "type": "Bright",
         "condition": lambda cards: sum(1 for card in cards if card['type'] == BRIGHT and card['name'] != RAINMAN) == 3
    }
])

# --- Animal Yaku ---
YAKU_DEFINITIONS.extend([
    {
        "name": "Ino-Shika-Cho", "points": 5, "type": "Animal", # Boar, Deer, Butterflies
        "condition": lambda cards: all(has_card(cards, name) for name in [BOAR, DEER, BUTTERFLIES])
    },
    {
        "name": "Itsutsu Tane", "points": 1, "type": "Animal_Count", # Base for 5 animals, points accumulate
        "condition": lambda cards: count_cards(cards, 'type', ANIMAL) >= 5
        # Scoring for Tane is often: 5 animals = 1 pt, 6th animal = +1 pt, etc. Sake cup counts as Animal here.
    }
])

# --- Ribbon Yaku ---
RED_POETRY_RIBBONS = ["Pine Red Ribbon", "Plum Red Ribbon", "Cherry Red Ribbon"]
# Assuming card names from cards.py are: "Peony Blue Ribbon", "Chrysanthemum Blue Ribbon", "Maple Blue Ribbon"
BLUE_POETRY_RIBBONS = ["Peony Blue Ribbon", "Chrysanthemum Blue Ribbon", "Maple Blue Ribbon"] 

YAKU_DEFINITIONS.extend([
    {
        "name": "Akatan", "points": 5, "type": "Ribbon_Special", # Red Poetry Ribbons
        "condition": lambda cards: count_specific_cards(cards, RED_POETRY_RIBBONS) == 3
    },
    {
        "name": "Aotan", "points": 5, "type": "Ribbon_Special", # Blue Poetry Ribbons
        "condition": lambda cards: count_specific_cards(cards, BLUE_POETRY_RIBBONS) == 3
    },
    {
        "name": "Itsutsu Tanzaku", "points": 1, "type": "Ribbon_Count", # Base for 5 ribbons
        "condition": lambda cards: count_cards(cards, 'type', RIBBON) >= 5
    }
])

# --- Plain/Kasu Yaku ---
YAKU_DEFINITIONS.extend([
    {
        "name": "Tsukimi-zake", "points": 5, "type": "Special", # Moon Viewing (Susuki Moon + Sake Cup)
        "condition": lambda cards: has_card(cards, MOON) and has_card(cards, SAKE_CUP)
    },
    {
        "name": "Hanami-zake", "points": 5, "type": "Special", # Cherry Blossom Viewing (Cherry Curtain + Sake Cup)
        "condition": lambda cards: has_card(cards, CURTAIN) and has_card(cards, SAKE_CUP)
    },
    { 
        "name": "Kasu", "points": 1, "type": "Plain_Count", # Base for 10 plains
        "condition": lambda cards: count_cards(cards, 'type', PLAIN) >= 10
        # Assuming SAKE_CUP is type ANIMAL and does not count towards Kasu.
    }
])

def get_formed_yaku(captured_cards):
    formed_yaku_list = []
    
    # --- Bright Yaku (exclusive) ---
    goko_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Goko")
    shiko_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Shiko")
    ame_shiko_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Ame-Shiko")
    sanko_nr_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Sanko (No Rain)")

    if goko_def['condition'](captured_cards):
        formed_yaku_list.append({"name": goko_def['name'], "points": goko_def['points'], "type": goko_def['type']})
    elif shiko_def['condition'](captured_cards):
        formed_yaku_list.append({"name": shiko_def['name'], "points": shiko_def['points'], "type": shiko_def['type']})
    elif ame_shiko_def['condition'](captured_cards):
        formed_yaku_list.append({"name": ame_shiko_def['name'], "points": ame_shiko_def['points'], "type": ame_shiko_def['type']})
    elif sanko_nr_def['condition'](captured_cards):
         formed_yaku_list.append({"name": sanko_nr_def['name'], "points": sanko_nr_def['points'], "type": sanko_nr_def['type']})

    # --- Animal Yaku ---
    ino_shika_cho_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Ino-Shika-Cho")
    if ino_shika_cho_def['condition'](captured_cards):
        formed_yaku_list.append({"name": ino_shika_cho_def['name'], "points": ino_shika_cho_def['points'], "type": ino_shika_cho_def['type']})

    num_animals = count_cards(captured_cards, 'type', ANIMAL) # Sake Cup is ANIMAL
    if num_animals >= 5:
        # Ino-Shika-Cho animals also count towards Tane.
        # Points: 1 for 5, +1 for each additional. (5 animals = 1pt, 6 animals = 2pts)
        animal_points = (num_animals - 5) + 1
        # Add or update Tane yaku. If Ino-Shika-Cho gave 5, this adds on top if more animals, or establishes if no ISC.
        # This is a bit complex; let's just add a 'Tane' yaku with its points.
        # A common ruling is that Ino-Shika-Cho is 5 points, and the Tane yaku (animals) is separate.
        # So if you have ISC (3 cards, 5 pts) + 2 other animals (total 5 animals), you get ISC (5) + Tane (1) = 6 pts.
        # If this interpretation is correct, the points are additive.
        # The current 'Itsutsu Tane' definition is a flag for >=5.
        # Let's make the points for Tane itself, not just a flag.
        formed_yaku_list.append({"name": f"{num_animals} Tane", "points": animal_points, "type": "Animal_Count"})


    # --- Ribbon Yaku ---
    akatan_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Akatan")
    if akatan_def['condition'](captured_cards):
        formed_yaku_list.append({"name": akatan_def['name'], "points": akatan_def['points'], "type": akatan_def['type']})
    
    aotan_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Aotan")
    if aotan_def['condition'](captured_cards):
        formed_yaku_list.append({"name": aotan_def['name'], "points": aotan_def['points'], "type": aotan_def['type']})

    num_ribbons = count_cards(captured_cards, 'type', RIBBON)
    if num_ribbons >= 5:
        # Akatan/Aotan ribbons also count towards this total.
        # Points: 1 for 5, +1 for each additional.
        ribbon_points = (num_ribbons - 5) + 1
        # Similar to Tane, Akatan/Aotan points are typically separate.
        # So 3 Red Poetry (5pts) + 2 other ribbons (total 5 ribbons) = Akatan (5) + Tanzaku (1) = 6pts.
        formed_yaku_list.append({"name": f"{num_ribbons} Tanzaku", "points": ribbon_points, "type": "Ribbon_Count"})

    # --- Special Yaku ---
    # Tsukimi-zake and Hanami-zake can be scored with Bright yaku if cards align.
    # E.g. Moon (Bright) + Sake Cup (Animal) for Tsukimi.
    # If player has Moon + 2 other non-Rainman brights + Sake Cup: Sanko (No Rain) + Tsukimi-zake.
    tsukimi_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Tsukimi-zake")
    if tsukimi_def['condition'](captured_cards):
        formed_yaku_list.append({"name": tsukimi_def['name'], "points": tsukimi_def['points'], "type": tsukimi_def['type']})

    hanami_def = next(y for y in YAKU_DEFINITIONS if y['name'] == "Hanami-zake")
    if hanami_def['condition'](captured_cards):
        formed_yaku_list.append({"name": hanami_def['name'], "points": hanami_def['points'], "type": hanami_def['type']})
        
    # --- Plain/Kasu Yaku ---
    # Assuming SAKE_CUP is ANIMAL type and does not count as PLAIN for Kasu.
    num_plains = count_cards(captured_cards, 'type', PLAIN)
    if num_plains >= 10:
        plain_points = (num_plains - 10) + 1
        formed_yaku_list.append({"name": f"{num_plains} Kasu", "points": plain_points, "type": "Plain_Count"})

    # Calculate total points.
    # The logic above for Bright yaku already ensures exclusivity for them.
    # Other yaku are generally additive (e.g., Ino-Shika-Cho + Tane points from other animals).
    # A yaku like "Tane" or "Tanzaku" or "Kasu" will only appear once with the total count.
    
    # We need to filter out duplicate types of count yaku if they somehow got added twice (e.g. Tane)
    # For example, ensure only one "Tane" entry, one "Tanzaku", one "Kasu" in the final list.
    # The current code should produce this naturally for Tane/Tanzaku/Kasu.

    final_yaku_list = []
    # Prioritize Brights
    bright_yaku_names = ["Goko", "Shiko", "Ame-Shiko", "Sanko (No Rain)"]
    bright_found = None
    for by_name in bright_yaku_names:
        yaku_entry = next((y for y in formed_yaku_list if y['name'] == by_name), None)
        if yaku_entry:
            bright_found = yaku_entry
            break # Found the highest priority bright yaku
    if bright_found:
        final_yaku_list.append(bright_found)

    # Add other yaku types (Animal, Ribbon, Special, Counts)
    # Ensure that count-based yaku (Tane, Tanzaku, Kasu) are only added once with their total points.
    # The name f"{num_animals} Tane" already makes them unique if num_animals changes.
    
    # The list `formed_yaku_list` can have multiple entries for the same "category" if not careful.
    # E.g. if we had "Itsutsu Tane" (5 animals) and "Rokko Tane" (6 animals) as separate YAKU_DEFINITIONS.
    # The current code calculates points for Tane/Tanzaku/Kasu based on counts, so it should be fine.
    
    added_categories = set()
    if bright_found:
        added_categories.add("Bright")

    for yaku in formed_yaku_list:
        # Skip already added bright yaku
        if yaku.get('type') == "Bright" and bright_found and yaku['name'] == bright_found['name']:
            continue
        if yaku.get('type') != "Bright": # Add all non-bright yaku
            # For count yaku, ensure we only add one of each (Tane, Tanzaku, Kasu)
            # The naming convention f"{count} Tane" handles this.
            is_count_yaku = yaku['type'] in ["Animal_Count", "Ribbon_Count", "Plain_Count"]
            can_add = True
            if is_count_yaku:
                if yaku['type'] in added_categories: # e.g. if we already added an "Animal_Count"
                    can_add = False # Avoid adding multiple "Tane" entries if logic was different
                else:
                    added_categories.add(yaku['type'])
            
            if can_add:
                 # Check if this specific yaku name is already in final_yaku_list (e.g. "Ino-Shika-Cho")
                if not any(fy['name'] == yaku['name'] for fy in final_yaku_list):
                    final_yaku_list.append(yaku)

    total_points = sum(y['points'] for y in final_yaku_list)
    return final_yaku_list, total_points
