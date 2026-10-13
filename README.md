# Congressional Mail (CSS/CMS)

## Overview
Providing basic access to congressional correspondent system exports. DRAFT

The archival office export type is a non-standard export received for a single collection.
This script is not in sync with the rest, and only has the ability to read and report on the metadata file.

## Getting Started

### Dependencies

### Installation

### Script Arguments

input_directory: path to the folder with the export
This is required by all the scripts.
The export directory will be named Lastname_Constituent_Mail_Export (UGA naming convention)
and contain the metadata files and a folder named "documents" with the letters.

script_mode: access, access_restart, accession, appraisal

access
* Redact a copy of the metadata: remove rows for appraisal and restrictions and columns for PII
* Make a copy of the redacted metadata split by calendar year, for smaller files that are easier to open
* Make a copy of incoming and outgoing correspondence in folders by topic (restricted not included), 
  with a CSV with the redacted metadata for each letter found in the export. 

access_restart
* Continue sorting by topic where access mode left off.

accession
* Make appraisal reports
* Make metadata usability reports, including how many files in the export match the metadata
* Make topic report

appraisal
* Delete letters due to appraisal
* Make restrictions review report

### Testing

To keep the expected test results manageable, most tests only use a small subset of the metadata fields.

## Workflow

appraisal_delete_log.csv (created in accession mode) must be in the output_directory before running appraisal or access modes.
restriction_review.csv (created in appraisal mode) must be in the output_directory before running access mode.
topics_sort_metadata.csv and topics_sort_complete.txt must be in the output_directory before running access_restart mode.
The output_directory is the parent folder of input_directory

## Author

## Acknowledgements
