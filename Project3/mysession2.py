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
#gets all available slots for the specified type
def get_slots(objectType):
    while True:
        try:
            if objectType == band:
                print("Getting available slots for band ...")
            else:
                print("Getting available slots for hotel ...")
            slots = objectType.get_slots_available()
            free_slots = []
            #appends slots to a list and retruns it
            for slot in slots:
                free_slots.append(slot["id"])
            break
        except Exception as e:
            print(e)
            continue
    return free_slots

#gets the slots that are held by the object and returns a list of them
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

#gets the intersect of 2 lists and returns it (see common slots)
def intersect(list1,list2):
    newList = [value for value in list1 if value in list2]
    return newList

#removes a slot and calls release slot
def remove_slots(objectType,slot):
    while True:
        try:
            release = objectType.release_slot(slot)
            break
        except Exception as e:
            print(e)
            continue

#checks that band and hotel are the same at the beginning
def checkSlots(band,hotel):
    #get the slots held by both band and hotel
    bandSlots = get_held_slots(band)
    hotelSlots = get_held_slots(hotel)
    #get any matching slots
    CommonSlot = intersect(bandSlots,hotelSlots)
    #get any slots that are different
    bandDifference = list(set(bandSlots) ^ set(CommonSlot))
    #if no slots are different, remove the larger slot
    if len(bandSlots) != 0:
        #both the same but have 2 slots
        if len(bandDifference) == 0 and len(bandSlots) >1:
            if bandSlots[0] > bandSlots[1]:
                remove_slots(band,bandSlots[0])
            else:
                remove_slots(band,bandSlots[1])
        #both the same and just 1 slot
        elif len(bandDifference) == 0:
            pass
        #different slots
        elif len(bandDifference) >0:
            for i in range(len(bandDifference)):
                remove_slots(band,bandDifference[i])

    #repeat for hotel
    hotelDifference = list(set(hotelSlots) ^ set(CommonSlot))
    if len(hotelSlots) !=0:
        if len(hotelDifference) == 0 and len(hotelSlots) >1:
            if hotelSlots[0] > hotelSlots[1]:
                remove_slots(hotel,hotelSlots[0])
            else:
                remove_slots(hotel,hotelSlots[1])
        
        elif len(hotelDifference) == 0:
            pass
        elif len(hotelDifference) >0:
            for i in range(len(hotelDifference)):
                remove_slots(hotel,hotelDifference[i])

#returns the combined slots that are available
def get_combined_slots(band,hotel):
    band_slots = get_slots(band)
    hotel_slots = get_slots(hotel)
    combined = intersect(band_slots,hotel_slots)
    return combined



#########################################  MAIN BODY  ##################################################
print("Checking previous band and hotel slots...")
band_slots = get_held_slots(band)
hotel_slots = get_held_slots(hotel)
if len(band_slots) ==0:
    print("Held slots by Band: No Slots held")
else:
    print("Held slots by Band: ",','.join(band_slots))
if len(hotel_slots) ==0:
    print("Held slots by Hotel: No Slots held")
else:
    print("Held slots by Hotel: ",','.join(hotel_slots))
print("Comparing to find matching slots...")
checkSlots(band,hotel)
band_slots = get_held_slots(band)
hotel_slots = get_held_slots(hotel)
if len(band_slots) ==0:
    print("Held slots by Band: No Slots held")
else:
    print("Held slots by Band: ",','.join(band_slots))
if len(hotel_slots) ==0:
    print("Held slots by Hotel: No Slots held")
else:
    print("Held slots by Hotel: ",','.join(hotel_slots))

#if initially both are empty, then get the earliest slot
if len(band_slots) == 0:
    while True:
        try:
            free_slots = get_combined_slots(band,hotel)
            reserve_band = band.reserve_slot(free_slots[0])
            reserve_hotel = hotel.reserve_slot(free_slots[0])

            if (len(get_held_slots(band)) ==1 and len(get_held_slots(hotel)) == 1):
                break
        except Exception as e:
            print(e)
            checkSlots(band,hotel)
            continue

    band_slots = get_held_slots(band)
    hotel_slots = get_held_slots(hotel)
    if len(band_slots) ==0:
        print("Held slots by Band: No Slots held")
    else:
        print("Held slots by Band: ",','.join(band_slots))
    if len(hotel_slots) ==0:
        print("Held slots by Hotel: No Slots held")
    else:
        print("Held slots by Hotel: ",','.join(hotel_slots))

#recheck the slots atleast twice to see if there are any earlier slots
attempts = 1
while attempts <3:
    redo = False
    if attempts >= 3:
         break
    try:
        print("Attempt in finding better slot: ",attempts)
        free_slots = get_combined_slots(band,hotel)
        bandSlots = get_held_slots(band)
        early_slot = bandSlots[0]
        if int(bandSlots[0]) > int(free_slots[0]):
            print("Previous Slot: ",early_slot)
            print("Potential new slot: ",free_slots[0])
            reserve_band = band.reserve_slot(free_slots[0])
            reserve_hotel = hotel.reserve_slot(free_slots[0])
            band_slots = get_held_slots(band)
            hotel_slots = get_held_slots(hotel)
            #if you find an earlier slot then reset the rechk attempts so we can check for anything earlier
            if (len(band_slots) == 2 and len(hotel_slots) ==2):
                print("Resetting recheck attempts")
                attempts = 1
                redo = True
            
            #remove the slots that are no longer needed
            if get_held_slots(band) == get_held_slots(hotel):
                remove_slots(hotel,early_slot)
                remove_slots(band,early_slot)
        band_slots = get_held_slots(band)
        hotel_slots = get_held_slots(hotel)
        if len(band_slots) ==0:
            print("Held slots by Band: No Slots held")
        else:
            print("Held slots by Band: ",','.join(band_slots))
        if len(hotel_slots) ==0:
            print("Held slots by Hotel: No Slots held")
        else:
            print("Held slots by Hotel: ",','.join(hotel_slots))
        if redo != True:
            attempts +=1
    except Exception as e:
        print(e)
        checkSlots(band,hotel)
        attempts +=1
        continue

band_slots = get_held_slots(band)
hotel_slots = get_held_slots(hotel)

print("\nThe program has finished running")
print("The earliest matching slot found is: ")
print("Band slot: ",band_slots[0])
print("Hotel slot: ",hotel_slots[0])