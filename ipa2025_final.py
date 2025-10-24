#######################################################################################
# Yourname: Peerapat Meesangngoen
# Your student ID: 66070138
# Your GitHub Repo: https://github.com/peerapat138/IPA2025-Final.git

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import os
import requests
from requests_toolbelt import MultipartEncoder
import time
import json
from dotenv import load_dotenv

import restconf_final
import netconf_final
import netmiko_final
import ansible_final
import ansible_motd_final
import netmiko_motd_final

load_dotenv()
#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("WEBEX_TOKEN")
WEBEX_MESSAGES_API = "https://webexapis.com/v1/messages"
ROOM_ID_GET_MESSESGE = os.environ.get("ROOM_ID")

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId

restconf =False
netconf = False
motd = False
while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)
   
    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": ROOM_ID_GET_MESSESGE, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        WEBEX_MESSAGES_API,
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    if not message.startswith("/66070138"):
        continue
    message_command = message.split()
    ip_specified = False
    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070138"):
        print("Received message: " + message)
        # extract the command
        if len(message_command) == 3:
            command = message_command[2]
            ip = message_command[1]
            ip_specified = True
            print(ip)
            print(command)
        else:
            command = message_command[1]
            print(command)
        if command in ["restconf", "netconf"]:
            if command == "restconf":
                restconf = True
                netconf =False
                responseMessage = "Ok: Restconf"
            elif command == "netconf":
                restconf =False
                netconf = True
                responseMessage ="Ok: Netconf"
# 5. Complete the logic for each command
        elif command in ["gigabit_status", "showrun"]:
            if command == "gigabit_status":
                responseMessage =netmiko_final.gigabit_status(ip)
            elif command == "showrun":
                if ip == "10.0.15.61":
                    ip = "R1-Exam"
                elif ip == "10.0.15.62":
                    ip = "R2-Exam"
                elif ip == "10.0.15.63":
                    ip = "R3-Exam"
                elif ip == "10.0.15.64":
                    ip = "R4-Exam"
                elif ip == "10.0.15.65":
                    ip = "R5-Exam"
                responseMessage = ansible_final.showrun(ip)
        elif len(message_command) >= 3 and message_command[2] == "motd":
            ip = message_command[1]
            motd = True
            if len(message_command) > 3:
                # มีข้อความ motd ตามหลัง
                motd_text = " ".join(message_command[3:])
                responseMessage = ansible_motd_final.set_motd(ip, motd_text)
            else:
                # ไม่มีข้อความ -> แสดงค่า MOTD
                responseMessage = netmiko_motd_final.get_motd(ip)
        elif restconf == True and ip_specified == True:
            if command == "create":
                responseMessage = restconf_final.create(ip)
            elif command == "delete":
                responseMessage = restconf_final.delete(ip)
            elif command == "enable":
                responseMessage = restconf_final.enable(ip)
            elif command == "disable":
                responseMessage = restconf_final.disable(ip)
            elif command == "status":
                responseMessage =restconf_final.status(ip)
            elif command == "gigabit_status":
                responseMessage =netmiko_final.gigabit_status(ip)
            elif command == "showrun":
                if ip == "10.0.15.61":
                    ip = "R1-Exam"
                elif ip == "10.0.15.62":
                    ip = "R2-Exam"
                elif ip == "10.0.15.63":
                    ip = "R3-Exam"
                elif ip == "10.0.15.64":
                    ip = "R4-Exam"
                elif ip == "10.0.15.65":
                    ip = "R5-Exam"
                responseMessage = ansible_final.showrun(ip)
            else:
                responseMessage = "Error: No command or unknown command"
        elif netconf == True and ip_specified == True:
            if command == "create":
                responseMessage = netconf_final.create(ip)
            elif command == "delete":
                responseMessage = netconf_final.delete(ip)
            elif command == "enable":
                responseMessage = netconf_final.enable(ip)
            elif command == "disable":
                responseMessage = netconf_final.disable(ip)
            elif command == "status":
                responseMessage =netconf_final.status(ip)
            else:
                responseMessage = "Error: No command or unknown command"
        elif (ip_specified == False and motd == True):
            print("Error: No IP specified MOTD")
            responseMessage = "Error: No IP specified"
        elif (ip_specified == False and (restconf == True or netconf == True)):
            print("Error: No IP specified")
            responseMessage = "Error: No IP specified"
        elif (restconf == False and netconf == False):
            print("Error: No method specified")
            responseMessage = "Error: No method specified"
        
        
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail
        print("res: ",responseMessage)
        if command == "showrun" and responseMessage == 'ok':
            filename = f"show_run_66070138_{ip}.txt"
            fileobject = open(filename, 'rb')
            filetype = "text/plain"
            postData = {
                "roomId": ROOM_ID_GET_MESSESGE,
                "text": "show running config",
                "files": (filename, fileobject, filetype),
            }
            postData = MultipartEncoder(postData)
            HTTPHeaders = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": postData.content_type,
            }
        # other commands only send text, or no attached file.
        else:
            postData = {"roomId":ROOM_ID_GET_MESSESGE, "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

        # Post the call to the Webex Teams message API.
        r = requests.post(
            WEBEX_MESSAGES_API,
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )