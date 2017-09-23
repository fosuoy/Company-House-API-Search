#!/usr/bin/python3
from requests import get
from sys import exit
from json import loads, dumps
from re import compile
import argparse


def resultsToJSON(page_number, api_token, post_code_regex, search_term):
  """ Converts string gained from search into JSON for parsing """
  search_url = "https://api.companieshouse.gov.uk/search/companies?" + \
           "q=" + search_term + "&items_per_page=100&start_index=" + page_number
  r = get( search_url, auth=(api_token,'') )
  json_data = r.json()
  return json_data


def perform_search( api_token, post_code_regex, search_term ):
  """ Goes through data from resultsToJSON and logs companies by postcode """
  f = open('results.txt', 'w')
  t = open('titles.txt', 'w')
  json_data = resultsToJSON("1", api_token, post_code_regex, search_term)
  total_results = json_data['total_results']
  pages_of_results = str( int( int(total_results) / 100) )
  post_code=compile( post_code_regex )

  
  print("There are %s pages of results." % pages_of_results)
  print("only the first 4 pages can be searched :(")
  print("See here for more details: " + \
          "http://forum.aws.chdev.org/t/" + \
          "search-company-officers-returns-http-416-when-start-index-over-300/897")

  for number in range(4):
    print("Searching page: %s" % str(number))
    json_data = resultsToJSON(
                  str(number * 100), api_token, post_code_regex, search_term)

    for item in json_data["items"]:
      try:
        if post_code.match(dumps(item["address"]["postal_code"])):
          f.write(dumps(item, indent=4, separators=(',', ':')) + "\n")
          t.write(dumps(item["title"], indent=4, separators=(',', ':'))\
                                                      .replace('"', '') + "\n")
          t.write(dumps(item["address_snippet"], indent=4, \
                                separators=(',', ':')).replace('"', '') + "\n")
          t.write("\n")
      except:
        f.write("Postcode not listed for: " + dumps(item["company_number"], \
                                       indent=4, separators=(',', ':')) + "\n")

  f.write("End of search.\nTotal number of results: " \
                                                   + str(total_results) + "\n")


if __name__ == "__main__":
  """
  Parse args then trigger search if all OK
  """
  parser = argparse.ArgumentParser(description='Company House search details...')
  parser.add_argument('-a', metavar='--api-token', type=str, required=True,
          help='Your companies house API token.')
  parser.add_argument('-p', metavar='--post-code', type=str, required=True,
          help='The post code you want to search for companies within')
  parser.add_argument('-s', metavar='--search-term', type=str, required=True,
          help='The company names you want to search for.')
  args = parser.parse_args()
  if None in vars(args).values():
      print("You must supply a valid api token, post code and search term if " +
            "you want this to work properly...")
      print("Use the -h option to see a help menu.")
      exit(1)
  perform_search( args.a, args.p, args.s )
