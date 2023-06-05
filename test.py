food_list = ['penis', 'food'
             ]
def food_list():
    """
    """
    if len(food_list) == 0:
        return 0
    else:
        list_of_food = ''
        for f in food_list:
            f_but_string = str(f)
            list_of_food += f_but_string + '\n'
            return list_of_food
        
food = food_list()

print(food)