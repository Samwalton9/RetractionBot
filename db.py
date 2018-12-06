#import mysqlclient # TODO: Install


def save_retraction_to_db(type, original_id, retraction_id):
    """
    Given a certain type of identifier (e.g. doi, pmid), and both the
    new (retraction) id and old (retracted) id, save this to the DB.
    """
    pass


def check_retracted_ids(identifier):
    current_ids = load_retracted_identifiers()
    for db_id in current_ids:
        if db_id[1] == identifier:
            return False

    return True


def load_retracted_identifiers():
    # This return is purely placeholder for testing.
    # Returns identifier type, retraction DOI, original DOI
    return [['doi', '10.783947932473298/retracted', '10.783947932473298/dth.12107']]
