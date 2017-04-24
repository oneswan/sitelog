from flask import Flask, jsonify
from models import db_session, Site, Response

app = Flask(__name__)


@app.route('/')
def index_view():
    return 'Index View. The Main Informational Panel Would Come Here.'


@app.route('/api/stats')
def stats_view():
    return jsonify(some_data='some_data')


@app.route('/api/sites')
def sites_view():
    sites = db_session.query(Site).all()
    return jsonify(sites=[s.serialize for s in sites])


@app.route('/api/responses')
def responses_view():
    responses = db_session.query(Response).all()
    return jsonify(responses=[r.serialize for r in responses])


app.run(debug=True)
