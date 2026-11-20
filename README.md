# Congressional Mail (CSS/CMS)

## Overview
Providing basic access to congressional correspondent system exports. DRAFT

The archival office export type is a non-standard export received for a single collection.
This script is not in sync with the rest, and only has the ability to read and report on the metadata file.

The archiving and data interchange export formats have their own scripts.
The actions are close but there is enough difference in metadata (especially column names and delimiters) to require their own.
We intend to phase out data interchange and focus on archiving, or else would have spent more time on shared functions.

## Getting Started

### Dependencies

### Installation

### Script Arguments

appraisal_delete_log.csv (created in appraisal_review mode) must be in the output_directory before running appraisal_delete or access modes.
restriction_review.csv (created in appraisal_review mode) must be in the output_directory before running access mode.
topics_sort_metadata.csv and topics_sort_complete.txt must be in the output_directory before running access_restart mode.
The output_directory is the parent folder of input_directory

input_directory: path to the folder with the export
This is required by all the scripts.
The export directory will be named Lastname_Constituent_Mail_Export (UGA naming convention)
and contain the metadata files and a folder named "documents" with the letters.

script_mode: accession, appraisal_review, appraisal_delete, access, access_restart

accession
* Make metadata matching reports
* Make metadata usability reports
* Make topics report

appraisal_review
* Make appraisal reports
* Make restrictions review report

appraisal_delete
* Delete letters due to appraisal

access
* Redact a copy of the metadata: remove rows for appraisal and restrictions and columns for PII
* Make a copy of the redacted metadata split by calendar year, for smaller files that are easier to open
* Make a copy of incoming and outgoing correspondence in folders by topic (restricted not included), 
  with a CSV with the redacted metadata for each letter found in the export.
* Make inventory for ArchiveSpace with title, dates, and extent.

access_restart (only implemented with css_archiving)
* Continue sorting by topic where access mode left off.
* Make inventory for ArchivesSpace with title, dates, and extent.

### Testing

To keep the expected test results manageable, most tests only use a small subset of the metadata fields.

The unit tests require the working directory to be the parent directory of the test files (tests/export_type).
In PyCharm, this will automatically work when running all tests in an exports folder,
but will need to be adjusted when running tests from within the files.

## Workflow

1. As soon as a constituent mail is received, [accession](documentation/accession.md)
   and determine if it is complete enough to accept.

2. If the accession is accepted, proceed to [appraisal](documentation/appraisal.md).

3. If the collection is closed, [preservation](documentation/preservation.md) and [access](documentation/access.md)
   may wait until it can be opened, or can be done now. TBD - zip to reduce strain on Hub?

Run all scripts remotely on Hub for exports with larger numbers of files (size uncertain - 100,000?)

All scripts read the metadata and remove columns with PII (names, addresses, office notes.)
However, notes columns are initially kept to use for appraisal and restriction review, and only later removed.
There is some data loss during reading from character encoding and parsing errors, so this metadata is only suitable for access.
If there are multiple metadata files, they are combined using the correspondence id, to avoid a lot of incomplete rows (e.g., address only).
For the multiple metadata files, we only read select files that contain information needed for the access copies or appraisal and restriction review.
The original metadata file(s) are retained in the preservation copy for when PII is no longer restricted.

The beginning of the file paths in the metadata must be updated to match how they are organized in the export
in order to align the metadata and files for sorting.

## Author

## Acknowledgements
