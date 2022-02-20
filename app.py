from flask import Flask, render_template,request, json, send_file, current_app
import os
from pytube import YouTube
app = Flask(__name__)
info_dict = {}
url = None
msg = None

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/process/", methods=["GET"])
def process():
	global info_dict
	videoes = []
	res_list = []
	global url
	url = request.args["url"]
	try:
		yt = YouTube(url)
		all_videoes = yt.streams
		filtered_videoes = all_videoes.filter(mime_type="video/mp4")
		for video in filtered_videoes:
			if video.resolution not in res_list:
				videoes.append(video)
				res_list.append(video.resolution)
		info_dict["title"] = yt.title,
		info_dict["thumbnail"] = yt.thumbnail_url
		info_dict["videoes"] = [ {"itag": item.itag, "res": item.resolution} for item in videoes]
		if os.path.exists("./tmp/info.json"):
			os.remove("./temp/info.json")

		with open("./temp/info.json", "w+") as f:
			json.dump(info_dict, f, indent = 4)
		return render_template("info.html")
	except Exception as e:
		return f"error:- {e}"
		
@app.route("/json")
def fetchjson():
	with open("./temp/info.json") as f:
		content = json.load(f)
	return content

@app.route("/download/", methods=["GET"])
def download():
	msg = None
	itag = request.args["itag"]
	try:
		yt = YouTube(url)
	except Exception as e:
		msg = f"line1:- {e}"
	try:
		video = yt.streams.get_by_itag(itag)
	except Exception as e:
		msg = f"line2:- {e}"
	try:
		global info_dict
		filename = f'{info_dict["title"][0].replace(" ", "_")}.mp4'
		info_dict["filename"] = f"{filename}"
		get_file_path = f'temp/video/{filename}'
		video.download(filename=get_file_path)
	except Exception as e:
		msg = f"line4:- {e}"
	return render_template("download.html")
	
@app.route("/temp/video")
def download_file():
	try:
		path = os.path.join(current_app.root_path, "temp/video/", info_dict["filename"])
		return send_file(path, as_attachment=True)
	except Exception as e:
		global msg
		msg = e
		return None
	
@app.route("/msg")
def ermsg():
	return f"{msg}"
	
	
@app.route("/list")
def give_list():
	lst = os.listdir(os.path.join(current_app.root_path, "temp/video/"))
	return f"{lst}"

if __name__ == "__main__":
    app.run()