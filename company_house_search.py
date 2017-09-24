#!/usr/bin/env python3
from argparse import ArgumentParser
from json import loads, dumps
from re import compile
from requests import get
from sys import exit

from variables import COMPANIES_HOUSE_API_KEY, SEARCH_TERM, POSTCODE_REGEX


def resultsToJSON(page_number, api_token, search_term):
  """ Converts string gained from search into JSON for parsing """
  search_url = "https://api.companieshouse.gov.uk/search/companies?" + \
           "q=" + search_term + "&items_per_page=100&start_index=" + page_number
  r = get( search_url, auth=(api_token,'') )
  json_data = r.json()
  return json_data


def write_results(write_file_one, write_file_two, item):
  write_file_one.write(dumps(item, indent=4, separators=(',', ':')) + "\n")
  write_file_two.write(dumps(item["title"], indent=4, separators=(',', ':'))\
                                              .replace('"', '') + "\n")
  write_file_two.write(dumps(item["address_snippet"], indent=4, \
                        separators=(',', ':')).replace('"', '') + "\n")
  write_file_two.write("\n")


def perform_search( api_token, post_code_regex, search_term ):
  """ Goes through data from resultsToJSON and logs companies by postcode """
  f = open('results.txt', 'w')
  t = open('titles.txt', 'w')
  post_code = None
  post_code_search = False

  json_data = resultsToJSON("1", api_token, search_term)
  total_results = json_data['total_results']
  pages_of_results = int( int(total_results) / 100)

  if post_code_regex != None:
    post_code = compile( post_code_regex )
    post_code_search = True

  
  print("There are %s results / %s pages of results." %
                                        (total_results, str(pages_of_results)) )
  print("only the first 4 pages can be searched :(")
  print("See here for more details: " + \
          "http://forum.aws.chdev.org/t/" + \
          "search-company-officers-returns-http-416-when-start-index-over-300/897")

  for number in range(min(4, pages_of_results + 1)):
    print("Searching page: %s" % str(number))
    json_data = resultsToJSON(str(number * 100), api_token, search_term)

    for item in json_data["items"]:
      if post_code_search:
        item_post_code = dumps(item["address"]["postal_code"]) if 'postal_code' in item["address"] else ''
        if post_code.match(item_post_code):
          write_results(f, t, item)
      else:
        write_results(f, t, item)

  f.write("End of search.\nTotal number of results: " \
                                                   + str(total_results) + "\n")


if __name__ == "__main__":
  """
  Parse args then trigger search if all OK
  """
  parser = ArgumentParser(description='Company House search details...')
  parser.add_argument('-a', metavar='--api-token', type=str,
          help='Your companies house API token.')
  parser.add_argument('-p', metavar='--post-code', type=str,
          help='The post code you want to search for companies within (optional)')
  parser.add_argument('-s', metavar='--search-term', type=str,
          help='The company names you want to search for.')
  args = parser.parse_args()
  if (args.a == None and COMPANIES_HOUSE_API_KEY) or \
             (args.s == None and SEARCH_TERM == None):
      print("You must supply a valid api token and search term if " +
            "you want this to work properly...")
      print("Use the -h option to see a help menu.")
      exit(1)
  api_token = args.a if args.a else COMPANIES_HOUSE_API_KEY
  post_code_regex = args.p if args.p else POST_CODE_REGEX
  search_term = args.s if args.s else SEARCH_TERM
  perform_search( api_token, post_code_regex, search_term )
