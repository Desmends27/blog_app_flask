from flask import Flask
import json

app = Flask(__name__)


try:
  with open('articles.json', 'r') as fp:
    article_dict = json.load(fp)
except FileNotFoundError:
  article_dict = {}

from blog_app import routes

