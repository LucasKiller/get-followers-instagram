from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_instagram_followers(username):
    url = f"https://www.instagram.com/{username}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', property="og:description")
            if meta_tag:
                content = meta_tag['content']
                followers = content.split(' ')[0]
                return followers
        return None
    except Exception as e:
        print(f"Error fetching followers: {e}")
        return None

@app.route('/followers', methods=['GET'])
def followers():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    followers = get_instagram_followers(username)
    if followers:
        return jsonify({"username": username, "followers": followers})
    else:
        return jsonify({"error": "Unable to fetch followers"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
