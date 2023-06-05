class Main:
    #  Create a HashMap object called capitalCities
    capitalCities = {}
    #  Add keys and values (Country, City)
    capitalCities["qw"] = "London"
    capitalCities["Germany"] = "Berlin"
    capitalCities["Norway"] = "Oslo"
    capitalCities["USA"] = "Washington DC"
    del capitalCities["USA"]
    capitalCities.clear()
    print(capitalCities)
