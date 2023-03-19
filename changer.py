import requests
import json
from config import token  # load token from non public file

params = {"token": token}  # dict for wialon params

data = {
    "svc": "token/login",
    "params": json.dumps(params, ensure_ascii=False)  # to make it clean and convenient, first we create dict for wialon
    # params and then transform it to string via json's dumps func
}

r = requests.post("https://hst-api.wialon.com/wialon/ajax.html", data=data)
data["sid"] = r.json()["eid"]  # get a sid

data["svc"] = "core/search_items"
params = {
    "spec": {
        "itemsType": "avl_unit",
        "propName": "sys_name",
        "propValueMask": "*",
        "sortType": "sys_name",
    },
    "force": 1,
    "flags": 1,
    "from": 0,
    "to": 0
}
data["params"] = json.dumps(params, ensure_ascii=False)

r = requests.post("https://hst-api.wialon.com/wialon/ajax.html", data=data)
units = r.json()["items"]  # get all the items to change

# data["svc"] = "item/update_name"
# params = {"itemId": 20181251, "name": "77. Камаз к483оо 124 вахта"}
# data["params"] = json.dumps(params, ensure_ascii=False)
# r = requests.post("https://hst-api.wialon.com/wialon/ajax.html", data=data)
# print(r.json())  this is when we need to change some single item by it's id


def number_changer(start: int, list: dict, sid: str) -> list:
    '''
    func to raise by one every number in the begging of the name of every item in the "list"
    started from "start" including

    items in the list should contain name("nm") and id("id") properties

    it returns list with error string, if they occur

    '''

    print(f"Do you really want to rename items from {start}?(Yes/no)")
    if input() != "Yes":
        return []

    data = {
        "svc": "item/update_name",
        "sid": sid
    }

    errors = []

    import re

    for item in list:

        name = item["nm"].strip()
        num_name = re.findall(r"\d+", name)[0]

        if int(num_name) < start:
            continue

        params = {"itemId": item["id"], "name": name.replace(num_name, str(int(num_name)+1), 1)}
        data["params"] = json.dumps(params, ensure_ascii=False)

        r = requests.post("https://hst-api.wialon.com/wialon/ajax.html", data=data)

        print(r.json())
        if "error" in r.json().keys():
            errors.append(r.json())

        print(name+"->"+name.replace(num_name, str(int(num_name)+1), 1))

    return errors


errors = number_changer(77, units, data["sid"])
print("---------------------------------")
print("Errors:")
for error in errors:
    print(error)

# print(json.dumps(r.json(), indent=4, ensure_ascii=False))
