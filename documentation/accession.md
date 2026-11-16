# Workflow for Constituent Mail: Accession

Accession as soon as possible after the donation is received, so we can address any problems with the export with the donor.

## Copy Export

### Copy from Transfer Media

1.  Follow the usual [Born Digital Accessioning](https://github.com/uga-libraries/born-digital-accessioning) 
   steps for transfer media (virus scanning, copy to Hub, documentation). 
    * If received on an external hard drive, do not include the hard drive software when copying
    * Wait to bag until after the next step (unzipping)
    * QUESTION: still want the initial manifest or format report? If so, wait until unzip

 
2. Unzip all zipped files with 7-Zip.
    * Document folders are often zipped as rar files
    * Remote into Hub for unzipping to make it faster
    * Retain the zips until processing is done

   
3. Bag the accession now the files are unzipped, so we can better verify authenticity after processing.

### Appraisal Copy

1. Set up folders within the collection folder.

Within the collection folder, make a new folder named CSSAppraisalCopy or CMSAppraisalCopy (name with export type).
This will keep constituent mail separate from other born-digital content.
Within that, make a folder named name_constituent_mail_export, where "name" is the last name of the congressperson.

Make a folder named "reports and logs" within AppraisalCopy. 
All permanent script outputs should be added to this folder throughout this workflow.

2. Copy files to AppraisalCopy.

Copy the accession (if bagged, just the contents of the data folder), without any zips, to the export folder. 
For smaller exports, use TeraCopy over the network. 
For larger exports (unclear what the threshold is, but it is from file count),
remote into Hub and use robocopy instead. This may still take multiple hours.

To use robocopy, change the terminal directory to the collection folder on Hub and use the following command:
   
    `robocopy SOURCE DESTINATION /S /E /COPY:DAT /LOG:PATH\AppraisalCopy.log` 

The source folder is not copied. Just its contents are. It will show as skipped in the log.

The log size in file properties will not increase, but it still may be working.
You have to make a copy of the file for it to update file properties and to review progress.

The resulting log is so long that it is not easy to find error messages.
We haven't encountered an error yet to know what message to search for.
The number of "New File" should match the number of files.
The number of "100%" (indicates success) may be lower than that, as it doesn't count all 0 byte files as complete.

For extra confidence, compare the file count and size in bytes between AppraisalCopy and the source folder.

Move AppraisalCopy.log to the reports and logs folder.

3. Start processing plan.

Use the [processing plan template](ConstituentMailProcessingPlan.docx) 
to start a processing plan in the AppraisalCopy folder. Reference the template for what to document.

## Export Completeness

Check the export contains all expected files:

* One or more metadata files
  * CMS DIF has multiple .out files
  * CSS Archiving has 2 .dat files (one with primary metadata, one for form letters)
  * CSS DIF has multiple .dat files
* Description of the metadata fields in the export (filename varies, usually a Word doc)
* Reports on missing files (often named nonexist.txt)
* A README
* Directories with the text of the letters (common directories: formletters, indivletters, objects)

We request they not send us casework. If there is a directory including the word case,
make a note to review it during appraisal, after the metadata-based review.
It may just be templates, which are fine to retain, but anything with a constituent's personal information will be deleted.

Also note any non-standard files received, like a PST of their schedule.
If it is not directly part of the export, it should be processed with the rest of the born-digital.

## Reorganize ApppraisalCopy

The scripts require a consistent directory structure.
This typically means combining files from multiple disks to one directory and removing extra directory levels.
Metadata files may need to be moved out of a separate folder.

For extra protection against error, use TeraCopy when moving the files.
The finished arrangement should look like the following, where "name" is the last name of the congressperson.

* name_constituent_mail_export 
  * documents
    * _folders that contain the letters, e.g. form letters_ 
  * _metadata files_ 

The folders that contain the letters may also have subfolders, which should stay where they are.
We just want to remove any additional folders between "documents" and the first folders that contain files,
such as blobexport and dos.

The metadata files include the description of the export, reports, and README, as well as the metadata for the letters (DAT or OUT).

## Run script in accession mode

### Script preparation

Prior to running the script, verify:
 
* For data interchange exports with multiple metadata files, check if any new were received that we should incorporate. 
  Use the function read_metadata() to see what files are currently included, and the export description to see what information is in the skipped ones. 
* The expected metadata file(s) are present, by comparing to read_metadata().
* For the archiving format metadata file, which has a header, see if the column names match what the script expects.

For the last two, the script will give an error if the expected conditions are not met,
but it may save time to catch the problem before starting, if possible.

### Script command

`python path/to/script input_directory accession`

The input_directory is the path to AppraisalCopy/name_constituent_mail_export

### Script outputs

All outputs are saved in AppraisalCopy. The export is not changed.

* appraisal_check_log.csv (metadata rows that might be a new indicator of appraisal)
* appraisal_delete_log.csv (metadata rows likely to be appraisal)
* metadata_formatting_errors_COLUMN.csv (1 per column with errors, used to find parsing errors)
* usability_report_matching.csv (how well the document paths in the metadata match the files in the export)
* usability_report_matching_details.csv (the document paths in the metadata or files in the export with no match)
* usability_report_metadata.csv (how many columns are missing, blank, or have formatting errors)
* topics_report.csv (number of occurrences of each topic, or each topic combination if the export allows delimiters)

## Review script results

### Printed warnings

If there is a warning that characters were skipped due to UnicodeEncodeError, no action is required.

For the data interchange format, if there is a warning that lines were skipped for having too many fields,
this can be addressed by adding additional column names. Only do this if it is a significant number of rows.
It is acceptable for a few rows to be skipped, since they are still in the preservation copy.
1. In the read_metadata() function for CSS or read_metadata_file() for CMS, 
   add as many columns named "extra#" to the file's column names as the maximum number of fields from the error message. 
   All column names must be unique, so continue with the sequential number for extra if the file already has some.


2. Add the extra# column names to remove_pii(), so they will be removed.
   Thus far, the error is from additional, unexpected columns at the end of the data.
   We don't have a strategy for if it is some middle columns that need to be dropped to keep data in the right columns.
   The metadata formatting error reports should reveal if the data is shifted incorrectly.


3. Delete all script outputs and run the script again, verifying the lines are no longer skipped.

If there are warnings about the script itself (e.g., deprecation warnings), make a GitHub issue, if one does not already exist.
These may indicate code that will stop working with later versions of Python.

### Letter Types

Based on the folder names in documents, does the export include letters from constituents or just by the office?
The letters from constituents are usually in a folder named objects.
The letters by the office are usually in folders named form letters and indivletters.

We have retained an export that just had letters by the office, but it lessens the value.
If an export also had very incomplete metadata, being by the office only may further decrease the chance we keep it.

### Metadata Formatting Errors

There will be one report for each column with potential errors.
The columns tested are dates, document paths, states, and zip codes.

We do not currently do any data cleanup, so these reports are not needed to find and fix formatting errors.
Instead, they are used to find errors in the metadata.

#### Column Parsing Error

It is possible for data in rows to be put in the wrong columns, which risks PII being put in public columns.
This is detected when a different kind of data shows up in a column with a formatting rule, like a city in the zip code column.

If the rows with this formatting error do not have both a document path and a topic, which is required for access to the files,
and there is no PII in public columns included in the redacted metadata, no action is required.
We may still try to fix it if it is a large number of rows, since that impacts the quality of the redacted metadata.
If there is PII in public columns, this needs to be fixed or the rows removed from the redacted metadata.


The primary case we've had with that so far is when most information was in the first few columns.
There were tabs (the delimiter) in the contents of a few cells that were not escaped properly. 
They had the quote at the start of the contents but not the end.
The next quote many rows later was detected as the end of that cell's contents and the data from all those rows was combined in that one cell.

Fixing the file (AppraisalCopy only):
1. Make a copy of any metadata file to be edited
2. Read into a pandas df
3. Save as a csv with the index number
4. Use a plain text editor to find any rows (a row starts with the file number, like 1B) without an index number
5. Search for those rows in the copy and add the missing quote at the end of the cell's contents
6. To check, repeat 2-4 with the edited metada file and confirm all rows have an index number
7. Once you're satisfied, overwrite the metadata file in AppraisalCopy with the edited version
8. Delete script outputs and run the script again with the updated metadata

#### Path Errors

Use the document path formatting report to find new patterns for translating the metadata paths to match the export.
Any path in this report (as opposed to other types of data that ended up in a document column) is a new pattern.
Add the new transformation(s) to the update_path() function.

This happened once where the metadata had "formletter" and the directory had "form letter".
In this case, we renamed the directory to match the metadata, rather than changing update_path().

If there were a large number of document paths with a new pattern, the usability reports for matching need to be recreated.
1. Delete the two usability report matching csvs
2. Comment out the function calls under `if script_mode == 'accession'` except for check_letter_matching()
3. Run the script in accession mode again

### Topic Report

For topics, consider the number of blanks and how understandable the topics are without research.
We can only provide access to letters with topics.

For exports that use delimiters in the topic column (assigning more than one topic to a letter), 
the topic report shows every topic combination separately.
It can be helpful to make a unique list of individual topics to more quickly review their understandability.
We can add this version of the report to the script at some point.

1. Open in Excel
2. Delete the count column(s)
3. Split the topic column by ^ (the delimiter)
4. Move topics from all other columns back to the first column (sort by each column first to get all non-blanks next to each other before copying and pasting into the first column)
5. Remove duplicates
6. Save to "reports and logs" with the name "topics_report_unique.csv"

### Usability Reports for Matching

The matching report shows how well the metadata and files in the export match.
We haven't determined a threshold of matching required, but we can only provide access to files that are matched.
When there are large numbers of files, a lower percent match can still be useful, since it is still a lot of content.

The script removes duplicates before attempting to match (response letters often repeat),
so the number of metadata rows matched, unmatched, and blank will be fewer than the total metadata rows.

### Usability Report for Metadata

Check which columns have a high number of blanks.
This is especially a problem for in/out date, topic, and document path, which are essential for access and analysis.
A high number of blanks in text fields means less information for appraisal and restriction review.
Other columns are less essential.

If the formatting is "uncheckable", that means it is a text field with no pattern to verify.

## Acceptance of the accession

We have received some incomplete exports, which are less useful because of missing metadata.
If the problem is in the portion of the export received (e.g., did not get the topic metadata file), we could ask for missing files at the time of receipt.
If the problem is limited data entry or the missing files cannot be supplied, 
we must decide if it is worth the considerable effort to make the export usable.

We hope to establish guidelines with the collecting archivists for what constitutes a complete enough export.
For now, review any with low numbers of document matches or topics with the collecting archivist for a decision.

If the export is accepted, move on to appraisal. 
If the export requires additional files, redo the accession steps once the files are received.
If the export is not accepted, follow deaccessioning procedures.