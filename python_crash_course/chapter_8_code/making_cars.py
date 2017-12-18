def make_car(manufacturer, model_name, **options):
    car = {
        'manufacturer': manufacturer,
        'model_name': model_name,
    }
    for option_name, option_value in options.items():
        car[option_name] = option_value
    return car
