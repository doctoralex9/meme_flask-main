from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# New function to get a meme from meme-api.com
def get_meme():
    url = "https://meme-api.com/gimme"  # This API returns random memes from Reddit
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure we got a valid response
        data = response.json()  # Convert to JSON
        
        # Extract the meme information
        meme_pic = data['url']  # URL of the meme image
        meme_title = data['title']  # Title of the meme
        return meme_pic, meme_title
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None, "Error fetching meme"
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return None, "Error parsing JSON"

@app.route("/")
def index():
    meme_pic, meme_title = get_meme()  # Fetch meme data
    return render_template("meme_index.html", meme_pic=meme_pic, meme_title=meme_title)

@app.route("/new_meme")
def new_meme():
    meme_pic, meme_title = get_meme()
    if meme_pic:
        return jsonify(meme_pic=meme_pic, meme_title=meme_title)
    else:
        return jsonify(meme_pic=None, meme_title="Error fetching meme"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
