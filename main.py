from random import randint
from datetime import datetime
from Player import Player

DEBUG = False


def play(players):
        deck = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13
        ]
        # shuffle deck
        for i in range(52):
            r = randint(0, 51)
            carry = deck[i]
            deck[i] = deck[r]
            deck[r] = carry
        # empty hands and distribute cards
        for i in range(4):
            players[i].hand = []
            for j in range(13):
                players[i].hand.append(deck.pop())
        
        # players exchange hands except on first round
        if players[0].position != -1:
            first_lowest = min(players[0].hand)
            players[0].hand.remove(first_lowest)
            second_lowest = min(players[0].hand)
            players[0].hand.remove(second_lowest)
            
            first_highest = max(players[3].hand)
            players[3].hand.remove(first_highest)
            second_highest = max(players[3].hand)
            players[3].hand.remove(second_highest)

            players[0].hand.append(first_highest)
            players[0].hand.append(second_highest)
            players[3].hand.append(first_lowest)
            players[3].hand.append(second_highest)

            lowest = min(players[1].hand)
            players[1].hand.remove(lowest)
            
            highest = max(players[2].hand)
            players[2].hand.remove(highest)

            players[1].hand.append(highest)
            players[2].hand.append(lowest)

        # start game
        turn = 0
        game_ongoing = True
        played_cards = []
        current = 0
        winners = []
        while game_ongoing:
            # play hand
            last_to_play = current
            n = len(players)

            if DEBUG:
                print(f"Turn: {turn}\n")
                for i in range(n):
                    #players[i].print_info()
                    pass
            
            stack = []
            players[current % n].start(played_cards, stack)
            
            if DEBUG:
                print(f"{players[current % n].name} opens with {stack[0]} x {stack[-1]}\n")

            for i in range(1, n):
                # go to next player
                new_current = (current+i) % n
                can_play = players[new_current].play(played_cards, stack)
                if can_play:
                    last_to_play = new_current

                    if DEBUG:
                        print(f"{players[new_current].name} plays {stack[0]} x {stack[-1]}\n")
                elif DEBUG:
                    print(f"{players[new_current].name} skips\n")

            current = last_to_play

            if DEBUG:
                print(f"Stack: {stack}\n")
            
            # check if anyone finished
            players_to_remove = []
            for i in range(n):
                if len(players[i].hand) == 0:
                    players_to_remove.append(players[i])
                    # possibly shift current player
                    if i < current:
                        current -= 1
            for p in players_to_remove:
                players.remove(p)
                winners.append(p)
            turn += 1
            # game ends if there is only one guy left
            if len(players) < 2:
                if len(players) == 1:
                    winners.append(players[0])
                game_ongoing = False
        for i in range(4):
            winners[i].position = i
            winners[i].wins[i] += 1
        
        if DEBUG:
            print(f"First place: {winners[0].name}")
            print(f"Second place: {winners[1].name}")
            print(f"Third place: {winners[2].name}")
            print(f"Fourth place: {winners[3].name}\n")
        
        return winners


if __name__ == "__main__":
    # Name, Opening strategy, Playing strategy
    p0 = Player("Albert", 6, 4)
    p1 = Player("Benson", 1, 1)
    p2 = Player("Carl", 1, 1)
    p3 = Player("Dave", 1, 1)

    players = [p0, p1, p2, p3]

    t1 = datetime.now()

    for i in range(10000):
        players = play(players)

    t2 = datetime.now()

    print(f"total time: {t2-t1}\n")

    # result table header
    cell_width = 15
    print("player name" + (cell_width-11) * " ", end="")
    print("first place" + (cell_width-11) * " ", end="")
    print("second place" + (cell_width-12) * " ", end="")
    print("third place" + (cell_width-11) * " ", end="")
    print("fourth place" + (cell_width-12) * " ")

    # sort players
    players = sorted(players, key=lambda x: x.name)

    # print results
    for player in players:
        player_name = player.name
        print(player_name + (cell_width-len(player_name)) * " ", end="")
        player_first = str(player.wins[0])
        print(player_first + (cell_width-len(player_first)) * " ", end="")
        player_second = str(player.wins[1])
        print(player_second + (cell_width-len(player_second)) * " ", end="")
        player_third = str(player.wins[2])
        print(player_third + (cell_width-len(player_third)) * " ", end="")
        player_fourth = str(player.wins[3])
        print(player_fourth + (cell_width-len(player_fourth)) * " ")