import requests
import datetime
import json

api_key = "your_api_key_goes_here"

resolve_input = input("\nEnter Vanity Steam url (leave blank to skip and enter Steam64 ID instead): ")

try:
    get_sid = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=" + api_key + "&vanityurl=" + resolve_input).json()

    #print("Steam64 ID:", get_sid["response"]["steamid"])
except Exception:
    print("Error!")
    quit()

try:
    sid_input = get_sid["response"]["steamid"]
except Exception:
    sid_input = input("Enter Steam64 ID: ")

try:
    get_info = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=" + api_key +"&steamids=" + sid_input).json()

    prof_vis = get_info["response"]["players"][0]["communityvisibilitystate"]

    print("\nUser Info")
    print("Name:", get_info["response"]["players"][0]["personaname"])

    if prof_vis == 3:
        try:
            print("Real Name:", get_info["response"]["players"][0]["realname"])
        except Exception:
            print("Real Name: None")

        try:
            print("Country:", get_info["response"]["players"][0]["loccountrycode"])
        except Exception:
            print("Country: None")

        def availability_switch(availability_state):
            match availability_state:
                case 0:
                    return "Offline" 
                case 1:
                    return "Online"
                case 2:
                    return "Busy"
                case 3:
                    return "Away"
                case 4:
                    return "Snooze"
                case 5:
                    return "Looking to trade"
                case 6:
                    return "looking to play"
        
        availability_state_state = availability_switch(get_info["response"]["players"][0]["personastate"])

        print("Availability:", availability_state_state)

        try:
            print("Currently Playing:", get_info["response"]["players"][0]["gameid"], "AppID")
        except Exception:
            print("Currently Playing: None")

        try:
            acc_created = get_info["response"]["players"][0]["timecreated"]

            print("Account Creation Date:", datetime.datetime.fromtimestamp(acc_created).strftime("%d/%m/%Y"))
        except Exception:
            print("Account Creation Date: Unknown")


        print("Profile Visibility: Public")
    else:
        print("Profile Visibility: Private")
    

    
    print("\nUser Restrictions")
    try:
        get_bans = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerBans/v0001/?key=" + api_key + "&steamids=" + sid_input).json()

        def com_switch(com):
            match com:
                case True:
                    return "Banned"
                case False:
                    return "None"
        
        def vac_switch(vac):
            match vac:
                case True:
                    return "Banned"
                case False:
                    return "None"
        
        def eco_switch(eco):
            match eco:
                case "banned":
                    return "Banned"
                case "none":
                    return "None"   

        print("Community:", com_switch(get_bans["players"][0]["CommunityBanned"]))
        print("Economy:", eco_switch(get_bans["players"][0]["EconomyBan"]))
        print("VAC:", vac_switch(get_bans["players"][0]["VACBanned"]), "\n")

    except Exception:
        print("Failed to load restrictions!")

#76561198281645509

except Exception:
    print("Error!")
    quit()
