import requests
import apikeys

response = requests.post("https://domino.xomnia.net/v1/rob_waternet/test_for_api/endpoint",
    headers = {
        "X-Domino-Api-Key": apikeys.DOMINO,
        "Content-Type": "application/json"
    },
    json = {
        "parameters": [6.0, 2.73, 1.8, 2.08e-4, 48.2, 1.2e-4, 54, 1, 5e-5, 1, 2, False]
    }
)

print(response.status_code)
print(response.headers)
print(response.json())
