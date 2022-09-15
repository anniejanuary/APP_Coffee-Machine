from data import MENU, resources, coins, art

money_in_machine = 0
current_resource_list = []
needed_resource_list = []

'''Type of beverage chosen'''
choice = ""

'''Keeps asking what coffee to make'''
keep_going = True

'''Only checks if enough resources in machine to make a beverage instead of updating current_resource_list'''
check_only = True


def user_choice(keep_going):
    """ - Checks if machine has enough resources to make any coffee
        - Asks to select coffee type and checks if there's enough resources to make it"""
    if out_of_order_check(MENU, keep_going) != False: # did this bc "if keep_going:" always turned out True, the False from out_of_order_check
                                                      # always switched back to True
        choice = input("What would you like? (espresso/latte/cappuccino): ")
        if choice == "espresso" or choice == "latte" or choice == "cappuccino":
            resource_check(current_resource_list, resources_needed(MENU, choice), choice, check_only)
            insert_coins(needed_resource_list, coins, money_in_machine, check_only)
            make_coffee(current_resource_list, needed_resource_list, choice)
        elif choice == "off":
            keep_going = False
        elif choice == "report":
            print("---------------")
            print("Resources stat:")
            print(f"Water: {current_resource_list[0]} ml")
            print(f"Milk: {current_resource_list[1]} ml")
            print(f"Coffee: {current_resource_list[2]} g")
            print(f"Money: ${current_resource_list[3]}")
            print("---------------")
            user_choice(keep_going)
        return choice, keep_going


def initial_resource_stat(resources, money_in_machine, current_resource_list):
    """Sets initial resources (water, milk, coffee) as those from data.py"""
    current_resource_list.append(resources["water"])
    current_resource_list.append(resources["milk"])
    current_resource_list.append(resources["coffee"])
    current_resource_list.append(money_in_machine)
    return current_resource_list


def current_resource_stat(current_resource_list, needed_resource_list):
    """Updates current_resource_list by deducting needed_resource_list from its elements"""
    for i in range(len(current_resource_list)-1):
        current_resource_list[i] -= needed_resource_list[i]
    current_resource_list[3] += needed_resource_list[3]
    return current_resource_list


def resources_needed(MENU, choice):
    """Draws amount of resources needed to make a selected beverage from data.py into needed_resource_list"""
    del needed_resource_list[:] #deleting or emptying? before each beverage check?
    needed_resource_list.append(MENU[choice]["ingredients"]["water"])
    if choice != "espresso":
        needed_resource_list.append(MENU[choice]["ingredients"]["milk"])
    else:
        needed_resource_list.append(0)
    needed_resource_list.append(MENU[choice]["ingredients"]["coffee"])
    needed_resource_list.append(MENU[choice]["cost"])
    return (needed_resource_list)


def out_of_order_check(MENU, keep_going):
    """ - Checks if there's enough resources in the machine to make any beverage and prints which are unavailable
        - If current resources are not enough to make any one beverage, it prints Out of order and exits program"""
    not_enough_for_espresso = False
    not_enough_for_latte = False
    not_enough_for_cappuccino = False
    if MENU["espresso"]["ingredients"]["water"] > current_resource_list[0] or MENU["espresso"]["ingredients"]["coffee"] > current_resource_list[2]:
        not_enough_for_espresso = True
    if MENU["latte"]["ingredients"]["water"] > current_resource_list[0] or MENU["latte"]["ingredients"]["milk"] > current_resource_list[1] or MENU["latte"]["ingredients"]["coffee"] > current_resource_list[2]:
        not_enough_for_latte = True
    if MENU["cappuccino"]["ingredients"]["water"] > current_resource_list[0] or MENU["cappuccino"]["ingredients"]["milk"] > current_resource_list[1] or MENU["cappuccino"]["ingredients"]["coffee"] > current_resource_list[2]:
        not_enough_for_cappuccino = True

    if not_enough_for_espresso == True and not_enough_for_latte == True and not_enough_for_cappuccino == True:
        print("Machine out of order. All resources need refilling.")
        keep_going = False
        return keep_going
    elif not_enough_for_cappuccino == True and not_enough_for_latte == False:
        print("Cappuccino unavailable. Some resources need refilling.")
    elif not_enough_for_cappuccino == False and not_enough_for_latte == True:
        print("Latte unavailable. Some resources need refilling.")
    elif not_enough_for_cappuccino == True and not_enough_for_latte == True:
        print("Latte and Cappuccino unavailable. Some resources need refilling.")


def resources_after_brew(current_resource_list, needed_resource_list):
    """Creates amount of resources after a simulated brew w/o updating current_resource_list"""
    water_after_brew = (current_resource_list[0] - needed_resource_list[0])
    milk_after_brew = (current_resource_list[1] - needed_resource_list[1])
    coffee_after_brew = (current_resource_list[2] - needed_resource_list[2])
    return water_after_brew, milk_after_brew, coffee_after_brew


def resource_check(resources_now, resources_to_brew, choice, check_only):
    """ - Checks if there's enough resources for the selected beverage. If user selects a beverage there isn't enough
            for it displays that and asks to select another
        - """
    resources_after = resources_after_brew(resources_now, resources_to_brew)

    if check_only is False:
        #### DOES THIS EVER RUN?
        current_resource_list = list(resources_after)
        print(f"Water: {current_resource_list[0]} ml")
        print(f"Milk: {current_resource_list[1]} ml")
        print(f"Coffee: {current_resource_list[2]} g")
        print(f"Money: ${current_resource_list[3]}")

        return current_resource_list

    if check_only is True:
        for i in range(0,
                       len(list(
                           resources_after))):  # changed tuple to list temporarily so pycharm doesnt underline it
            if resources_after[i] < 0:
                if i in range(0, 2):
                    print(f"There's not enough {list(resources.keys())[i]} in the machine for a {choice}.")
                    # `got it from here https://stackoverflow.com/a/44139468/19181783
                    print("Please choose a different beverage.")
                    choice = ""
                    user_choice()

    return resources_after


def insert_coins(needed_resource_list, coins, money_in_machine, check_only):
    """ - Displays how much money to pay for a beverage and updates as user inserts coins
        - If user inserts too many coins, it returns changes
        - If at the end there's not enough coins inserted it returns user all coins"""
    print(f"The price is ${needed_resource_list[3]}. Insert coins.")
    money_inserted = 0
    for i in range(len(coins)):
        this_many_coins = int(input(f"How many {list(coins.keys())[i]}?: "))
        money_inserted += list(coins.values())[i] * this_many_coins
        if money_inserted < needed_resource_list[3]:
            print(f"Insert remaining ${round((needed_resource_list[3] - money_inserted), 2)}")
            # rounded to 2 decimal point bc after entering 1 nickle there'd be"
            # Insert remaining $0.4500000000000002"
        elif money_inserted > needed_resource_list[3]:
            change = money_inserted - needed_resource_list[3]
            money_inserted -= change
            print(f"Here's ${round(change, 2)} change")
            money_in_machine += money_inserted
            check_only = False
            return money_in_machine, current_resource_list, check_only
            break
        elif money_inserted == needed_resource_list[3]:
            money_in_machine += money_inserted
            check_only = False
            return money_in_machine, current_resource_list, check_only
            break
    if money_inserted < needed_resource_list[3]:
        print("Sorry, that's not enough money. Money refunded")
        money_inserted = 0
        needed_resource_list = []
        user_choice(current_resource_list, money_in_machine)


def make_coffee(current_resource_list, needed_resource_list, choice):
    """ - It updates current_resource_list and gives user the selected beverage
        - It goes back to asking user to choose a new beverage"""
    current_resource_stat(current_resource_list, needed_resource_list)
    print(f"{art}\nHere is your {choice}. Enjoy!")
    print("------------------------------")
    user_choice(keep_going)
    return current_resource_list, needed_resource_list


'''Begins the game'''
if not current_resource_list:   # == if empty, simpler than:   if current_resource_list == []
                                    # https://stackoverflow.com/a/53522/19181783
    initial_resource_stat(resources, money_in_machine, current_resource_list)  # draw initial resource stat from data.py
user_choice(keep_going)
