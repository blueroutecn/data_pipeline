'''
Copyright 2014-2016 EMBL - European Bioinformatics Institute, Wellcome
Trust Sanger Institute, GlaxoSmithKline and Biogen

This software was developed as part of Open Targets. For more information please see:

	http://targetvalidation.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

from __future__ import absolute_import, print_function
from nose.tools.nontrivial import with_setup
from modules.Ontology import OntologyClassReader, DiseasePhenotypes, PhenotypeSlim
from SPARQLWrapper import SPARQLWrapper, JSON
from settings import Config
import logging
import os
from logging.config import fileConfig

__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2016, Open Targets"
__credits__ = []
__license__ = "Apache 2.0"
__version__ = ""
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@opentargets.org"
__status__ = "Production"

from logging.config import fileConfig

try:
    fileConfig(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logging_config.ini'))
except:
    pass
logger = logging.getLogger(__name__)

def setup_module(module):
    logger.info("Setting up the ontology tests")

def teardown_module(module):
    logger.info("Tearing down the ontology tests")

def my_setup_function():
    print("my_setup_function")

def my_teardown_function():
    print("my_teardown_function")


@with_setup(my_setup_function, my_teardown_function)
def test_hpo_load():
    obj = OntologyClassReader()
    assert not obj == None
    obj.load_ontology_graph(Config.ONTOLOGY_CONFIG.get('uris', 'hpo'))

@with_setup(my_setup_function, my_teardown_function)
def test_mp_load():
    obj = OntologyClassReader()
    assert not obj == None
    obj.load_ontology_graph(Config.ONTOLOGY_CONFIG.get('uris', 'mp'))

@with_setup(my_setup_function, my_teardown_function)
def test_load_hpo_classes():

    obj = OntologyClassReader()
    assert not obj == None
    obj.load_hpo_classes()

    logger.info(len(obj.current_classes))

    assert obj.current_classes["http://purl.obolibrary.org/obo/HP_0008074"] == "Metatarsal periosteal thickening"
    assert obj.current_classes["http://purl.obolibrary.org/obo/HP_0000924"] == "Abnormality of the skeletal system"
    assert obj.current_classes["http://purl.obolibrary.org/obo/HP_0002715"] == "Abnormality of the immune system"
    assert obj.current_classes["http://purl.obolibrary.org/obo/HP_0000118"] == "Phenotypic abnormality"

    # Display obsolete terms
    logger.info(len(obj.obsolete_classes))
    for k,v in obj.obsolete_classes.iteritems():
        logger.info("%s => %s "%(k, v))
        assert obj.obsolete_classes[k] == v

    # check the top_level classes
    logger.info(len(obj.top_level_classes))
    assert len(obj.top_level_classes) > 0
    assert 'http://purl.obolibrary.org/obo/HP_0001871' in obj.top_level_classes
    assert 'http://purl.obolibrary.org/obo/HP_0003549' in obj.top_level_classes
    assert 'http://purl.obolibrary.org/obo/HP_0000152' in obj.top_level_classes
    assert 'http://purl.obolibrary.org/obo/HP_0040064' in obj.top_level_classes


@with_setup(my_setup_function, my_teardown_function)
def test_load_mp_classes():

    obj = OntologyClassReader()
    assert not obj == None
    obj.load_mp_classes()

    logger.info(len(obj.current_classes))

    assert obj.current_classes["http://purl.obolibrary.org/obo/MP_0005559"] == "increased circulating glucose level"
    assert obj.current_classes["http://purl.obolibrary.org/obo/MP_0005376"] == "homeostasis/metabolism phenotype"
    assert obj.current_classes["http://purl.obolibrary.org/obo/MP_0003631"] == "nervous system phenotype"
    assert obj.current_classes["http://purl.obolibrary.org/obo/MP_0005370"] == "liver/biliary system phenotype"

    # Display obsolete terms
    logger.info(len(obj.obsolete_classes))
    for k,v in obj.obsolete_classes.iteritems():
        logger.info("%s => %s "%(k, v))
        assert obj.obsolete_classes[k] == v

@with_setup(my_setup_function, my_teardown_function)
def test_load_efo_classes():

    obj = OntologyClassReader()
    assert not obj == None
    obj.load_efo_classes()

    logger.info(len(obj.current_classes))

    assert obj.current_classes["http://www.ebi.ac.uk/efo/EFO_0000408"] == "disease"
    assert obj.current_classes["http://www.ebi.ac.uk/efo/EFO_0000651"] == "phenotype"
    assert obj.current_classes["http://www.ebi.ac.uk/efo/EFO_0001444"] == "measurement"
    assert obj.current_classes["http://purl.obolibrary.org/obo/GO_0008150"] == "biological process"

    # Display obsolete terms
    logger.info(len(obj.obsolete_classes))
    for k,v in obj.obsolete_classes.iteritems():
        logger.info("%s => %s "%(k, v))
        assert obj.obsolete_classes[k] == v


@with_setup(my_setup_function, my_teardown_function)
def test_get_disease_phenotypes():
    obj = DiseasePhenotypes()
    assert not obj == None
    obj.get_disease_phenotypes()

@with_setup(my_setup_function, my_teardown_function)
def test_parse_local_files():
    sparql = SPARQLWrapper(Config.SPARQL_ENDPOINT_URL)
    assert not sparql == None
    obj = PhenotypeSlim(sparql)
    assert not obj == None
    local_files = [ os.path.join(os.path.abspath(os.path.dirname(__file__)), '../samples/cttv008-22-07-2016.json.gz') ]
    obj.create_phenotype_slim(local_files=local_files)