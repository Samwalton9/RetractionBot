import requests

from db import save_retraction_to_db

user_agent = "RetractionBot (https://github.com/Samwalton9/RetractionBot; mailto:Samwalton9@gmail.com)"


def get_crossref_retractions(from_date):
    # List of crossref retraction types based on, but stricter than,
    # https://github.com/fathomlabs/crossref-retractions/blob/master/index.js

    #TODO: Loop through results to expend them all.
    #TODO: Only run from most recent result in DB
    #TODO: Run regularly on CRON job on production

    retraction_types = [
        'removal',
        'retraction',
        'Retraction',
        'retration',
        'withdrawal',
        ]

    crossref_api_url = 'http://api.crossref.org/works?filter=update-type:{type}'

    for retraction_type in retraction_types:
        response = requests.get(crossref_api_url.format(
            type=retraction_type),
            headers={'User-Agent': user_agent}
        )
        json_response = response.json()
        if json_response['message']['total-results'] > 0:
            for item in json_response['message']['items']:
                old_doi = item['update-to'][0]['DOI']
                new_doi = item['DOI']

                save_retraction_to_db('doi', 'Crossref', old_doi, new_doi)


def get_ncbi_retractions():
    pass
