def make_pizza(size_inches, *toppings):
    """Summarize the pizza we are about to make."""
    print('\nMaking a ' + str(size_inches) + '-inch pizza with the following toppings:')
    for topping in toppings:
        print('- ' + topping)
