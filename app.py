#! usr/bin/python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_graphql import GraphQLView

from database import db_session, Base as model_base, engine
from schema import schema
from seeds import gen_seeds

app = Flask(__name__)
app.debug = True

if os.environ["ENV"] != 'prod':
    app.add_url_rule('/api', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True,
                                                           context={'session': db_session}))
else:
    app.add_url_rule('/api', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=False,
                                                           context={'session': db_session}))


@app.route('/')
def index():
    return "Click here to to go to <a href='/api'> /api</a>"


if __name__ == "__main__":
    exists = engine.dialect.has_table(engine.connect(), "source")
    if exists is False:
        model_base.metadata.create_all(engine)
        gen_seeds()
    app.run()
