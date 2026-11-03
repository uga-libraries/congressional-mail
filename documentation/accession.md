# Workflow for Constituent Mail: Accession

Accession as soon as possible after the donation is received, so we can address any problems with the export with the donor.

## Copy Export

*  Do usual steps (virus, copy to Hub, etc.) for transfer media
*  Unzip. Retain the zips until processing is done, but move into their own folder.
*  Bag now? We haven't been doing that, but there can be quite a delay before accessioning is done.
*  Make another copy to work on, as we're about to do appraisal
   *  TeraCopy over network if smaller
   *  Robocopy remoted into Hub if bigger (more a file count issue)

## Export Completeness

Check the export contains all expected files:

* One or more metadata files (depends on the export type, may be .DAT or .out)
* Description of the metadata fields in the export (filename varies, usually a Word doc)
* Reports on missing files (often named nonexist)
* A README
* Directories with the text of the letters (common directories: formletters, indivletters, objects)

We request they not send us casework. If there is a letter directory including the word case,
make a note to review it during appraisal, after the metadata-based review.

## Reorganize the copy

The scripts require a consistent directory structure.
This typically means combining files from multiple disks to one directory 
and removing extra directory levels (BlobExport, dos, etc.).
Document the original arrangement in the processing plan.
The finished arrangement should look like the following, where Smith is the last name of the congressperson.

* smith_constituent_mail_export 
  * documents
    * _folders that contain the letters_ 
  * _metadata files_ 


## Run script in accession mode

`python accession.py input_directory accession`

The script will read the metadata, combine it if there are multiple metadata files, and create:
* Appraisal reports
* Metadata usability reports, including how many files in the export match the metadata
* Topic report

Unless the export is particularly small, this should be done by remoting into Hub.

Prior to running the script, verify:
* The expected metadata file(s) are present
* For exports with multiple files, if any new were received that we should incorporate
* For metadata files with a header, if they match what the script expects

Read errors
- Unexpected number of columns: add columns named "extra"
- Unicode error: document it, but no action required

The appraisal reports are only searching columns we believe have any probability of showing a restriction, 
like topics, file paths, office notes, and fill in text fields.
It results in too many false positives to search other columns, 
due to columns like names and addresses that would never show a restriction. 

The letter matching report removes duplicates before attempting to match (response letters often repeat).
so the number of metadata rows matched, unmatched, and blank will be fewer than the total metadata rows.

## Review script results

### Usability

The matching report shows how well the metadata and files in the export match.
We haven't determined a threshold of matching required, but can only provide access to files that are matched.

The metadata reports show if the columns with predictable patterns match those patterns.
We're not doing any data cleanup right now.
This report is used to find rows that did not parse into the correct columns, which can expose PII.
Main issue so far is delimiters not escaped right, which required editing the metadata file.

Topics: consider the number of blanks and how understandable the topics are without research.
We can only provide access to letters with topics.

### Appraisal Logs

!!!Since this is about reviewing what to keep, it might belong in the appraisal section.
It doesn't have to do with accepting the accession.

Save an unedited copy of both in "reports and logs" folder.

The appraisal delete log is more likely to be appraisal.
* Delete any rows that are false positives
* !!! Add tips and tricks for what to look for
* !!! Add tips and tricks if cannot open in Excel.
* Summarize decisions in processing plan.

The appraisal check log is looking for new terms that indicate appraisal, and will have a lot of false positives.
If the metadata is inconclusive (e.g., don't have enough detail), do not remove for appraisal.
* Watch for big patterns of not appraisal that we might want to add to the script.
* Narrow it down by removing any rows that don't have enough info (no doc or doc is id number and no notes)
* Indicators of casework:
  * Privacy form or PARF referenced
  * Staffer signature in fill shows them responsible for casework
  * Notes about your problem/situation or a family members problem/situation
  * Forwarding to another office is not enough, as that could be for more information
* !!! Add more tips and tricks for what to look for
* Add any rows for appraisal to the appraisal delete log
* Summarize decisions in processing plan.

5. Review the usability reports and determine if the donation is accepted.
6. If accepted, move on to appraisal. If not accepted, stop the accession and discuss with the collecting archivist.
During the initial review, determine if the export meets acceptance guidelines.