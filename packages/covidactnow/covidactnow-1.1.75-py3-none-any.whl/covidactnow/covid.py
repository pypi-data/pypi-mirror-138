import requests 

# As CovidActNow's API is a REST API, queries are stored as URLs.

class User:
    """Main User class taking api_key with attributes to get COVID statistics."""
    
    def __init__(self, api_key):
        self.api_key = api_key

    def queryUrl(self, state):
        """Returns the query url for requests based on statistic."""
        return f"http://api.covidactnow.org/v2/state/{state}.json?apiKey=" + self.api_key

    def infRate(self, state):
        """Gets today's COVID infection rate by state."""
        # Infection Rate
        try:
            return float(requests.get(self.queryUrl(state)).json()['metrics']['infectionRate'])
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
        
    def posRate(self, state):
        """Gets today's COVID positive testing rate by state."""    
        # Positive Rate
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['metrics']['testPositivityRatio']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
    
    def vaxRate(self, state):
        """Get's the vaccination rate as of today, by state."""
        # Vax Rate
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['metrics']['vaccinationsCompletedRatio']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
    
    def freeBedPercentage(self, state):
        """Get's the percentage of free hospital beds by state."""
        # Free Bed Percentage
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageTotal'])/\
                float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
        
    def newCases(self, state):
        """Gets the number of new cases today by state."""
        # New Cases
        try:
            return int(requests.get(self.queryUrl(state)).json()['actuals']['newCases'])
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")

    def newDeaths(self, state):
        """Gets the number of new deaths today, by state."""
        # New Deaths
        try:
            return int(requests.get(self.queryUrl(state)).json()['actuals']['newDeaths'])
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
        
    def covidBedPercentage(self, state):
        """Gets the percentage of hospital beds occupied by COVID patients."""
        # Covid Bed Percentage
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageCovid'])/\
                float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")