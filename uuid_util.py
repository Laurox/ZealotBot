import requests


def get_name_from_uuid(uuid):
    request = requests.get('https://api.mojang.com/user/profiles/' + uuid.replace("-", "") + '/names')
    # invalid request -> status 204
    if request.status_code == 204:
        return None
    # valid request -> status 200
    else:
        return request.json()[len(request.json()) - 1]['name']


def get_uuid_from_name(name):
    request = requests.get('https://api.mojang.com/users/profiles/minecraft/' + name)
    # invalid request -> status 204
    if request.status_code == 204:
        return None
    # valid request -> status 200
    else:
        return request.json()['id']
