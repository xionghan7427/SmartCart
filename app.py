# app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Shopping Assistant!"

@app.route('/find_deals', methods=['POST'])
def find_deals():
    user_input = request.json.get('input')
    # Here you would integrate with an API to find deals based on user_input
    # For demonstration, we'll return a mock response.
    deals = fetch_deals(user_input)
    return jsonify(deals)

#def fetch_deals(query):
#    # Mock deal data
#    return [
#        {"title": "Deal 1", "price": "$19.99", "link": "http://example.com/deal1"},
#        {"title": "Deal 2", "price": "$29.99", "link": "http://example.com/deal2"},
#    ]

def fetch_deals(query):
    # eBay API endpoint
    url = "https://svcs.ebay.com/services/search/FindingService/v1"
    app_id = "YOUR_EBAY_APP_ID"  # Replace with your eBay App ID
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.13.0",
        "SECURITY-APPNAME": app_id,
        "GLOBAL-ID": "EBAY-US",
        "keywords": query,
        "paginationInput.entriesPerPage": "5",
        "outputSelector": [
            "searchResult.item.title",
            "searchResult.item.viewItemURL",
            "searchResult.item.sellingStatus.currentPrice",
        ],
        "responseEncoding": "JSON",
        "callback": "_cb_findItemsByKeywords",
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        deals = []
        items = data.get("findItemsByKeywordsResponse", [{}])[0].get("searchResult", [{}])[0].get("item", [])
        
        for item in items:
            title = item.get("title", "No Title")
            price = item.get("sellingStatus", [{}])[0].get("currentPrice", {}).get("__value__", "N/A")
            link = item.get("viewItemURL", "No Link")
            deals.append({"title": title, "price": f"${price}", "link": link})
        
        return deals
    else:
        return [{"title": "Error fetching deals", "price": "", "link": ""}]

if __name__ == '__main__':
    app.run(debug=True)
