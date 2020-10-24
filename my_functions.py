
import random
import time

import subprocess #for playing sound


card_values = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}


def enter_num_decks():
    '''
    This function asks user to input number of decks to play game with.
    Args:

    Returns:
        int(num_decks): number of decks input by player.

    '''
    num_decks = input('How many decks you want to play with at start of game? Input integer please.')
    if num_decks.isdigit() and num_decks != '0':
        return int(num_decks)
    else:
        print('Wrong input value. Please enter an integer and equal or above 1')
        return enter_num_decks()



def prepare_deck():
    '''
    Based on player input on fucntion enter_num_decks(), creates the deck.

    Args:

    Returns:
        card_drawer (iterator): The deck as iterator.
        num_decks_temp (int): Number of decks input by player (to be used for determining in which round to reload full deck).
        deck_in_game_initial(list): The full deck (to be used when reloading).

    '''
    cards_type = ('A','2','3','4','5','6','7','8','9','10','J','Q','K')

    one_deck = cards_type*4

    num_decks_temp = enter_num_decks()
    deck_in_game_initial = list(one_deck)*num_decks_temp
    current_deck = deck_in_game_initial*1 #This to create a copy and be sure they are not linked
    random.shuffle(current_deck)
    card_drawer = iter(current_deck)
    play_sound('shuffle')

    return card_drawer, num_decks_temp, deck_in_game_initial

def reload_drawer(card_drawer, game_counter, num_decks, deck_in_game_initial):

    '''
    Function to reload deck when deck is more or less half spent.
    Assumed every round it is spent on average 6 cards.
    If 1 deck is used, deck is reloaded every 5 rounds.

   Args:
        card_drawer(iter): the deck in use.
        game_counter(int): Number of rounds already played.
        num_decks (int): Number of decks to play with.
        deck_in_game_initial(list): The intial full deck.

    Returns:
        card_drawer (iter): the full deck reloaded.

    '''
    divisor = num_decks * 5

    if (game_counter % divisor == 0) and (game_counter != 0):

        print(f'You have played already {game_counter} rounds.\nThe casino does not want you to count cards. Hence, deck is reloaded and shuffled again')
        current_deck = deck_in_game_initial*1
        random.shuffle(current_deck)
        card_drawer = iter(current_deck)
        play_sound('shuffle')
        return card_drawer
    else:
        return card_drawer

def play_sound(sound):
    '''
    Plays a sound by calling a subprocess with terminal command.

    Args:
        sound(str): Type of sound to play
    
    Returns:

    '''
    if sound == 'win':
        bashCommand = "play -q sounds/win.wav -t alsa"

    elif sound == 'defeat':
        bashCommand = "play -q sounds/gameover.wav -t alsa"

    elif sound == 'tie':
        bashCommand = "play -q sounds/tie.wav -t alsa"

    elif sound == 'draw':
        bashCommand = "play -q sounds/draw.wav -t alsa"

    elif sound == 'shuffle':
        bashCommand = "play -q sounds/shuffle.wav -t alsa"

    # How to solve the problem of getting warn t alsa on bash
    #https://www.mail-archive.com/debian-bugs-dist@lists.debian.org/msg1057438.html

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
        


def draw_card(card_drawer):
    '''
    This simulates the draw of a card.

    Args:
        card_drawer(iter): The deck in use.

    Returns:
        card_drawn(str):The card drawn in next item by iterator
    '''
    card_drawn = next(card_drawer)
    play_sound('draw')

    print(f'The card is a....{card_drawn}!!')
    return card_drawn


def user_decision(user_cards,card_drawer):
    '''
    On this script, player is asked whether to hit or stand based on current hand.

    Args:
        user_cards(list): List of cards on players's hand after first two cards.
        card_drawer(iter): The deck in use.

    Returns:
        user_cards(list): List of cards on players's hand after player's turn.
    '''
    check = True
    while check: #This to allow ask player after first hit.
    
        decision = input('Now is your turn again! What\'s gonna be, hit or stand?\n\'0\' for stand.\n\'1\' for hit)\n')
        if decision == '0':
            print('You stand')

            return user_cards

        elif decision == '1':
            print('Here it comes your new card...')
            time.sleep(1)
            user_cards.append(draw_card(card_drawer)) #New card is added to list of cards on player's hand
            user_count = get_count(user_cards)
            print(f'Your count is {user_count}')

        else:
            print('Wrong input value. Please enter either 0 to stand or 1 to hit')
            return user_decision() #This recursion forces player to input correct value

        if user_count > 21:

            return user_cards

    

def get_count(card_list):
    '''
    This function counts the cards given a list of cards.

    Args:
        card_list(list): List of cards.

    Returns:
        count(int): score give list of cards.
    '''
    
    def reorder_aces(card_list):
        '''
        This function reorder Aces and places them at the end of the list. this is needed to handle 
        with the dual value of aces.

        Args:
            card_list(list): List of cards.

        Returns:
            card_list(list): List of cards sorted.

        '''

        if 'A' in card_list:
            card_list = sorted(card_list, key= lambda x: card_values[x]) #Sorted by value. Ace as define with 10 value is sorted to the end

        else:
            pass

        return card_list


    count = 0

    card_list = reorder_aces(card_list) #This is needed to deal with Aces

    for card in card_list:
        if card != 'A':
            count += card_values[card]
        else: #it means it is an Ace
            if count + card_values['A'] <= 21: #This checks if Ace as 11 exceeds 21 or not
                count += card_values['A']
            else:
                count += 1 #If exceeded 21, ace takes value of 1
    
    return count



def initial_user_two_cards(card_drawer):
    '''
    This function is to simulate the first two hits for player
    Args:
        card_drawer(iter): The deck in use.

    Returns:
        temp_list(list): list of first two cards for player


    '''
    temp_list = []
    for x in range(2):
        temp_list.append(draw_card(card_drawer))
        time.sleep(1)
    return temp_list

        
def dealer_play(dealer_cards,card_drawer):
    '''
    This script computes the dealer's decision based on list of cards.

    Args:
        dealer_cards(list): List of cards.
        card_drawer(iter): The deck in use.

    Returns:
        dealer_cards(list): List of dealer's cards after dealer's play.

    '''

    check = True
    while check:
        print('Here it comes a new card for dealer...')
        time.sleep(1)
        dealer_cards.append(draw_card(card_drawer))
        dealer_count = get_count(dealer_cards)
        
        if dealer_count > 21:
            return dealer_cards
        
        elif dealer_count >= 17:
            return dealer_cards
        
        else:
            print(f'Dealer\'s count is now {dealer_count}')
            print(f'Count is below 17, therefore dealer decides to hit one more card')
            
def who_win(user_count, dealer_count, user_wins, dealer_wins):
    '''
    This function compares results between player and dealer and determines who won.

    Args:
        user_count(int): Player's final score
        dealer_count(int): Deaaler's final score
        user_wins(int): Number of wins by Player
        dealer_wins(int): Number of wins by Dealer

    Returns:
        user_wins(int): Updated number of wins by Player
        dealer_wins(int): Updated number of wins by Dealer

    '''
    if dealer_count > 21:
        print('Congratulations!! You won!')
        print(f'Dealer exceeded 21. Dealer got {dealer_count}')
        play_sound('win')
        return user_wins + 1, dealer_wins

    elif dealer_count < user_count:
        print('Congratulations!! You won!')
        print(f'Dealer got {dealer_count} ... but you got {user_count}!!')
        play_sound('win')
        return user_wins + 1, dealer_wins

    elif user_count < dealer_count:
        print('You lose!!')
        print(f'Dealer got {dealer_count} ... but you got {user_count}....')
        print(f'It is so sad a machine outplayed you...')
        play_sound('defeat')
        return user_wins, dealer_wins + 1
    else:
        
        print('it was a tie!!')
        print(f'Dealer got {dealer_count} ... but you got {user_count}....')
        play_sound('tie')
        return user_wins, dealer_wins



def new_round_continue(user_wins, dealer_wins, game_counter):

    '''
    Asks user whether to play a new round, review statistics on this game, create a new game or exit the game.

    Args:
        user_wins(int): Number of wins by Player
        dealer_wins(int): Number of wins by Dealer
        game_counter(int): Number of rounds already played.

    Returns:
        Boolean: True if new round, False if new game


    '''
    answer = input('What do you want to do next?\nPress 0 for a new round\nPress 1 for review statistics on this game\nPress 2 for a total new game\nPress other key to escape.')
    if answer == '0':
        return True

    elif answer == '1':
        tie_rounds = game_counter - (user_wins + dealer_wins)
        print(f'Total number of rounds: {game_counter} rounds.\n User wins:  {user_wins} rounds.\n Dealer wins: {dealer_wins} rounds.\n Tie rounds: {tie_rounds} rounds')
        time.sleep(2)
        return new_round_continue(user_wins, dealer_wins, game_counter)
        
    elif answer == '2':
        return False

    else:
        exit()    

