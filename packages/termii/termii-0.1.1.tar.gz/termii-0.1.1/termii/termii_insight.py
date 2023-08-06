import requests
import json

BALANCE_URL = "https://api.ng.termii.com/api/get-balance"
SEARCH_URL = "https://api.ng.termii.com/api/check/dnd"
STATUS_URL = "https://api.ng.termii.com/api/insight/number/query"
HISTORY_URL = "https://api.ng.termii.com/api/sms/inbox"

def check_balance(api_key):
    """
    A function to check a client's termii balance

    Params: 
    api_key: str
        The termii api_key associated with the client
    """

    response = requests.get(url=f"{BALANCE_URL}?api_key={api_key}")
    response = json.loads(response.content)
    return response

def check_number(api_key, phone_number):
    """
    A function to verify phone numbers and automatically detect their status

    Params: 
    api_key: str
        The termii api_key associated with the client
    phone_number: str
        Represents the phone number to be verified. Phone number must be in the international format without the '+'
    """

    response = requests.get(url=f"{SEARCH_URL}?api_key={api_key}&phone_number={phone_number}")
    response = json.loads(response.content)
    return response

def get_number_status(api_key, phone_number, country_code):
    """
    A function to detect if a number is fake or has ported to a new network.

    Params: 
    api_key: str
        The termii api_key associated with the client
    phone_number: str
        Represents the phone number to be verified. Phone number must be in the international format without the '+'
    country_code: str
        Represents short alphabetic codes developed to represent countries (Example: NG ).
    """

    payload = {
        "api_key": api_key,
        "phone_number": phone_number,
        "country_code": country_code
    }

    headers = {
    'Content-Type': 'application/json',
    }

    response = requests.get(STATUS_URL, json=payload, headers=headers)
    response = json.loads(response.content)
    return response

def get_full_history(api_key):
    """
    A function that returns reports for messages sent across the sms, voice & whatsapp channels.

    Params: 
    api_key: str
        The termii api_key associated with the client
    """

    response = requests.get(url=f"{HISTORY_URL}?api_key={api_key}")
    return json.loads(response.content)