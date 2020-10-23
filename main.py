import my_functions as myf
import random
import time

user_count=0
user_cards=[]
dealer_count=0
dealer_cards=[]

card_drawer=myf.prepare_deck()

print('Game is ready to start. May the force be with you')
time.sleep(1)
print('Here comes your first two cards...')
time.sleep(1)
user_cards = myf.initial_user_two_cards(card_drawer)
user_count=myf.get_count(user_cards)
print(f'Your count is {user_count}')
time.sleep(1)
print('Now the dealer gets his/her first card...')
dealer_cards = list(myf.draw_card(card_drawer))
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
    print(f'You lose!! Sorry but you exceeded 21.\n You got a total number of {user_count}')
else:
    print('Now is time for the dealer.')
    dealer_cards=myf.dealer_play(dealer_cards,card_drawer)
    dealer_count=myf.get_count(dealer_cards)
    myf.who_win(user_count, dealer_count)