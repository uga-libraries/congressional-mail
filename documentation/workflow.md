# Workflow for Constituent Mail

## Accession
Accession as soon as possible after the donation is received,
so we can address any problems with the export with the donor.

### Review
During the initial review, determine if the export meets acceptance guidelines.
1. Check the export for expected files.
2. Make a copy of the export and reorganize to a consistent directory structure for the scripts.
   - Primary folder named Last_Constituent_Mail_Export
   - Metadata files within primary folder
   - Exported files in "documents" folder, with unnecessary folders removed (BlobExport, dos, etc)
3. Update the script if needed, including verifying the columns in the export description match the script.
4. Run the script in "accession" mode.
5. Review the usability reports and determine if the donation is accepted.
6. If accepted, move on to appraisal. If not accepted, stop the accession and discuss with the collecting archivist.

### Appraisal
1. Check the appraisal reports made during review for errors (based on file names) in what will be deleted or not delete.
2. Refine the script to catch new patterns, but some errors are acceptable given the scale.
3. Update the function update_path() for transforming the metadata path into the directory path, if needed.
4. Run the script in "appraisal" mode to delete letters flagged for appraisal. The metadata is not changed.
5. Delete any folders that are labeled casework and document those deleted files (probably with accessioning script).
6. Delete any metadata files that are just for casework.

Continue with the standard accessioning workflow to complete the accession.

## Process
Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and future validation process.

### Preservation
This workflow and script still needs to be developed.
The preservation version has letters deleted for appraisal and the entire metadata file.
The script "preservation" mode will split the export into folders to keep AIP size reasonable
and make the metadata.csv file.
Then the general_aip.py script can be run to produce the AIPs and they may be ingested into ARCHive.

### Access
This workflow needs to be further developed.
Run the script in "access" mode to make anonymized versions of the metadata that can be shared with researchers.
Package these into DIPs with the form letters and documentation (TBD) according to the standard born-digital workflow.