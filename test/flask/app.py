from flask import Flask , render_template , request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("form.html")



@app.route("/submit" , methods=["POST"])
def submit():
    name = request.form["name"]
    age = request.form["age"]

    with open("data.txt" , "a") as f:
        f.write(f"Name : {name} , Age : {age} \n")
    
    print("Data saved successfully ")
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)