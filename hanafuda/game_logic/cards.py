import random

# Card types
BRIGHT = "Bright"
ANIMAL = "Animal"
RIBBON = "Ribbon"
PLAIN = "Plain"

# Special card names for easier identification
CRANE = "Pine Crane"
CURTAIN = "Cherry Blossom Curtain"
MOON = "Susuki Moon"
RAINMAN = "Willow Ono no Michikaze" # Rainman
PHOENIX = "Paulownia Phoenix"
WARBLER = "Plum Warbler" # Sometimes special
CUCKOO = "Wisteria Cuckoo" # Sometimes special
BUTTERFLIES = "Peony Butterflies" # Sometimes special
BOAR = "Clover Boar"
DEER = "Maple Deer"
GEESE = "Susuki Geese" # Animal, but part of a Yaku with Moon

# Sake Cup (can be Animal or Plain depending on Yaku)
SAKE_CUP = "Chrysanthemum Sake Cup"

# Traditional Hanafuda Deck
HANAFUDA_DECK_STRUCTURE = [
    # January (Matsu - Pine)
    {"month": 1, "name": CRANE, "type": BRIGHT, "points": 20, "image_filename": "matsu_crane.png"},
    {"month": 1, "name": "Pine Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "matsu_red_ribbon.png"},
    {"month": 1, "name": "Pine Plain 1", "type": PLAIN, "points": 1, "image_filename": "matsu_plain1.png"},
    {"month": 1, "name": "Pine Plain 2", "type": PLAIN, "points": 1, "image_filename": "matsu_plain2.png"},

    # February (Ume - Plum Blossom)
    {"month": 2, "name": WARBLER, "type": ANIMAL, "points": 10, "image_filename": "ume_warbler.png"}, # Bush Warbler
    {"month": 2, "name": "Plum Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "ume_red_ribbon.png"},
    {"month": 2, "name": "Plum Plain 1", "type": PLAIN, "points": 1, "image_filename": "ume_plain1.png"},
    {"month": 2, "name": "Plum Plain 2", "type": PLAIN, "points": 1, "image_filename": "ume_plain2.png"},

    # March (Sakura - Cherry Blossom)
    {"month": 3, "name": CURTAIN, "type": BRIGHT, "points": 20, "image_filename": "sakura_curtain.png"}, # Camp Curtain
    {"month": 3, "name": "Cherry Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "sakura_red_ribbon.png"}, # Poetry Ribbon
    {"month": 3, "name": "Cherry Plain 1", "type": PLAIN, "points": 1, "image_filename": "sakura_plain1.png"},
    {"month": 3, "name": "Cherry Plain 2", "type": PLAIN, "points": 1, "image_filename": "sakura_plain2.png"},

    # April (Fuji - Wisteria)
    {"month": 4, "name": CUCKOO, "type": ANIMAL, "points": 10, "image_filename": "fuji_cuckoo.png"}, # Lesser Cuckoo
    {"month": 4, "name": "Wisteria Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "fuji_red_ribbon.png"}, # Plain Red Ribbon
    {"month": 4, "name": "Wisteria Plain 1", "type": PLAIN, "points": 1, "image_filename": "fuji_plain1.png"},
    {"month": 4, "name": "Wisteria Plain 2", "type": PLAIN, "points": 1, "image_filename": "fuji_plain2.png"},

    # May (Ayame - Iris)
    {"month": 5, "name": "Iris Bridge", "type": ANIMAL, "points": 10, "image_filename": "ayame_bridge.png"}, # Water Iris or Eight Plank Bridge
    {"month": 5, "name": "Iris Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "ayame_red_ribbon.png"}, # Plain Red Ribbon
    {"month": 5, "name": "Iris Plain 1", "type": PLAIN, "points": 1, "image_filename": "ayame_plain1.png"},
    {"month": 5, "name": "Iris Plain 2", "type": PLAIN, "points": 1, "image_filename": "ayame_plain2.png"},

    # June (Botan - Peony)
    {"month": 6, "name": BUTTERFLIES, "type": ANIMAL, "points": 10, "image_filename": "botan_butterflies.png"},
    {"month": 6, "name": "Peony Blue Ribbon", "type": RIBBON, "points": 5, "image_filename": "botan_blue_ribbon.png"}, # Blue Ribbon
    {"month": 6, "name": "Peony Plain 1", "type": PLAIN, "points": 1, "image_filename": "botan_plain1.png"},
    {"month": 6, "name": "Peony Plain 2", "type": PLAIN, "points": 1, "image_filename": "botan_plain2.png"},

    # July (Hagi - Bush Clover)
    {"month": 7, "name": BOAR, "type": ANIMAL, "points": 10, "image_filename": "hagi_boar.png"},
    {"month": 7, "name": "Clover Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "hagi_red_ribbon.png"}, # Plain Red Ribbon
    {"month": 7, "name": "Clover Plain 1", "type": PLAIN, "points": 1, "image_filename": "hagi_plain1.png"},
    {"month": 7, "name": "Clover Plain 2", "type": PLAIN, "points": 1, "image_filename": "hagi_plain2.png"},

    # August (Susuki - Pampas Grass)
    {"month": 8, "name": MOON, "type": BRIGHT, "points": 20, "image_filename": "susuki_moon.png"}, # Moon over Susuki
    {"month": 8, "name": GEESE, "type": ANIMAL, "points": 10, "image_filename": "susuki_geese.png"}, # Geese in Flight
    {"month": 8, "name": "Susuki Plain 1", "type": PLAIN, "points": 1, "image_filename": "susuki_plain1.png"},
    {"month": 8, "name": "Susuki Plain 2", "type": PLAIN, "points": 1, "image_filename": "susuki_plain2.png"},

    # September (Kiku - Chrysanthemum)
    {"month": 9, "name": SAKE_CUP, "type": ANIMAL, "points": 10, "image_filename": "kiku_sake_cup.png"}, # Sake Cup (often treated as Animal for yaku)
    {"month": 9, "name": "Chrysanthemum Blue Ribbon", "type": RIBBON, "points": 5, "image_filename": "kiku_blue_ribbon.png"}, # Blue Ribbon
    {"month": 9, "name": "Chrysanthemum Plain 1", "type": PLAIN, "points": 1, "image_filename": "kiku_plain1.png"},
    {"month": 9, "name": "Chrysanthemum Plain 2", "type": PLAIN, "points": 1, "image_filename": "kiku_plain2.png"},

    # October (Momiji - Maple)
    {"month": 10, "name": DEER, "type": ANIMAL, "points": 10, "image_filename": "momiji_deer.png"},
    {"month": 10, "name": "Maple Blue Ribbon", "type": RIBBON, "points": 5, "image_filename": "momiji_blue_ribbon.png"}, # Blue Ribbon
    {"month": 10, "name": "Maple Plain 1", "type": PLAIN, "points": 1, "image_filename": "momiji_plain1.png"},
    {"month": 10, "name": "Maple Plain 2", "type": PLAIN, "points": 1, "image_filename": "momiji_plain2.png"},

    # November (Yanagi - Willow)
    {"month": 11, "name": RAINMAN, "type": BRIGHT, "points": 20, "image_filename": "yanagi_rainman.png"}, # Ono no Michikaze (Rainman) or Swallow (sometimes Animal)
    # Note: The "Swallow" is often considered the Animal for November. The Rainman is a Bright.
    # Some decks have Swallow as Animal and Rainman as special plain. Here, Rainman is Bright.
    # Let's add Swallow as a separate animal card for November if needed by rules, or adjust.
    # For now, sticking to common representations where Rainman is the key card.
    # The typical Willow animal is the Swallow. For Koi Koi, Rainman is a bright.
    # The Swallow is often depicted with the Rainman or separately.
    # The issue is that Willow has 1 Bright, 1 Animal (Swallow), 1 Ribbon, 1 Plain.
    # The Rainman card itself is sometimes debated if it's "Bright" or a special "Plain" that can be an animal.
    # Let's treat Rainman as Bright as per the points. The Swallow is an Animal.
    # The card with Ono no Michikaze is usually the Bright. The Swallow is usually the Animal.
    # The task description doesn't specify, so I'll use a common structure.
    # The typical Willow set is: Rainman (Bright), Swallow (Animal), Willow Red Ribbon, Willow Plain (Storm/Demon).
    # For now, I will make Rainman the Bright. I will add a Swallow card. The "Plain" for Willow is often special (lightning/oni drum).
    {"month": 11, "name": "Willow Swallow", "type": ANIMAL, "points": 10, "image_filename": "yanagi_swallow.png"},
    {"month": 11, "name": "Willow Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "yanagi_red_ribbon.png"}, # Plain Red Ribbon (often with lightning)
    {"month": 11, "name": "Willow Plain", "type": PLAIN, "points": 1, "image_filename": "yanagi_plain_storm.png"}, # Often called the "Storm" or "Demon" card

    # December (Kiri - Paulownia)
    {"month": 12, "name": PHOENIX, "type": BRIGHT, "points": 20, "image_filename": "kiri_phoenix.png"},
    # December has 3 plains, one is usually yellow or a different color. No ribbon.
    {"month": 12, "name": "Paulownia Plain 1 (Yellow)", "type": PLAIN, "points": 1, "image_filename": "kiri_plain_yellow.png"},
    {"month": 12, "name": "Paulownia Plain 2", "type": PLAIN, "points": 1, "image_filename": "kiri_plain2.png"},
    {"month": 12, "name": "Paulownia Plain 3", "type": PLAIN, "points": 1, "image_filename": "kiri_plain3.png"},
]

def create_deck():
    """Creates a new, ordered Hanafuda deck."""
    # Ensure the deck has 48 cards. The Willow month needs adjustment.
    # Standard deck: 1 Bright, 1 Animal, 1 Ribbon, 1 Plain for November.
    # My current structure for November: Rainman (Bright), Swallow (Animal), Ribbon, Plain. This is correct.
    # My current structure for December: Phoenix (Bright), 3 Plains. This is correct.
    deck = []
    for card_template in HANAFUDA_DECK_STRUCTURE:
        deck.append(card_template.copy()) # Use copy to ensure distinct dicts
    if len(deck) != 48:
        # This is a check for myself during development.
        raise ValueError(f"Deck should have 48 cards, but found {len(deck)}")
    return deck

def shuffle_deck(deck):
    """Shuffles the given deck in place."""
    random.shuffle(deck)

def deal_cards_koi_koi(deck):
    """
    Deals cards for a two-player Koi-Koi game.
    Returns:
        (player1_hand, player2_hand, field_cards)
    The remaining deck is modified in place.
    Koi-Koi dealing: 2 to P1, 2 to P2, 2 to Field, repeated 4 times.
    So, 8 for P1, 8 for P2, 8 for Field.
    """
    if len(deck) < 24: # 8 cards for 2 players + 8 for field
        raise ValueError("Not enough cards in the deck to deal for Koi-Koi.")

    player1_hand = []
    player2_hand = []
    field_cards = []

    for _ in range(4): # Deal in 4 rounds
        # Player 1
        player1_hand.append(deck.pop())
        player1_hand.append(deck.pop())
        # Player 2
        player2_hand.append(deck.pop())
        player2_hand.append(deck.pop())
        # Field
        field_cards.append(deck.pop())
        field_cards.append(deck.pop())
    
    return player1_hand, player2_hand, field_cards

# Example usage (optional, for testing the script directly)
if __name__ == '__main__':
    new_deck = create_deck()
    print(f"Created a deck with {len(new_deck)} cards.")
    
    # Verify specific cards (optional check)
    # Example: Check November cards
    # november_cards = [card for card in new_deck if card['month'] == 11]
    # print(f"November cards ({len(november_cards)}): {november_cards}")
    # Expected: Rainman (Bright), Swallow (Animal), Ribbon, Plain.
    
    # Example: Check December cards
    # december_cards = [card for card in new_deck if card['month'] == 12]
    # print(f"December cards ({len(december_cards)}): {december_cards}")
    # Expected: Phoenix (Bright), 3 Plains.

    shuffle_deck(new_deck)
    print("Deck shuffled.")
    
    try:
        p1_hand, p2_hand, field = deal_cards_koi_koi(new_deck)
        print(f"Player 1 Hand ({len(p1_hand)} cards): {p1_hand}")
        print(f"Player 2 Hand ({len(p2_hand)} cards): {p2_hand}")
        print(f"Field Cards ({len(field)} cards): {field}")
        print(f"Remaining deck ({len(new_deck)} cards).") # Should be 24
    except ValueError as e:
        print(f"Error: {e}")
