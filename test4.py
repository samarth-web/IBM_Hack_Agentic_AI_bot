import requests

API_KEY = "98ba5fac32841e02dc31ce69994ceefb"
TOKEN = "ATTA3de43fcdffa9256748f9cb858565555175358f99eeebfd2312e56796866467fd79DAD6BF"
BOARD_ID = "HU04NoGx"
LIST_NAME = "To Do"

def get_list_id(board_id, list_name):
    url = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = {"key": API_KEY, "token": TOKEN}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        for lst in response.json():
            if lst['name'].lower() == list_name.lower():
                return lst['id']
        print("❌ List not found.")
    else:
        print("❌ Failed to fetch lists:", response.text)
    return None

def create_trello_card(list_id, name, desc):
    url = "https://api.trello.com/1/cards"
    query = {
        'key': API_KEY,
        'token': TOKEN,
        'idList': list_id,
        'name': name,
        'desc': desc
    }
    response = requests.post(url, params=query)
    if response.status_code == 200:
        print("✅ Card created:", response.json()["url"])
    else:
        print("❌ Failed to create card:", response.text)

if __name__ == "__main__":
    list_id = get_list_id(BOARD_ID, LIST_NAME)
    if list_id:
        create_trello_card(
            list_id,
            "Finish Hackathon Project",
            "This task was created via the Trello API!"
        )
