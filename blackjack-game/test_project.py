import pytest
from project import create_deck, calculate_hand_value

def test_create_deck():
    """Test deck has 52 unique cards."""
    deck = create_deck()
    assert len(deck) == 52
    assert len(set(tuple(card.items()) for card in deck)) == 52  # Ensure uniqueness

def test_calculate_hand_value():
    """Test hand value calculations."""
    assert calculate_hand_value([{'rank': 'A', 'suit': 'Hearts'}, {'rank': 'K', 'suit': 'Spades'}]) == 21
    assert calculate_hand_value([{'rank': '2', 'suit': 'Diamonds'}, {'rank': '3', 'suit': 'Clubs'}]) == 5