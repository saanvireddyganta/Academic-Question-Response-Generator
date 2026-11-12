import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from model.model_utils import validate_request
def test_valid(): assert validate_request({"prompt":"Explain CNN","max_new_tokens":50})
def test_empty():
    with pytest.raises(ValueError): validate_request({"prompt":" "})
def test_long():
    with pytest.raises(ValueError): validate_request({"prompt":"x"*12001})
