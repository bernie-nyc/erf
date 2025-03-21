import random
from collections import deque, defaultdict

# Constants: Define rules for face cards and properties of a standard deck
FACE_CARDS = {'J': 1, 'Q': 2, 'K': 3, 'A': 4}  # Face cards trigger special play conditions
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # Standard card ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # Standard card suits

# Create a standard deck of 52 unique cards
def create_deck():
    # Combine each rank with each suit to form a full deck
    return [(rank, suit) for rank in RANKS for suit in SUITS]

# Function to check if current pile state allows a slap
# Slap rules: https://bicyclecards.com/how-to-play/egyptian-rat-screw/#rules
def can_slap(pile):
    # Doubles: Two identical cards played consecutively
    if len(pile) >= 2 and pile[-1][0] == pile[-2][0]:
        return True
    # Sandwiches: Two identical cards separated by a single different card
    if len(pile) >= 3 and pile[-1][0] == pile[-3][0]:
        return True
    return False

# Display ASCII art representing the winner's hand
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

# Main function controlling the game flow
def play_game():
    while True:
        # Prepare and shuffle the deck
        deck = create_deck()
        random.shuffle(deck)

        # Prompt for number of human players and collect their names
        num_humans = int(input("How many human players? (1-3): "))
        human_names = []
        for i in range(num_humans):
            name = input(f"Enter name for Player {i+1}: ")
            human_names.append(name)

        # Automatically add a CPU player
        player_names = human_names + ["CPU Player"]
        num_players = len(player_names)
        hands = [deque() for _ in range(num_players)]  # Each player's hand

        # Distribute shuffled cards among players
        for idx, card in enumerate(deck):
            hands[idx % num_players].append(card)

        pile = deque()  # Central pile of played cards
        turn = 0
        rounds_played = 0
        slap_counts = defaultdict(int)  # Tracks successful slaps per player
        pile_wins = defaultdict(int)  # Tracks piles won by each player

        print("\nGame Start!")
        for idx, name in enumerate(player_names):
            print(f"Player {idx + 1}: {name}")

        # Continue gameplay until only one player has cards remaining
        while sum(1 for hand in hands if hand) > 1:
            rounds_played += 1
            current_player = hands[turn % num_players]
            current_name = player_names[turn % num_players]

            if not current_player:
                turn += 1
                continue

            # Prompt human players before playing card
            if current_name != "CPU Player":
                input(f"{current_name}, press Enter to play your next card...")

            # Play card to the pile
            card_played = current_player.popleft()
            pile.append(card_played)

            # Check for slap opportunity
            if can_slap(pile):
                slapped = False
                for idx, name in enumerate(player_names):
                    if name != "CPU Player" and hands[idx]:
                        slap = input(f"{name}, type 'slap' to take the pile, or press Enter to skip: ")
                        if slap.lower() == 'slap':
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
                        slap_counts["CPU Player"] += 1
                        pile_wins["CPU Player"] += 1
                        hands[cpu_idx].extend(pile)
                        pile.clear()
                        turn = cpu_idx
                        continue

            # Face-card challenge logic
            if card_played[0] in FACE_CARDS:
                penalty = FACE_CARDS[card_played[0]]
                successful = False
                next_player_idx = (turn + 1) % num_players

                while penalty > 0 and hands[next_player_idx]:
                    penalty_card = hands[next_player_idx].popleft()
                    pile.append(penalty_card)

                    if penalty_card[0] in FACE_CARDS:
                        turn = next_player_idx
                        successful = True
                        break

                    penalty -= 1

                if not successful:
                    pile_wins[current_name] += 1
                    current_player.extend(pile)
                    pile.clear()

            turn += 1

        # Determine winner based on who has remaining cards
        winner_idx = hands.index(max(hands, key=len))
        winner_name = player_names[winner_idx]

        # Display results
        display_winning_hand(winner_name)

        # Game statistics overview
        print("\n*** Game Statistics ***")
        print(f"Total rounds played: {rounds_played}")
        total_slaps = sum(slap_counts.values())
        for name in player_names:
            slap_percentage = (slap_counts[name] / total_slaps * 100) if total_slaps else 0
            pile_percentage = (pile_wins[name] / sum(pile_wins.values()) * 100) if pile_wins else 0
            print(f"{name}: {slap_counts[name]} slaps ({slap_percentage:.1f}%), {pile_wins[name]} piles won ({pile_percentage:.1f}%)")

        # Prompt for new round or exit
        play_again = input("\nWould you like to play another round? (yes/no): ")
        if play_again.lower() != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
