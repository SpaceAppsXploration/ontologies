__author__ = 'lorenzo'

import os
import platform
import simplejson as json

from contexts import ONTOLOGIES

CACHE = {}


def get_o_path():
    path = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        ''' linux path '''
        path += '/SensorOntology/'
    else:
        '''  windows path  '''
        path += '\\SensorOntology\\'

    return path

path = get_o_path()


def get_or_set(nm, obj=None):
    spath = path + ONTOLOGIES[nm][1]
    if not obj:
        if nm in CACHE.keys() and CACHE[nm]:
            ontology = CACHE[nm]
        else:
            with open(str(spath), "r", encoding="utf8") as jsonld:
                CACHE[nm] = json.loads(jsonld.read())
                ontology = CACHE[nm]
        return ontology
    else:
        if obj in CACHE.keys() and CACHE[obj]:
            result = CACHE[obj]
        else:
            with open(str(spath), "r", encoding="utf8") as jsonld:
                defines = json.loads(jsonld.read())['defines']
                print('http://pramantha.eu/' + nm + '/ontology/' + obj)
                for d in defines:
                    if '@id' in d:
                        if d['@id'] == 'http://pramantha.eu/' + nm + '/ontology/' + obj:
                            CACHE[obj] = d
                            return CACHE[obj]
                return None



