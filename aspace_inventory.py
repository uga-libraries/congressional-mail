"""
Script to create a spreadsheet with information for the finding aid.
Works with all export types.

Parameter: path to the "correspondence_by_topic" folder
Returns: CSV in the parent folder of "correspondence_by_topic" named aspace_import.csv
"""
import csv
import os
import pandas as pd
import sys


def save_to_csv(path, row):
    """Save a row to the csv"""
    if row == 'header':
        row = ['title', 'start_date', 'end_date', 'date_type', 'date_expression',
               'extent_portion', 'extent_number', 'extent_type']
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


if __name__ == '__main__':

    # Start
    topic_folder = sys.argv[1]
    log_path = os.path.join(os.path.dirname(topic_folder), 'aspace_import.csv')
    save_to_csv(log_path, 'header')

    for topic in os.listdir(topic_folder):

        # Title

        # Date

        # Extent

        # Save