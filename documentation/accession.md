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

### Preparation

Prior to running the script, verify:
 
* For exports with multiple files, decide if any new were received that we should incorporate
* The expected metadata file(s) are present, by comparing to what is expected in check_arguments()
* For the css archiving format, which has a header, see if the column names match what the script expects

For the last two, the script will give an error if the expected conditions are not met,
but it may save time to catch the problem before starting, if possible.

### Script

Unless the export is particularly small, this should be done by remoting into Hub.

`python accession.py input_directory accession`

The input_directory is the path to AppraisalCopy/name_constituent_mail_export.

### Script Outputs

All script outputs will be saved to AppraisalCopy.

* appraisal_check_log.csv (metadata rows that might be a new indicator of appraisal)
* appraisal_delete_log.csv (metadata rows likely to be appraisal)
* metadata_formatting_errors_COLUMN.csv (1 per column with errors)
* usability_report_matching.csv (how well the document metadata matches the files in the export)
* usability_report_matching_details.csv (the document paths in the metadata or files in the export with no match)
* usability_report_metadata.csv (how many columns are missing, blank, or have formatting errors)
* topics_report.csv (number of occurrences of each topic or topic combination if the export allows delimiters)

The appraisal reports are only searching columns we believe have any probability of showing a restriction, 
like topics, file paths, office notes, and fill in text fields.
It results in too many false positives to search other columns, 
due to columns like names and addresses that would never show a restriction. 

The usability reports for matching removes duplicates before attempting to match (response letters often repeat).
so the number of metadata rows matched, unmatched, and blank will be fewer than the total metadata rows.

## Review script results

### Printed warnings

If there is a warning that characters were skipped due to UnicodeEncodeError,
document that in the processing plan. No action is required.

If there is a warning that lines were skipped for having too many fields,
this can be addressed by adding columns named "extra#" (each has to be unique) when reading the file,
and then removing those files along with columns that have PII. Delete all script outputs and run the script again.
However, if there are not many rows being skipped, they do not need to be recovered.
The metadata is just for the access copies, and the complete metadata with these rows is still in the preservation copy.
Document the number skipped and if action was taken in the processing plan.

If there are warnings about the script itself, make a GitHub issue, if one does not already exist.
These may indicate code that will stop working with later versions of Python.

### Metadata Formatting Errors

There will be one report for each column with potential errors.
The columns tested are dates, document paths, states, and zip codes.

We do not currently do any data cleanup, so these reports are not needed to find and fix formatting errors.
Instead, they are used to find rows that may not have parsed correctly, where PII could be shifted to public columns.

The primary case we've had with that so far is when most information was in the far left columns.
A delimiter within a cell that was not escaped properly, which put data from multiple rows in one cell.
To detect, read the file into a dataframe and print the number of rows. 
If it is smaller than the number of rows if you open the file in Notepad++, it means some rows are merged.

Fixing the file (AppraisalCopy only):
1. Make a copy of any metadata file to be edited
2. Read into a pandas df
3. Save as a csv with the index number
4. Use Notepad++ to find any rows (a row starts with the file number, like 1B) without an index number
5. Search for those rows in the copy and add the missing end quote
6. To check, read the edited copy into pandas and verify the row number
7. Once you're satisfied, overwrite the metadata file in AppraisalCopy with the edited version
8. Delete script outputs and run the script again with the updated metadata

If the rows do not have both a document path and a topic, which is required for access to the files,
and there is no PII in public columns included in the redacted metadata, no action is required.
We may still try to fix it if it is a large number of rows, since that impacts the quality of the redacted metadata.
If there is PII in public columns, this needs to be fixed or the rows removed from the redacted metadata.

Also use the document paths formatting report to find any new patterns.
The paths in the metadata need to be updated to match the paths in the export.
Add the required transformation to the update_path() function.
If it is a large number, the usability reports for matching need to be recreated.

### Topic Report

For topics, consider the number of blanks and how understandable the topics are without research.
We can only provide access to letters with topics.

The topic report shows every topic combination separately.
Make a unique list of topics for easier review with Excel: 
split the column at the delimiter (^), merge into one column, and deduplicate.
Save this to "reports and logs" with the name "topics_report_unique.csv"

### Usability Reports for Matching

The matching report shows how well the metadata and files in the export match.
We haven't determined a threshold of matching required, but we can only provide access to files that are matched.
When there are large numbers of files, a lower percent match can still be useful, since it is a lot of content.

Also review the matching details report for any errors caused by how the expected paths were generated.
There might be a lot of metadata only and directory only where the filenames match but the paths are a little off.
This happened once where the metadata had "formletter" and the directory had "form letter".

### Usability Report for Metadata

Check which columns have a high number of blanks.
This is especially a problem for in/out date, topic, and document path, which are essential for access and analysis.
Other columns are less essential.

### Acceptance of the accession

We have received some incomplete exports, which are less useful because of missing metadata.
If the problem is in the portion of the export received, we could ask for missing files at the time of receipt.
If the problem is limited data entry or the missing files cannot be supplied, 
we must decide if it is worth the considerable effort to make the export usable.

We hope to establish guidelines with the collecting archivists for what constitues a complete enough export.
For now, review any with low numbers of document matches or topics with the collecting archivist for a decision.

If the export is accepted, move on to appraisal. 
If it isn't, document that in ArchivesSpace and the collection folder, and delete from Hub (unless waiting on a fix).