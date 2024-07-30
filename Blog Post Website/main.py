from flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        header_message = "Contact Me"
    else:
        header_message = "Form submitted!"
        name = request.form["name"]
        email = request.form["email"]
        with smtplib.SMTP("outlook.office365.com", port=587) as connection:
            connection.starttls()
            connection.login("your email", "your pass")
            connection.sendmail(
                from_addr="your email",
                to_addrs=email,
                msg=f"Subject:Message from {name}\n\nhi!"
            )
    return render_template("contact.html", header_message=header_message)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
