import random
from collections import deque

# Constants: Define face card rules and card properties
FACE_CARDS = {'J': 1, 'Q': 2, 'K': 3, 'A': 4}  # Face cards require opponent to play additional cards
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # Card ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']  # Card suits

# Create a standard deck of 52 cards
def create_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]

# Check if a slap can be made based on the pile of cards
# Slap Rules: https://bicyclecards.com/how-to-play/egyptian-rat-screw/#rules
def can_slap(pile):
    # Check for doubles: two cards of the same rank in a row
    if len(pile) >= 2 and pile[-1][0] == pile[-2][0]:
        return True
    # Check for sandwiches: two cards of the same rank separated by one different card
    if len(pile) >= 3 and pile[-1][0] == pile[-3][0]:
        return True
    return False

# Main game function
def play_game():
    deck = create_deck()  # Generate a fresh deck
    random.shuffle(deck)  # Shuffle deck randomly

    # Ask user for number of human players
    num_humans = int(input("Enter the number of human players (1-3): "))
    human_names = []
    for i in range(num_humans):
        name = input(f"Enter name for Player {i+1}: ")
        human_names.append(name)

    # Assign CPU player
    player_names = human_names + ["CPU Player"]
    num_players = len(player_names)

    # Distribute deck among players
    hands = [deque() for _ in range(num_players)]
    for idx, card in enumerate(deck):
        hands[idx % num_players].append(card)

    pile = deque()  # Cards played in the middle
    turn = 0

    print("\nGame Start!")
    for idx, name in enumerate(player_names):
        print(f"Player {idx + 1}: {name}")

    # Main game loop: continue as long as all players have cards
    while all(hands):
        current_player = hands[turn % num_players]
        current_name = player_names[turn % num_players]

        if not current_player:
            turn += 1
            continue

        if current_name != "CPU Player":
            input(f"{current_name}, press Enter to play your next card...")

        # Draw card from current player's hand
        card_played = current_player.popleft()
        pile.append(card_played)
        print(f"{current_name} plays: {card_played[0]} of {card_played[1]}")

        # Check if anyone can slap the pile
        if can_slap(pile):
            slapped = False
            for idx, name in enumerate(player_names):
                if name != "CPU Player":
                    slap = input(f"{name}, type 'slap' to take the pile, or press Enter to skip: ")
                    if slap.lower() == 'slap':
                        print(f"{name} slaps and takes the pile! ({len(pile)} cards)")
                        hands[idx].extend(pile)
                        pile.clear()
                        turn = idx  # Slap winner takes next turn
                        slapped = True
                        break

            if not slapped:
                cpu_decision = random.choice([True, False])
                if cpu_decision:
                    cpu_idx = player_names.index("CPU Player")
                    print(f"CPU Player slaps and takes the pile! ({len(pile)} cards)")
                    hands[cpu_idx].extend(pile)
                    pile.clear()
                    turn = cpu_idx
                    continue

        # Face-card challenge logic
        if card_played[0] in FACE_CARDS:
            penalty = FACE_CARDS[card_played[0]]
            successful = False
            next_player_idx = (turn + 1) % num_players

            # Opponent plays penalty cards
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
                print(f"{current_name} wins pile due to unsuccessful face-card challenge! ({len(pile)} cards)")
                current_player.extend(pile)
                pile.clear()

        turn += 1

    # Determine and announce the game winner
    winner_idx = hands.index(max(hands, key=len))
    print(f"{player_names[winner_idx]} wins the game!")

# Start the game
if __name__ == "__main__":
    play_game()
