import os
import random
from utils.user_manager import UserManager
from utils.score import Score

class DiceGame:
    def __init__(self):
        self.user_manager = UserManager()
        self.scores = []
        self.current_user = None
        self.load_scores()

    def load_scores(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/rankings.txt", "r") as file:
                for line in file:
                    username, game_id, points, wins = line.strip().split(',')
                    score = Score(username, int(game_id), int(points), int(wins))
                    self.scores.append(score)
        except FileNotFoundError:
            pass

    def save_scores(self):
        with open("data/rankings.txt", "w") as file:
            for score in self.scores:
                file.write(f"{score.username},{score.game_id},{score.points},{score.wins}\n")

    def play_game(self, username):
        self.current_user = username
        user_score = next((score for score in self.scores if score.username == username), None)
        if not user_score:
            user_score = Score(username)
            self.scores.append(user_score)
        
        while True:
            print(f"Welcome, {username}!")
            print(f"Stage: {user_score.game_id}")
            print(f"Wins: {user_score.wins}")
            choice = input("Menu:\n1. Roll dice\n2. Show top scores\n3. Log out\nEnter your choice, or leave blank to cancel: ")
            if not choice:
                return
            if choice == "1":
                self.roll_dice(user_score)
            elif choice == "2":
                self.show_top_scores()
            elif choice == "3":
                self.logout()
                return
            else:
                print("Invalid choice. Please try again.")
        self.save_scores()

    def roll_dice(self, user_score):
        user_roll = random.randint(1, 6)
        cpu_roll = random.randint(1, 6)
        print(f"{self.current_user} rolled: {user_roll}")
        print(f"CPU rolled: {cpu_roll}")
        if user_roll > cpu_roll:
            print("You win this round!")
            user_score.wins += 1
            user_score.points += 1
            user_score.game_id += 1
        elif user_roll < cpu_roll:
            print("CPU wins this round!")
            user_score.points -= 1
            user_score.game_id += 1
        else:
            print("It's a tie!")
        self.update_top_scores()

    def show_top_scores(self):
        print("Top scores:")
        sorted_scores = sorted(self.scores, key=lambda x: x.points, reverse=True)
        for score in sorted_scores:
            print(f"{score.username}: {score.points} points, {score.wins} wins")

    def update_top_scores(self):
        self.scores = sorted(self.scores, key=lambda x: x.points, reverse=True)

    def logout(self):
        print(f"Goodbye {self.current_user}!")
        self.current_user = None

    def run(self):
        while True:
            print("Welcome to Dice Roll Game!")
            choice = input("1. Register\n2. Login\n3. Exit\nEnter your choice, or leave blank to cancel: ")
            if not choice:
                return
            if choice == "1":
                self.user_manager.register()
            elif choice == "2":
                username = self.user_manager.login()
                if username:
                    self.play_game(username)
            elif choice == "3":
                return
            else:
                print("Invalid choice. Please try again.")