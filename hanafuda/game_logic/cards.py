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
    {"month": 1, "name": CRANE, "type": BRIGHT, "points": 20, "image_filename": "matsu_crane.png", "image_themes": {"traditional": "matsu_crane.png", "modern": "matsu_crane_modern.png", "pop": "matsu_crane_pop.png", "jiji": "matsu_crane_jiji.png"}},
    {"month": 1, "name": "Pine Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "matsu_red_ribbon.png", "image_themes": {"traditional": "matsu_red_ribbon.png", "modern": "matsu_red_ribbon_modern.png", "pop": "matsu_red_ribbon_pop.png", "jiji": "matsu_red_ribbon_jiji.png"}},
    {"month": 1, "name": "Pine Plain 1", "type": PLAIN, "points": 1, "image_filename": "matsu_plain1.png", "image_themes": {"traditional": "matsu_plain1.png", "modern": "matsu_plain1_modern.png", "pop": "matsu_plain1_pop.png", "jiji": "matsu_plain1_jiji.png"}},
    {"month": 1, "name": "Pine Plain 2", "type": PLAIN, "points": 1, "image_filename": "matsu_plain2.png", "image_themes": {"traditional": "matsu_plain2.png", "modern": "matsu_plain2_modern.png", "pop": "matsu_plain2_pop.png", "jiji": "matsu_plain2_jiji.png"}},

    # February (Ume - Plum Blossom)
    {"month": 2, "name": WARBLER, "type": ANIMAL, "points": 10, "image_filename": "ume_warbler.png", "image_themes": {"traditional": "ume_warbler.png", "modern": "ume_warbler_modern.png", "pop": "ume_warbler_pop.png", "jiji": "ume_warbler_jiji.png"}}, # Bush Warbler
    {"month": 2, "name": "Plum Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "ume_red_ribbon.png", "image_themes": {"traditional": "ume_red_ribbon.png", "modern": "ume_red_ribbon_modern.png", "pop": "ume_red_ribbon_pop.png", "jiji": "ume_red_ribbon_jiji.png"}},
    {"month": 2, "name": "Plum Plain 1", "type": PLAIN, "points": 1, "image_filename": "ume_plain1.png", "image_themes": {"traditional": "ume_plain1.png", "modern": "ume_plain1_modern.png", "pop": "ume_plain1_pop.png", "jiji": "ume_plain1_jiji.png"}},
    {"month": 2, "name": "Plum Plain 2", "type": PLAIN, "points": 1, "image_filename": "ume_plain2.png", "image_themes": {"traditional": "ume_plain2.png", "modern": "ume_plain2_modern.png", "pop": "ume_plain2_pop.png", "jiji": "ume_plain2_jiji.png"}},

    # March (Sakura - Cherry Blossom)
    {"month": 3, "name": CURTAIN, "type": BRIGHT, "points": 20, "image_filename": "sakura_curtain.png", "image_themes": {"traditional": "sakura_curtain.png", "modern": "sakura_curtain_modern.png", "pop": "sakura_curtain_pop.png", "jiji": "sakura_curtain_jiji.png"}}, # Camp Curtain
    {"month": 3, "name": "Cherry Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "sakura_red_ribbon.png", "image_themes": {"traditional": "sakura_red_ribbon.png", "modern": "sakura_red_ribbon_modern.png", "pop": "sakura_red_ribbon_pop.png", "jiji": "sakura_red_ribbon_jiji.png"}}, # Poetry Ribbon
    {"month": 3, "name": "Cherry Plain 1", "type": PLAIN, "points": 1, "image_filename": "sakura_plain1.png", "image_themes": {"traditional": "sakura_plain1.png", "modern": "sakura_plain1_modern.png", "pop": "sakura_plain1_pop.png", "jiji": "sakura_plain1_jiji.png"}},
    {"month": 3, "name": "Cherry Plain 2", "type": PLAIN, "points": 1, "image_filename": "sakura_plain2.png", "image_themes": {"traditional": "sakura_plain2.png", "modern": "sakura_plain2_modern.png", "pop": "sakura_plain2_pop.png", "jiji": "sakura_plain2_jiji.png"}},

    # April (Fuji - Wisteria)
    {"month": 4, "name": CUCKOO, "type": ANIMAL, "points": 10, "image_filename": "fuji_cuckoo.png", "image_themes": {"traditional": "fuji_cuckoo.png", "modern": "fuji_cuckoo_modern.png", "pop": "fuji_cuckoo_pop.png", "jiji": "fuji_cuckoo_jiji.png"}}, # Lesser Cuckoo
    {"month": 4, "name": "Wisteria Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "fuji_red_ribbon.png", "image_themes": {"traditional": "fuji_red_ribbon.png", "modern": "fuji_red_ribbon_modern.png", "pop": "fuji_red_ribbon_pop.png", "jiji": "fuji_red_ribbon_jiji.png"}}, # Plain Red Ribbon
    {"month": 4, "name": "Wisteria Plain 1", "type": PLAIN, "points": 1, "image_filename": "fuji_plain1.png", "image_themes": {"traditional": "fuji_plain1.png", "modern": "fuji_plain1_modern.png", "pop": "fuji_plain1_pop.png", "jiji": "fuji_plain1_jiji.png"}},
    {"month": 4, "name": "Wisteria Plain 2", "type": PLAIN, "points": 1, "image_filename": "fuji_plain2.png", "image_themes": {"traditional": "fuji_plain2.png", "modern": "fuji_plain2_modern.png", "pop": "fuji_plain2_pop.png", "jiji": "fuji_plain2_jiji.png"}},

    # May (Ayame - Iris)
    {"month": 5, "name": "Iris Bridge", "type": ANIMAL, "points": 10, "image_filename": "ayame_bridge.png", "image_themes": {"traditional": "ayame_bridge.png", "modern": "ayame_bridge_modern.png", "pop": "ayame_bridge_pop.png", "jiji": "ayame_bridge_jiji.png"}}, # Water Iris or Eight Plank Bridge
    {"month": 5, "name": "Iris Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "ayame_red_ribbon.png", "image_themes": {"traditional": "ayame_red_ribbon.png", "modern": "ayame_red_ribbon_modern.png", "pop": "ayame_red_ribbon_pop.png", "jiji": "ayame_red_ribbon_jiji.png"}}, # Plain Red Ribbon
    {"month": 5, "name": "Iris Plain 1", "type": PLAIN, "points": 1, "image_filename": "ayame_plain1.png", "image_themes": {"traditional": "ayame_plain1.png", "modern": "ayame_plain1_modern.png", "pop": "ayame_plain1_pop.png", "jiji": "ayame_plain1_jiji.png"}},
    {"month": 5, "name": "Iris Plain 2", "type": PLAIN, "points": 1, "image_filename": "ayame_plain2.png", "image_themes": {"traditional": "ayame_plain2.png", "modern": "ayame_plain2_modern.png", "pop": "ayame_plain2_pop.png", "jiji": "ayame_plain2_jiji.png"}},

    # June (Botan - Peony)
    {"month": 6, "name": BUTTERFLIES, "type": ANIMAL, "points": 10, "image_filename": "botan_butterflies.png", "image_themes": {"traditional": "botan_butterflies.png", "modern": "botan_butterflies_modern.png", "pop": "botan_butterflies_pop.png", "jiji": "botan_butterflies_jiji.png"}},
    {"month": 6, "name": "Peony Blue Ribbon", "type": RIBBON, "points": 5, "image_filename": "botan_blue_ribbon.png", "image_themes": {"traditional": "botan_blue_ribbon.png", "modern": "botan_blue_ribbon_modern.png", "pop": "botan_blue_ribbon_pop.png", "jiji": "botan_blue_ribbon_jiji.png"}}, # Blue Ribbon
    {"month": 6, "name": "Peony Plain 1", "type": PLAIN, "points": 1, "image_filename": "botan_plain1.png", "image_themes": {"traditional": "botan_plain1.png", "modern": "botan_plain1_modern.png", "pop": "botan_plain1_pop.png", "jiji": "botan_plain1_jiji.png"}},
    {"month": 6, "name": "Peony Plain 2", "type": PLAIN, "points": 1, "image_filename": "botan_plain2.png", "image_themes": {"traditional": "botan_plain2.png", "modern": "botan_plain2_modern.png", "pop": "botan_plain2_pop.png", "jiji": "botan_plain2_jiji.png"}},

    # July (Hagi - Bush Clover)
    {"month": 7, "name": BOAR, "type": ANIMAL, "points": 10, "image_filename": "hagi_boar.png", "image_themes": {"traditional": "hagi_boar.png", "modern": "hagi_boar_modern.png", "pop": "hagi_boar_pop.png", "jiji": "hagi_boar_jiji.png"}},
    {"month": 7, "name": "Clover Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "hagi_red_ribbon.png", "image_themes": {"traditional": "hagi_red_ribbon.png", "modern": "hagi_red_ribbon_modern.png", "pop": "hagi_red_ribbon_pop.png", "jiji": "hagi_red_ribbon_jiji.png"}}, # Plain Red Ribbon
    {"month": 7, "name": "Clover Plain 1", "type": PLAIN, "points": 1, "image_filename": "hagi_plain1.png", "image_themes": {"traditional": "hagi_plain1.png", "modern": "hagi_plain1_modern.png", "pop": "hagi_plain1_pop.png", "jiji": "hagi_plain1_jiji.png"}},
    {"month": 7, "name": "Clover Plain 2", "type": PLAIN, "points": 1, "image_filename": "hagi_plain2.png", "image_themes": {"traditional": "hagi_plain2.png", "modern": "hagi_plain2_modern.png", "pop": "hagi_plain2_pop.png", "jiji": "hagi_plain2_jiji.png"}},

    # August (Susuki - Pampas Grass)
    {"month": 8, "name": MOON, "type": BRIGHT, "points": 20, "image_filename": "susuki_moon.png", "image_themes": {"traditional": "susuki_moon.png", "modern": "susuki_moon_modern.png", "pop": "susuki_moon_pop.png", "jiji": "susuki_moon_jiji.png"}}, # Moon over Susuki
    {"month": 8, "name": GEESE, "type": ANIMAL, "points": 10, "image_filename": "susuki_geese.png", "image_themes": {"traditional": "susuki_geese.png", "modern": "susuki_geese_modern.png", "pop": "susuki_geese_pop.png", "jiji": "susuki_geese_jiji.png"}}, # Geese in Flight
    {"month": 8, "name": "Susuki Plain 1", "type": PLAIN, "points": 1, "image_filename": "susuki_plain1.png", "image_themes": {"traditional": "susuki_plain1.png", "modern": "susuki_plain1_modern.png", "pop": "susuki_plain1_pop.png", "jiji": "susuki_plain1_jiji.png"}},
    {"month": 8, "name": "Susuki Plain 2", "type": PLAIN, "points": 1, "image_filename": "susuki_plain2.png", "image_themes": {"traditional": "susuki_plain2.png", "modern": "susuki_plain2_modern.png", "pop": "susuki_plain2_pop.png", "jiji": "susuki_plain2_jiji.png"}},

    # September (Kiku - Chrysanthemum)
    {"month": 9, "name": SAKE_CUP, "type": ANIMAL, "points": 10, "image_filename": "kiku_sake_cup.png", "image_themes": {"traditional": "kiku_sake_cup.png", "modern": "kiku_sake_cup_modern.png", "pop": "kiku_sake_cup_pop.png", "jiji": "kiku_sake_cup_jiji.png"}}, # Sake Cup (often treated as Animal for yaku)
    {"month": 9, "name": "Chrysanthemum Blue Ribbon", "type": RIBBON, "points": 5, "image_filename": "kiku_blue_ribbon.png", "image_themes": {"traditional": "kiku_blue_ribbon.png", "modern": "kiku_blue_ribbon_modern.png", "pop": "kiku_blue_ribbon_pop.png", "jiji": "kiku_blue_ribbon_jiji.png"}}, # Blue Ribbon
    {"month": 9, "name": "Chrysanthemum Plain 1", "type": PLAIN, "points": 1, "image_filename": "kiku_plain1.png", "image_themes": {"traditional": "kiku_plain1.png", "modern": "kiku_plain1_modern.png", "pop": "kiku_plain1_pop.png", "jiji": "kiku_plain1_jiji.png"}},
    {"month": 9, "name": "Chrysanthemum Plain 2", "type": PLAIN, "points": 1, "image_filename": "kiku_plain2.png", "image_themes": {"traditional": "kiku_plain2.png", "modern": "kiku_plain2_modern.png", "pop": "kiku_plain2_pop.png", "jiji": "kiku_plain2_jiji.png"}},

    # October (Momiji - Maple)
    {"month": 10, "name": DEER, "type": ANIMAL, "points": 10, "image_filename": "momiji_deer.png", "image_themes": {"traditional": "momiji_deer.png", "modern": "momiji_deer_modern.png", "pop": "momiji_deer_pop.png", "jiji": "momiji_deer_jiji.png"}},
    {"month": 10, "name": "Maple Blue Ribbon", "type": RIBBON, "points": 5, "image_filename": "momiji_blue_ribbon.png", "image_themes": {"traditional": "momiji_blue_ribbon.png", "modern": "momiji_blue_ribbon_modern.png", "pop": "momiji_blue_ribbon_pop.png", "jiji": "momiji_blue_ribbon_jiji.png"}}, # Blue Ribbon
    {"month": 10, "name": "Maple Plain 1", "type": PLAIN, "points": 1, "image_filename": "momiji_plain1.png", "image_themes": {"traditional": "momiji_plain1.png", "modern": "momiji_plain1_modern.png", "pop": "momiji_plain1_pop.png", "jiji": "momiji_plain1_jiji.png"}},
    {"month": 10, "name": "Maple Plain 2", "type": PLAIN, "points": 1, "image_filename": "momiji_plain2.png", "image_themes": {"traditional": "momiji_plain2.png", "modern": "momiji_plain2_modern.png", "pop": "momiji_plain2_pop.png", "jiji": "momiji_plain2_jiji.png"}},

    # November (Yanagi - Willow)
    {"month": 11, "name": RAINMAN, "type": BRIGHT, "points": 20, "image_filename": "yanagi_rainman.png", "image_themes": {"traditional": "yanagi_rainman.png", "modern": "yanagi_rainman_modern.png", "pop": "yanagi_rainman_pop.png", "jiji": "yanagi_rainman_jiji.png"}}, # Ono no Michikaze (Rainman) or Swallow (sometimes Animal)
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
    {"month": 11, "name": "Willow Swallow", "type": ANIMAL, "points": 10, "image_filename": "yanagi_swallow.png", "image_themes": {"traditional": "yanagi_swallow.png", "modern": "yanagi_swallow_modern.png", "pop": "yanagi_swallow_pop.png", "jiji": "yanagi_swallow_jiji.png"}},
    {"month": 11, "name": "Willow Red Ribbon", "type": RIBBON, "points": 5, "image_filename": "yanagi_red_ribbon.png", "image_themes": {"traditional": "yanagi_red_ribbon.png", "modern": "yanagi_red_ribbon_modern.png", "pop": "yanagi_red_ribbon_pop.png", "jiji": "yanagi_red_ribbon_jiji.png"}}, # Plain Red Ribbon (often with lightning)
    {"month": 11, "name": "Willow Plain", "type": PLAIN, "points": 1, "image_filename": "yanagi_plain_storm.png", "image_themes": {"traditional": "yanagi_plain_storm.png", "modern": "yanagi_plain_storm_modern.png", "pop": "yanagi_plain_storm_pop.png", "jiji": "yanagi_plain_storm_jiji.png"}}, # Often called the "Storm" or "Demon" card

    # December (Kiri - Paulownia)
    {"month": 12, "name": PHOENIX, "type": BRIGHT, "points": 20, "image_filename": "kiri_phoenix.png", "image_themes": {"traditional": "kiri_phoenix.png", "modern": "kiri_phoenix_modern.png", "pop": "kiri_phoenix_pop.png", "jiji": "kiri_phoenix_jiji.png"}},
    # December has 3 plains, one is usually yellow or a different color. No ribbon.
    {"month": 12, "name": "Paulownia Plain 1 (Yellow)", "type": PLAIN, "points": 1, "image_filename": "kiri_plain_yellow.png", "image_themes": {"traditional": "kiri_plain_yellow.png", "modern": "kiri_plain_yellow_modern.png", "pop": "kiri_plain_yellow_pop.png", "jiji": "kiri_plain_yellow_jiji.png"}},
    {"month": 12, "name": "Paulownia Plain 2", "type": PLAIN, "points": 1, "image_filename": "kiri_plain2.png", "image_themes": {"traditional": "kiri_plain2.png", "modern": "kiri_plain2_modern.png", "pop": "kiri_plain2_pop.png", "jiji": "kiri_plain2_jiji.png"}},
    {"month": 12, "name": "Paulownia Plain 3", "type": PLAIN, "points": 1, "image_filename": "kiri_plain3.png", "image_themes": {"traditional": "kiri_plain3.png", "modern": "kiri_plain3_modern.png", "pop": "kiri_plain3_pop.png", "jiji": "kiri_plain3_jiji.png"}},
]

def create_deck(theme="traditional"):
    """Creates a new, ordered Hanafuda deck with a specific theme."""
    # Ensure the deck has 48 cards. The Willow month needs adjustment.
    # Standard deck: 1 Bright, 1 Animal, 1 Ribbon, 1 Plain for November.
    # My current structure for November: Rainman (Bright), Swallow (Animal), Ribbon, Plain. This is correct.
    # My current structure for December: Phoenix (Bright), 3 Plains. This is correct.
    deck = []
    for card_template in HANAFUDA_DECK_STRUCTURE:
        card = card_template.copy() # Use copy to ensure distinct dicts
        image_themes = card_template.get("image_themes", {})

        if theme in image_themes:
            card['image_filename'] = image_themes[theme]
        else:
            # Fallback to traditional if theme not found or invalid
            card['image_filename'] = image_themes.get('traditional', card.get('image_filename'))
            # Further fallback to existing image_filename if 'traditional' is somehow missing in image_themes

        deck.append(card)

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
    print("--- Testing Traditional Theme (default) ---")
    traditional_deck = create_deck()
    print(f"Created a traditional deck with {len(traditional_deck)} cards.")
    if traditional_deck:
        print(f"First card (traditional): {traditional_deck[0]}")

    print("\n--- Testing Modern Theme ---")
    modern_deck = create_deck(theme="modern")
    print(f"Created a modern deck with {len(modern_deck)} cards.")
    if modern_deck:
        print(f"First card (modern): {modern_deck[0]}")
        # Verify a specific known filename change
        if modern_deck[0]['image_filename'] == "matsu_crane_modern.png":
            print("Modern theme correctly applied for matsu_crane.png.")
        else:
            print(f"Error: Modern theme INCORRECTLY applied. Expected 'matsu_crane_modern.png', got {modern_deck[0]['image_filename']}")


    print("\n--- Testing Invalid Theme (fallback to traditional) ---")
    invalid_theme_deck = create_deck(theme="nonexistent_theme")
    print(f"Created an invalid theme deck with {len(invalid_theme_deck)} cards.")
    if invalid_theme_deck:
        print(f"First card (invalid theme): {invalid_theme_deck[0]}")
        if invalid_theme_deck[0]['image_filename'] == "matsu_crane.png":
            print("Fallback to traditional theme correctly applied.")
        else:
            print(f"Error: Fallback to traditional theme FAILED. Expected 'matsu_crane.png', got {invalid_theme_deck[0]['image_filename']}")


    # Original shuffle and deal example (using traditional deck)
    print("\n--- Testing Shuffle and Deal (with traditional deck) ---")
    shuffle_deck(traditional_deck)
    print("Traditional deck shuffled.")
    
    try:
        p1_hand, p2_hand, field = deal_cards_koi_koi(traditional_deck)
        print(f"Player 1 Hand ({len(p1_hand)} cards).") # Don't print all cards for brevity
        print(f"Player 2 Hand ({len(p2_hand)} cards).")
        print(f"Field Cards ({len(field)} cards).")
        print(f"Remaining deck ({len(traditional_deck)} cards).") # Should be 24
    except ValueError as e:
        print(f"Error during dealing: {e}")
