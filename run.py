from blog_app import app
if __name__ == "__main__":
    app.run(debug=True)
    app.config["TEMPLATES_AUTO_RELOAD"] = True