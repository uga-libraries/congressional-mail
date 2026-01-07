# Congressional Mail (CSS/CMS)

## Overview
Providing basic access to metadata from congressional correspondent system exports.
Tables are combined if there is more than one, columns with personally identifiable information are removed, 
and the data is saved into one spreadsheet (Access_Copy.csv), as well as one CSV per Congress Year.

## Getting Started

### Dependencies

### Installation

### Script Arguments
Path to the metadata file: archival_office_correspondence_data.py and css_archiving_format.py

Path to the folder with all metadata files: cms_data_interchange_format.py and css_data_interchange_format.py

Script mode (all three export types)
accession: produce usability and appraisal reports; export not changed
appraisal: delete letters due to appraisal; metadata not changed
access: remove metadata rows for appraisal and columns for PII, make copy of metadata split by congress year,
and make a copy of incoming and outgoing correspondence in folders by topic

aip_prep: input_directory (path to the folder with the export)

### Testing

## Workflow

## Author

## Acknowledgements
