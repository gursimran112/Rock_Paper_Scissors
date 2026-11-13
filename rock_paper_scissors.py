import random
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class RockPaperScissorsGame:
    """A simple best-of-three Rock, Paper, Scissors desktop game."""

    WINNING_SCORE = 3
    CHOICES = ("Rock", "Paper", "Scissors")

    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("650x650")
        self.root.minsize(560, 570)
        self.root.configure(bg="#f2f5f9")

        self.player_name = ""
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 0
        self.game_over = False

        self._build_interface()
        self._set_controls_enabled(False)

    def _build_interface(self):
        header = tk.Frame(self.root, bg="#243b53", pady=18)
        header.pack(fill="x")
        tk.Label(
            header, text="ROCK  •  PAPER  •  SCISSORS",
            font=("Arial", 20, "bold"), fg="white", bg="#243b53"
        ).pack()
        tk.Label(
            header, text="First to 3 points wins!",
            font=("Arial", 11), fg="#d9e2ec", bg="#243b53"
        ).pack(pady=(5, 0))

        main = tk.Frame(self.root, bg="#f2f5f9", padx=24, pady=18)
        main.pack(fill="both", expand=True)

        name_frame = tk.Frame(main, bg="#f2f5f9")
        name_frame.pack(fill="x", pady=(0, 14))
        tk.Label(name_frame, text="Player name:", font=("Arial", 11, "bold"),
                 bg="#f2f5f9").pack(side="left")
        self.name_entry = tk.Entry(name_frame, font=("Arial", 11), width=24)
        self.name_entry.pack(side="left", padx=10)
        self.start_button = tk.Button(
            name_frame, text="Start Game", command=self.start_game,
            bg="#2f855a", fg="white", activebackground="#276749",
            font=("Arial", 10, "bold"), relief="flat", padx=12, pady=6
        )
        self.start_button.pack(side="left")

        score_frame = tk.Frame(main, bg="white", bd=1, relief="solid", padx=18, pady=12)
        score_frame.pack(fill="x", pady=8)
        self.player_score_label = tk.Label(
            score_frame, text="Player: 0", font=("Arial", 15, "bold"),
            fg="#1a365d", bg="white"
        )
        self.player_score_label.pack(side="left", expand=True)
        self.computer_score_label = tk.Label(
            score_frame, text="Computer: 0", font=("Arial", 15, "bold"),
            fg="#9b2c2c", bg="white"
        )
        self.computer_score_label.pack(side="right", expand=True)

        self.status_label = tk.Label(
            main, text="Enter your name and click Start Game.",
            font=("Arial", 12), bg="#f2f5f9", fg="#334e68",
            wraplength=560
        )
        self.status_label.pack(pady=12)

        tk.Label(main, text="Choose your move", font=("Arial", 13, "bold"),
                 bg="#f2f5f9").pack(pady=(8, 10))
        choices_frame = tk.Frame(main, bg="#f2f5f9")
        choices_frame.pack()
        self.choice_buttons = []
        for choice, symbol in (("Rock", "✊"), ("Paper", "✋"), ("Scissors", "✌")):
            button = tk.Button(
                choices_frame, text=f"{symbol}\n{choice}",
                font=("Arial", 13, "bold"), width=11, height=3,
                bg="#d9eafd", fg="#102a43", activebackground="#bcccdc",
                relief="flat", command=lambda c=choice: self.play_round(c)
            )
            button.pack(side="left", padx=7)
            self.choice_buttons.append(button)

        self.result_label = tk.Label(
            main, text="", font=("Arial", 11, "bold"),
            bg="#f2f5f9", fg="#334e68", wraplength=560
        )
        self.result_label.pack(pady=12)

        history_title = tk.Label(main, text="Round History",
                                 font=("Arial", 12, "bold"), bg="#f2f5f9")
        history_title.pack(anchor="w", pady=(8, 4))
        history_frame = tk.Frame(main)
        history_frame.pack(fill="both", expand=True)
        self.history = tk.Listbox(history_frame, height=7, font=("Arial", 10))
        self.history.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(history_frame, command=self.history.yview)
        scrollbar.pack(side="right", fill="y")
        self.history.config(yscrollcommand=scrollbar.set)

        bottom = tk.Frame(main, bg="#f2f5f9")
        bottom.pack(fill="x", pady=(14, 0))
        tk.Button(bottom, text="New Game", command=self.new_game,
                  font=("Arial", 10, "bold"), bg="#486581", fg="white",
                  relief="flat", padx=16, pady=7).pack(side="left")
        tk.Button(bottom, text="Exit", command=self.root.destroy,
                  font=("Arial", 10, "bold"), bg="#c53030", fg="white",
                  relief="flat", padx=16, pady=7).pack(side="right")

    def _set_controls_enabled(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        for button in self.choice_buttons:
            button.config(state=state)

    def start_game(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Name required", "Please enter your name first.")
            self.name_entry.focus_set()
            return
        self.player_name = name
        self.name_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.status_label.config(text=f"Good luck, {self.player_name}! Make your move.")
        self._set_controls_enabled(True)

    def play_round(self, player_choice):
        if not self.player_name or self.game_over:
            return

        computer_choice = random.choice(self.CHOICES)
        self.round_number += 1

        if player_choice == computer_choice:
            outcome = "Draw"
            message = "It's a draw!"
        elif (
            (player_choice == "Rock" and computer_choice == "Scissors")
            or (player_choice == "Paper" and computer_choice == "Rock")
            or (player_choice == "Scissors" and computer_choice == "Paper")
        ):
            self.player_score += 1
            outcome = f"{self.player_name} wins"
            message = f"You win this round! {player_choice} beats {computer_choice}."
        else:
            self.computer_score += 1
            outcome = "Computer wins"
            message = f"Computer wins this round! {computer_choice} beats {player_choice}."

        self.player_score_label.config(text=f"{self.player_name}: {self.player_score}")
        self.computer_score_label.config(text=f"Computer: {self.computer_score}")
        self.result_label.config(
            text=f"You: {player_choice}    |    Computer: {computer_choice}\n{message}"
        )
        self.history.insert(
            tk.END,
            f"Round {self.round_number}: You={player_choice}, "
            f"Computer={computer_choice} — {outcome}"
        )
        self.history.see(tk.END)

        if self.player_score >= self.WINNING_SCORE:
            self.finish_game(self.player_name)
        elif self.computer_score >= self.WINNING_SCORE:
            self.finish_game("Computer")

    def finish_game(self, winner):
        self.game_over = True
        self._set_controls_enabled(False)
        self.status_label.config(text=f"Game over! {winner} is the winner.")
        self._save_match(winner)
        messagebox.showinfo(
            "Match Complete",
            f"Winner: {winner}\n"
            f"{self.player_name}: {self.player_score}\n"
            f"Computer: {self.computer_score}\n\n"
            "Match details saved to match_history.txt."
        )

    def _save_match(self, winner):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = (
            f"{timestamp} | Player: {self.player_name} | "
            f"Player Score: {self.player_score} | "
            f"Computer Score: {self.computer_score} | Winner: {winner}\n"
        )
        try:
            with open("match_history.txt", "a", encoding="utf-8") as file:
                file.write(record)
        except OSError as error:
            messagebox.showerror("Save Error", f"Could not save match history:\n{error}")

    def new_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.round_number = 0
        self.game_over = False
        self.player_name = ""
        self.player_score_label.config(text="Player: 0")
        self.computer_score_label.config(text="Computer: 0")
        self.status_label.config(text="Enter your name and click Start Game.")
        self.result_label.config(text="")
        self.history.delete(0, tk.END)
        self.name_entry.config(state=tk.NORMAL)
        self.name_entry.delete(0, tk.END)
        self.start_button.config(state=tk.NORMAL)
        self._set_controls_enabled(False)
        self.name_entry.focus_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissorsGame(root)
    root.mainloop()
