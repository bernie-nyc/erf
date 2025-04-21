import random
from collections import deque, defaultdict

# Constants: These determine the special rules for face cards and list all card ranks and suits
FACE_CARDS = {'J': 1, 'Q': 2, 'K': 3, 'A': 4}  # Face cards trigger special "challenge" conditions
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

# Create a complete deck of 52 playing cards by pairing ranks with suits
def create_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]

# Determine if the current pile of cards can be slapped according to game rules
def can_slap(pile):
    # Rule 1: Two identical cards placed consecutively can be slapped
    if len(pile) >= 2 and pile[-1][0] == pile[-2][0]:
        return True
    # Rule 2: Two identical cards separated by exactly one different card can also be slapped
    if len(pile) >= 3 and pile[-1][0] == pile[-3][0]:
        return True
    # If neither rule applies, no slap is allowed
    return False

# Display celebratory ASCII art for the winning player
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

# Main function that runs the gameplay
def play_game():
    # Ask players how many humans will participate
    num_humans = int(input("How many human players? (1-3): "))
    human_names = []

    # Collect the names of the human players
    for i in range(num_humans):
        name = input(f"Enter name for Player {i+1}: ")
        human_names.append(name)

    # Include one computer-controlled player by default
    player_names = human_names + ["CPU Player"]
    num_players = len(player_names)

    # Main loop: play multiple rounds until players choose to stop
    while True:
        deck = create_deck()  # Create a fresh deck
        random.shuffle(deck)  # Shuffle the deck randomly

        # Deal the shuffled cards evenly among players
        hands = [deque() for _ in range(num_players)]
        for idx, card in enumerate(deck):
            hands[idx % num_players].append(card)

        pile = deque()  # Central pile of cards played
        turn = 0  # Player turn tracker
        rounds_played = 0  # Track total rounds played in this game
        slap_counts = defaultdict(int)  # Record the number of successful slaps per player
        pile_wins = defaultdict(int)  # Record how many piles each player wins

        print("\nGame Start!")
        for idx, name in enumerate(player_names):
            print(f"Player {idx + 1}: {name}")

        # Continue gameplay until only one player has cards left
        while sum(1 for hand in hands if hand) > 1:
            rounds_played += 1
            current_player = hands[turn % num_players]
            current_name = player_names[turn % num_players]

            # Skip any player who has run out of cards
            if not current_player:
                turn += 1
                continue

            # Human players must press Enter to play their card
            if current_name != "CPU Player":
                input(f"{current_name}, press Enter to play your next card...")

            # Current player places their top card onto the pile
            card_played = current_player.popleft()
            pile.append(card_played)
            print(f"{current_name} plays: {card_played[0]} of {card_played[1]}")

            # Check if the current pile state can be slapped
            if can_slap(pile):
                slapped = False
                # Humans get first chance to slap
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

                # CPU randomly decides whether to slap if humans don't
                if not slapped and hands[player_names.index("CPU Player")]:
                    cpu_decision = random.choice([True, False])
                    if cpu_decision:
                        cpu_idx = player_names.index("CPU Player")
                        print(f"CPU Player slaps and takes the pile! ({len(pile)} cards)")
                        slap_counts["CPU Player"] += 1
                        pile_wins["CPU Player"] += 1
                        hands[cpu_idx].extend(pile)
                        pile.clear()
                        turn = cpu_idx
                        continue

            # Special face-card challenge logic
            if card_played[0] in FACE_CARDS:
                penalty = FACE_CARDS[card_played[0]]  # Number of cards next player must play
                successful = False  # Track if the challenge succeeds
                next_player_idx = (turn + 1) % num_players

                # Next player attempts to counter with their own face card
                while penalty > 0 and hands[next_player_idx]:
                    penalty_card = hands[next_player_idx].popleft()
                    pile.append(penalty_card)
                    print(f"{player_names[next_player_idx]} penalty plays: {penalty_card[0]} of {penalty_card[1]}")

                    if penalty_card[0] in FACE_CARDS:
                        turn = next_player_idx  # Challenge passes to next player
                        successful = True
                        break

                    penalty -= 1

                # If the challenged player fails, challenger wins the pile
                if not successful:
                    print(f"{current_name} wins the pile due to unsuccessful face-card challenge! ({len(pile)} cards)")
                    pile_wins[current_name] += 1
                    current_player.extend(pile)
                    pile.clear()

            turn += 1  # Move to next player's turn

        # Identify and celebrate the winner of this round
        winner_idx = hands.index(max(hands, key=len))
        winner_name = player_names[winner_idx]
        display_winning_hand(winner_name)

        # Display detailed statistics after the round
        print("\n*** Game Statistics ***")
        print(f"Total rounds played: {rounds_played}")
        total_slaps = sum(slap_counts.values())
        for name in player_names:
            slap_percentage = (slap_counts[name] / total_slaps * 100) if total_slaps else 0
            pile_percentage = (pile_wins[name] / sum(pile_wins.values()) * 100) if pile_wins else 0
            print(f"{name}: {slap_counts[name]} slaps ({slap_percentage:.1f}%), {pile_wins[name]} piles won ({pile_percentage:.1f}%)")

        # Ask players if they want another round
        if input("\nPlay another round? (yes/no): ").lower() != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    play_game()
