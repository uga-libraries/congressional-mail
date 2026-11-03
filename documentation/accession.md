# Workflow for Constituent Mail: Accession

Accession as soon as possible after the donation is received, so we can address any problems with the export with the donor.

## Copy Export

### Copy from Transfer Media

*  Do usual steps (virus, copy to Hub, etc.) for transfer media [Born Digital Accessioning](https://github.com/uga-libraries/born-digital-accessioning)
*  If received on an external hard drive, do not include the hard drive software.
*  Unzip. Retain the zips until processing is done, but move into their own folder.
*  Bag now? We haven't been doing that, but there can be quite a delay before accessioning is done,
   so it would be better for verifying authenticity. It is just slow.

### Appraisal Copy

Make another copy to work on, so it is easier to recover if there are errors during arrangement or appraisal.

Within the collection folder, make a new folder named CSSAppraisalCopy or CMSAppraisalCopy (name with export type).
This will keep constituent mail separate from other born-digital.
Within that, make a folder names smith_constituent_mail_export, where "Smith" is the last name of the congressperson.
Then copy the accession (if bagged, just the contents of the objects folder, without any zips) to the export folder.

For smaller exports, use TeraCopy over the network. 
For larger exports (unclear what the threshold is, but it is from file count),
remote into Hub and use robocopy instead. This may still take multiple hours.

Change the terminal directory to the collection folder on Hub and use the following command:
   
    `robocopy SOURCE DESTINATION /S /E /COPY:DAT /LOG:PATH\AppraisalCopy.log` 

The source folder is not copied. Just its contents are. It will show as skipped in the log.

The log size in file properties will not increase, but it still may be working.
You have to make a copy of the file for it to update file properties and to review progress.

The resulting log is so long that it is not easy to find error messages.
The number of "New File" should match the number of files.
The number of "100%" (indicates success) may be lower than that, as it doesn't count all 0 byte sizes.

For extra confidence, compare the file count and size in bytes between this copy and the original accession folder.

Make a folder named "reports and logs" within AppraisalCopy and move AppraisalCopy.log to it.
All script outputs of permanent value should be added to this folder throughout this workflow.

## Export Completeness

Check the export contains all expected files:

* One or more metadata files
  * CMS DIF has multiple .out files
  * CSS Archiving has 2 .dat files (one with primary metadata, one for form letters)
  * CMS DIF has multiple .dat files
* Description of the metadata fields in the export (filename varies, usually a Word doc)
* Reports on missing files (often named nonexist.txt)
* A README
* Directories with the text of the letters (common directories: formletters, indivletters, objects)

We request they not send us casework. If there is a letter directory including the word case,
make a note to review it during appraisal, after the metadata-based review.

Also note any non-standard files received, like a PST of their schedule.
If it is not directly part of the export, it should be processed with the rest of the born-digital.

## Reorganize ApppraisalCopy

The scripts require a consistent directory structure.
This typically means combining files from multiple disks to one directory and removing extra directory levels.

For extra protection against error, use TeraCopy when moving the files.
The finished arrangement should look like the following, where "Smith" is the last name of the congressperson.

* smith_constituent_mail_export 
  * documents
    * _folders that contain the letters_ 
  * _metadata files_ 

The folders that contain the letters may also have subfolders, which should stay where they are.
We just want to remove any additional folders between "documents" and the first folders that contain files,
such as blobexport and dos.

Document the original arrangement in the processing plan.

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

5. Review the usability reports and determine if the donation is accepted.
6. If accepted, move on to appraisal. If not accepted, stop the accession and discuss with the collecting archivist.
During the initial review, determine if the export meets acceptance guidelines.