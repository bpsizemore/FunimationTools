#!/bin/python3
import requests

def delete_history_item(external_ver_id, headers, api_base):
    url = api_base + "api/source/funimation/history/" + external_ver_id + "/"
    print("deleting: " + url)
    r = requests.delete(url, headers=headers)
    if r.status_code != 200:
        print("Failed to delete.")
        print(r.content)
        quit(1)



jwt_token = input("Please enter your funimation JWT token: ")

xsrf_token = input("Please enter your funimation XSRF token: ")
url = "https://prod-api-funimationnow.dadcdigital.com/api/source/funimation/history/?return_all=true&offset=0&limit=100"
api_base = "https://prod-api-funimationnow.dadcdigital.com/"
headers = {"authorization": "Token "+jwt_token, "x-csrftoken": xsrf_token}
show_to_delete = str(input("Enter title of show to erase history for: "))

r = requests.get(url, headers=headers);

if r.status_code != 200:
    print("Request failed.")
    print(r.content)
    exit(1)

json = r.json()
total = json['total']
num_reqs = int(total / 100)
print("About to query funimation API for history of " + str(total) +" objects in " + str(num_reqs) + " requests. Hang in there...")
# print(num_reqs)
if total % 10 != 0:
    num_reqs = num_reqs + 1

items = json['items']

items = []
for i in range(0, num_reqs + 1):
    url = "https://prod-api-funimationnow.dadcdigital.com/api/source/funimation/history/?return_all=true&offset=" + str(i*100) + "&limit=100"
    r = requests.get(url, headers=headers)
    j = r.json()
    items.extend(j['items'])
    print("req {} finished with status {}".format(i, r.status_code)) 


# print(len(items))
for item in items:
    title = item['show']['title']
    if show_to_delete.lower() == title.lower():
        delete_history_item(item['external_ver_id'], headers, api_base)
    else:
        print("Skipping episode from " + title)

