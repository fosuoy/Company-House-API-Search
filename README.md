# Company-House-API-Search
A helpful command line utility which uses the Company House API to search 
for companies within a geographic locality given a search string and a regex of
the postcode you are looking for companies within -
possible uses are lead generation / job searching, enjoy

Requirements:
Companies House API Key - see here:
https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/apikey_authorisation.html
Python 3

Run the script with the -h option for a help menu.
Takes the following arguments:
  -a --api-token    Your companies house API token.
  -p --post-code    The post code you want to search for companies within in regex form
  -s --search-term  The company names you want to search for.

e.g.
./company_house_search.py -a 12345 -p ^\"LS[0-9]+ -s petroleum

Outputs a results.txt file with all the data gained from the search, and a
titles.txt for a text file full of the companies titles, followed by their 
addresses.

Possible uses are:
Lead generation (finding companies within a certain locality to easily start
                 an advertising campaign.)
Job searching (finding companies within a certain locality to check for 
               vacancies)

Any questions, let me know.

Please note the following if having issues using this:
http://forum.aws.chdev.org/t/search-company-officers-returns-http-416-when-start-index-over-300/897
