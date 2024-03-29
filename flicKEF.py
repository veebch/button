#!/bin/bash python3

import asyncio
import os
from aioflic import *


def dostuff(channel, click_type, was_queued, time_diff):
# This is the function that can be adapted to invoke other scripts/commands
# There are three seperate commands for Single Click, Double Click, and Hold respectively, edit them to contain whatever you find useful
    if str(click_type)=="ClickType.ButtonSingleClick":
# Just want to toggle between our two used outputs (possibly add mute check)
        state=os.popen("/home/pi/kefctl/kefctl -s | grep Source | awk \'/Source/{print $NF}\'").read().strip('\n')
        print(state)
        if state=='Optical':
            os.system('/home/pi/kefctl/kefctl -i usb')
        elif state=='USB':
            os.system('/home/pi/kefctl/kefctl -i optical')
        else:
            os.system('/home/pi/kefctl/kefctl -i usb')
    elif str(click_type)=="ClickType.ButtonDoubleClick":
# Double Click to toggle muted
        os.system('/home/pi/kefctl/kefctl -t')
    else:
# hold to turn off 
        os.system('/home/pi/kefctl/kefctl -o')
    return

def got_button(bd_addr):
    cc = ButtonConnectionChannel(bd_addr)
    cc.on_button_single_or_double_click_or_hold = dostuff
 #       lambda channel, click_type, was_queued, time_diff: \
 #           print("Simple or Double or hold {} {} {}".format(channel.bd_addr,str(click_type),time_diff))
    cc.on_connection_status_changed = \
        lambda channel, connection_status, disconnect_reason: \
            print(channel.bd_addr + " " + str(connection_status) + (" " + str(disconnect_reason) if connection_status == ConnectionStatus.Disconnected else ""))
    client.add_connection_channel(cc)

def got_info(items):
    print(items)
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        got_button(bd_addr)
    scan()
        
def on_found_private_button(scan_wizard):
        print("Found a private button. Please hold it down for 7 seconds to make it public.")

def on_found_public_button(scan_wizard, bd_addr, name):
        print("Found public button " + bd_addr + " (" + name + "), now connecting...")

def on_button_connected(scan_wizard, bd_addr, name):
        print("The button was connected, now verifying...")
        got_button(bd_addr)

def on_completed(scan_wizard, result, bd_addr, name):
        print("Scan wizard completed with result " + str(result) + ".")
        if result == ScanWizardResult.WizardSuccess:
                print("Your button is now ready. The bd addr is " + bd_addr + ".")


def scan():
    print("Starting the scan")
    mywiz=ScanWizard()
    mywiz.on_found_private_button = on_found_private_button
    mywiz.on_found_public_button = on_found_public_button
    mywiz.on_button_connected = on_button_connected
    mywiz.on_completed = on_completed
    client.add_scan_wizard(mywiz)

            
FlicClient.on_get_info=got_info
loop = asyncio.get_event_loop()  
try:
    coro = loop.create_connection(lambda: FlicClient( loop),
                            'localhost', 5551)
    conn,client=loop.run_until_complete(coro)
    client.on_get_info=got_info
    client.get_info()
    loop.run_forever()
except  KeyboardInterrupt:
    print("\n","Exiting at user's request")
finally:
    # Close the server
    client.close()
    loop.close()   
