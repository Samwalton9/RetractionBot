import requests

from db import save_retraction_to_db, retracted_id_exists, get_latest_timestamp

user_agent = "RetractionBot (https://github.com/Samwalton9/RetractionBot; mailto:Samwalton9@gmail.com)"


def get_crossref_retractions():
    # List of crossref retraction types based on, but stricter than,
    # https://github.com/fathomlabs/crossref-retractions/blob/master/index.js

    retraction_types = [
        'removal',
        'retraction',
        'Retraction',
        'retration',
        'withdrawal',
        ]

    crossref_api_url = ('https://api.crossref.org/works'
                        '?filter=update-type:{type},from-index-date:{date}'
                        '&select=DOI,update-to,indexed'
                        '&rows=1000'
                        '&offset={offset}')

    latest_date = get_latest_timestamp()

    for retraction_type in retraction_types:
        items_count = 0
        continue_running = True

        while continue_running:
            response = requests.get(crossref_api_url.format(
                date=latest_date,
                type=retraction_type,
                offset=items_count
                ),
                    headers={'User-Agent': user_agent}
            )
            json_response = response.json()

            returned_items = json_response['message']['items']

            if len(returned_items) == 0:
                continue_running = False
            else:
                items_count += len(returned_items)

            for item in returned_items:
                timestamp = item['indexed']['date-time']
                old_doi = item['update-to'][0]['DOI']
                new_doi = item['DOI']

                if not retracted_id_exists(new_doi):
                    save_retraction_to_db(timestamp, 'doi', 'Crossref',
                                          old_doi, new_doi)


def get_ncbi_retractions():
    pass


if __name__ == '__main__':
    get_crossref_retractions()
