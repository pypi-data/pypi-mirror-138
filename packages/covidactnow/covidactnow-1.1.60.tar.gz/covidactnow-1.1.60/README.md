# Covid Act Now Database Wrapper

This package is an extremely bare-bones wrapper around Covid Act Now's database of COVID-19 related information. View the PyPi project [here](https://pypi.org/project/covidactnow/), and the original post page [here](https://covidinfo.preritdas.com). 

Usage is simple. Install the package with `pip install covidactnow`.

Instantiate a user object with your API key as an argument. You can easily generate an API key [here](https://covidactnow.org/data-api).

```python
import covidactnow

api = covidactnow.User(api_key = 'yourapikey')

washingtonInfectionRate = api.infRate('WA')
massachussettsVaxRate = api.vaxRate('MA')

print(f"{washingtonInfectionRate = }")
print(f"{massachussettsVaxRate = }")
```
This will result (with different data, of course):
```
washingtonInfectionRate = 1.16
massachussettsVaxRate = 76.3
```

----
For more information on how the wrapper works, particularly how it was redesigned to be package-friendly, read the "Updated for Distribution" section of this [page](https://covidinfo.preritdas.com). Note that this version has been updated to get data from within a `User` class allowing individual API keys to be used (as opposed to defining a state as an object and defining statistics as object attributes).
