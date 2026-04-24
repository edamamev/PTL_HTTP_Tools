#!/usr/bin/env python3

import requests
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')


### User Stories
##  Simple GET Request
#   ./script -g URL.COM
##  Simple POST

input = sys.argv[1:]
logging.debug(str(input))


def post_request(url: str, datajson=None, has_data=False, has_json=False, params=None):
    """
    Creates a POST request for the `url`,
    parsing the input into headers.
    """
    data = json = None
    if has_data: data = datajson
    if has_json: json = datajson
    if params: url = add_params_to_url(url, params)
    logging.debug(f"POST: URL = {url} DATA = {data} JSON = {json} PARAMS = {params}")
    return requests.post(url=url, data=data, json=json,)

def add_params_to_url(url: str, params: list):
    output = "?"
    for i in range(len(params)):
        output = output + f"{params[i][0]}={params[i][1]}&"
    return url + output

def get_request(url: str, params=None, cookies=None, headers=None, data=None):
    logging.debug(f"GET: URL = {url} PARAMS = {params} COOKIES = {cookies} HEADERS = {headers} DATA = {data}")
    return requests.get(url=url, params=params, cookies=cookies, headers=headers, data=data)


def parse_dict_from_string(dict_string: str) -> dict:
    """
    Parses a string of format "KEY: VALUE, KEY: VALUE,..."
    into a python dictionary.
    """
    result = {}
    for pair in dict_string.split(", "):
        key, value = pair.split(": ", 1)
        result[key.strip()] = value.strip()
    return result

def parse_book_from_string(book_string: str):
    result = []
    for pair in book_string.split(", "):
        key, value = pair.split(": ", 1)
        result.append((key, value))
    return result


def get_url(url_param, is_url_present):
    if not(is_url_present):
        return url_param, True
    else:
        logging.debug("Cunt you've put two (2) URL arguments >:(")
        sys.exit()


# Check how many arguments there are.
# [1, 2, 3, 4, 5, 6]
# Each `-x` ought to have a parameter.
# len / 2
def main():
    # For GET, `params` are GET Parameters, like `?page=20&name=hacker`

    url = user_agent = content_type = accept_language = ""
    cookies = params = headers = datajson = None
    # Checks
    is_url_present = is_post = is_get = has_params = has_body = has_data = has_json= False
    logging.debug(len(input))
    for i in range(int(len(input) / 2)):
        if input[2 * i]   == "-p":
            is_post = True
            url, is_url_present = get_url(input[(2 * i) + 1], is_url_present)
        elif input[2 * i] == "-g":
            is_get = True
            url, is_url_present = get_url(input[(2 * i) + 1], is_url_present)
        elif input[2 * i] == "-m":
            params = parse_book_from_string(input[(2 * i) + 1])
        elif input[2 * i] == "-c":
            cookies = parse_book_from_string(input[(2 * i) + 1])
        elif input[2 * i] == "-h":
            headers = parse_book_from_string(input[(2 * i) + 1])
        elif input[2 * i] == "-d":
            has_data = True
            datajson = parse_book_from_string(input[(2 * i) + 1])
        elif input[2 * i] == "-j":
            has_json = True
            datajson = parse_book_from_string(input[(2 * i) + 1])
        else:
            sys.exit()

    if is_post:
        response = post_request(url, datajson, has_data, has_json, params)
        print(response.text)
        print(response.request.headers)
        print(response.request.body)
    elif is_get:
        response = get_request(url, params, cookies, headers, datajson)
        print(response.text)
        print(response.request.headers)
        print(response.request.body)

main()
