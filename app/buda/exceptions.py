class BudaServicesException(Exception):
    """ Buda server didn't return the data """
    pass


class BudaInvalidResponse(Exception):
    """ Buda server response has an invalid format or schema """
    pass
