import os
from utils.user import User

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/users.txt", "r") as file:
                for line in file:
                    username, password = line.strip().split(',')
                    self.users[username] = User(username, password)
        except FileNotFoundError:
            pass

    def save_users(self):
        with open("data/users.txt", "w") as file:
            for user in self.users.values():
                file.write(f"{user.username},{user.password}\n")

    def register(self):
        while True:
            username = input("Enter username (at least 4 characters), or leave blank to cancel: ")
            if not username:
                return
            if len(username) < 4:
                print("Username must be at least 4 characters long.")
                continue
            if username in self.users:
                print("Username already exists.")
                continue
            password = input("Enter password (at least 8 characters), or leave blank to cancel: ")
            if not password:
                return
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
                continue
            self.users[username] = User(username, password)
            self.save_users()
            print("Registration successful.")
            break

    def login(self):
        while True:
            username = input("Enter username, or leave blank to cancel: ")
            if not username:
                return None
            password = input("Enter password, or leave blank to cancel: ")
            if not password:
                return None
            if username not in self.users or self.users[username].password != password:
                print("Invalid username or password.")
                continue
            return username
