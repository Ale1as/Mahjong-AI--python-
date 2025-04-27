import random
import sys
import time
import tkinter as tk
from tkinter import messagebox

# Fancy colors
PLAYER_COLOR = '#00CED1'  # Cyan
AI_COLOR = '#DA70D6'      # Orchid
MATCH_COLOR = '#7CFC00'   # LawnGreen
MISMATCH_COLOR = '#FF6347' # Tomato
DEFAULT_TILE_COLOR = '#FFFFFF'

class TileMatchingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tile Matching Game 🎮")
        self.deck = []
        self.player_hand = []
        self.ai_hand = []
        self.player_tiles_buttons = []
        self.selected_tiles = []
        self.difficulty = 'easy'

        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text="Welcome to Tile Matching!", font=("Arial", 16))
        self.info_label.pack(pady=10)

        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)

        self.ai_frame = tk.Frame(self.root)
        self.ai_frame.pack(pady=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.draw_button = tk.Button(self.control_frame, text="Draw Tile", command=self.draw_tile_for_player)
        self.draw_button.grid(row=0, column=0, padx=10)

        self.start_button = tk.Button(self.control_frame, text="Choose Difficulty", command=self.choose_difficulty)
        self.start_button.grid(row=0, column=1, padx=10)

    def initialize_game(self):
        self.deck = [i for i in range(1, 10)] * 2
        random.shuffle(self.deck)
        self.player_hand = [self.draw_tile() for _ in range(5)]
        self.ai_hand = [self.draw_tile() for _ in range(5)]
        self.update_display()

    def draw_tile(self):
        return self.deck.pop(0) if self.deck else None

    def update_display(self):
        # Clear player tiles
        for btn in self.player_tiles_buttons:
            btn.destroy()
        self.player_tiles_buttons = []

        for idx, tile in enumerate(self.player_hand):
            btn = tk.Button(self.player_frame, text=f"{tile}", font=("Arial", 18), width=4, height=2,
                            bg=DEFAULT_TILE_COLOR, command=lambda idx=idx: self.select_tile(idx))
            btn.grid(row=0, column=idx, padx=5)
            self.player_tiles_buttons.append(btn)

        # Show AI hand (hidden)
        for widget in self.ai_frame.winfo_children():
            widget.destroy()

        for idx, tile in enumerate(self.ai_hand):
            lbl = tk.Label(self.ai_frame, text="[ ? ]", font=("Arial", 18), width=4, height=2, bg=AI_COLOR)
            lbl.grid(row=0, column=idx, padx=5)

    def select_tile(self, idx):
        if idx in self.selected_tiles:
            self.selected_tiles.remove(idx)
            self.player_tiles_buttons[idx].config(bg=DEFAULT_TILE_COLOR)
        else:
            self.selected_tiles.append(idx)
            self.player_tiles_buttons[idx].config(bg=PLAYER_COLOR)

        if len(self.selected_tiles) == 2:
            self.root.after(500, self.check_match)

    def check_match(self):
        idx1, idx2 = self.selected_tiles
        if self.player_hand[idx1] == self.player_hand[idx2]:
            self.info_label.config(text="✅ You made a match!")
            self.flash_tiles(MATCH_COLOR)
            self.root.after(800, self.remove_tiles)
        else:
            self.info_label.config(text="❌ Not a match!")
            self.flash_tiles(MISMATCH_COLOR)
            self.root.after(800, self.reset_selection)

    def flash_tiles(self, color):
        for idx in self.selected_tiles:
            self.player_tiles_buttons[idx].config(bg=color)

    def remove_tiles(self):
        idx1, idx2 = sorted(self.selected_tiles, reverse=True)
        del self.player_hand[idx1]
        del self.player_hand[idx2]
        self.selected_tiles.clear()
        self.update_display()
        self.check_game_over()
        self.root.after(1000, self.ai_turn)

    def reset_selection(self):
        for idx in self.selected_tiles:
            self.player_tiles_buttons[idx].config(bg=DEFAULT_TILE_COLOR)
        self.selected_tiles.clear()

    def draw_tile_for_player(self):
        if not self.can_match(self.player_hand):
            new_tile = self.draw_tile()
            if new_tile is not None:
                self.player_hand.append(new_tile)
                self.update_display()
                self.info_label.config(text=f"🎯 Drew a {new_tile}!")
            else:
                self.info_label.config(text="❗ Deck empty, can't draw!")
            self.root.after(1000, self.ai_turn)
        else:
            self.info_label.config(text="❗ You can still match, no draw allowed!")

    def choose_difficulty(self):
        answer = messagebox.askquestion("Difficulty", "Play on Hard mode?")
        self.difficulty = 'hard' if answer == 'yes' else 'easy'
        self.info_label.config(text=f"Difficulty set to {self.difficulty.upper()}.")

    def ai_turn(self):
        self.info_label.config(text="🤖 AI's Turn...")
        self.root.update()
        time.sleep(1)

        if self.difficulty == 'hard':
            self.ai_make_smart_decision()
        else:
            self.ai_random_decision()

        self.check_game_over()

    def ai_make_smart_decision(self):
        possible_matches = []
        for i in range(len(self.ai_hand)):
            for j in range(i + 1, len(self.ai_hand)):
                if self.ai_hand[i] == self.ai_hand[j]:
                    possible_matches.append((i, j))

        if possible_matches:
            i, j = possible_matches[0]
            del self.ai_hand[j]
            del self.ai_hand[i]
            self.info_label.config(text="🤖 AI matched smartly!")
        else:
            self.ai_draw_tile()

        self.update_display()

    def ai_random_decision(self):
        if self.can_match(self.ai_hand):
            for i in range(len(self.ai_hand)):
                for j in range(i + 1, len(self.ai_hand)):
                    if self.ai_hand[i] == self.ai_hand[j]:
                        del self.ai_hand[j]
                        del self.ai_hand[i]
                        self.info_label.config(text="🤖 AI matched randomly!")
                        self.update_display()
                        return
        self.ai_draw_tile()
        self.update_display()

    def ai_draw_tile(self):
        new_tile = self.draw_tile()
        if new_tile:
            self.ai_hand.append(new_tile)
            self.info_label.config(text=f"🤖 AI drew a tile.")
        else:
            self.info_label.config(text=f"🤖 Deck empty for AI!")

    def can_match(self, hand):
        return any(hand[i] == hand[j] for i in range(len(hand)) for j in range(i+1, len(hand)))

    def check_game_over(self):
        if not self.player_hand:
            self.end_game("🏆 YOU WIN!")
        elif not self.ai_hand:
            self.end_game("💀 AI WINS!")
        elif not self.deck and not self.can_match(self.player_hand) and not self.can_match(self.ai_hand):
            self.sudden_death()

    def sudden_death(self):
        self.info_label.config(text="⚡ Sudden Death Mode Activated!")
        self.root.update()
        time.sleep(1.5)

        while True:
            if not self.player_hand or not self.ai_hand:
                break

            player_tile = random.choice(self.player_hand)
            ai_tile = random.choice(self.ai_hand)

            self.info_label.config(text=f"⚔️ Player draws {player_tile} vs AI draws {ai_tile}!")
            self.root.update()
            time.sleep(2)

            if player_tile > ai_tile:
                self.end_game("🏆 YOU WIN by Sudden Death!")
                break
            elif ai_tile > player_tile:
                self.end_game("💀 AI WINS by Sudden Death!")
                break
            else:
                self.info_label.config(text="😮 Tie! Drawing again...")
                self.root.update()
                time.sleep(1.5)

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TileMatchingGame(root)
    root.mainloop()
