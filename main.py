from data import MENU, resources, coins, art
money_in_machine = 0

'''Type of beverage chosen'''
choice = ""
'''Keeps asking what coffee to make'''
keep_going = True


def user_choice(keep_going, money_in_machine):
    """ - Checks if machine has enough resources to make any coffee
        - Asks to select coffee type and checks if there's enough resources to make it"""
    if out_of_order_check(MENU, resources, keep_going) != False: # did this bc "if keep_going:" always turned out True, the False from out_of_order_check
                                                                 # always switched back to True
        choice = input("What would you like? (espresso/latte/cappuccino): ")
        if choice == "espresso" or choice == "latte" or choice == "cappuccino":
            resource_check(MENU[choice]["ingredients"], resources, choice)
            insert_coins(MENU[choice]["cost"],  coins, money_in_machine)
            make_coffee(resources, MENU[choice]["ingredients"], MENU, choice, money_in_machine)
        elif choice == "off":
            keep_going = False
        elif choice == "report":
            print("---------------")
            print("Resources stat:")
            print(f"Water: {resources['water']} ml")
            print(f"Milk: {resources['milk']} ml")
            print(f"Coffee: {resources['coffee']} g")
            print(f"Money: ${money_in_machine}")
            print("---------------")
            user_choice(keep_going, money_in_machine)
        else:
            print("Please check your spelling and try again.")
            user_choice(keep_going, money_in_machine)
        return choice, keep_going


def out_of_order_check(MENU, resources, keep_going):
    """ - Checks if there's enough resources in the machine to make any beverage and prints which are unavailable
        - If current resources are not enough to make any one beverage, it prints Out of order and exits program"""
    not_enough_for_espresso = False
    not_enough_for_latte = False
    not_enough_for_cappuccino = False
    espresso_dict = MENU["espresso"]["ingredients"]
    latte_dict = MENU["latte"]["ingredients"]
    cappuccino_dict = MENU["cappuccino"]["ingredients"]

    if espresso_dict["water"] > resources["water"] or espresso_dict["coffee"] > resources["coffee"]:
        not_enough_for_espresso = True
    if latte_dict["water"] > resources["water"] or latte_dict["milk"] > resources["milk"] or latte_dict["coffee"] > resources["coffee"]:
        not_enough_for_latte = True
    if cappuccino_dict["water"] > resources["water"] or cappuccino_dict["milk"] > resources["milk"] or cappuccino_dict["coffee"] > resources["coffee"]:
        not_enough_for_cappuccino = True

    if not_enough_for_espresso is True and not_enough_for_latte is True and not_enough_for_cappuccino is True:
        print("Machine out of order. All resources need refilling.")
        keep_going = False
        return keep_going
    elif not_enough_for_cappuccino is True and not_enough_for_latte is False:
        print("Cappuccino unavailable. Some resources need refilling.")
    elif not_enough_for_cappuccino is False and not_enough_for_latte is True:
        print("Latte unavailable. Some resources need refilling.")
    elif not_enough_for_cappuccino is True and not_enough_for_latte is True:
        print("Latte and Cappuccino unavailable. Some resources need refilling.")


def resource_check(beverage_dict, resources, choice):
    """ - Checks if there's enough resources for the selected beverage. If user selects a beverage there isn't enough
            for it displays that and asks to select another"""
    for i in beverage_dict:
        if beverage_dict[i] > resources[i]:  # [i] here doesnt mean index but name of dictionary key. thats why it knows to correctly compare
                                             # 2 resources in beverage_dict to 3 resources in resources
            print(f"There's not enough {i} in the machine for a {choice}.")
            print("Please choose a different beverage.")
            choice = ""
            user_choice(keep_going, money_in_machine)


def insert_coins(beverage_price, coins, money_in_machine):
    """ - Displays how much money to pay for a beverage and updates as user inserts coins
        - If user inserts too many coins, it returns changes
        - If at the end there's not enough coins inserted it returns user all coins"""
    print(f"The price is ${beverage_price}. Insert coins.")
    money_inserted = 0
    for i in range(len(coins)):
        try:
            this_many_coins = int(input(
                f"How many {list(coins.keys())[i]}?: "))  # idea: https://stackoverflow.com/a/44139468/19181783
            money_inserted += list(coins.values())[i] * this_many_coins
            if money_inserted < beverage_price:
                print(f"Insert remaining ${round((beverage_price - money_inserted), 2)}")  # rounded to 2 decimal point bc after entering 1 nickle there'd be"
                                                                                           # Insert remaining $0.4500000000000002"
            elif money_inserted > beverage_price:
                change = money_inserted - beverage_price
                money_inserted -= change
                print(f"Here's ${round(change, 2)} change")
                return money_in_machine
            elif money_inserted == beverage_price:
                return money_in_machine
        except ValueError:
            print("Not a valid number, please try again.")
    if money_inserted < beverage_price:
        print("Sorry, that's not enough money. Money refunded.")
        money_inserted = 0
        user_choice(keep_going, money_in_machine)


def make_coffee(resources, beverage_dict, MENU, choice, money_in_machine):
    """ - It updates resources and gives user the selected beverage
        - It goes back to asking user to choose a new beverage"""
    for i in beverage_dict:
        resources[i] -= beverage_dict[i]
    money_in_machine += MENU[choice]["cost"]
    print(f"{art}\nHere is your {choice}. Enjoy!")
    print("------------------------------")
    user_choice(keep_going, money_in_machine)


'''Begins the game'''
user_choice(keep_going, money_in_machine)







