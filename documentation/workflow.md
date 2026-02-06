# Workflow for Constituent Mail

## Accession
Accession as soon as possible after the donation is received,
so we can address any problems with the export with the donor.

### Review
During the initial review, determine if the export meets acceptance guidelines.
1. Check the export for expected files.
2. Make a copy of the export and reorganize to a consistent directory structure for the scripts.
   - Primary folder named Lastname_Constituent_Mail_Export
   - Metadata files within primary folder
   - Exported files in "documents" folder, with unnecessary folders removed (BlobExport, dos, etc)
3. Update the script if needed, including verifying the tables and columns in the export description match the script.
   If there are new tables or columns, add to appraisal and PII removal portions of the script, if applicable.
4. Run the script in "accession" mode.
5. Review the usability reports and determine if the donation is accepted.
6. If accepted, move on to appraisal. If not accepted, stop the accession and discuss with the collecting archivist.

Note: the letter matching report removes duplicates before attempting to match (response letters often repeat).
so the number of metadata rows matched, unmatched, and blank will be fewer than the total metadata rows.

### Appraisal

Requires appraisal_delete_log.csv, created in accession mode.
This CSV may be manually edited (remove rows to not delete, add rows from appraisal_check_log.csv to delete).
For casework, delete even if the phrase indicates it is not a case or casework, 
because the fact they considered it suggests it includes sensitive personal information. 

1. Check the appraisal reports made during review for errors (based on file names) in what will be deleted or not deleted. Double check no form letters are being deleted.
2. Refine the script to catch new patterns, but some errors are acceptable given the scale.
3. Update the function update_path() for transforming the metadata path into the directory path, if needed.
4. Run the script in "accession" mode again to check your changes. It takes a long time to recopy an export if there are mistakes with deletion (next step).
5. Review the topics report and update the restrictions list in restriction_report() with additional highly sensitive topics.
6. Run the script in "appraisal" mode to delete letters flagged for appraisal. The metadata is not changed.
7. Delete any folders that are labeled casework and document those deleted files (probably with accessioning script).
8. Delete any metadata files that are just for casework.

Continue with the standard accessioning workflow to complete the accession.

## Process
Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and future validation process.

### Preservation
The preservation version has letters deleted for appraisal and the entire metadata file.
1. Run aip_prep.py to split a copy of the export into folders to keep AIP size reasonable 
while maintaining the directory structure and start the metadata.csv file.
2. Add the department, collection, and AIP ids to the metadata.csv.
3. Run general_aip.py script to produce the AIPs, and follow that workflow for QC.
4. Once the AIPs are successfully ingested into ARCHive and access copies are made, delete the unsplit copy.

### Access

Requires appraisal_delete_log.csv, created in accession mode and potentially edited during appraisal.
Requires restriction_review.csv, created in appraisal mode.

Delete any rows from restriction_review.csv (made in Appraisal mode) that express opinions about the topic,
and only leaves rows where someone is requesting assistance with their own situation.
Anything left in restriction_review.csv will not be part of the access copy.
Requests for assistance on these topics are likely to include highly sensitive information 
and are being restricted from access until we make a determination of if they should be retained 
or restricted for 75 years.

Run the script in "access" mode to make anonymized versions of the metadata that can be shared with researchers
and a copy of all unrestricted letters with topical metadata, reorganized by topic, for class use.

Package the script output into DIPs according to the standard born-digital workflow:
* Form letters and metadata 
* Letters by topic: each topic folder is a separate DIP
* Redacted metadata: single CSV and CSV by calendar year 
 
Include an explanation of the export and how it has been altered during processing in each DIP
and summarize that information in the finding aid as a processing note. 

Delete any topic folders that do not provide meaningful access, such as dates or numerical codes.

For CMS Data Interchange Format, include Table 8C for the form letter metadata.
If we every receive 8D, merge fields, potentially merge that with 8C.
Do not include the other form letter file, 8E, as it links to the individual letter and may be a privacy concern.