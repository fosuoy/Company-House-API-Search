#!/usr/bin/python3
from requests import get
from json import loads, dumps
from re import compile
from variables import *

def companySearch(SEARCH_TERM, API_KEY, PAGE_NUMBER):
  r = get(\
      'https://api.companieshouse.gov.uk/search/companies?'\
      'q=' + SEARCH_TERM + '&items_per_page=100&start_index=' + PAGE_NUMBER , 
       auth=(API_KEY,''))
  return r

def resultsToJSON(PAGE_NUMBER):
  """ Converts string gained from companySearch into JSON for searching """
  search = companySearch(SEARCH_TERM, COMPANIES_HOUSE_API_KEY, PAGE_NUMBER)
  json_data = loads(search.text)
  return json_data

def performSearch():
  """ Goes through data from resultsToJSON and logs companies by postcode """
  f = open('results.txt', 'w')
  t = open('titles.txt', 'w')
  json_data = resultsToJSON("1")
  TOTAL_RESULTS = json_data['total_results']
  TOTAL_RESULTS_int = int(TOTAL_RESULTS)
  POSTCODE=compile(POSTCODE_REGEX)

  for number in range(int(TOTAL_RESULTS_int / 100)):
    json_data = resultsToJSON(str(number * 100))
    for item in json_data["items"]:
      try:
        if POSTCODE.match(dumps(item["address"]["postal_code"])):
          f.write(dumps(item, indent=4, separators=(',', ':')) + "\n")
          t.write(dumps(item["title"], indent=4, separators=(',', ':'))\
                                                      .replace('"', '') + "\n")
          t.write(dumps(item["address_snippet"], indent=4, \
                                separators=(',', ':')).replace('"', '') + "\n")
          t.write("\n")
      except:
        f.write("Postcode not listed for: " + dumps(item["company_number"], \
                                       indent=4, separators=(',', ':')) + "\n")
    print("Searching page: %s of %s" % \
                              (str(number), str(int(TOTAL_RESULTS_int / 100))))

  f.write("End of search.\nTotal number of results: " \
                                                   + str(TOTAL_RESULTS) + "\n")

if __name__ == "__main__":
  performSearch()
