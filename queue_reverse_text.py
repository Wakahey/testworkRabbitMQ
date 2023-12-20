import requests
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python queue_reverse_text.py <text>")
        sys.exit(1)

    text = sys.argv[1]
    url = "http://127.0.0.1:8000/queue_reverse_text"

    response = requests.post(url, json={"text": text})

    if response.status_code == 200:
        print("Text queued for processing")
    else:
        print("Error:", response.text)
