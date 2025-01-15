import requests

# Define the URL for the endpoint
url = 'http://127.0.0.1:5000/api/predict'

# Define the predefined data
data = {
    "sentences": [
        "I have depression",
        "I felt a bit odd about seeing a stray dog",
        "Sometimes I get anxious about meeting new people."
    ]
}

# Make the POST request
response = requests.post(url, json=data)

# Print the response
print(response.json())