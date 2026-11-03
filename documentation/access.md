# Workflow for Constituent Mail: Access

Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and future validation process.

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
* Form letters and form letter metadata 
* Letters by topic: each topic folder is a separate DIP
* Redacted metadata: single CSV and CSV by calendar year 
 
Include an explanation of the export and how it has been altered during processing in each DIP
and summarize that information in the finding aid as a processing note. 

Delete any topic folders that do not provide meaningful access, such as dates or numerical codes.

For CMS Data Interchange Format, include Table 8C for the form letter metadata.
If we every receive 8D, merge fields, potentially merge that with 8C.
Do not include the other form letter file, 8E, as it links to the individual letter and may be a privacy concern.
