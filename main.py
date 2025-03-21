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

    # Split deck into two halves for player and computer
    human_player = deque(deck[:26])
    computer_player = deque(deck[26:])
    pile = deque()  # Cards played in the middle

    players = [human_player, computer_player]
    turn = 0  # 0 for human, 1 for computer

    print("Game Start! You are Player 1, and the computer is Player 2.")

    # Main game loop: continue as long as both players have cards
    while all(players):
        current_player = players[turn % 2]
        opponent_player = players[(turn + 1) % 2]

        # Check if current player has cards left
        if not current_player:
            break

        # Human player's turn
        if turn % 2 == 0:
            input("Press Enter to play your next card...")

        # Draw card from current player's hand
        card_played = current_player.popleft()
        pile.append(card_played)
        print(f"Player {turn % 2 + 1} plays: {card_played[0]} of {card_played[1]}")

        # Check if anyone can slap the pile
        if can_slap(pile):
            if turn % 2 == 0:
                slap = input("Slap opportunity! Type 'slap' to take the pile, or press Enter to skip: ")
                if slap.lower() == 'slap':
                    winner = 0
                else:
                    winner = 1
            else:
                winner = random.choice([0, 1])  # Computer randomly decides to slap

            print(f"Player {winner + 1} slaps and takes the pile! ({len(pile)} cards)")
            players[winner].extend(pile)
            pile.clear()
            turn = winner  # Player who won slap takes next turn
            continue

        # Face-card challenge logic
        if card_played[0] in FACE_CARDS:
            penalty = FACE_CARDS[card_played[0]]  # Number of cards opponent must play
            successful = False

            # Opponent plays penalty cards
            while penalty > 0 and opponent_player:
                penalty_card = opponent_player.popleft()
                pile.append(penalty_card)
                print(f"Player {(turn + 1) % 2 + 1} penalty plays: {penalty_card[0]} of {penalty_card[1]}")

                # If opponent plays a face card, challenge reverses
                if penalty_card[0] in FACE_CARDS:
                    turn += 1  # Opponent now challenges
                    successful = True
                    break

                penalty -= 1

            # If no face card played, challenger wins the pile
            if not successful:
                print(f"Player {turn % 2 + 1} wins pile due to unsuccessful face-card challenge! ({len(pile)} cards)")
                current_player.extend(pile)
                pile.clear()

        # Alternate turns
        turn += 1

    # Determine and announce the game winner
    winner = "1 (You)" if human_player else "2 (Computer)"
    print(f"Player {winner} wins the game!")

# Start the game
if __name__ == "__main__":
    play_game()
