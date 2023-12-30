""" Reservation API wrapper

This class implements a simple wrapper around the reservation API. It
provides automatic retries for server-side errors, delays to prevent
server overloading, and produces sensible exceptions for the different
types of client-side error that can be encountered.
"""

# This file contains areas that need to be filled in with your own
# implementation code. They are marked with "Your code goes here".
# Comments are included to provide hints about what you should do.

import requests
import simplejson
import warnings
import time

from requests.exceptions import HTTPError
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError,ReservationLimitError,ExceededRetriesLimitError)

class ReservationApi:
    def __init__(self, base_url: str, token: str, retries: int, delay: float):
        """ Create a new ReservationApi to communicate with a reservation
        server.

        Args:
            base_url: The URL of the reservation API to communicate with.
            token: The user's API token obtained from the control panel.
            retries: The maximum number of attempts to make for each request.
            delay: A delay to apply to each request to prevent server overload.
        """
        self.base_url = base_url
        self.token    = token
        self.retries  = retries
        self.delay    = delay

    def _reason(self, req: requests.Response) -> str:
        """Obtain the reason associated with a response"""
        reason = ''

        # Try to get the JSON content, if possible, as that may contain a
        # more useful message than the status line reason
        try:
            json = req.json()
            reason = json['message']

        # A problem occurred while parsing the body - possibly no message
        # in the body (which can happen if the API really does 500,
        # rather than generating a "fake" 500), so fall back on the HTTP
        # status line reason
        except simplejson.errors.JSONDecodeError:
            if isinstance(req.reason, bytes):
                try:
                    reason = req.reason.decode('utf-8')
                except UnicodeDecodeError:
                    reason = req.reason.decode('iso-8859-1')
            else:
                reason = req.reason

        return reason


    def _headers(self) -> dict:
        """Create the authorization token header needed for API requests"""
        # Your code goes here
        headers = {"accept": "application/json","Authorization" : "Bearer " +self.token}
        return headers

    def errorHandling(self,code,r,tries):
        if code == 400:
            print("Status code: ",code)
            raise BadRequestError("The requested slot does not exist")
            
        elif code == 401:
            print("Status code: ",code)
            raise InvalidTokenError("The API token was invalid or missing.")
            
        elif code == 403:
            print("Status code: ",code)
            raise BadSlotError("The requested slot does not exist.")
            
        elif code == 404:
            print("Status code: ",code)
            raise NotProcessedError("The request has not been processed.")
            
        elif code == 409:
            print("Status code: ",code)
            raise SlotUnavailableError("The requested slot is not available.")
            
        elif code == 451:
            print("Status code: ",code)
            raise ReservationLimitError("The client already holds the maximum number of reservations.")
            
        else:
            print(r.json()['message'],"| Status code: "+str(code),"Retrying...")
            print("Number of Attempts out of 3: ",tries+1)
            print("-----------------------------------------------------------")
            return tries +1


    def _send_request(self, method: str, endpoint: str) -> dict:
        """Send a request to the reservation API and convert errors to
           appropriate exceptions"""
        # Your code goes here

        # Allow for multiple retries if needed
        # Perform the request.
        tries =0
        while tries < self.retries:
            if method == "GET":
                URL = self.base_url + endpoint
                r = requests.get(URL,headers = self._headers())
                time.sleep(self.delay)
                code = r.status_code
                if code == 200:
                    # print("-------------------------------------------")
                    # if endpoint == "/reservation":
                    #     print("Request Successful | Checking Held Slots...")
                    # else:
                    #     print("Request Successful ")
                    return r.json()
                else:
                    tries = self.errorHandling(code,r,tries)

            if method == "DELETE":
                URL = self.base_url + endpoint
                r = requests.delete(URL,headers = self._headers())
                time.sleep(self.delay)
                code = r.status_code
                if code == 200:
                    print("Request Successful | Releasing slot...")
                    print(r.json()['message'])
                    return r.json()
                else:
                    tries = self.errorHandling(code,r,tries)

            if method == "POST":
                URL = self.base_url + endpoint
                r = requests.post(URL,headers = self._headers())
                time.sleep(self.delay)
                code = r.status_code
                if code == 200:
                    print("Request Successful | Reserving slot...")
                    print("Slot ",r.json()['id']," Reserved")
                    return r.json()
                else:
                    tries = self.errorHandling(code,r,tries)

        if tries >= self.retries:
            raise ExceededRetriesLimitError("The Number of retries have been exceeded, Reattempting new request...")
            # Delay before processing the response to avoid swamping server.
            
            # 200 response indicates all is well - send back the json data.
            # 5xx responses indicate a server-side error, show a warning
            # (including the try number).

            # 400 errors are client problems that are meaningful, so convert
            # them to separate exceptions that can be caught and handled by
            # the caller.

            # Anything else is unexpected and may need to kill the client.

        # Get here and retries have been exhausted, throw an appropriate
        # exception.



    def get_slots_available(self):
        """Obtain the list of slots currently available in the system"""
        # Your code goes here
        slots = self._send_request("GET","/reservation/available")
        return slots


    def get_slots_held(self):
        """Obtain the list of slots currently held by the client"""
        # Your code goes here
        slots_held = self._send_request("GET","/reservation")
        return slots_held

    def release_slot(self, slot_id):
        """Release a slot currently held by the client"""
        # Your code goes here
        self._send_request("DELETE",("/reservation/"+ str(slot_id)))

    def reserve_slot(self, slot_id):
        """Attempt to reserve a slot for the client"""
        # Your code goes here
        self._send_request("POST",("/reservation/"+str(slot_id)))