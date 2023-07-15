from pypresence import Presence 
import time
import requests
import sys


#Cookie
robloxcookie = False
with open('cookie.txt','r') as f:
  robloxcookie = f.read()


current_user_name = False
current_user_display_name = False
request = False
current_user_id = ""
with open('userid.txt','r') as f:
  current_user_id = f.read()
while (current_user_id == ""):
  try:
    request = requests.get(url="https://users.roblox.com/v1/users/authenticated",
                                cookies={".ROBLOSECURITY": robloxcookie})
    current_user_id = request.json()["id"]
    current_user_name = request.json()["name"]
    current_user_display_name = request.json()["displayName"]
  except:
     print("")
     print("")
     print("No authenticated user found! Are you sure you put your cookie inside 'robloxcookie' value correctly?")
     print("It can also be a connection problem!")
     time.sleep(15)
     print("Retrying")
     continue

while (not request):
  try:
    request = requests.post(url="https://users.roblox.com/v1/users",
                            json={"userIds": [current_user_id], "excludeBannedUsers": True})
    current_user_name = request.json()["data"][0]["name"]
    current_user_display_name = request.json()["data"][0]["displayName"]
  except:
    print("")
    print("")
    print("Bad request! You sure your user id is the right one?")
    print("You can simply just leave it blank and it will get the user id of your current cookie")
    request = False
    time.sleep(15)
    print("Retrying")
    continue





#How do we display your name (keep the {0} and {1} as 0 means your display name and 1 means your username)
name_to_display = "{0} @{1}".format(current_user_display_name, current_user_name)


json = {
  "userIds": [
    current_user_id
  ]
}


isitrunning = False


client_id = '1102365919763775598'

RPC = False
while (not RPC):
  try:
    RPC = Presence(client_id)
    RPC.connect()
  except:
    print("")
    print("")
    print("Application error! Is discord open?")
    time.sleep(15)
    continue
    

start = int(time.time())
not_in_game = False
previously_in_game_or_not = False
previous_game_name = ""
previous_job_id = ""
changed_state = True
first_execution = True


while True:
  try:
    request = requests.post(url="https://presence.roblox.com/v1/presence/users",
                headers={'Content-Type': 'application/json',
                          'Accept': 'application/json',
                          },
                cookies={".ROBLOSECURITY": robloxcookie},
                json=json)
  except:
      print("")
      print("")
      print("Network error on API! Are you connected to the internet?")
      time.sleep(15)
      continue
  

  not_in_game = request.json()["userPresences"][0]["userPresenceType"] != 2
  place = request.json()["userPresences"][0]["placeId"]
  job = request.json()["userPresences"][0]["gameId"]
  game_name = request.json()["userPresences"][0]["lastLocation"]


  if (not_in_game != previously_in_game_or_not):
    previously_in_game_or_not = not_in_game
    start = int(time.time())
    changed_state = True
  if (previous_game_name != game_name):
      previous_game_name = game_name
      start = int(time.time())
      changed_state = True
  if (previous_job_id != job):
      previous_job_id = job
      start = int(time.time())
      changed_state = True


  if (not_in_game and changed_state):
      if (first_execution): 
        print("")
        print("")
        print("User not in game!")
        print("Proceeding to commit first status update.")
        print("")
        print("")
        first_execution = False
      else:
        print("")
        print("")
        print("Left the game!")
        print("Proceeding status update.")
  elif(changed_state):
      if (first_execution):  
        print("")
        print("")
        print("User in game!")
        print("Proceeding to commit first status update.")
        print("")
        print("")
        first_execution = False
      else:
        print("")
        print("")
        print("Joined a new game server!")
        print("Proceeding status update.")


  if not_in_game:
    try: 
      RPC.update(
        large_image = "roblox",
        large_text = "Roblox logo",
        details = name_to_display,
        state = "Not in game",
        start = start,
        buttons = [
                    {"label": "User profile", "url": "https://www.roblox.com/users/{0}/profile".format(current_user_id)}, 
                  ]
      )
      changed_state = False
    except:
      print("")
      print("")
      print("Application error! Is discord open?")
      print("Reconnecting!")
      time.sleep(15)
      try:
        RPC = Presence(client_id)
        RPC.connect()
        print("Reconnected!")
      except:
        print("")
        print("")
        print("Reconnecting failed!! Check your discord to see if it's open!")
      continue
  else:
    try:
      RPC.update(
        large_image = "roblox",
        large_text = "Roblox logo",
        details = name_to_display,
        state = game_name,
        start = start,
        buttons = [
                    {"label": "Current server", "url": "roblox://experiences/start?placeId={0}&gameInstanceId={1}".format(place,job)}, 
                    {"label": "Game link", "url": "https://www.roblox.com/games/{0}".format(place)}, 
                  ]
      )
      changed_state = False
    except:
      print("")
      print("")
      print("Application error! Is discord open?")
      print("Reconnecting!")
      time.sleep(15)
      try:
        RPC = Presence(client_id)
        RPC.connect()
        print("Reconnected!")
      except:
        print("")
        print("")
        print("Reconnecting failed!! Check your discord to see if it's open!")
        continue
      continue

  time.sleep(15)
