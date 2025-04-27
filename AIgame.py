import random
import time
import sys

# Fancy color printing for console (works in most terminals)
class Colors:
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

# Initialize variables
deck = []
player_hand = []
ai_hand = []
player_played_tiles = []
difficulty = "easy"

def print_separator():
    print("\n" + "-" * 40 + "\n")

def tile_string(number):
    return f"[ {number} ]"

def shuffle(deck):
    random.shuffle(deck)

def draw_tile():
    if deck:
        return deck.pop(0)
    return None

def show_hand(hand, title):
    print(f"\n{title}:")
    for idx, tile in enumerate(hand):
        print(f"[{idx}] {tile_string(tile)}", end='  ')
    print()

def is_valid_selection(first, second, hand):
    return 0 <= first < len(hand) and 0 <= second < len(hand) and first != second

def remove_tiles(hand, idx1, idx2):
    for idx in sorted([idx1, idx2], reverse=True):
        del hand[idx]

def initialize_game():
    global deck, player_hand, ai_hand
    deck = [i for i in range(1, 10)] * 2  # 1-9 tiles, two of each
    shuffle(deck)
    player_hand = [draw_tile() for _ in range(5)]
    ai_hand = [draw_tile() for _ in range(5)]

def choose_difficulty():
    global difficulty
    print_separator()
    print("🎯 Choose AI Difficulty: (easy / hard)")
    diff = input("> ").lower()
    if diff == "hard":
        difficulty = "hard"
    else:
        difficulty = "easy"

def can_match(hand):
    for i in range(len(hand)):
        for j in range(i + 1, len(hand)):
            if hand[i] == hand[j]:
                return True
    return False

def player_turn():
    global player_hand
    print_separator()
    print(f"{Colors.CYAN}🎮 YOUR TURN{Colors.RESET}")
    show_hand(player_hand, "Your Hand")

    if not can_match(player_hand):
        print(f"\n⚠️ No possible matches. You must draw a tile.")
        draw_tile_for_player()
        return

    try:
        selection = input("\n👉 Select two tiles to match (indexes separated by space): ").split()
        first, second = int(selection[0]), int(selection[1])

        if is_valid_selection(first, second, player_hand):
            if player_hand[first] == player_hand[second]:
                print(f"\n{Colors.GREEN}✅ Matched!{Colors.RESET}")
                played_tile = player_hand[first]
                remove_tiles(player_hand, first, second)
                player_played_tiles.append(played_tile)
            else:
                print(f"\n{Colors.RED}❌ Not a match!{Colors.RESET}")
        else:
            print("\n⚠️ Invalid selection. Turn skipped.")
    except (ValueError, IndexError):
        print("\n⚠️ Invalid input. Turn skipped.")

def draw_tile_for_player():
    new_tile = draw_tile()
    if new_tile is not None:
        print(f"{Colors.CYAN}🎮 You drew a tile: {tile_string(new_tile)}{Colors.RESET}")
        player_hand.append(new_tile)
    else:
        print(f"{Colors.RED}💀 No tiles left in the deck!{Colors.RESET}")
        print(f"{Colors.RED}💀 You cannot draw anymore. Your turn is skipped.{Colors.RESET}")

def ai_turn():
    global ai_hand
    print_separator()
    print(f"{Colors.MAGENTA}🤖 AI'S TURN{Colors.RESET}")
    time.sleep(1)

    if difficulty == "hard":
        ai_make_smart_decision()
    else:
        ai_random_decision()

    ai_hand = [tile for tile in ai_hand if tile is not None]
    ai_hand.sort()

def ai_make_smart_decision():
    global ai_hand
    """AI on hard difficulty will make smarter matching decisions."""
    possible_matches = []
    
    # Look for pairs in AI's hand
    for i in range(len(ai_hand)):
        for j in range(i + 1, len(ai_hand)):
            if ai_hand[i] == ai_hand[j]:
                possible_matches.append((i, j))

    if possible_matches:
        i, j = possible_matches[0]
        print(f"🤖 AI matched {tile_string(ai_hand[i])} and {tile_string(ai_hand[j])}!")
        remove_tiles(ai_hand, i, j)
    else:
        draw_tile_for_ai()

def ai_random_decision():
    global ai_hand
    """AI on easy difficulty will randomly match or draw tiles."""
    if can_match(ai_hand):
        for i in range(len(ai_hand)):
            for j in range(i + 1, len(ai_hand)):
                if ai_hand[i] == ai_hand[j]:
                    print(f"🤖 AI matched {tile_string(ai_hand[i])} and {tile_string(ai_hand[j])}!")
                    remove_tiles(ai_hand, i, j)
                    return
    else:
        draw_tile_for_ai()

def draw_tile_for_ai():
    new_tile = draw_tile()
    if new_tile is not None:
        print(f"🤖 AI drew a tile: {tile_string(new_tile)}")
        ai_hand.append(new_tile)
    else:
        print(f"{Colors.RED}💀 AI cannot draw, deck is empty!{Colors.RESET}")
        print(f"{Colors.RED}🤖 AI WINS!{Colors.RESET}")
        sys.exit()

def play_game():
    while True:
        # Player's turn
        player_turn()
        if not player_hand:
            print_separator()
            print(f"{Colors.GREEN}🏆 YOU WIN!{Colors.RESET}")
            break

        # AI's turn
        time.sleep(1)
        ai_turn()
        if not ai_hand:
            print_separator()
            print(f"{Colors.RED}💀 AI WINS!{Colors.RESET}")
            break

        time.sleep(2)

def main():
    initialize_game()
    choose_difficulty()
    play_game()
    print("\n🎮 Game Over. Press Enter to exit.")
    input()

if __name__ == "__main__":
    main()
