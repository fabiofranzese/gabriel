from flask import Flask, request
import private
import requests
import webex

access_token = private.access_token
base_url = 'https://webexapis.com'

headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}

app = Flask(__name__)

def get_public_url() -> str:
    res = requests.get("http://localhost:4040/api/tunnels")
    res.raise_for_status()
    tunnels = res.json()
    return tunnels['tunnels'][0]['public_url']

def create_webhook(public_url: str) -> None:
    url = base_url + "/v1/webhooks"
    body = {
        "name": "webex-bot",
        "targetUrl": public_url + "/webhook",
        "resource": "messages",
        "event": "created"
    }
    res = requests.post(url, headers=headers, json=body)


    if res.status_code != 200:
        print("error creating webhook continuing anyways")
        print(res.json())

print("connecting to ngrok local api...")
ngrok_url = get_public_url()
print("found ngrok public url", ngrok_url)

print("attempting to update webhook")
create_webhook(ngrok_url)
print("updated webhook successfully")


def get_room_details(id: str) -> dict:
    url = base_url + "/v1/rooms/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_self_details() -> dict:
    url = base_url + "/v1/people/me"
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


def get_message_details(id: str) -> dict:
    url = base_url + "/v1/messages/" + id
    res = requests.get(url, headers=headers)

    res.raise_for_status()

    return res.json()


@app.route("/webhook", methods=["POST"])
def webhook():
    json_data = request.json

    print("\n")
    print("WEBHOOK POST RECEIVED:")
    print(json_data)
    print("\n")

    me = get_self_details()
    if json_data["data"]["personId"] == me["id"]:
        return "OK"

    room_id = json_data["data"]["roomId"]

    message_id = json_data["data"]["id"]
    message = get_message_details(message_id)
    print(message['text'].split()[1])
    if message['text'].split()[1].lower() == 'done':
        webex.delete_room(room_id)
    return "OK"

if __name__ == "__main__":
    app.run(debug=True)