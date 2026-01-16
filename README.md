# Congressional Mail (CSS/CMS)

## Overview
Providing basic access to congressional correspondent system exports. DRAFT

## Getting Started

### Dependencies

### Installation

### Script Arguments

input_directory: path to the folder with the export
This is required by all the scripts.
The export directory will be named Lastname_Constituent_Mail_Export (UGA naming convention)
and contain the metadata files and a folder named "documents" with the letters.

script_mode: access, accession, appraisal
This is required by all except aip_prep.py

access
* Redact a copy of the metadata: remove rows for appraisal and restrictions and columns for PII
* Make a copy of the redacted metadata split by calendar year, for smaller files that are easier to open
* Make a copy of incoming and outgoing correspondence in folders by topic (restricted not included)

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

## Author

## Acknowledgements
