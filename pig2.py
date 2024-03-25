import random
import time

class Die:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return random.randint(1, self.num_sides)

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll(self, die):
        roll = die.roll()
        print(f"{self.name} rolled a {roll}")
        self.turn_total += roll
        print(f"{self.name}'s score is now {self.score} and turn total is {self.turn_total}")
        return roll

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0
        print(f"{self.name}'s score is now {self.score}")

class HumanPlayer(Player):
    def decide_roll_or_hold(self, turn_score):
        return input("Roll again or hold? (r/h): ").strip().lower() == 'r'

class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.total_score = 0

    def decide_roll_or_hold(self, turn_score):
        threshold = min(25, 100 - self.total_score)
        return turn_score < threshold

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return HumanPlayer(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Unknown player type")

class Game:
    def __init__(self, max_score=100, num_players=2, die=Die()):
        self.max_score = max_score
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.current_player = 0
        self.die = die

    def switch_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def play(self):
        while True:
            current_player = self.players[self.current_player]
            print(f"\nIt's {current_player.name}'s turn.")
            print(f"{current_player.name}'s score is {current_player.score} and turn total is {current_player.turn_total}")
            while True:
                decision = input("Press 'r' to roll or 'h' to hold: ").lower()
                if decision == 'r':
                    roll = current_player.roll(self.die)
                    if roll == 1:
                        print(f"{current_player.name} rolled a 1 and lost their turn total.")
                        self.switch_player()
                        break
                    elif current_player.score + current_player.turn_total >= self.max_score:
                        print(f"{current_player.name} has reached or exceeded the max score and won the game!")
                        return
                elif decision == 'h':
                    current_player.hold()
                    if current_player.score >= self.max_score:
                        print(f"{current_player.name} has reached or exceeded the max score and won the game!")
                        return
                    else:
                        self.switch_player()
                        break
                else:
                    print("Invalid input, please try again.")

class TimedGameProxy(Game):
    def __init__(self, max_score=100, num_players=2, die=Die(), timeout=60):
        super().__init__(max_score, num_players, die)
        self.timeout = timeout
        self.start_time = None

    def play(self):
        self.start_time = time.time()
        while True:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= self.timeout:
                print("Time's up! Game over.")
                return
            super().play()

if __name__ == "__main__":
    random.seed(0)
    game_type = input("Enter game type (regular/timed): ").lower()
    if game_type == "regular":
        game = Game()
    elif game_type == "timed":
        game = TimedGameProxy()
    else:
        print("Invalid game type.")
        exit(1)
    game.play()
