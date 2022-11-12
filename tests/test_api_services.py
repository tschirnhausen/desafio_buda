import pytest
from buda import buda

@pytest.fixture
def buda_instance() -> buda.Buda:
    ''' Returns an instance of Buda environment '''
    return buda.Buda()

