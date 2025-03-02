from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Card deck (values and image paths)
suits = ['hearts', 'diamonds', 'clubs', 'spades']
values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

deck = [{'value': v, 'suit': s, 'img': f"/static/cards/{v}_of_{s}.svg"} for v in values for s in suits]

player_hand = []
dealer_hand = []
game_over = False

def calculate_hand(hand):
    """Calculate total hand value considering Aces as 1 or 11."""
    total = sum(values[card['value']] for card in hand)
    aces = sum(1 for card in hand if card['value'] == 'A')

    while total > 21 and aces:
        total -= 10  # Convert Ace from 11 to 1
        aces -= 1

    return total

def deal_card(hand):
    """Draws a card from the deck."""
    card = random.choice(deck)
    deck.remove(card)
    hand.append(card)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game by resetting hands."""
    global player_hand, dealer_hand, game_over
    player_hand = []
    dealer_hand = []
    game_over = False

    # Deal two cards each
    for _ in range(2):
        deal_card(player_hand)
        deal_card(dealer_hand)

    return jsonify({'player': player_hand, 'dealer': [dealer_hand[0]], 'hidden': True})

@app.route('/hit', methods=['POST'])
def hit():
    """Player draws a card."""
    global game_over
    if not game_over:
        deal_card(player_hand)

        if calculate_hand(player_hand) > 21:
            game_over = True
            return jsonify({'player': player_hand, 'dealer': dealer_hand, 'result': 'bust'})

    return jsonify({'player': player_hand, 'dealer': [dealer_hand[0]]})

@app.route('/stand', methods=['POST'])
def stand():
    """Dealer reveals cards and plays."""
    global game_over
    game_over = True

    while calculate_hand(dealer_hand) < 17:
        deal_card(dealer_hand)

    player_score = calculate_hand(player_hand)
    dealer_score = calculate_hand(dealer_hand)

    if dealer_score > 21 or player_score > dealer_score:
        result = 'win'
    elif player_score < dealer_score:
        result = 'lose'
    else:
        result = 'draw'

    return jsonify({'player': player_hand, 'dealer': dealer_hand, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)