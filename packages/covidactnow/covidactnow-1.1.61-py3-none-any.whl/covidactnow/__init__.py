# from covidactnow import covid

import requests 

# As CovidActNow's API is a REST API, queries are stored as URLs.

class User:
    def __init__(self, api_key):
        self.api_key = api_key

    def queryUrl(self, state):
        return f"http://api.covidactnow.org/v2/state/{state}.json?apiKey=" + self.api_key

    def infRate(self, state):
        # Infection Rate
        try:
            return float(requests.get(self.queryUrl(state)).json()['metrics']['infectionRate'])
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
        
    def posRate(self, state):    
        # Positive Rate
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['metrics']['testPositivityRatio']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
    
    def vaxRate(self, state):
        # Vax Rate
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['metrics']['vaccinationsCompletedRatio']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
    
    def freeBedPercentage(self, state):
        # Free Bed Percentage
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageTotal'])/\
                float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
        
    def newCases(self, state):
        try:
            return int(requests.get(self.queryUrl(state)).json()['actuals']['newCases'])
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")

    def newDeaths(self, state):
        try:
            return int(requests.get(self.queryUrl(state)).json()['actuals']['newDeaths'])
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")
        
    def covidBedPercentage(self, state):
        try:
            return round(100*float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['currentUsageCovid'])/\
                float(requests.get(self.queryUrl(state)).json()['actuals']['hospitalBeds']['capacity']), 2)
        except TypeError:
            return "NaN"
        except Exception as e:
            print(f"An error occured in data collection: {e}")