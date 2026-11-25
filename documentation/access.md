# Workflow for Constituent Mail: Access

See the processing plan (started during accessioning) for what to document from this stage.

Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and backlog validation process.

QUESTION: if there is a delay before processing, how to update appraisal to match current practice?
Do we have to run appraisal mode again? 
Is there a risk we've removed things that current practice would retain?
Would it be better to not appraisal until it is time to process, since it doesn't save much space?

QUESTION: is it ok to skip the ProcessingCopy?
The usual practice for born-digital is separate AppraisalCopy and ProcessingCopy.
But for constituent mail, the script makes a copy of the input to generate the access copy, 
and that is all the processing happening. 
So, I'm planning to use AppraisalCopy for the script input without making a new copy.
UNLESS, are there standard born-digital processing steps that should be happening?

## Run Script in Access Mode

### Script preparation

AppraisalCopy must contain:

* appraisal_delete_log.csv, created in accession mode and edited during appraisal
* restriction_review.csv, created and edited in appraisal mode

The metadata in appraisal_delete_log.csv and restriction_review.csv, and their associated files (if present),
will not be included in the access copy.

Check the number of columns in 8C.out, which is form letter metadata.
We've encountered 3-4 additional columns besides the ones in the export description. These are kept and named untitled_#.
Open a copy in Excel and turn on filters to detect the maximum number of columns in the file.
Update the columns list in form_letter_metadata() to have the correct number of columns.

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

For CMS DIF and CSS Archiving, if the script is interrupted during topic sort,
see Restarting the Script (below) to continue without losing what is already done.
This hasn't been implemented for CSS DIF yet.

### Script actions and outputs

All outputs are saved in AppraisalCopy. 

* archiving_correspondence_redacted.csv
* correspondence_by_topic with a copy of correspondence organized by topic
* correspondence_metadata_by_year with the redacted metadata split into one csv per year
* finding_aid_inventory.csv (most of the information needed for the import template for ArchiveSpace)
* topic_sort_complete.txt
* topic_sort_expected_file_count.csv
* topic_sort_file_move_errors.csv
* topic_sort_metadata.csv

Redacted metadata means that all rows from appraisal_delete_log.csv and restriction_review.csv are removed,
as are all columns intended for PII.

If the script breaks during topic sorting, finding_aid_inventory.csv will not be made.
It is not made until topic sorting finishes successfully.

CSS DIF does not have all topic sort logs. It needs to be updated to match the others still.

### Script QC

The number of topics makes sense based on the topics report. 
Not all topics will be included, since not all will have a letter in the export.

Spot check the number of files in a few of the topics, 
either from topics_sort_expected_file_count.csv or the number of files printed at the start of the topic,
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

The CMS DIF and CSS Archiving formats are currently the only ones set up to restart.
Something similar has been done with CSS Data Interchange format by commenting out different parts of the code.

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
See the outputs section for running the script the first time for a complete list.

The finding aid inventory is not made until after topic sorting completes, so it will contain all the folders,
even if the script is restarted multiple times.

## Review Correspondence by Topic

The finding_aid_inventory.csv must be updated to reflect these changes.
If enough changes are going to be made, recreate the finding_aid_inventory.csv with the script 
by commenting out the rest of access mode instead.

### Delete

Delete folders for topics that do not provide meaningful access, such as:
* Dates
* Numerical codes
* Staff names or roles (e.g., answered by intern)
* Workflow steps (e.g., no response required)

For exports with delimited topics, it might be possible for a topic selected for routine office to show up in the topic sort,
if it was paired with another topic that is retained. If so, delete the routine office topic folder.

Unless it is obviously staffer initials, do leave folders named with letter codes, as they may be a meaningful acronym.

Do not add these to the deletion log, since they are still in the restricted original export.

### Edit

In most cases, we leave the topics as assigned by the office.
Correct obvious misspellings and optionally replace the underscore from an unpermitted character with something more meaningful.
If you change the folder name, also update the topic portion of the metadata.csv filename to match the change.

Expand acronyms or add other information to improve searching in the finding aid inventory, not the folder name.
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
Should the research be done sooner? I don't want to edit the finding_aid_inventory.csv at this stage, 
since it may need to be re-generated.

NOTE: we could adjust the topic sort to use a CSV mapping current topics to intended topics,
rather than editing after the fact. It could also skip ones without enough research value.

## Package DIPs

Package the script output into DIPs according to the standard born-digital workflow.
This is in development, but rename to add access number and probably zip.

Once the collection is ready to open, move DIPs to the born-digital-access-copies folder.

Constituent mail has one DIP per topic, as well as one for the redacted correspondence metadata and one for the form letters.

### Correspondence by topic

Each topic folder is a separate DIP. 
The folder name matches the topic assigned by the office, 
except characters that cannot be in a Windows folder name are replaced with an underscore.
The export folder structure is maintained with the topic folders.
If topics were delimited (more than one topic assigned to a file), 
each topic has its own folder and the file with be in each topic.

Each topic folder contains a csv with the metadata for every file that was in the export and sorted into the DIP. 
Rows are not included if they didn't have a file path or the file wasn't in the export (or both documents, for archiving).

Use [dip-numbering.py](https://github.com/uga-libraries/processing-scripts) to add access ids to the start of each topic folder.
Start the sequential number at 1 unless there are already born-digital access copies for this collection.
Verify the access numbers match what is in the inventory, since systems sort differently if there is punctuation in a title.
The AIP ID (the er number) is a separate numbering scheme, so that doesn't factor in to assigning the access number.

NOTE: if DIP numbers in alignment becomes too time-consuming, see issue #167 for an alternative idea.

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
* all form letters (copy from the export folder - it will repeat the folder name form_letters)
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

Most of the information needed is in finding_aid_inventory.csv. 
It must be copied to the ArchivesSpace import template, as we couldn't generate something that ArchivesSpace accepted.
Update the inventory before copying to the template, as the template is cumbersome to filter due to hidden rows.

Template columns used:

| Template Column           | Values for Constituent Mail                                    |
|---------------------------|----------------------------------------------------------------|
| EAD ID                    | ID in the finding aid section of ArchivesSpace                        |
| Title                     | Title [electronic files]                                       |
| Hierarchical Relationship | 1 for the first row, 3 for the topic folders, 2 for the rest   |
| Description Level         | "series" for the first row and "file" for the rest             |
| Publish?                  | True (or False if adding to ArchivesSpace before can go live)  |
| Restrictions apply?       | True for original export, blank for rest                       |
| Date(1) Begin             | Earliest year from date received column                        |
| Date(1) end               | Latest year from date received column (blank if same as begin) |
| Date(1) Type              | "inclusive" or "single"                                        |
| Date(1) expression        | Begin-End or blank if "single"                                 |
| Extent Portion            | Whole                                                          |
| Extent number             | Folder size rounded to 3 decimals, or the fewest to not be 0   |
| Extent type               | gigabyte(s)                                                    |
| Container Instance Type   | electronic_records                                             |
| Top Container type        | electronic_records                                             |
| Top Container             | ER barcode                                                     |
| Barcode                   | DIP ID (rbrl-123-access-000001) or AIP ID (rbrl-123-er-000001) |

While the export is rarely a series, it needs to be designated as one for the spreadsheet import to work.
It will be updated to the correct descriptive level after the import into ArchivesSpace. 

Changes to make before importing into ArchivesSpace:

1. Add EAD ID to every row


2. Enhance titles
  * Explain acronyms and abbreviations in square brackets after the text but before [electronic records] to improve searchability
  * Use the form letters as evidence to be confident in the information, since most acronyms have multiple meanings
  * If there are too many to research, focus on the ones with the most files (use topics_sort_expected_file_count.csv)
  * Delete the folder if it turns out to be a staffer's initials or combine it with other topics if it turns out to be closely related, and update the inventory accordingly

3. Supply missing information
  * If the dates are "unknown", get them from the metadata.csv
  * If extent is "could_not_calculate", get the size from folder properties
  * If the value is "TBD", get from metadata or file properties (last 3 rows)

3. Convert small extents in scientific format (e.g., 1e-05) to decimals
  * Add a column with a sequential number, so you can put this back in order
  * Sort by size, so the rows are all next to each other
  * Highlight all cells with scientific format and change the format to number
  * Highlight the column and change the format to text, so keep the decimal when importing into ArchivesSpace
  * The cells need to show they are numbers stored as text (green triangle in the cell) for this - click on them if not
  * Sort to get back in sequential order and delete that column

4. Update top container and barcode
  * Replace "collid" with the collection number, e.g., rbrl-123
  * If there are other access copies already for this collection, update the sequential number in these ids.

TBD: we might include a link to the redacted metadata for each DIP in the finding aid.

NOTE: we can prevent the scientific notation in the initial inventory by formatting to fix number of decimal places,
but that will result in extra trailing 0 (e.g., 0.00100)
To do this, use `format(extent_number, ".#f")`, where # is the number of decimals.
We could use rounder for the number of decimals to reduce the number of trailing 0s.

### Import into ArchivesSpace

1. Use ArchivesSpace import functionality to add the spreadsheet to the finding aid
   1. Open the collection in Edit mode
   2. Click "Load via Spreadsheet"
   3. Select the spreadsheet
   4. A new window will open to show status of the upload
2. Move it to the correct location (within the constituent mail series or subseries) 
3. Adjust the description level of the export folder, which is usually file but occasionally subseries, 
   whichever comes next in the collection hierarchy.
4. Process TBD: Include the AIP ID(s) on the original export folder. 
   Not sure if these are top containers or a note restricted to staff since the export is restricted.

### Finding aid notes

First write these notes in a document in the collection folder, 
for spell check and to have a copy in case we need to reimport into ArchivesSpace to fix issues.
Below are examples, with data that always needs to be updated in curly brackets.
These should be customized to capture anything specific to this export that a researcher needs to know.

#### Constituent Mail Export Scope and content 
Constituent mail is managed by congressional offices in a proprietary database system. 
We received an export of the database information in {2 DAT files} and each letter in a separate file.
{add note if only received letters by the office and not from constituents}

The export is in the {CSS archiving} format, with fields described in more detail in {layout.txt} 
(Correspondence Metadata [electronic files], {rbrl-190-access-000287}). 
There are many files described in the database that are not in the export, 
and many files in the export which are not described in the database.

#### Constituent Mail Export Appraisal
Deleted {16,162} files that were academy applications, casework, job applications, requests for recommendations, or for routine office functions.

#### Correspondence by Topic Scope and content note
The letters in the export were reorganized into folders named with their topic from the office-assigned metadata for improved access. 
Acronyms and abbreviations are expanded based on information in the form letters for better searching. 
There are {286} topics and {approximately 4.2 million} files. 
A copy of a letter is included in each topic that it was associated with.  

The original folders that the letters were in are replicated within the topic folder. 
Each topic folder also contains a CSV with the metadata for the letters in that topic. 

#### Form Letters Scope and content note 
Form letters are the templates used by the office to respond to common inquiries. 
There are {9,155} letters. 
There is also a file with metadata for these letters, {which has been converted from a DAT to a CSV. Rows that were blank except the ID were deleted.} 
We have not evaluated how well the metadata aligns with the form letters we received. 

#### Correspondence Metadata Scope and content note for archiving format
Columns identifying individuals (names, addresses, and office note fields) and rows for letters deleted during appraisal 
are excluded from this metadata to protect constituent privacy. 
The file archiving_correspondence_redacted.csv is the complete resulting metadata, 
and a copy of the same information was saved in one CSV per year to provide smaller files for easier review in spreadsheet programs. 
The metadata also includes {layout.txt}, which describes all metadata columns in this export format in more detail. 

For the data interchange format, add this sentence to the start of the note:
Selected columns from files {'out_1B.dat', 'out_2A.dat', 'out_2C.dat', 'out_2D.dat'} were combined using the {person_id and communication_id columns} from 2A to make a single metadata CSV with information on the location, topic, and dates of the letters. 

#### Original Export Conditions Governing Access 
The complete export is closed for 75 years to protect constituent privacy. 
It will be open for research on January 1, {2090}.

### Bulk editing in ArchivesSpace

Once the inventory has been added to ArchivesSpace, it can be edited using the bulk updated feature.

To get the spreadsheet to edit,
1. Open the collection in ArchivesSpace
2. Click on the collection name
3. Under more, click on bulk updater
4. Select the portion of the collection and the fields to include

The spreadsheet will be downloaded to your downloads folder.
Make a copy of the spreadsheet before editing, to have as a reference if more records are updated than you expect.

Make the edits in the spreadsheet and then upload back to ArchivesSpace under create > background job > bulk update job.

Warning: updating the container is tricky!
We ran into errors when renumbering after deleting a few folders.
The container could not be found to link to the item but also could not be made because the barcode was a duplicate.
If needing to renumber:
1. Leave in the folders being deleted
2. Use the bulk update spreadsheet to update the container numbers and barcodes
3. Delete the folders that are no longer needed