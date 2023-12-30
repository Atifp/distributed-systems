#!/usr/bin/python3

import reservationapi
import configparser
from exceptions import (
    BadRequestError, InvalidTokenError, BadSlotError, NotProcessedError,
    SlotUnavailableError,ReservationLimitError,ExceededRetriesLimitError)
# Load the configuration file containing the URLs and keys
config = configparser.ConfigParser()
config.read("api.ini")

# Create an API object to communicate with the hotel API
hotel  = reservationapi.ReservationApi(config['hotel']['url'],
                                       config['hotel']['key'],
                                       int(config['global']['retries']),
                                       float(config['global']['delay']))

# Your code goes here
# Create an API object to communicate with the band API
band  = reservationapi.ReservationApi(config['band']['url'],
                                       config['band']['key'],
                                       int(config['global']['retries']),
                                      float(config['global']['delay']))

#gets the available slots
def get_slots(objectType):
    while True:
        try:
            print("Getting available slots...")
            slots = objectType.get_slots_available()
            print(slots,"\n")
            free_slots = []
            for slot in slots:
                free_slots.append(slot["id"])
            break
        except Exception as e:
            print(e)
            continue
    return free_slots

#gets the slots held calling the required function in reservationapi
def get_held_slots(objectType):
    while True:
        try:
            mySlots = objectType.get_slots_held()
            free_slots = []
            for slot in mySlots:
                free_slots.append(slot["id"])
            break
        except InvalidTokenError:
            print("The API token was invalid or missing.")
            quit()   
        except Exception as e:
            print(e)
            continue
    return free_slots

#checks that the size of the slots initially is 1
def checkSlots(objectType):
    while True:
        try:
            mySlots = get_held_slots(objectType)
            #if the size is 2, remove the later slot
            if len(mySlots) == 2:
                if mySlots[0] > mySlots[1]:
                    release = objectType.release_slot(mySlots[0])
                else:
                    release = objectType.release_slot(mySlots[1])
            break
        except Exception as e:
            print(e)
            continue

#book a free slot by checking what is available
def book_free_slot(objectType):
    while True:
        try:
            free_slots = get_slots(objectType)
            reserve = objectType.reserve_slot(free_slots[0])
            break
        except Exception as e:
            print(e)
            continue

#remove the first slot that is held
def remove_slots(objectType):
    while True:
        try:
            mySlots = get_held_slots(objectType)
            release = objectType.release_slot(mySlots[0])
            break
        except Exception as e:
            print(e)
            continue

print("Checking slots for hotel...")
mySlots = get_held_slots(hotel) #get the slots that are held
if len(mySlots) ==0:
    print("Held slots by Hotel: No Slots held")
else:
    print("Held slots by Hotel: ",','.join(mySlots))

print("Checking slots for hotel...")
checkSlots(hotel) # Initally check to make sure there is only 1/0 slot booked
mySlots = get_held_slots(hotel) #get the slots that are held
if len(mySlots) ==0:
    print("Held slots by Hotel: No Slots held")
else:
    print("Held slots by Hotel: ",','.join(mySlots))
#book one slot or 2 depending on how many slots are free
if len(mySlots) == 1:
    book_free_slot(hotel)
elif len(mySlots) == 0:
    book_free_slot(hotel)
    book_free_slot(hotel)

#print the new slots that are held
mySlots = get_held_slots(hotel) 
if len(mySlots) ==0:
    print("Held slots by Hotel: No Slots held")
else:
    print("Held slots by Hotel: ",','.join(mySlots))

#remove each slot
if len(mySlots) == 1:
    remove_slots(hotel)
elif len(mySlots) ==2:
    remove_slots(hotel)
    remove_slots(hotel)
#print that there are no more slots held
mySlots = get_held_slots(hotel) 
if len(mySlots) ==0:
    print("Held slots by Hotel: No Slots held")
else:
    print("Held slots by Hotel: ",','.join(mySlots))

##------------------- Band ---------------------##
print()
print("Checking slots for Band...")
mySlots = get_held_slots(band) #get the slots that are held
if len(mySlots) ==0:
    print("Held slots by Band: No Slots held")
else:
    print("Held slots by Band: ",','.join(mySlots))

checkSlots(band) # Initally check to make sure there is only 1/0 slot booked
mySlots = get_held_slots(band) #get the slots that are held
if len(mySlots) ==0:
    print("Held slots by Band: No Slots held")
else:
    print("Held slots by Band: ",','.join(mySlots))
#book one slot or 2 depending on how many slots are free
if len(mySlots) == 1:
    book_free_slot(band)
elif len(mySlots) == 0:
    book_free_slot(band)
    book_free_slot(band)

#print the new slots that are held
mySlots = get_held_slots(band) 
if len(mySlots) ==0:
    print("Held slots by Band: No Slots held")
else:
    print("Held slots by Band: ",','.join(mySlots))

#remove each slot
if len(mySlots) == 1:
    remove_slots(band)
elif len(mySlots) ==2:
    remove_slots(band)
    remove_slots(band)
#print that there are no more slots held
mySlots = get_held_slots(band)
if len(mySlots) ==0:
    print("Held slots by Band: No Slots held")
else:
    print("Held slots by Band: ",','.join(mySlots))