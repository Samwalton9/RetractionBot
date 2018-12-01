from bs4 import BeautifulSoup
import logging
import pywikibot
from pywikibot import pagegenerators
import os
import re
import yaml

# TODO: Replace IDs in retracted templates with the retracted DOI, not the original DOI.

directory = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.path.join(directory, 'retractionbot.log'),level=logging.INFO)


def check_bot_killswitch(site):
    """
    Verifies that bot killswitch hasn't been edited.

    Checks User:RetractionBot/run, an openly editable page, to see if an
    editor has disabled the bot. If the page contains anything other than
    "yes", don't run. Checks per-wiki.
    Returns True if bot can run, False otherwise.
    """
    run_page_name = "User:RetractionBot/run"
    run_page = pywikibot.Page(site, run_page_name)

    if run_page.text == "yes":
        return True
    else:
        log_text = "{run_page_name} not set to 'yes', not running.".format(
            run_page_name=run_page_name
        )
        logger.error(log_text)
        return False


def load_bot_languages():
    """Returns the contents of bot_settings.yaml"""
    with open('bot_settings.yml') as bot_settings_file:
        loaded_yaml = yaml.load(bot_settings_file)
    return loaded_yaml


def load_identifier_templates():
    """Returns the contents of identifiers.yaml"""
    with open('identifiers.yml') as identifier_templates:
        templates_loaded = yaml.load(identifier_templates)

    return templates_loaded


def load_retracted_identifiers():
    # TODO: This data, in the database, should have type, identifier, and original identifier.
    return [['doi', '10.783947932473298/dth.12107']]


def run_bot():
    bot_languages = load_bot_languages()
    retracted_identifiers = load_retracted_identifiers()
    identifier_templates = load_identifier_templates()
    template_template = '{{{{{template_name} |{{{{{id_template} |{id}}}}}}}}}'

    for language, lang_items in bot_languages.items():

        site = pywikibot.Site(language, 'wikipedia')
        bot_can_run = check_bot_killswitch(site)
        if not bot_can_run:
            continue

        for identifier in retracted_identifiers:
            retracted_template = template_template.format(
                template_name=lang_items['retracted_template'],
                id_template= identifier_templates[identifier[0]]['template_name'],
                id=identifier[1])

            page_list = pagegenerators.SearchPageGenerator(identifier, namespaces=[2]) #TODO: Turn back to 0 when not testing in sandbox

            cites_added = 0
            for wp_page in page_list:
                print(wp_page)
                page_text = wp_page.text

                soup = BeautifulSoup(page_text, 'html.parser')
                page_cites = soup.find_all("ref", string=re.compile('.*{id}.*'.format(
                    id=identifier[1]
                )))
                num_cites_found = len(page_cites)
                if num_cites_found == 0:
                    print("Error: Couldn't find the identifier {id} inside"
                          "<ref> tags on page {page}.".format(
                            id=identifier[1],
                            page=wp_page))
                    continue

                for page_cite in page_cites:
                    cite_str = page_cite.string
                    ref_to_insert = cite_str + " " + retracted_template

                    page_text = page_text.replace(cite_str, ref_to_insert)
                    cites_added += 1

                wp_page.text = page_text
                edit_summary_template = "Flagging {num_sources} as retracted."
                if cites_added == 1:
                    edit_summary = edit_summary_template.format(
                        num_sources="1 source")
                else:
                    edit_summary = edit_summary_template.format(
                        num_sources=str(cites_added) + " sources")
                wp_page.save(edit_summary, minor=False)


if __name__ == '__main__':
    run_bot()