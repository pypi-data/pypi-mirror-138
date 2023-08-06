import requests
import json

SEND_TOKEN_URL = 'https://api.ng.termii.com/api/sms/otp/send'
SEND_TOKEN_VOICE_URL = "https://api.ng.termii.com/api/sms/otp/send/voice"
SEND_TOKEN_VOICECALL_URL = "https://api.ng.termii.com/api/sms/otp/send/voice"
SEND_TOKEN_VERIFYTOKEN_URL = "https://api.ng.termii.com/api/sms/otp/verify"
SEND_TOKEN_IN_APP = "https://api.ng.termii.com/api/sms/otp/generate"

def send_new_token(api_key, message_type, phone_number, 
        sender_id, channel, pin_attempts, pin_time_to_live,
        pin_length, pin_placeholder, message_text):
    """
    This function allows businesses generate a one-time-passwords(OTP).
    It happens across every channel on Termii.
    They are generated randomly and can be set to expire within a time-frame.

    Parameters:
    api_key : string
        API key for Termii account.
    message_type : ALPHANUMERIC / NUMERIC
        Dynamic string that will be sent as part of OTP message.
    phone_number : integer
        The destination number of the client receiving the OTP message.
        Number must be in international format.
    sender_id : string
        ID of the sender of the OTP.
    channel : string
        Dynamic string route through which the OTP message is sent.
        Can be set to dnd or Whatsapp or generic.
    pin_attempts : ALPHANUMERIC / NUMERIC
        PIN code that is generated and sent with the OTP message.
        Has a minimum of one attempt.
    pin_time_to_live : integer
        Represents time of PIN validation before expiry.
        Time is in minutes and has a minimum of 0 and maximum of 60.
    pin_length : integer
        Length of PIN code. Has a minimum of 4 and maximum of 8.
    pin_placeholder : string
        Before sending the OTP message, the PIN placeholder is replaced with
        generic pin code.
    message_text : string
        Message text that would be sent to destination phone number.
    """
    payload = {
        'api_key' : api_key,
        'message_type' : 'NUMERIC',
        'to' : phone_number,
        'from' : sender_id,
        'channel' : 'generic',
        'pin_attempts' : 10,
        'pin_time_to_live' : 5,
        'pin_length' : 6,
        'pin_placeholder' : '< 1234 >',
        'message_text' : 'Your pin is < 1234 >',
        'pin_type' : 'NUMERIC',
    }
    
    headers = {
        'Content-Type' : 'application/json',
    }

    response = requests.post(SEND_TOKEN_URL, headers=headers, json=payload)
    response = json.loads(response.content)
    return response


def send_voice_token(api_key, phone_number, pin_attempts, pin_time_to_live, pin_length):
    """
    This function enables you to generate and trigger one-time-passwords
    via a voice channel to a phone number. OTPs are generated and sent to
    phone numbers and can only be verified using Verify Token function.

    Parameters:
    api_key : string
        API key for Termii account.
    phone_number : integer
        The destination number of the client receiving the voice token.
        Number must be in international format.
    pin_attempts : NUMERIC / ALPHANUMERIC
        PIN code that is generated and sent with the OTP message.
        Has a minimum of one attempt.
    pin_time_to_live : integer
        Represents time of pin validation before expiry.
        Time is in minutes and has a minimum of 0 and maximum of 60.
    pin_length : integer
        Length of PIN code. Has a minimum of 4 and maximum of 8.
    """
    payload = {
        'api_key' : api_key,
        'phone_number' : phone_number,
        'pin_attempts' : 10,
        'pin_time_to_live' : 5,
        'pin_length' : 6,  
    }
    
    headers = {
        'Content-Type' : 'application/json',
    }
    
    response = requests.post(SEND_TOKEN_VOICE_URL, headers=headers, json=payload)
    response = json.loads(response.content)
    return response


def make_voice_call(api_key, phone_number, code, pin_attempts, pin_time_to_live, pin_length):
    """
    This function enables you to send messages from your application through
    a voice channel to a client's phone number. Only one-time-passwords are
    allowed for now and they cannot be verified via the Verify Token Function

    Parameters:
    api_key : string
        API key for Termii account.
    phone_number : integer
        The destination number of the client receiving the voice token.
        Number must be in international format.
    code : numeric
        The code the client receives. It has to be numeric and length must
        be between 4 and 8 digits.
    """
    payload = {
        'api_key' : api_key,
        'phone_number' : phone_number,
        'code' : code,
        'pin_attempts' : 2,
        'pin_time_to_live' : 5,
        'pin_length' : 5,
    }
    
    headers = {
        'Content-Type' : 'application/json',
    }
    
    response = requests.post(SEND_TOKEN_VOICECALL_URL, headers=headers, json=payload)
    response = json.loads(response.content)
    return response


def verify_sent_token(api_key, pin_id, pin):
    """
    Ths function checks tokens sent to customers and returns a response
    confirming the status of the token. A token can either be confirmed
    as verified or expired based on the timer set for the token.

    Parameters:
    api_key : string
        API key for Termii account
    pin_id : string
        ID of the pin sent (Example: "c8dcd048-5e7f-4347-8c89-4470c3af0b")
    pin : string
        The pin code (Example: "195558")
    """
    payload = {
        'api_key' : api_key,
        'pin_id' : pin_id,
        'pin' : pin,
    }

    headers = {
        'Content-Type' : 'application/json',
    }

    response = requests.post(SEND_TOKEN_VERIFYTOKEN_URL, headers=headers, json=payload)
    response = json.loads(response.content)
    return response


def send_token_in_app(api_key, phone_number, pin_attempts, pin_time_to_live, pin_length):
    """
    This function returns OTP code in JSON fromat which can be used in any
    web or mobile app. Tokens are numeric or alpha-numeric codes generated
    to authenticate login requests and verify customer transactions.

    Parameters:
    api_key : string
        API key for Termii account
    pin_type : NUMERIC / ALPHANUMERIC
       Type of pin code that will be generated and sent as part of the OTP
       message. Can be set to numeric or alphanumeric.
    phone_number : string
        Represents the destination phone number. Phone number must be in
        international format.
    pin_attempts : integer
        Represents the number of times the PIN can be attempted before
        expiration. Has a minimum of one attempt.
    pin_time_to_live : integer
        Represents how long the pin is valid before expiration. The time is
        in minutes. The minimum time value is 0 and maximum is 60.
    pin_length : integer
        Length of the pin code. Has a minimum of 4 and maximum of 8.
    """
    payload = {
        'api_key' : api_key,
        'pin_type' : "NUMERIC",
        'phone_number' : phone_number,
        'pin_attempts' : 3,
        'pin_time_to_live' : 0,
        'pin_length' : 6,
    }

    headers = {
        'Content-Type' : 'application/json',
    }

    response = requests.post(SEND_TOKEN_IN_APP, headers=headers, json=payload)
    response = json.loads(response.content)
    return response