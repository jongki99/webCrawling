"""
실행 위치도 중요하네... 이건좀... 암튼...
이 파일이 위치한 경로로 이동 cd
python this.py
이렇게 해야 templates 를 찾음. -_-;;,
"""
from flask import Flask, render_template, request, send_file

app = Flask("JapScrapper")

@app.route("/")
def home():
    return render_template("home.html", name="nico")

@app.route("/search")
def search():
    print(request.args.get("keyword"))
    return render_template("search.html")

@app.route("/export")
def export():
    return send_file("./test.csv", as_attachment=True)

app.run(port=5001);

