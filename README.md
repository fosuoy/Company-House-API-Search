# Company-House-API-Search
A helpful command line utility which uses the Company House API to search 
for companies within a geographic locality given a search string and a regex of
the postcode you are looking for companies within -
possible uses are lead generation / job searching, enjoy

Requirements:
Companies House API Key - see here:
https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/apikey_authorisation.html
Python 3

See the variables.py file to input the required variables to complete a search:
1. Search term - e.g. "Petroleum" to find companies with the string petroleum
   in their title
2. Companies House API Key - see above
3. regex of postcode you are searching for companies within

Outputs a results.txt file with all the data gained from the search, and a
titles.txt for a text file full of the companies titles, followed by their 
addresses.

Possible uses are:
Lead generation (finding companies within a certain locality to easily start
                 an advertising campaign.)
Job searching (finding companies within a certain locality to check for 
               vacancies)

Any questions, let me know.
