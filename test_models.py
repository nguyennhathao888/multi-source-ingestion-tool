import pytest
from models import product
from pydantic import ValidationError
def test_hop_le():
    p = product(id=1, title="Laptop", price=599.0, stock=10, rating=4.5, category="electronics")
    assert p.price==599.0
    assert p.title=="Laptop"
def test_stock_valid():  
    with pytest.raises(ValidationError):
        product(id=1, title="Laptop", price=599.0, stock=-1, rating=4.5, category="electronics")