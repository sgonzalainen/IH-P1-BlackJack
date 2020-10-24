import my_functions as myf
import random
import time

this_game = True

while this_game == True:
    game_counter = 0
    user_wins = 0
    dealer_wins = 0
    
    game_counter = 0
    user_wins = 0
    dealer_wins = 0

    

    card_drawer, num_decks, deck_in_game_initial = myf.prepare_deck()
    print('Game is ready to start. May the force be with you')

    new_round = True

    while new_round == True:
        user_cards = []
        dealer_cards = []
        user_count = 0
        dealer_count = 0

        card_drawer=myf.reload_drawer(card_drawer, game_counter, num_decks, deck_in_game_initial)


        print('New round!!!')
        time.sleep(1)
        print('Here comes your first two cards...')
        time.sleep(1)
        user_cards = myf.initial_user_two_cards(card_drawer)
        user_count=myf.get_count(user_cards)
        print(f'Your count is {user_count}')
        time.sleep(1)
        print('Now the dealer gets his/her first card...')
        dealer_cards.append(myf.draw_card(card_drawer)) #Append in order to avoid problems with 10 and mixing lists with single value
        dealer_count=myf.get_count(dealer_cards)
        time.sleep(1)
        print(f'Dealer\'s count is {dealer_count}')
        time.sleep(1)
        print(f'Let\'ts recap.\nYour count is {user_count}.\nDealer\'s count is {dealer_count}')
        time.sleep(1)
        user_cards=myf.user_decision(user_cards,card_drawer)
        user_count=myf.get_count(user_cards)
        time.sleep(1)

        if user_count > 21:
            print(f'You lose!! Sorry but you exceeded 21.\nYou got a total number of {user_count}')
            dealer_wins += 1
        else:
            print('Now is time for the dealer.')
            dealer_cards=myf.dealer_play(dealer_cards,card_drawer)
            dealer_count=myf.get_count(dealer_cards)
            user_wins, dealer_wins = myf.who_win(user_count, dealer_count, user_wins, dealer_wins)

        game_counter += 1

        new_round = myf.new_round_continue(user_wins, dealer_wins, game_counter) #If this returns False it means user wants a new game, not a new round




    

    


    