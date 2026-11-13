# Workflow for Constituent Mail: Access

See the processing plan (started during accessioning) for what to document from this stage.

Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and backlog validation process.

QUESTION: how to update appraisal to match current practice?
Do we have to run appraisal mode again? 
Is there a risk we've removed things that current practice would retain?
Would it be better to not appraisal until it is time to process, since it doesn't save much space?

QUESTION: is it ok to skip the ProcessingCopy?
The usual practice for born-digital is separate AppraisalCopy and ProcessingCopy.
But for constituent mail, the script makes a copy of the input to generate the access copy, 
and that is all the processing happening. 
So, I'm planning to use AppraisalCopy for the script input without making a new copy.

## Run Script in Access Mode

### Script preparation

AppraisalCopy must contain:

* appraisal_delete_log.csv, created in accession mode and edited during appraisal
* restriction_review.csv, created and edited in appraisal mode

The metadata in appraisal_delete_log.csv and restriction_review.csv, and their associated files (if present),
will not be included in the access copy.

QUESTION: should we give these files a more obvious name, to differentiate from the originals in "reports and logs"?

For the Data Interchange Formats, check for new files received for form letters and decide if they should be included.
If so, update the function form_letter_metadata().
For the CMS Data Interchange Format, we do want to include 8D if it is received. 
We choose not to include 8E, as it links to the individual letter and may be a privacy concern.

### Script command

`python path/to/script input_directory access`

The input_directory is the path to AppraisalCopy/name_constituent_mail_export

When running on Hub, you may need to unfreeze the script periodically by typing any letter in the terminal window.
If it was frozen, it will print that it started the next topic right away.
If it is just on a topic with a lot of letters, that will do nothing.

### Script actions and outputs

All outputs are saved in AppraisalCopy. 

* archiving_correspondence_redacted.csv
* by_year with the redacted metadata split into one csv per year
* correspondence_by_topic with a copy of correspondence organized by topic
* logs from sorting by topic
* aspace_inventory.csv (the start of an inventory for ArchiveSpace with title, dates, and extent)

Redacted metadata means that all rows from appraisal_delete_log.csv and restriction_review.csv are removed,
as are all columns intended for PII.

If the script breaks during topic sorting, aspace_inventory.csv will not be made.

### Script QC

The number of topics makes sense based on the topics report. 
Not all topics will be included, since not all will have a letter in the export.

Spot check the number of files in a few of the topics.
For CSS Archiving, check with topics_sort_expected_file_count.csv.
Otherwise, the number of unique files associated with a topic is printed at the start of the topic,
but not all of these files will be in the export.

Spot check a few of the files in topics_sort_file_move_errors.csv are not in the export,
and check for any errors that are due to the expected path being made incorrectly.

For the redacted metadata, confirm the correct column headers are present
and the number of rows for each year match what is in the full redacted metadata.

Once the script is done (including any restarts), move logs to "reports and logs",
and the correspondence_by_topic and redacted metadata to a new folder CSSAccessCopy or CMSAccessCopy in the collection folder.

## Restarting the Script

Because topic sorting can involve copying millions of files,
the script runs over multiple days and is vulnerable to being interrupted.
The script has also broken due to path length errors and strange characters in filenames.

The CSS Archiving format is currently the only one set up to restart.
Something similar has been done with CSS Data Interchange format by commenting out different parts of the code.
We haven't needed this yet for CMS Data Interchange format.

### Script preparation

AppraisalCopy must contain topics_sort_metadata.csv and topics_sort_complete.txt.
If the script didn't get that far, delete all access outputs and run the script again in access mode.

Delete the topic folder that was in progress when the script broke.

### Script command

`python path/to/script input_directory access_restart`

The input_directory is the path to AppraisalCopy/name_constituent_mail_export

The script may be restarted as many times as needed to finish sorting all the topics.

### Script outputs

The output_directory is AppraisalCopy.

AppraisalCopy will already contain the following from the script running in access mode the first time:
* archiving_correspondence_redacted.csv
* by_year with the redacted metadata split into one csv per year

These are added by restarting the script:
* correspondence_by_topic with a copy of correspondence organized by topic
* logs from sorting by topic
* aspace_inventory.csv

The ArchivesSpace inventory is not made until after topic sorting completes, so it will contain all the folders,
even if the script is restarted multiple times.

## Review Correspondence by Topic

The aspace_inventory.csv must be updated to reflect these changes.
If enough changes are going to be made, 
recreate the aspace_inventory.csv with the script 
by commenting out the rest of access mode instead.

### Delete

Delete folders for topics that do not provide meaningful access, such as:
* Dates
* Numerical codes
* Staff names or roles (e.g., answered by intern)
* Workflow steps (e.g., no response required)

Unless it is obviously staffer initials, do leave folders named with letter codes, as they may be a meaningful acronym.

Do not add these to the deletion log, since they are still in present in the restricted original export.

### Edit

In most cases, we leave the topics as assigned by the office.
Correct obvious misspellings and optionally replace the underscore from an unpermitted character with something more meaningful.
If you change the folder name, also update the topic portion of the metadata.csv filename to match the change.

Wait to expand acronyms or add other information to improve searching until making the ArchivesSpace inventory.
Adding this text to the folder name frequently causes path length errors.

### Combine

Combined topics that are highly related, like pro/con versions of the same topic.
This gives the researcher fewer DIPs to request.

1. Make a new folder with the combined topic name.
2. Move all folders inside this new folder, which retains their original topic name.
3. Combine the metadata.csv for each folder into one, named with the combined topic name.

Combining the metadata can typically be done by opening in a plain text editor and copying/pasting.
We could make a script to do this if we do it frequently enough.

QUESTION: researching acronyms and abbreviations can surface topics that need to be combined or deleted.
Should the research be done sooner? I don't want to edit the aspace_inventory at this stage, 
since it may need to be re-generated.

## Package DIPs

Package the script output into DIPs according to the standard born-digital workflow.
This is in development, but rename to add access number and probably zip.

Once the collection is ready to open, move DIPs to the born-digital-access-copies folder.

### Correspondence by topic

Each topic folder is a separate DIP. 
The folder name matches the topic assigned by the office, except characters that cannot be in a Windows folder name are replaced with an underscore.
The export folder structure is maintained with the topic folders.
If topics were delimited (more than one topic assigned to a file), 
each topic has its own folder and the file with be in each topic.

Each topic folder contains a csv with the metadata for every file that was in the export and sorted into the DIP. 
Rows are not included if they didn't have a file path or the file wasn't in the export (or both documents, for archiving).

Use [dip-numbering.py](https://github.com/uga-libraries/processing-scripts) to add access ids to the start of each topic folder.
Start the sequential number at 1 unless there are already born-digital access copies for this collection.

Once they are numbered, they can be moved out of the Correspondence_by_Topic folder (and that empty folder deleted),
into the AccessCopies folder.

### Correspondence metadata

Make a folder named "correspondence_metadata" in AccessCopies.
Add the access id to this folder, using the next sequential number after the last topic.

This DIP contains:
* archiving_correspondence_redacted.csv
* by_year folder with redacted metadata
* the description of the export format (copy from the export folder)

### Form letters

Make a folder named "form_letters in AccessCopies".
Add the access id to this folder, using the next sequential number after correspondence_metadata.

This DIP contains:
* all form letters (copy from the export folder)
* form letter metadata

For the archiving export with a form letter DAT file, convert to CSV (just for access copy, preservation has DAT)
1. Open in Excel, selecting tab as the delimiter
2. Use filters to check each column has the right kind of information and there are no extra columns
3. Save as a CSV
4. Open in a text editor and confirm the number of rows matches the DAT and there are no obvious Excel formatting issues

For data interchange exports with multiple form letter metadata files, 
only include the combined form letter metadata made by the script.

Open the form letter metadata in a text editor and briefly review for useless rows.
We have deleted rows with nothing but a document_id before.

## ArchivesSpace  

### Folder list

Start with aspace_inventory.csv, which will have the title, start and end date, and extent in GB for every topic folder,
and the title for the other folders. Edit in the csv, because filtering doesn't work well in the ASpace Excel template.

Edit titles
  * Explain acronyms and abbreviations in square brackets after the text but before [electronic records]
  * Use the form letters as evidence to be confident in the information, since most acronyms have multiple meanings
  * If there are too many to research, focus on the ones with the most files (!!!Add link once script to count files is in GitHub)
  * Delete the folder if it turns out to be a staffer's initials or combine it with other topics if it turns out to be closely related, and update the aspace_inventory.csv accordingly

Edit dates
  * Make new columns for type and expression
  * If the dates are "unknown", get them from the metadata.csv (possible typo in filename or path length error)
  * If the start and end dates are the same
    * Delete the end date
    * Set the type to "single"
    * Leave the expression blank
  * If the start and end dates are not the same
    * Set the type to "inclusive"
    * Set the expression to "start-end" (use concatenate)

Edit extent
  * Round extent if still not working correctly (!!!I think it is though)
    - Make a new column for the updated extent
    - Reformat cells with scientific notation to be numbers
    - Use Excel to round the column, and then type the rounded version in the new column
    - More efficient if sort by size first
  * If extent is "could_not_calculate", get the size from folder properties

Add dates and extent for form letters, metadata, and original export, which are the last rows in the inventory.

### Import into ArchivesSpace

* Copy the information from aspace_inventory.csv into the correct columns in the ASpace Excel template.
* Add EAD ID, which is the ID in the finding aid data section of ASpace
* Add the hierarchical relationship, which is 1 for the first row, 
  2 for correspondence_by_topic, correspondence_metadata, form letters, and original export, 
  and 3 for the topic folders
* Add Description level, which is "series" for the first row and "file" for the rest
* Add Publish, which is True for all, unless the collection isn't ready to open yet (then do False)
* For the original export, add True for Restrictions Apply?
* The rest of the information is for DIP folders only, not the few folders that are for hierarchical organization
  - For Extent portion, add Whole
  - To prevent small extents from being converted to scientific notation when importing into ArchivesSpace, 
    change the cell formatting to text and then click on the cells so the Excel warning for number stored as text appears.
  - For extent type, add gigabyte(s)
  - For Container Instance Type and Top Container Type, add "electronic_records"
  - For Top Container, add "ER access-id"
  - For barcode, add access-id

The access-id is collection-access-###### and is part of the DIP folder name.
It generally works to use Excel to generate these numbers independent of the folder names.
However, if a folder title has punctuation early in the word (e.g., F-150),
it may be alphabetized differently by Excel and Windows, which means the numbers are assigned in a different order.
Do compare the numbers generated by Excel to the folder titles to check for differences,
and update the folder title if needed.
If this becomes a common issue, we'll figure out a better way to keep the inventory and folder name ids in alignment.

Once the spreadsheet is complete:
1. Use ASpace import functionality to add it to the finding aid 
2. Move it to the correct location (within the constituent mail series or subseries) 
3. Adjust the description level of the export folder to match with the collection organization

### Finding aid notes

First write these notes in a document in the collection folder, 
for spell check and to have a copy in case we need to reimport into ASpace to fix issues.
Below are examples, with data that always needs to be updated in curly brackets.
These should be customized to capture anything specific to this export that a researcher needs to know.

#### Constituent Mail Export Scope and content 
Constituent mail is managed by congressional offices in a proprietary database system. 
We received an export of the database information in {2 DAT files} and each letter in a separate file.

The export is in the {CSS archiving} format, with fields described in more detail in {layout.txt} 
(Correspondence Metadata [electronic files], {rbrl-190-access-000287}). 
There are many files described in the database that are not in the export, 
and many files in the export which are not described in the database.

#### Constituent Mail Export Appraisal
Deleted {16,162} files that were academy applications, casework, job applications, requests for recommendations, or for routine office functions.

#### Correspondence by Topic Scope and content note
The letters in the export were reorganized into folders named with their topic from the office-assigned metadata for improved access. 
Acronyms and abbreviations are expanded based on information in the form letters for better searching. 
There are {286} topics and approximately {4.2 million} files. 
A copy of a letter is included in each topic that it was associated with.  

The original folders that the letters were in ({form, letter}, and any subfolders) are replicated within the topic folder. 
Each topic folder also contains a CSV with the metadata for the letters in that topic. 

#### Form Letters Scope and content note 
Form letters are the templates used by the office to respond to common inquiries. 
There are {9,155} letters. 
{There is also a file with metadata for these letters, which has been converted from a DAT to a CSV.} 
We have not evaluated how well the metadata aligns with the form letters we received. 

#### Correspondence Metadata Scope and content note
Columns identifying individuals (names, addresses, and office note fields) and rows for letters deleted during appraisal 
are excluded from this metadata to protect constituent privacy. 
The file archiving_correspondence_redacted.csv is the complete resulting metadata, 
and a copy of the same information was saved in one CSV per year to provide smaller tables for easier review in spreadsheet programs. 
The metadata also includes {layout.txt}, which describes all metadata columns in this export format in more detail. 

#### Original Export Conditions Governing Access 
The complete export is closed for 75 years to protect constituent privacy. 
It will be open for research on January 1, {2090}.