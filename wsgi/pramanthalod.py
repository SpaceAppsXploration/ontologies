__author__ = 'lorenzo'

import os

from flask import Flask
from flask import request, jsonify, Response, redirect, url_for, render_template
import simplejson as json

from wsgi.cache import get_or_set
from wsgi.contexts import ONTOLOGIES
from wsgi.utilities import classes_and_properties


app = Flask(__name__)
app.config['DEBUG'] = True
host = None


@app.route("/documentation/<name>", methods=['GET'])
def documentation(name):
    name = name.lower()
    if name and name in ONTOLOGIES.keys():
        if request.method == 'GET':
            ontology = json.loads(get_or_set(name))
            title = { "label": ontology['rdfs:label'], 
                      "comment": ontology['rdfs:comment'],
                      "name": host+name+"/" }
            context = ontology['@context']
            content = ontology['defines']
            classes, properties = classes_and_properties(content)

            return render_template('jsonld.html', title=title, name=name, context=context, 
                                    classes=classes, properties=properties, host=host)
    return wrong_uri()
        

@app.route("/", methods=['GET'])
def hello():
    res =  {
            "chronos": ["a generic ontology for space activities semantically linked to Wikipedia documents", "/chronos", "/documentation/chronos"],
            "sensors": ["an ontology for detectors, device that use some kind of sensor", "/sensors", "/documentation/sensors"],
            "astronomy": ["an ontology for astronomical objects", "/astronomy", "/documentation/astronomy"],
            "solarsystem" : ["an ontology for astronomical objects in the solar system", "/solarsystem", "/documentation/solarsystem"],
            "engineering": ["an ontology for engineering concepts", "/engineering", "/documentation/engineering"],
            "spacecraft": ["an ontology for a spacecraft and its systems", "/spacecraft", "/documentation/spacecraft"],
            "subsystems": ["an ontology for subsystems in a spacecraft", "/subsystems", "/documentation/subsystems"]
        }
    return render_template('index.html', content=res)


@app.route("/<name>/", methods=['GET'])
def index(name):
    name = name.lower()
    if name and name in ONTOLOGIES.keys():
        #
        # serve name/ontology
        #
        ontology = get_or_set(name)
        res = Response(response=str(ontology), content_type="application/ld+json; charset=utf-8")
        print(res)
        return res
    elif name == 'documentation':
        return redirect(url_for('documentation'))
    return wrong_uri()


@app.route("/<name>/<obj>/", methods=['GET'])
def chronos(name, obj):
    name = name.lower()
    if name in ONTOLOGIES.keys():
        obj = get_or_set(name, obj)
        return Response(response=str(obj), content_type="application/ld+json; charset=utf-8")
    return wrong_object()


@app.errorhandler(404)
def wrong_uri(e=None):
    message = {
            "status": 404,
            "message": "Not one of Pramantha LOD URI: " + request.url,
    }
    resp = Response(response=str(message), content_type="application/ld+json; charset=utf-8")
    # resp.status_code = 404
    return resp

@app.errorhandler(404)
def wrong_object(e=None):
    message = {
            "status": 404,
            "message": "Object not in the ontology: " + request.url,
    }
    resp = Response(response=str(message), content_type="application/ld+json; charset=utf-8")
    # resp.status_code = 404
    return resp


if __name__ == "__main__":
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        #store = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], 'newsletter.save')
        host = "http://ontology.projectchronos.eu/"
        #app.config['DEBUG'] = False
    else:
        #store = os.path.join(os.path.dirname(__file__), 'newsletter.save')
        host = "http://127.0.0.1:5000/"
        #app.config['DEBUG'] = True

    app.config.from_object('config')
    app.run()
