#!/usr/bin/env python3

try:
    import requests
    import argparse
    import sys
    import time
    import string
    import random
    import urllib3
    import os
    import re

    from bs4 import BeautifulSoup
    from colored import fg, attr

except ImportError as i:
    print(f"{attr(1)}{fg(1)}[-]{attr(0)} Some libraries are missing !")
    print(f"{attr(1)}{fg(1)}[-]{attr(0)} Python error: {i}")

# Disable insecure SSL warnings
requests.packages.urllib3.disable_warnings()

def ascii():
    ascii_art = f"""{attr(1)}{fg(45)}   

 ______  ______   ______   ______  ______    
/\  == \/\  __ \ /\  ___\ /\__  _\/\  __ \   
\ \  _-/\ \  __ \\\ \___  \\\/_/\ \/\ \  __ \  
 \ \_\   \ \_\ \_\\\/\_____\  \ \_\ \ \_\ \_\ 
  \/_/    \/_/\/_/ \/_____/   \/_/  \/_/\/_/{attr(0)}      
                                       {fg(106)}v0.1{attr(0)}   
    """
    print(ascii_art)

class TimeMeasure:

    def time_estimate(arg=''):
        start = time.time()
        end = time.time()

        if arg == "start":
            return start
        
        if arg == "end":
            return end

class Search:
    
    def __init__(self, str_range):
        self.str_range = int(str_range)

    # LA = Length of Alphabet 
    # Essentially what string will be send to PasteBin
    def randomize_alpha(LA=8, str_range=0):
        alpha = string.ascii_letters + string.digits

        # Check if strings.txt exists where random strings will be inserted
        if not os.path.isfile("./strings.txt") and not os.path.exists("./strings.txt"):
            
            print(f"{attr(1)}{fg(129)}[?]{attr(0)} File 'strings.txt' doesn't exist !")
            print(f"{attr(1)}{fg(4)}[*]{attr(0)} Making 'strings.txt' !")
            
            strings_file = open("strings.txt", "w+")
            strings_file.close()
        
        else:
            print(f"{attr(1)}{fg(2)}[+]{attr(0)} File 'strings.txt' exists !")

        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Writing {str_range} strings in 'strings.txt' !")        
        
        with open("./strings.txt", "w") as strings_file:
            
            for strings in range(str_range):
                strings = ''.join(random.sample(alpha, LA))
                strings_file.write(strings)
                # Just need to apend a newline between each string
                strings_file.write('\n')
    
            strings_file.close()
        
    def search_request(str_range=0):
        begin = TimeMeasure.time_estimate("start")
        
        #if str_range != 0:
        Search.randomize_alpha(8, str_range)

        # Safari cuz why not look fancy :P
        user_agent = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            }
        
        # Initiallise GET request
        r = requests.Session()

        # Check each string in the strings.txt file
        with open("./strings.txt", "r") as strings_file:
            for string in strings_file:
                
                s = string.strip()
                URL = f"https://pastebin.com/{s}"
                
                try:
                    # Perform GET
                    search = r.get(
                        URL, 
                        headers=user_agent,
                        verify=False
                        )
                    
                    # Find out what's the response code
                    if search.status_code == 404:
                        print(f"{attr(1)}{fg(3)}[!]{attr(0)} Response {fg(1)}404{attr(0)} for - {fg(1)}{s}{attr(0)}")

                    elif search.status_code == 200:
                        URL = f"https://pastebin.com/raw/{s}"
                        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Response {fg(2)}200{attr(0)} for - {fg(6)}{s}{attr(0)}")
                        print(f"- URL: {URL}")
                    
                    else:
                        print(f"{attr(1)}{fg(1)}[-]{attr(0)} Response is different that 404 or 200 for - {fg(13)}{s}{attr(0)}")
                        # sys.exit(1) # Not sure if we should exit here...??

                except KeyboardInterrupt:
                    print(f"{attr(1)}{fg(203)}[x]{attr(0)} Killing the script..\r\n")
                    sys.exit(0)
        
        strings_file.close()
        print(f"Time taken to complete: {TimeMeasure.time_estimate('end') - begin} seconds")

class CheckBin:
    
    def view_pastebin(string):
        
        print(f"{attr(1)}{fg(2)}[+]{attr(0)} Checking the contents of {fg(12)}{string}{attr(0)}")

        if string == "" or len(string) < 8 or len(string) > 8:
            print(f"{attr(1)}{fg(3)}[!]{attr(0)} An 8 character string has to be provided.")
            print(f"{attr(1)}{fg(3)}[!]{attr(0)} Example: {sys.argv[0]} -c \"KHK2ndnC\"")
            sys.exit(1)
        
        elif string != "" and len(string) == 8:
            
            r = requests.Session()
            URL = f"https://pastebin.com/raw/{string}"
            user_agent = {
            "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15"
            }

            search = r.get(
                URL, 
                headers=user_agent,
                verify=False
                )

            if search.status_code == 200:
                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Saving the contents of {fg(12)}{string}{attr(0)} to {fg(3)}output/{string}.pastebin.txt{attr(0)}")
                if not os.path.isdir("output") and not os.path.exists("output"):
                    print(f"{attr(1)}{fg(129)}[?]{attr(0)} Folder 'output' doesn't exist !")
                    print(f"{attr(1)}{fg(4)}[*]{attr(0)} Making folder 'output' !")
                    
                    try:
                        os.mkdir("output")
                    except Exception as e:
                        print(f"{attr(1)}{fg(3)}[!]{attr(0)} Exception when making directory !")
                        print(f"{e}")

                
                with open(f"output/{string}.pastebin.txt", "w") as pastebin_entry:
                    pastebin_entry.write(search.text)
                    pastebin_entry.close()

                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Showing the content of {fg(12)}{string}{attr(0)} PasteBin entry !")
                print(f"{attr(1)}{fg(2)}[+]{attr(0)} Content:")
                print(50 * "-")
                print(search.text)
                sys.exit(0)
            
            elif search.status_code == 404:
                print(f"{attr(1)}{fg(3)}[!]{attr(0)} Response {fg(1)}404{attr(0)} for - {fg(1)}{string}{attr(0)}")
                sys.exit(1)
            
            else:
                print(f"{attr(1)}{fg(1)}[-]{attr(0)} Response is different that 404 or 200 for - {fg(13)}{string}{attr(0)}")
                sys.exit(1)

        else:
            print(f"{attr(1)}{fg(1)}[-]{attr(0)} Something is not right ! Try again !")
            sys.exit(1)

# !! Implement somehow, good to look for usernames, passwords, emails, etc. (Anything of value) !!
# Get the most recent 200 pastes from pastebin.com/archive
def get_recent():
    
    URL = requests.get('https://pastebin.com/archive')
    href_regex = r"<a href=\"\/(.+?)\">(.+?)<\/a><\/td>"
    
    pastes = re.findall(href_regex, str(URL.text))

    recent_pastes = []

    for paste_id, paste_title in pastes:
        #recent_pastes.append(paste_id)
        return paste_title, paste_id

print(get_recent())

#Initilize parser for arguments
def argparser():
    parser = argparse.ArgumentParser(description='Pasta - A PasteBin Scraper')
    parser.add_argument("-s", 
            "--search", 
            help="Search PasteBin with a set of strings", 
            action="store_true", 
            required=False
            )
    
    parser.add_argument("-rs",
            "--range_str", 
            help="How many strings to generate", 
            type=int, 
            required=False
            # default=5
            )
    
    parser.add_argument("-c", 
            "--check", 
            help="Check contents of a specific PasteBin entry", 
            type=str, 
            required=False
            )
            
    args = parser.parse_args(args=None if sys.argv[1:] else ['-h']) #Show help menu if no arguments provided
    #args = parser.parse_args()
    
    if args.search:
        if args.range_str:
            str_range = args.range_str
        
        Search.search_request(str_range)

    if args.range_str and not args.search:
        str_range = args.range_str
        Search.randomize_alpha(8, str_range)

    if args.check:
        string = args.check
        CheckBin.view_pastebin(string)

if __name__ == "__main__":
    try:
        ascii()
        argparser()

    except Exception as e:
        print(f"{attr(1)}{fg(1)}[-]{attr(0)} An exception arose !")
        print(f"{attr(1)}{fg(1)}[-]{attr(0)} Exception: {e}")
