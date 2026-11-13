# Workflow for Constituent Mail: Access

See the processing plan (started during accessioning) for what to document from this stage.

Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and future validation process.

## Run Script in Access Mode

The script will remove metadata rows for appraisal and restrictions and columns for PII, 
make copy of metadata split by calendar year,
make a copy of incoming and outgoing correspondence in folders by topic
make the start of an inventory for ArchiveSpace with title, dates, and extent

When running on Hub, you may need to unfreeze it periodically by typing any letter in the terminal window.
If it was frozen, it will start printing that it started the next topic right away.
If it is just on a topic with a lot of letters, that will do nothing.

`python accession.py input_directory access`

The input_directory is the path to AppraisalCopy/name_constituent_mail_export.
The output_directory will be AppraisalCopy.

Prior to running the script, verify:
* Output directory contains appraisal_delete_log.csv, created in accession mode and edited during appraisal.
* Output directory contains restriction_review.csv, created and edited in appraisal mode.

QC:
* Number of topics
* Spot check the number of files in a few of the topics
* Spot check a few of the files in files not found log are not in the export
* Redacted full metadata compared to the by year

The metadata in appraisal_delete_log.csv and restriction_review.csv, and their associated files (if present)
will not be included in the access copy.

QUESTION: should we give the files a more obvious name, to differentiate from the originals in "reports and logs"?

For CMS Data Interchange Format, include Table 8C for the form letter metadata.
If we every receive 8D, merge fields, potentially merge that with 8C.
Do not include the other form letter file, 8E, as it links to the individual letter and may be a privacy concern.

## Restarting the script

start topics sorting where the script left off,
make the start of an inventory for ArchiveSpace with title, dates, and extent

`python accession.py input_directory access_restart`

The input_directory is the path to AppraisalCopy/name_constituent_mail_export.
The output_directory will be AppraisalCopy.

For access_restart mode, the access mode must have created topics_sort_metadata.csv and topics_sort_complete.txt.
If it didn't get that far, delete the outputs and run the access mode again.

Just css_archiving has this right now, although css_dif has a more manual (have to comment things out) version.
The topic sorting takes a long time and can either break (path length issues) 
or just get stuck (terminal cursor is blinking, no error message, but it isn't doing anything.

It doesn't make the inventory for ArchivesSpace until the topic sorting finishes without an error,
so the inventory should include everything.

## Review DIPs

Delete any topic folders that do not provide meaningful access, such as:
* Dates
* Numerical codes
* Staff names or roles
* Workflows (e.g., no response required)

Do not add to the deletion log, since they are still in present in the restricted full export.

Unless it is obviously staffer initials, do leave in letter codes, as they may be a meaningful acronym.

I have also combined topics that were highlight related, like pro/con versions of the same topic.
If do this, must combine the metadata csvs as well.

Mostly leave the folder names as is, but you can correct obvious misspellings,
and replace the underscore from an unpermitted character with something more meaningful.
Update the topic portion of the metadata.csv filename to match any changes.
Wait to expand on acronyms or add additional information until making the ArchivesSpace inventory.

## Package DIPs

Package the script output into DIPs according to the standard born-digital workflow.
This is in development, but rename to add access number, maybe zip.

### Letters by Topic

Each topic folder is a separate DIP. Characters that cannot be in a Windows folder name are replaced with an underscore.
It will have a csv with the metadata for every file that was in the export and sorted into the DIP. 
Rows are not included if they didn't have a document or the document wasn't in the export (or both documents, for archiving).
If topics were delemited, each topic is sorted separately, with the same file copied to each topic.
Export folder structure is maintained with the topic folders.

### Form Letters

Copy the entire form letter folder form the export.

For data interchange exports with multiple form letter metadata files, 
only include the combined form letter metadata made by the script.

For the archiving export with a form letter DAT file, convert to CSV (just for access copy, preservation has DAT)
1. Open in Excel, selecting tab as the delimiter.
2. Use filter to check each column has the right kind of information and there are no extra columns.
3. Save as a CSV.
4. Open in Notepad++ and confirm the number of rows matches the DAT and there are no obvious Excel formatting issues.

Open the form letter metadata in Notepad++ and briefly review for useless rows.
We have deleted rows with nothing but a document_id before.

### Correspondence Metadata

Full redacted metadata and by_year folder are in one DIP together.

The by_year is the same metadata as full redacted, just for that calendar year to make smaller csvs for easier review.
The calendar year is based on date received ("in"), and if blank then date responded ("out"), and for data interchange format "update" or "reminder/tickler".
If all of these are blank, it goes in undated.

## ArchivesSpace  

Include an explanation of the export and how it has been altered during processing in each DIP
and summarize that information in the finding aid as a processing note.

Start with aspace_inventory.csv, which will have the title, start and end date, and extent in GB for every topic folder,
and the title for the other folders. Edit here, because filtering doesn't work well in the Excel template.

* Edit dates
  * Start and end same = delete end, type single, expression blank
  * Start and end diff = type inclusive, expression start-end
  * Date unknown = check metadata.csv (possible typo in filename or path length)
* Round extent if still not working correctly (TBD - make a text formatted column to avoid conversion to scientific notation in ASpace if small)
  * Size count_not_calculate = get from folder properties
* Get dates and extent for form letters, metadata, and original export

Dates are from date received ("in"), which is sufficient estimate of the date range without factoring the other dates.

Edit titles to include explanations of acronyms and abbreviations.
Don't change the folder name, as that impacts path length and can cause errors.
This can surface things that need to be combined, so update the inventory.
Or if have a lot of abbreviations, do the research first and reorganize before re-generating the inventory.
