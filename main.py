import requests

response = requests.get("http://www.teamtreehouse.com")

print("This is number of {}".format(response.status_code))
