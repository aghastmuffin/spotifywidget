import requests
import webbrowser
import os
import websockets
import asyncio
#optimization improve by checking if there is already a websocket open then instead of doing anyting attempting to interface with that
authorization_code = ""
async def echo(websocket, path):
    async for message in websocket:
        global authorization_code
        authorization_code = message
        print(authorization_code)
        await websocket.send("200")
        asyncio.get_event_loop().stop()

# Set your Spotify API credentials
client_id = '4385bb2dcac44cbda9b9b546d376f8c1'
redirect_uri = 'https://aghastmuffin.github.io/webhome/spotify/'
scope = 'user-read-currently-playing'  # Add necessary scopes here

# Step 1: Get the authorization code by opening the authentication window
auth_url = (
    f'https://accounts.spotify.com/authorize?client_id={client_id}'
    f'&response_type=code&redirect_uri={redirect_uri}&scope={scope}'
)
print("Opening authentication window...")
webbrowser.open(auth_url)

# Step 2: After user authorization, input the code from the redirected URL
try:
    start_server = websockets.serve(echo, "localhost", 8765)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(f"WSS An error occurred: {e}")
    authorization_code = input("Enter the code from the redirected URL: ")

# Step 3: Exchange authorization code for an access token
token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': 'b0301e4d7d7b4171a939aa3d8ce21c56',  # Add your actual client secret here
}
response = requests.post(token_url, data=token_data)

if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print("Access Token:", access_token)
    #os.system(f"py SPOTgui.py {access_token}")
    os.system(f"py imagetest4.py {access_token}")
else:
    print("Error obtaining access token:", response.text)







