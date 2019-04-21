import MySQLdb
import os

db = MySQLdb.connect(host="tools.db.svc.eqiad.wmflabs",
                     db='s54021__retractionbot',
                     read_default_file=os.path.expanduser("~/replica.my.cnf"))


def save_retraction_to_db(timestamp, type, origin, original_id, retraction_id):
    """
    Given a certain type of identifier (e.g. doi, pmid), its origin
    (e.g. crossref, pubmed) and both the new (retraction) id and old
    (retracted) id, save this to the DB. type can be 'doi' or 'pmid'
    """
    cur = db.cursor()
    query = """
        INSERT INTO retractions
        VALUES ('{timestamp}', '{type}', '{origin}', '{original_id}', '{retraction_id}')"""
    cur.execute(query.format(
        timestamp=timestamp,
        type=type,
        origin=origin,
        original_id=original_id,
        retraction_id=retraction_id
    ))


def retracted_id_exists(retraction_id):
    """
    Given a retraction ID string, checks if an entry already exists for it
    in the database. If so, return True.
    """
    cur = db.cursor()
    query = """
        SELECT COUNT(*) FROM retractions
        WHERE retraction_id = "{retraction_id}"
    """
    cur.execute(query.format(retraction_id=retraction_id))
    count_result = cur.fetchone()

    if count_result[0] != 0:
        return True
    else:
        return False


def get_latest_timestamp():
    """
    Get the latest timestamp from the database in the format YYYY-MM-DD
    """
    cur = db.cursor()
    query = """
        SELECT timestamp FROM retractions
        ORDER BY timestamp DESC
        LIMIT 1
    """
    cur.execute(query)
    fetch_one = cur.fetchone()
    if fetch_one:
        max_timestamp = fetch_one[0].strftime('%Y-%m-%d')
    else:
        # If no objects are in the database, pick an arbitrarily old date.
        max_timestamp = '1970-01-01'

    return max_timestamp


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
