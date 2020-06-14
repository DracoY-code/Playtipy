# Playtipy

**Playtipy** is a *Spotify* terminal based client app written in *Python*.

>**Note**: You're welcome to modify the code under the license agreement. I don't have a premium account and music playback requires premium privileges. Contact me if the script works correctly on Spotify premium.




## Setup

Prerequisites:
* Spotify account ;)
* Python3
* Pip
* Spotipy
* Configparser (to parse .cfg files; system variables can be used too from `sys` module)


### Python3 && Pip

Python3 is needed to run the script. It comes with pip (package installer). On most Linux systems, it is already installed. For other systems, install from https://www.python.org/downloads/


### Spotipy

Spotipy is installed using pip. It is an API for creating Spotify apps. For windows, open cmd and use
                      
    pip install spotipy
                      
You can also clone the repository (better do this): https://github.com/plamere/spotipy
>Docs: https://spotipy.readthedocs.io/en/2.12.0/


### Configparser

Configparser parses a `.cfg` file. It can be installed using pip too.
                    
    pip install configparser
                    
Now you are good to go!


### Spotify Development && config.cfg

1. Create a spotify account on https://spotify.com/ (if you already have, it's not for you!)
2. Create a Spotify app at https://developer.spotify.com/dashboard/applications/.
3. Add a `Redirect URI` in the settings of the app.
4. If you are using configparser, add Client ID in `CLIENT_ID`.
5. Add Client secret in `CLIENT_SECRET` (hush; it's a secret).
6. Go to your account and copy `Profile Link`.
7. Paste the link in `USER_ID` and extract the numbers in the end only. (Do not write the whole link)
8. Save and you just need to authorize the app by running the script.




## Dev Contacts

Reviews are welcome. You can even contact me on following contacts.

>* [GitHub](https://github.com/DracoY-code)
>* [Reddit](https://reddit.com/user/Red_Death_08)
>* [Discord](https://discord.gg/@DracoY#5089)
