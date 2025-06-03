from .cards import create_deck, shuffle_deck, deal_cards_koi_koi
from .yaku import get_formed_yaku # New import

class KoiKoiGame:
    def __init__(self, player1_id="Player 1", player2_id="Player 2"):
        self.player_ids = {1: player1_id, 2: player2_id}
        self.deck = create_deck()
        shuffle_deck(self.deck)

        player1_hand, player2_hand, self.field_cards = deal_cards_koi_koi(self.deck)
        self.player_hands = {1: player1_hand, 2: player2_hand}
        
        self.captured_cards = {
            1: [],  # Player 1's captured cards
            2: []   # Player 2's captured cards
        }
        
        self.current_player_num = 1
        self.round_banked_score = {1: 0, 2: 0} # Score banked by calling Koi-Koi
        self.has_called_koi_koi = {1: False, 2: False}
        
        self.yaku_formed_this_turn = {1: [], 2: []} # Stores yaku objects for current player's active turn
        self.points_this_turn = {1: 0, 2: 0} # Points from yaku formed in current active part of turn

        self.game_over_for_round = False # Indicates current round is over
        self.round_winner = None
        self.round_winning_score = 0
        self.last_action_description = ""
        self.player_must_decide_koi_koi = False # Flag if player needs to make a choice

    def _set_last_action(self, description):
        print(description) # For debugging
        self.last_action_description = description

    def switch_player(self):
        self.current_player_num = 2 if self.current_player_num == 1 else 1
        self.yaku_formed_this_turn[self.current_player_num] = [] # Clear for the new player's turn part
        self.points_this_turn[self.current_player_num] = 0
        self._set_last_action(f"Turn switched to {self.player_ids[self.current_player_num]}.")

    def get_player_hand(self, player_num):
        return self.player_hands[player_num]

    def get_player_captured_pile(self, player_num):
        return self.captured_cards[player_num]

    def get_field_cards(self):
        return self.field_cards

    def _find_matches_on_field(self, card_to_match, field_cards):
        """Finds cards on the field that match the month of the given card."""
        matches = []
        # Iterate with index to handle cases where multiple cards of the same month are on field
        for i, field_card in enumerate(field_cards):
            if field_card['month'] == card_to_match['month']:
                matches.append({"card": field_card, "index": i})
        return matches

    def _capture_cards(self, player_num, played_or_drawn_card, matched_field_card_info):
        """Helper to move played/drawn and matched cards to player's captured pile."""
        self.captured_cards[player_num].append(played_or_drawn_card)
        
        field_card_to_capture = self.field_cards.pop(matched_field_card_info['index'])
        self.captured_cards[player_num].append(field_card_to_capture)
        
        self._set_last_action(
            f"{self.player_ids[player_num]} captured {played_or_drawn_card['name']} with {field_card_to_capture['name']}."
        )
        self._handle_capture_outcome(player_num)

    def _add_card_to_field(self, card):
        """Helper to add a card to the field when no match is made."""
        self.field_cards.append(card)
        self._set_last_action(f"{card['name']} was added to the field.")
        # No yaku check here as no capture occurred.

    def _handle_capture_outcome(self, player_num):
        """Called after any capture to check for yaku and set decision state."""
        newly_formed_yaku, points = self.check_yaku(player_num)
        
        if newly_formed_yaku:
            # Check if these new yaku offer more points than already banked + current turn yaku
            # This logic is important if a player forms a small yaku, calls koi-koi, then forms a bigger one.
            # The points for *this specific turn segment* are `points`.
            # `self.round_banked_score` holds points from previous koi-koi calls in this round.
            
            self.yaku_formed_this_turn[player_num] = newly_formed_yaku
            self.points_this_turn[player_num] = points # Total points from all yaku formed NOW

            self._set_last_action(
                f"{self.player_ids[player_num]} formed: " + 
                f"{', '.join([y['name'] for y in newly_formed_yaku])} for a total of {points} points this turn."
            )
            self.player_must_decide_koi_koi = True # Player must now decide Koi-Koi or Shojo
        # If no yaku, player_must_decide_koi_koi remains False, game proceeds.

    def play_card_from_hand(self, player_num, hand_card_index, chosen_field_card_match_index=None):
        if player_num != self.current_player_num:
            self._set_last_action("Error: Not this player's turn.")
            return {"success": False, "action": "Error: Not player's turn", "needs_koi_koi_decision": self.player_must_decide_koi_koi}
        if self.player_must_decide_koi_koi:
            self._set_last_action("Error: Player must decide Koi-Koi/Shojo before playing another card.")
            return {"success": False, "action": "Error: Must decide Koi-Koi/Shojo", "needs_koi_koi_decision": True}
        if not (0 <= hand_card_index < len(self.player_hands[player_num])):
            self._set_last_action("Error: Invalid card index in hand.")
            return {"success": False, "action": "Error: Invalid card index", "needs_koi_koi_decision": self.player_must_decide_koi_koi}

        played_card = self.player_hands[player_num].pop(hand_card_index)
        self._set_last_action(f"{self.player_ids[player_num]} plays {played_card['name']} from hand.")
        
        matches_on_field = self._find_matches_on_field(played_card, self.field_cards)
        action_taken_this_step = False

        if not matches_on_field:
            self._add_card_to_field(played_card)
            action_taken_this_step = True
        elif len(matches_on_field) == 1:
            self._capture_cards(player_num, played_card, matches_on_field[0])
            action_taken_this_step = True
        elif len(matches_on_field) >= 2: # Covers 2 or 3 matches
            # If 3 cards on field, player chooses one to match with played_card. The other 2 remain.
            # If 2 cards on field, player chooses one. The other 1 remains.
            # If player plays a card and there are 3 of that month on field (total 4), it's a sweep.
            if len(self.field_cards) >= 3 and sum(1 for fc in self.field_cards if fc['month'] == played_card['month']) == 3:
                 # This is the "played card matches 3 on field" scenario, resulting in a sweep of all 4.
                self._set_last_action(f"{self.player_ids[player_num]} plays {played_card['name']} to complete a month sweep!")
                self.captured_cards[player_num].append(played_card) # Capture the played card
                # Capture all field cards of that month
                indices_to_remove = sorted([match['index'] for match in matches_on_field], reverse=True)
                for index in indices_to_remove:
                    captured_field_card = self.field_cards.pop(index)
                    self.captured_cards[player_num].append(captured_field_card)
                self._handle_capture_outcome(player_num) # Check yaku after sweep
                action_taken_this_step = True
            else: # Standard case: 2 matches on field, player chooses one.
                if chosen_field_card_match_index is None or not (0 <= chosen_field_card_match_index < len(matches_on_field)):
                    # Default to first match if no valid choice, or signal need for choice
                    self._set_last_action(f"Multiple matches for {played_card['name']}. Auto-choosing first available match (index {matches_on_field[0]['index']}).")
                    self._capture_cards(player_num, played_card, matches_on_field[0])
                    action_taken_this_step = True
                else:
                    self._capture_cards(player_num, played_card, matches_on_field[chosen_field_card_match_index])
                    action_taken_this_step = True
        
        if not action_taken_this_step: 
            # Should not be reached if logic is correct
            self._add_card_to_field(played_card) # Failsafe: add to field if no other action taken
            self._set_last_action("Warning: play_card_from_hand reached failsafe. Card added to field.")

        return {"success": True, "action": "played_from_hand", "needs_koi_koi_decision": self.player_must_decide_koi_koi}

    def draw_card_from_deck_and_play(self, player_num, chosen_field_card_match_index=None):
        if player_num != self.current_player_num:
             return {"success": False, "action": "Error: Not player's turn", "needs_koi_koi_decision": self.player_must_decide_koi_koi}
        if self.player_must_decide_koi_koi:
            return {"success": False, "action": "Error: Must decide Koi-Koi/Shojo", "needs_koi_koi_decision": True}
        if not self.deck:
            self._set_last_action("Deck is empty. Cannot draw.")
            # Check for end of round if hands are also empty or specific conditions met
            if not self.player_hands[1] and not self.player_hands[2]:
                self._set_last_action("Deck and hands are empty. Round ends.")
                self.game_over_for_round = True
                # Scoring for round end due to exhaustion needs specific rules (e.g., oya-gachi, no winner)
            self.switch_player() # Or end round. For now, just switch.
            return {"success": False, "action": "Error: Deck empty", "needs_koi_koi_decision": self.player_must_decide_koi_koi}

        drawn_card = self.deck.pop()
        self._set_last_action(f"{self.player_ids[player_num]} draws {drawn_card['name']} from deck.")
        
        matches_on_field = self._find_matches_on_field(drawn_card, self.field_cards)
        action_taken_this_step = False

        if not matches_on_field:
            self._add_card_to_field(drawn_card)
            action_taken_this_step = True
        elif len(matches_on_field) == 1:
            self._capture_cards(player_num, drawn_card, matches_on_field[0])
            action_taken_this_step = True
        elif len(matches_on_field) >= 2: # Drawn card matches 2 or 3 on field
            # If drawn card matches 3 on field (total 4 of same month), it's a sweep
            if len(matches_on_field) == 3:
                self._set_last_action(f"{self.player_ids[player_num]} draws {drawn_card['name']} to complete a month sweep!")
                self.captured_cards[player_num].append(drawn_card)
                indices_to_remove = sorted([match['index'] for match in matches_on_field], reverse=True)
                for index in indices_to_remove:
                    captured_field_card = self.field_cards.pop(index)
                    self.captured_cards[player_num].append(captured_field_card)
                self._handle_capture_outcome(player_num)
                action_taken_this_step = True
            else: # Standard 2 matches, player choice needed (or default)
                if chosen_field_card_match_index is None or not (0 <= chosen_field_card_match_index < len(matches_on_field)):
                    self._set_last_action(f"Drawn card {drawn_card['name']} matches multiple. Auto-choosing first available match.")
                    self._capture_cards(player_num, drawn_card, matches_on_field[0])
                    action_taken_this_step = True
                else:
                    self._capture_cards(player_num, drawn_card, matches_on_field[chosen_field_card_match_index])
                    action_taken_this_step = True
        
        if not action_taken_this_step:
            self._add_card_to_field(drawn_card) # Failsafe
            self._set_last_action("Warning: draw_card_from_deck_and_play reached failsafe. Card added to field.")

        # After drawing and playing, if no decision is pending, the turn automatically ends.
        if not self.player_must_decide_koi_koi:
            self.switch_player()
            return {"success": True, "action": "drew_and_played_no_yaku_turn_ends", "needs_koi_koi_decision": False}
        else:
            # Player formed yaku from draw, must decide. Turn does not auto-switch.
            return {"success": True, "action": "drew_and_played_yaku_decision_pending", "needs_koi_koi_decision": True}

    def check_yaku(self, player_num):
        """Checks for yaku and returns list of yaku objects and total points."""
        formed_yaku, total_points = get_formed_yaku(self.captured_cards[player_num])
        return formed_yaku, total_points

    def decide_koi_koi_or_shojo(self, player_num, call_koi_koi):
        if player_num != self.current_player_num or not self.player_must_decide_koi_koi:
            self._set_last_action("Error: Not player's turn to decide or no decision pending.")
            return {"success": False, "message": "Cannot decide now."}

        self.player_must_decide_koi_koi = False # Decision is being made

        # points_this_turn already holds the total from all yaku formed in the current capture sequence
        current_yaku_total_points = self.points_this_turn[player_num]
        
        if call_koi_koi:
            self.has_called_koi_koi[player_num] = True
            self.round_banked_score[player_num] += current_yaku_total_points
            
            # Koi-Koi rule: if opponent called Koi-Koi and you form a yaku and call Koi-Koi again,
            # the points might be further modified (e.g. score doubles again). This is an advanced rule.
            # For now, just add to banked score.
            
            self._set_last_action(
                f"{self.player_ids[player_num]} calls KOI-KOI! Banked {current_yaku_total_points} points from this yaku. " +
                f"Total banked this round: {self.round_banked_score[player_num]}."
            )
            # Reset turn-specific yaku trackers, but not round_banked_score
            self.yaku_formed_this_turn[player_num] = [] 
            self.points_this_turn[player_num] = 0
            
            self.switch_player()
            return {"success": True, "action": "koi_koi_called", "score_banked_this_turn": current_yaku_total_points, "total_round_banked_score": self.round_banked_score[player_num]}
        else: # Player chooses to Shojo (Stop)
            final_round_score = self.round_banked_score[player_num] + current_yaku_total_points
            
            opponent_player_num = 2 if player_num == 1 else 1
            if self.has_called_koi_koi[opponent_player_num]:
                final_round_score *= 2 # Opponent called Koi-Koi, current player wins, score doubled.
                self._set_last_action("Opponent had called Koi-Koi! Your score for this round is doubled.")

            # Additional rule: 7+ points yaku automatically doubles.
            # This rule varies. Some apply it always, some only if not Koi-Koi'd against.
            # Let's assume if final_round_score (before opponent Koi-Koi double) >= 7, it doubles.
            # This needs clarification or a specific rule set. For now, let's keep it simple:
            # Opponent Koi-Koi doubles. Yaku points are as defined.

            yaku_names_display = ', '.join([y['name'] for y in self.yaku_formed_this_turn[player_num]])
            self._set_last_action(
                f"{self.player_ids[player_num]} calls SHOJO! Wins round with yaku: ({yaku_names_display}) " +
                f"plus banked score of {self.round_banked_score[player_num]}. Total round score: {final_round_score} points."
            )
            self.game_over_for_round = True
            self.round_winner = player_num
            self.round_winning_score = final_round_score
            
            # Reset round-specific states for a potential next round
            self.round_banked_score = {1: 0, 2: 0}
            self.has_called_koi_koi = {1: False, 2: False}
            self.yaku_formed_this_turn = {1: [], 2: []}
            self.points_this_turn = {1: 0, 2: 0}
            
            return {"success": True, "action": "shojo_round_ends", "winner": player_num, "final_score": final_round_score, "yaku_formed": yaku_names_display}
       
    def start_new_round(self):
        self.deck = create_deck()
        shuffle_deck(self.deck)
        player1_hand, player2_hand, self.field_cards = deal_cards_koi_koi(self.deck)
        self.player_hands = {1: player1_hand, 2: player2_hand}
        self.captured_cards = {1: [], 2: []}
        # self.current_player_num = ... (decide who starts next round, e.g., winner or alternate)
        # For now, player 1 starts or current player (if implementing alternating oya)
        self.round_banked_score = {1: 0, 2: 0}
        self.has_called_koi_koi = {1: False, 2: False}
        self.yaku_formed_this_turn = {1: [], 2: []}
        self.points_this_turn = {1: 0, 2: 0}
        self.game_over_for_round = False
        self.round_winner = None
        self.round_winning_score = 0
        self.player_must_decide_koi_koi = False
        self._set_last_action("New round started.")
        print(f"Player 1 Hand: {[card['name'] for card in self.get_player_hand(1)]}")
        print(f"Player 2 Hand: {[card['name'] for card in self.get_player_hand(2)]}")
        print(f"Field: {[card['name'] for card in self.get_field_cards()]}")


if __name__ == '__main__':
    game = KoiKoiGame("Alice", "Bob")
    game.start_new_round() # Initialize hands and field for the test

    # Simulate game flow for a few turns or until round ends
    MAX_TURNS = 16 # Each player plays from hand then draws = 1 turn for them. 8 such pairs approx.
    turns_played = 0

    while not game.game_over_for_round and turns_played < MAX_TURNS:
        current_p_id = game.current_player_num
        print(f"\n--- {game.player_ids[current_p_id]}'s Turn (Turn {turns_played // 2 + 1}) ---")
        print(f"Hand: {[c['name'] for c in game.get_player_hand(current_p_id)]}")
        print(f"Field: {[c['name'] for c in game.get_field_cards()]}")
        print(f"Captured P1: {[c['name'] for c in game.get_player_captured_pile(1)]}")
        print(f"Captured P2: {[c['name'] for c in game.get_player_captured_pile(2)]}")


        # 1. Play card from hand
        if game.get_player_hand(current_p_id):
            # Simple strategy: try to play the first card.
            # In a real game, player would choose card and match.
            # For testing, we need a way to choose a field card if multiple matches.
            # play_card_from_hand will auto-pick first match if chosen_field_card_match_index is None.
            play_res = game.play_card_from_hand(current_p_id, 0) 
            print(f"Play from hand result: {play_res}")

            if game.player_must_decide_koi_koi:
                print(f"{game.player_ids[current_p_id]} must decide after playing from hand.")
                # Test: Auto-Koi if total points (banked + current yaku) < 7, else Shojo
                total_potential_score = game.round_banked_score[current_p_id] + game.points_this_turn[current_p_id]
                will_koi = total_potential_score < 7 
                print(f"Auto-deciding: KoiKoi={will_koi} (Potential score: {total_potential_score})")
                decision_res = game.decide_koi_koi_or_shojo(current_p_id, will_koi)
                print(f"Decision result: {decision_res}")
                if game.game_over_for_round: break
                turns_played +=1 # Counts as a turn segment
                continue # Player's turn ends after decision (either Shojo or Koi-Koi switches player)
        else:
            print(f"{game.player_ids[current_p_id]} has no cards in hand.")
            # If hand is empty, player still draws.

        # 2. Draw card from deck (if turn didn't end/switch due to hand play decision)
        if not game.game_over_for_round and game.current_player_num == current_p_id: # Ensure player didn't switch
            if game.deck:
                draw_res = game.draw_card_from_deck_and_play(current_p_id)
                print(f"Draw from deck result: {draw_res}")

                if game.player_must_decide_koi_koi:
                    print(f"{game.player_ids[current_p_id]} must decide after drawing from deck.")
                    total_potential_score = game.round_banked_score[current_p_id] + game.points_this_turn[current_p_id]
                    will_koi = total_potential_score < 7
                    print(f"Auto-deciding: KoiKoi={will_koi} (Potential score: {total_potential_score})")
                    decision_res = game.decide_koi_koi_or_shojo(current_p_id, will_koi)
                    print(f"Decision result: {decision_res}")
                    if game.game_over_for_round: break 
                    # Turn already switched by KoiKoi or ended by Shojo
            else:
                print("Deck is empty. Attempting to switch player.")
                if not game.player_must_decide_koi_koi : # If no decision is pending
                    game.switch_player() 
                # If deck empty and hands empty, round should end.
                if not game.player_hands[1] and not game.player_hands[2] and not game.player_must_decide_koi_koi:
                    print("Deck and all hands are empty. Round ends (no winner by exhaustion in this test).")
                    game.game_over_for_round = True # Or specific exhaustion logic
                    break
        
        turns_played += 1
        if turns_played >= MAX_TURNS and not game.game_over_for_round:
            print("Max turns reached, round ends (no winner).")
            game.game_over_for_round = True # Or other logic for max turns

    if game.game_over_for_round:
        print(f"\n--- ROUND OVER ---")
        if game.round_winner:
            print(f"Winner: {game.player_ids[game.round_winner]}, Score: {game.round_winning_score}")
            print(f"Winning Yaku: {game.yaku_formed_this_turn.get(game.round_winner, 'N/A')}") # This might be empty if score was from bank
        else:
            print("Round ended with no winner (e.g., deck/hand exhaustion or max turns).")
    
    print("\n--- Final Game State (End of Test) ---")
    print(f"Player 1 Captured: {[card['name'] for card in game.get_player_captured_pile(1)]} ({len(game.get_player_captured_pile(1))} cards)")
    print(f"Player 2 Captured: {[card['name'] for card in game.get_player_captured_pile(2)]} ({len(game.get_player_captured_pile(2))} cards)")
    print(f"Field: {[card['name'] for card in game.get_field_cards()]} ({len(game.get_field_cards())} cards)")
    print(f"Deck: {len(game.deck)} cards remaining.")
