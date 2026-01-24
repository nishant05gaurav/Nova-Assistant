import webbrowser
import os
import platform
from assistant.speech import speak

def check_system():
    """
    Identify the operating system of the machine.

    This function uses the `platform` module to detect which OS is 
    currently running (Windows, macOS, or Linux). It simply returns 
    the system name as a string.
    """

    # Get the name of the operating system 
    namePlatform = platform.system()
    return namePlatform

def openLinkSystem(link):
    """
    Open a URL using system-level commands based on the OS type.

    This function acts as a fallback if `webbrowser.open()` fails.
    It detects the user's operating system and then uses the appropriate 
    system command to open the given URL manually.
    """
    
    # If the user is on Windows, use the 'start' command
    if check_system() == "Windows":
        os.system(f"start {link}")
    
    # If macOS (Darwin), use the 'open' command
    elif check_system() == "Darwin":
        os.system(f"open {link}")
        
     # If Linux, use the standard 'xdg-open' command
    else:
        os.system(f"xdg-open {link}")

def openLink(command):
    """
    Open a website in the user's default web browser based on voice command.

    This function checks if the user's command contains phrases like 
    'open google', 'open youtube', etc. It matches the website name from a 
    predefined dictionary and attempts to open the corresponding URL using 
    the `webbrowser.open()` function. If that fails, it falls back to 
    `openLinkSystem()` to handle the request
    """
    
    # Dictionary mapping common website names to their URLs
    site_dict = {
        "google":   "https://google.com",
        "facebook": "https://www.facebook.com/profile.php?id=100093097620855",
        "youtube":  "https://youtube.com",
        "instagram":"https://www.instagram.com/_im__nishant_/",
        "linkedin": "https://www.linkedin.com/in/nishant-05-gaurav/",
        "github":   "https://github.com/nishant05gaurav",
        "twitter":  "https://x.com/_im_nishant14"
    }

    for site, link in site_dict.items():
        if f"open {site}" in command.lower():
            try:
                # Try opening the link in default web browser
                webbrowser.open(link)
            except:
                # Fallback method if webbrowser fails
                openLinkSystem(link)
            
            speak(f"Opening {site}...")
            return True 

    return False 