from bs4 import BeautifulSoup
import datetime
import logging
import os
import pywikibot
from pywikibot import pagegenerators
import re
import yaml

from db import load_retracted_identifiers, log_retraction_edit

directory = os.path.dirname(os.path.realpath(__file__))

logger = logging.getLogger(__name__)
logging.basicConfig(filename=os.path.join(directory, 'retractionbot.log'),
                    level=logging.INFO)


def check_bot_killswitches(site):
    """
    Verifies that bot killswitch hasn't been edited, for this site or Meta.

    Checks User:RetractionBot/run, an openly editable page, to see if an
    editor has disabled the bot. If the page contains anything other than
    "yes", don't run. Checks per-wiki.
    Returns True if bot can run, False otherwise.
    """
    meta_site = pywikibot.Site('meta', 'meta')
    run_page_name = "User:RetractionBot/run"

    for a_site in [site, meta_site]:
        run_page = pywikibot.Page(a_site, run_page_name)

        if run_page.text != "yes":
            log_text = "{run_page_name} not set to 'yes' on {lang},"
            "not running.".format(
                run_page_name=run_page_name,
                lang=a_site.lang
                )
            logger.error(log_text)
            return False

    # If we haven't returned False then everything
    # seems to be fine, so return True.
    return True


def load_bot_settings():
    """Returns the contents of bot_settings.yaml"""
    with open('bot_settings.yml') as bot_settings_file:
        loaded_yaml = yaml.load(bot_settings_file)
    return loaded_yaml


def find_page_cites(page_text, id):
    """
    Given some page text and an identifier, finds all <ref> tags containing
    that identifier. Returns a list.
    """
    soup = BeautifulSoup(page_text, 'html.parser')
    escaped_id = re.escape(id)
    page_cites = soup.find_all("ref", string=re.compile(escaped_id, re.IGNORECASE))
    return page_cites


def run_bot():
    bot_settings = load_bot_settings()
    bot_languages = bot_settings['retracted_template_names']
    template_field_names = bot_settings['template_field_names']
    retracted_identifiers = load_retracted_identifiers()

    template_template = '{{{{{template_name} |{id_field}={id}}}}}'

    for language, lang_items in bot_languages.items():

        site = pywikibot.Site(language, 'wikipedia')
        bot_can_run = check_bot_killswitches(site)
        if not bot_can_run:
            continue

        for identifier in retracted_identifiers:
            original_id = identifier[2].decode("utf-8")
            retraction_id = identifier[3].decode("utf-8")
            retracted_template = template_template.format(
                template_name=lang_items,
                id_field=template_field_names[identifier[0].decode("utf-8")],
                id=retraction_id)

            page_list = pagegenerators.SearchPageGenerator('"' + original_id + '"',
                                                           namespaces=[0],
                                                           site=site)

            for wp_page in page_list:
                page_text = wp_page.text

                page_cites = find_page_cites(page_text, original_id)
                num_cites_found = len(page_cites)
                if num_cites_found == 0:
                    logger.error("Couldn't find the identifier {id} inside "
                                 "<ref> tags on page {page}.".format(
                                    id=original_id,
                                    page=wp_page))
                    continue

                unique_page_cites = {tag.string for tag in page_cites}
                for page_cite in unique_page_cites:
                    # Loop through each unique citation, updating the page text
                    # for each - in case this identifier is cited multiple
                    # times in a lazy and/or inconsistent way.
                    cite_str = page_cite

                    # Is this cite already flagged with a retraction template?
                    if "{{retracted" in cite_str.lower():
                        continue

                    ref_to_insert = cite_str + " " + retracted_template

                    page_text = page_text.replace(cite_str, ref_to_insert)

                # Only bother trying to make an edit if we changed anything
                if page_text != wp_page.text:
                    wp_page.text = page_text
                    edit_summary = "Flagging a cited source as retracted"

                    #wp_page.save(edit_summary, minor=False)
                    logger.info("Successfully edited {page_name} with "
                                "retracted source(s).".format(
                                    page_name=wp_page.title()
                                ))
                    log_retraction_edit(datetime.datetime.now(),
                                        language + ".wikipedia.org",
                                        wp_page,
                                        original_id,
                                        retraction_id)


if __name__ == '__main__':
    logger.info("Starting bot run at {dt}".format(
        dt=datetime.datetime.now()
    ))
    run_bot()
