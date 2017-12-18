def format_city_and_country(city_name, country_name, population=None):
    """Returns a string formatted like 'City, Country'"""
    formatted_city_and_country = city_name.title() + ', ' + country_name.title()
    if population:
        return formatted_city_and_country + ' - population ' + str(population)
    else:
        return formatted_city_and_country
