import random
import sys
import time
import tkinter as tk
from tkinter import messagebox

PLAYER_COLOR = '#00CED1'
AI_COLOR = '#DA70D6'
MATCH_COLOR = '#7CFC00'
MISMATCH_COLOR = '#FF6347'
DEFAULT_TILE_COLOR = '#FFFFFF'

class TileMatchingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tile Matching Game 🎮")
        self.deck = []
        self.player_hand = []
        self.ai_hand = []
        self.player_tiles_buttons = []
        self.ai_tiles_labels = []
        self.selected_tiles = []
        self.difficulty = 'easy'
        self.player_matches = 0
        self.ai_matches = 0

        self.create_widgets()
        self.initialize_game()

    def create_widgets(self):
        self.info_label = tk.Label(self.root, text="Welcome to Tile Matching!", font=("Arial", 16))
        self.info_label.pack(pady=10)

        self.ai_frame = tk.Frame(self.root)
        self.ai_frame.pack(pady=10)

        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=10)

        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        self.draw_button = tk.Button(self.control_frame, text="Draw Tile", command=self.draw_tile_for_player)
        self.draw_button.grid(row=0, column=0, padx=10)

        self.start_button = tk.Button(self.control_frame, text="Choose Difficulty", command=self.choose_difficulty)
        self.start_button.grid(row=0, column=1, padx=10)

        self.match_count_label = tk.Label(self.root, text="Player Matches: 0 | AI Matches: 0", font=("Arial", 12))
        self.match_count_label.pack(pady=5)

    def initialize_game(self):
        self.deck = [i for i in range(1, 10)] * 2
        random.shuffle(self.deck)
        self.player_hand = [self.draw_tile() for _ in range(5)]
        self.ai_hand = [self.draw_tile() for _ in range(5)]
        self.update_display()

    def draw_tile(self):
        return self.deck.pop(0) if self.deck else None

    def update_display(self):
        # Update Player Hand
        for btn in self.player_tiles_buttons:
            btn.destroy()
        self.player_tiles_buttons = []

        for idx, tile in enumerate(self.player_hand):
            btn = tk.Button(self.player_frame, text=f"{tile}", font=("Arial", 18), width=4, height=2,
                            bg=DEFAULT_TILE_COLOR, command=lambda idx=idx: self.select_tile(idx))
            btn.grid(row=0, column=idx, padx=5)
            self.player_tiles_buttons.append(btn)

        # Update AI Hand
        for widget in self.ai_frame.winfo_children():
            widget.destroy()
        self.ai_tiles_labels = []

        for idx, tile in enumerate(self.ai_hand):
            lbl = tk.Label(self.ai_frame, text=f"{tile}", font=("Arial", 18), width=4, height=2, bg=AI_COLOR)
            lbl.grid(row=0, column=idx, padx=5)
            self.ai_tiles_labels.append(lbl)

        # Update the match count
        self.match_count_label.config(text=f"Player Matches: {self.player_matches} | AI Matches: {self.ai_matches}")

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
            self.remove_tiles()
        else:
            self.info_label.config(text="❌ Not a match!")
            self.flash_tiles(MISMATCH_COLOR)
            self.reset_selection()

    def flash_tiles(self, color):
        for idx in self.selected_tiles:
            self.player_tiles_buttons[idx].config(bg=color)

    def remove_tiles(self):
        idx1, idx2 = sorted(self.selected_tiles, reverse=True)
        del self.player_hand[idx1]
        del self.player_hand[idx2]
        self.selected_tiles.clear()
        self.player_matches += 1  # Update player matches instantly
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
        if self.difficulty == 'hard':
            self.ai_make_smart_decision()
        else:
            self.ai_random_decision()

    def ai_make_smart_decision(self):
        matches = [(i, j) for i in range(len(self.ai_hand))
                   for j in range(i + 1, len(self.ai_hand))
                   if self.ai_hand[i] == self.ai_hand[j]]
        if matches:
            i, j = matches[0]
            self.animate_ai_match(i, j, "🤖 AI matched smartly!")
            self.ai_matches += 1  # Increment matches only when AI makes a match
        else:
            self.ai_draw_tile()
            self.update_display()

    def ai_random_decision(self):
        for i in range(len(self.ai_hand)):
            for j in range(i + 1, len(self.ai_hand)):
                if self.ai_hand[i] == self.ai_hand[j]:
                    self.animate_ai_match(i, j, "🤖 AI matched randomly!")
                    self.ai_matches += 1  # Increment matches only when AI makes a match
                    return
        self.ai_draw_tile()
        self.update_display()

    def animate_ai_match(self, i, j, msg):
        self.highlight_ai_tiles([i, j], "#FFFF00")
        self.root.after(500, lambda: self.highlight_ai_tiles([i, j], MATCH_COLOR))
        self.root.after(1000, lambda: self.remove_ai_tiles(i, j, msg))

    def highlight_ai_tiles(self, indices, color):
        for idx in indices:
            if idx < len(self.ai_tiles_labels):
                self.ai_tiles_labels[idx].config(bg=color)

    def remove_ai_tiles(self, i, j, msg):
        for idx in sorted([i, j], reverse=True):
            if idx < len(self.ai_hand):
                del self.ai_hand[idx]
        self.update_display()
        self.info_label.config(text=msg)

    def ai_draw_tile(self):
        new_tile = self.draw_tile()
        if new_tile:
            self.ai_hand.append(new_tile)
            self.info_label.config(text="🤖 AI drew a tile.")
        else:
            self.info_label.config(text="🤖 Deck empty for AI!")

    def can_match(self, hand):
        return any(hand[i] == hand[j] for i in range(len(hand)) for j in range(i+1, len(hand)))

    def check_game_over(self):
        if not self.player_hand:
            self.end_game("🏆 YOU WIN!")
        elif not self.ai_hand:
            self.end_game("💀 AI WINS!")
        elif not self.deck:
            self.check_for_stalemate_or_winner()

    def check_for_stalemate_or_winner(self):
        if self.player_matches == self.ai_matches:
            self.end_game("🤝 It's a DRAW!")
        elif self.player_matches > self.ai_matches:
            self.end_game("🏆 YOU WIN by Matches!")
        else:
            self.end_game("💀 AI WINS by Matches!")

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = TileMatchingGame(root)
    root.mainloop()
