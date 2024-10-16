from random import randint

"""
opening strategies:
0 = manual
1 = random. no splitting
2 = lowest. no splitting
3 = highest. no splitting
4 = lowest with unconditional splitting
5 = lowest of highest amount
6 = lowest + unbeatable ending

strategies:
0 = manual
1 = random. no splitting
2 = lowest. no splitting
3 = highest. no splitting
4 = lowest with unconditional splitting
"""

def is_unbeatable(value, size, played_cards):
    unplayed_cards = []
    for i in range(value + 1, 14):
        c = played_cards.count(i)
        if 4 - c >= size:
            return False
    return True

class Player:
    def __init__(self, name, opening, strategy):
        self.name = name
        self.hand = []
        self.position = -1
        self.opening = opening
        self.strategy = strategy
        self.wins = [0, 0, 0, 0]

    def start(self, played_cards, stack):
        if self.opening == 0:

            sorted_hand = sorted(self.hand)
            print(f"This is your hand: {sorted_hand}")
            value = ""
            while not value.isdigit():
                value = input("Enter card value: ")
                if value.isdigit():
                    if int(value) > 13 or int(value) < 1:
                        value = ""
                        continue
                    if self.hand.count(int(value)) == 0:
                        value = ""
            value = int(value)
            max_size = self.hand.count(value)
            size = ""
            while not size.isdigit():
                size = input("Enter amount: ")
                if size.isdigit():
                    if int(size) > max_size or int(size) < 1:
                        size = ""
            size = int(size)
            for i in range(size):
                self.hand.remove(value)
                played_cards.append(value)
            stack.append(size)
            stack.append(value)
            print("")

        elif self.opening == 1:

            # play a random value and don't split it
            size = 0
            index = randint(0, len(self.hand)-1)
            value = self.hand[index]
            while value in self.hand:
                # record size
                self.hand.remove(value)
                played_cards.append(value)
                size += 1
            stack.append(size)
            stack.append(value)

        elif self.opening == 2:

            size = 0
            value = min(self.hand)
            while value in self.hand:
                self.hand.remove(value)
                played_cards.append(value)
                size += 1
            stack.append(size)
            stack.append(value)

        elif self.opening == 3:

            size = 0
            value = max(self.hand)
            while value in self.hand:
                self.hand.remove(value)
                played_cards.append(value)
                size += 1
            stack.append(size)
            stack.append(value)

        elif self.opening == 4:

            size = 1
            value = min(self.hand)
            self.hand.remove(value)
            played_cards.append(value)
            stack.append(size)
            stack.append(value)

        elif self.opening == 5:

            pairs = []
            for i in range(1, 14):
                c = self.hand.count(i)
                if c > 0:
                    pairs.append((i, c))
            sorted_pairs = sorted(pairs, key=lambda x: -x[1])
            size = sorted_pairs[0][1]
            value = sorted_pairs[0][0]
            for i in range(size):
                self.hand.remove(value)
                played_cards.append(value)
            stack.append(size)
            stack.append(value)

        elif self.opening == 6:

            s = len(set(self.hand))
            highest = max(self.hand)
            amount_of_highest = self.hand.count(highest)
            if s == 2 and is_unbeatable(highest, amount_of_highest, played_cards):
                # play the unbeatable
                for i in range(amount_of_highest):
                    self.hand.remove(highest)
                    played_cards.append(amount_of_highest)
                stack.append(amount_of_highest)
                stack.append(highest)
            else:
                # play the lowest
                size = 0
                value = min(self.hand)
                while value in self.hand:
                    self.hand.remove(value)
                    played_cards.append(value)
                    size += 1
                stack.append(size)
                stack.append(value)

    def play(self, played_cards, stack):
        if self.strategy == 0:

            size = stack[0]
            last_value = stack[-1]
            
            sorted_hand = sorted(self.hand)
            print(f"This is your hand: {sorted_hand}")

            value = ""
            while not value.isdigit():
                value = input("Enter card value: ")
                if value.isdigit():
                    if int(value) > 13 or int(value) <= last_value:
                        value = ""
                        continue
                    if self.hand.count(int(value)) < size:
                        value = ""
                if value == "skip":
                    print("")
                    return False
            value = int(value)
            for i in range(size):
                self.hand.remove(value)
                played_cards.append(value)
            stack.append(value)
            print("")
            return True

        elif self.strategy == 1:

            # pick a random one out of the possibilities
            size = stack[0]
            last_value = stack[-1]
            possible = []
            for value in self.hand:
                if self.hand.count(value) == size and value > last_value:
                    possible.append(value)
            if len(possible) == 0:
                return False
            selected_value = possible[ randint(0, len(possible)-1) ]
            # add size amount to played_cards
            for i in range(size):
                self.hand.remove(selected_value)
                played_cards.append(selected_value)
            stack.append(selected_value)
            return True

        elif self.strategy == 2:

            size = stack[0]
            last_value = stack[-1]
            possible = []
            for value in self.hand:
                if self.hand.count(value) == size and value > last_value:
                    possible.append(value)
            if len(possible) == 0:
                return False
            selected_value = min(possible)
            for i in range(size):
                self.hand.remove(selected_value)
                played_cards.append(selected_value)
            stack.append(selected_value)
            return True

        elif self.strategy == 3:

            size = stack[0]
            last_value = stack[-1]
            possible = []
            for value in self.hand:
                if self.hand.count(value) == size and value > last_value:
                    possible.append(value)
            if len(possible) == 0:
                return False
            selected_value = max(possible)
            for i in range(size):
                self.hand.remove(selected_value)
                played_cards.append(selected_value)
            stack.append(selected_value)
            return True

        elif self.strategy == 4:

            size = stack[0]
            last_value = stack[-1]
            possible = []
            for value in self.hand:
                # split if you have more than necessary
                if self.hand.count(value) >= size and value > last_value:
                    possible.append(value)
            if len(possible) == 0:
                return False
            selected_value = min(possible)
            for i in range(size):
                self.hand.remove(selected_value)
                played_cards.append(selected_value)
            stack.append(selected_value)
            return True

    def print_info(self):
        sorted_hand = sorted(self.hand)
        print(f"name: {self.name}    position: {self.position}\nhand: {sorted_hand}\n")