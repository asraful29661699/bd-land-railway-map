import requests
import json
import os

# ভূমি মন্ত্রণালয়ের সার্ভার থেকে আখাউড়া ধরখার মৌজার (JL 005) ডেটা টানার আসল API/WFS URL
LAND_API_URL = "https://map.land.gov.bd/geoserver/wfs"
PARAMS = {
    'service': 'WFS',
    'version': '1.1.0',
    'request': 'GetFeature',
    'typeName': 'land_mouza_layer', 
    'outputFormat': 'application/json',
    'srsName': 'EPSG:4326',
    # ফিল্টার করে শুধু চট্টগ্রাম -> ব্রাহ্মণবাড়িয়া -> আখাউড়া -> ০০৫ ধরখার মৌজা লক করা হয়েছে
    'cql_filter': "division='Chattogram' AND district='Brahmanbaria' AND upazila='Akhaura' AND jl_no='005'"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def fetch_mouza_data():
    print("🤖 বট ভূমি মন্ত্রণালয়ের সার্ভার থেকে ডেটা সংগ্রহ করা শুরু করছে...")
    try:
        response = requests.get(LAND_API_URL, params=PARAMS, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            print("✅ ডেটা সফলভাবে ডাউনলোড হয়েছে!")
            return response.json()
        else:
            print(f"❌ সার্ভার রেসপন্স এরর! স্ট্যাটাস কোড: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ রিকোয়েস্ট পাঠাতে সমস্যা হয়েছে: {str(e)}")
        return None

def main():
    mouza_data = fetch_mouza_data()
    if mouza_data:
        filename = "dharkhar_005.geojson"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(mouza_data, f, ensure_ascii=False, indent=4)
        print(f"💾 ফাইলটি সফলভাবে '{filename}' নামে সেভ করা হয়েছে।")
    else:
        print("⚠️ কোনো ডেটা সেভ করা যায়নি।")

if __name__ == "__main__":
    main()
