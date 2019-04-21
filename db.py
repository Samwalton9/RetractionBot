import MySQLdb
import os

db = MySQLdb.connect(host="tools.db.svc.eqiad.wmflabs",
                     db='s54021__retractionbot',
                     read_default_file=os.path.expanduser("~/replica.my.cnf"))


def save_retraction_to_db(type, origin, original_id, retraction_id):
    """
    Given a certain type of identifier (e.g. doi, pmid), its origin (e.g. crossref, pubmed)
    and both the new (retraction) id and old (retracted) id, save this to the DB.
    type can be 'doi' or 'pmid'
    """
    cur = db.cursor()
    query = """
        INSERT INTO retractions
        VALUES ('{type}', '{origin}', '{original_id}', '{retraction_id}')"""
    cur.execute(query.format(
        type=type,
        origin=origin,
        original_id=original_id,
        retraction_id=retraction_id
    ))


def check_retracted_ids(identifier):
    current_ids = load_retracted_identifiers()
    # TODO: Check if this ID is already in the DB.

    return True


def load_retracted_identifiers():
    cur = db.cursor()
    query = """
        SELECT * FROM retractions
    """
    cur.execute(query)
    return list(cur.fetchall())


def log_retraction_edit(timestamp, domain, page_title, old_id, new_id):
    cur = db.cursor()
    query = """
        INSERT INTO edit_log
        VALUES ('{timestamp}', '{domain}', '{page_title}', '{old_id}', '{new_id}')
    """
    cur.execute(query.format(
        timestamp=timestamp,
        domain=domain,
        page_title=page_title,
        old_id=old_id,
        new_id=new_id
    ))
