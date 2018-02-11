from __future__ import print_function
from checkBioRxivRSS import check_RSS
from logging_utils import logger
import access_sqlite3
import checkAltmetrics


def main():
    # Parse RSS feed
    logger(__name__).info("Start Parsing RSS feed...")
    RSS_data_list = check_RSS("genomics", "bioinformatics")

    # Create sqlite3 database if not exists
    sqlite3_file = "../db/test.sqlite3"
    if not access_sqlite3.create_tables(sqlite3_file):
        return

    # Insert new target articles into sqlite3 db
    logger(__name__).info("Insert new target articles into sqlite3 db.")
    if not access_sqlite3.insert_new_doi(sqlite3_file, RSS_data_list):
        return

    # Get all target articles for checking altmetrics score
    logger(__name__).info(
        "Get all target articles for checking altmetrics score.")
    target_doi = access_sqlite3.select_target_doi(sqlite3_file)

    # Get altmetric score for each article
    for doi in target_doi:
        altmetrics_data = checkAltmetrics.checkAltmetrics(doi)
        if altmetrics_data == None:
            continue

        # Insert scores into sqlite3 db
        access_sqlite3.insert_altmetric_score(
            sqlite3_file, doi, altmetrics_data)

        # Delete an article scored high altmetric score from sqlite3 db
        if altmetrics_data.flg == 1:
            pass

        # Send a message to SNS
        return


if __name__ == '__main__':
    main()
