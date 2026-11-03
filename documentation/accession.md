# Workflow for Constituent Mail: Accession

Accession as soon as possible after the donation is received,
so we can address any problems with the export with the donor.

### Review
During the initial review, determine if the export meets acceptance guidelines.
1. Check the export for expected files.
2. Make a copy of the export and reorganize to a consistent directory structure for the scripts.
   - Primary folder named lastname_constituent_mail_export
   - Metadata files within primary folder
   - Exported files in "documents" folder, with unnecessary folders removed (BlobExport, dos, etc)
3. Update the script if needed, including verifying the tables and columns in the export description match the script.
   If there are new tables or columns, add to appraisal and PII removal portions of the script, if applicable.
4. Run the script in "accession" mode.
5. Review the usability reports and determine if the donation is accepted.
6. If accepted, move on to appraisal. If not accepted, stop the accession and discuss with the collecting archivist.

The appraisal reports are only searching columns we believe have any probability of showing a restriction, like topics and file paths.
It results in too many false positives to search other columns, due to columns like names and addresses that would never show a restriction. 

Note: the letter matching report removes duplicates before attempting to match (response letters often repeat).
so the number of metadata rows matched, unmatched, and blank will be fewer than the total metadata rows.
