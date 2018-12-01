# RetractionBot
Bot that will flag retracted references on Wikipedia - currently a work in progress.

The idea for this bot came from discussions at WikiCite 2018, in addition to on-wiki discussions such as [this one](https://en.wikipedia.org/wiki/Wikipedia_talk:WikiProject_Medicine/Archive_118#Med_article_retractions).

## How?

The current plan is to start by following the method used by [open-retractions](https://github.com/fathomlabs/open-retractions) to track retracted papers through Crossref DOIs and PubMed IDs. The bot will build up a database of retracted papers and periodically check for their presence on Wikipedia. If it finds a reference citing a retracted paper, it will add the [{{Retracted}}](https://en.wikipedia.org/wiki/Template:Retracted) template (or other language equivalent) to the citation, adding it to the [retracted citation tracking category](https://en.wikipedia.org/wiki/Category:Articles_citing_retracted_publications).
