import random
from collections import deque, defaultdict

# Constants defining the special play conditions for face cards and properties of a standard deck
FACE_CARDS = {'J': 1, 'Q': 2, 'K': 3, 'A': 4}  # Number of penalty cards to play after a face card
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Generate a standard deck of 52 playing cards
def create_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]

# Check if the pile can be slapped based on the game's slap rules
# Rules Reference: https://bicyclecards.com/how-to-play/egyptian-rat-screw/#rules
def can_slap(pile):
    # Doubles: Two consecutive cards of the same rank
    if len(pile) >= 2 and pile[-1][0] == pile[-2][0]:
        return True
    # Sandwich: Two cards of the same rank separated by exactly one different card
    if len(pile) >= 3 and pile[-1][0] == pile[-3][0]:
        return True
    return False

# Display ASCII art celebrating the winning player
def display_winning_hand(winner_name):
    ascii_hand = """
    ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
    │░░░░░░░░░│ │░░░░░░░░░│ │░░░░░░░░░│ │░░░░░░░░░│ │░░░░░░░░░│
    │░░ WIN ░░│ │░░ WIN ░░│ │░░ WIN ░░│ │░░ WIN ░░│ │░░ WIN ░░│
    │░░░░░░░░░│ │░░░░░░░░░│ │░░░░░░░░░│ │░░░░░░░░░│ │░░░░░░░░░│
    └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
    """
    print(ascii_hand)
    print(f"*** {winner_name.upper()} WINS THE GAME! ***")

# Main gameplay function
# Controls the game loop, player interactions, and tracks statistics
def play_game():
    while True:
        deck = create_deck()
        random.shuffle(deck)

        num_humans = int(input("How many human players? (1-3): "))
        human_names = []
        for i in range(num_humans):
            name = input(f"Enter name for Player {i+1}: ")
            human_names.append(name)

        player_names = human_names + ["CPU Player"]
        num_players = len(player_names)
        hands = [deque() for _ in range(num_players)]

        for idx, card in enumerate(deck):
            hands[idx % num_players].append(card)

        pile = deque()
        turn = 0
        rounds_played = 0
        slap_counts = defaultdict(int)
        pile_wins = defaultdict(int)

        print("\nGame Start!")
        for idx, name in enumerate(player_names):
            print(f"Player {idx + 1}: {name}")

        # Gameplay continues until only one player has cards remaining
        while sum(1 for hand in hands if hand) > 1:
            rounds_played += 1
            current_player = hands[turn % num_players]
            current_name = player_names[turn % num_players]

            if not current_player:
                turn += 1
                continue

            # Prompt human players before playing
            if current_name != "CPU Player":
                input(f"{current_name}, press Enter to play your next card...")

            # Play the next card to the pile and display it
            card_played = current_player.popleft()
            pile.append(card_played)
            print(f"{current_name} plays: {card_played[0]} of {card_played[1]}")

            # Check if the pile is slap-able and handle slap interactions
            if can_slap(pile):
                slapped = False
                for idx, name in enumerate(player_names):
                    if name != "CPU Player" and hands[idx]:
                        slap = input(f"{name}, type 'slap' to take the pile, or press Enter to skip: ")
                        if slap.lower() == 'slap':
                            print(f"{name} slaps and takes the pile! ({len(pile)} cards)")
                            slap_counts[name] += 1
                            pile_wins[name] += 1
                            hands[idx].extend(pile)
                            pile.clear()
                            turn = idx
                            slapped = True
                            break

                if not slapped and hands[player_names.index("CPU Player")]:
                    if random.choice([True, False]):
                        cpu_idx = player_names.index("CPU Player")
                        print(f"CPU Player slaps and takes the pile! ({len(pile)} cards)")
                        slap_counts["CPU Player"] += 1
                        pile_wins["CPU Player"] += 1
                        hands[cpu_idx].extend(pile)
                        pile.clear()
                        turn = cpu_idx
                        continue

            # Face-card challenge: Opponent plays penalty cards
            if card_played[0] in FACE_CARDS:
                penalty = FACE_CARDS[card_played[0]]
                successful = False
                next_player_idx = (turn + 1) % num_players

                while penalty > 0 and hands[next_player_idx]:
                    penalty_card = hands[next_player_idx].popleft()
                    pile.append(penalty_card)
                    print(f"{player_names[next_player_idx]} penalty plays: {penalty_card[0]} of {penalty_card[1]}")

                    if penalty_card[0] in FACE_CARDS:
                        turn = next_player_idx
                        successful = True
                        break

                    penalty -= 1

                if not successful:
                    print(f"{current_name} wins the pile due to unsuccessful face-card challenge! ({len(pile)} cards)")
                    pile_wins[current_name] += 1
                    current_player.extend(pile)
                    pile.clear()

            turn += 1

        winner_idx = hands.index(max(hands, key=len))
        winner_name = player_names[winner_idx]

        display_winning_hand(winner_name)

        # Provide game statistics
        print("\n*** Game Statistics ***")
        print(f"Total rounds played: {rounds_played}")
        total_slaps = sum(slap_counts.values())
        for name in player_names:
            slap_percentage = (slap_counts[name] / total_slaps * 100) if total_slaps else 0
            pile_percentage = (pile_wins[name] / sum(pile_wins.values()) * 100) if pile_wins else 0
            print(f"{name}: {slap_counts[name]} slaps ({slap_percentage:.1f}%), {pile_wins[name]} piles won ({pile_percentage:.1f}%)")

        if input("\nPlay another round? (yes/no): ").lower() != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
