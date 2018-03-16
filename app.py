#! usr/bin/python
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_graphql import GraphQLView
from werkzeug.routing import BaseConverter
from werkzeug.utils import redirect

from database import db_session, Base as model_base, engine, Source
from schema import schema
from scrapper import AndroidWeeklyScrapper
from seeds import gen_seeds

app = Flask(__name__)
app.debug = False

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# OR, the same with increased verbosity:
load_dotenv(dotenv_path, verbose=True)

if os.environ["ENV"] != 'prod':
    app.add_url_rule('/api', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True,
                                                           context={'session': db_session}))
else:
    app.add_url_rule('/api', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=False,
                                                           context={'session': db_session}))


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def index():
    return redirect('notfound.html')
    # return "Click here to to go to <a href='/api'> /api</a>"


@app.route('/scrap/<source_id>/<issuenumber>')
def scrap(source_id, issuenumber, context=db_session):
    source = Source.query.filter(Source.object_id == source_id).first()
    scrappers = {
        'android': AndroidWeeklyScrapper()
    }

    if scrappers[source.tag].scrap_response(source.object_id, source.base_url, issuenumber):
        return jsonify({"status": 200, "msg": "issue fetched"})
    else:
        return jsonify({"status": 200, "msg": "issue already exists"})


if __name__ == "__main__":
    exists = engine.dialect.has_table(engine.connect(), "source")
    if exists is False:
        model_base.metadata.create_all(engine)

        gen_seeds()
    app.run(host='0.0.0.0')
