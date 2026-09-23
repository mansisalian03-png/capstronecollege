import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from ingestion.hello import hello_ingestion
from nlp.hello import hello_nlp
from graph.hello import hello_graph
from scoring.hello import hello_scoring
from api.hello import hello_api
from ui.hello import hello_ui

def test_hello_modules():
    assert hello_ingestion() == "Hello from ingestion module"
    assert hello_nlp() == "Hello from nlp module"
    assert hello_graph() == "Hello from graph module"
    assert hello_scoring() == "Hello from scoring module"
    assert hello_api() == "Hello from api module"
    assert hello_ui() == "Hello from ui module"
