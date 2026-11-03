# Workflow for Constituent Mail: Access

See the processing plan (started during accessioning) for what to document from this stage.

Processing typically does not take place until after the collection can open.
If time allows, we may process at the time of accessioning to streamline the work and future validation process.

## Run Script in Access Mode

`python accession.py input_directory access`

The script will read the metadata, combine it if there are multiple metadata files, and create:
* Redact a copy of the metadata: remove rows for appraisal and restrictions and columns for PII
* Make a copy of the redacted metadata split by calendar year, for smaller files that are easier to open
* Make a copy of incoming and outgoing correspondence in folders by topic (restricted not included), 
  with a CSV with the redacted metadata for each letter found in the export.
* Make inventory for ArchiveSpace with title, dates, and extent.

Unless the export is particularly small, this should be done by remoting into Hub.
You may need to unfreeze it periodically by typing any letter in the terminal window.
If it was frozen, it will start printing that it started the next topic right away.
If it is just on a topic with a lot of letters, that will do nothing.

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

`python accession.py input_directory access_restart`

Just css_archiving has this right now, although css_dif has a more manual (have to comment things out) version.
The topic sorting takes a long time and can either break (path length issues) 
or just get stuck (terminal cursor is blinking, no error message, but it isn't doing anything.

It doesn't make the inventory for ArchivesSpace until the topic sorting finishes without an error,
so the inventory should include everything.

## Review DIPs

Delete any topic folders that do not provide meaningful access, such as dates or numerical codes.
Do not add to the deletion log, since they are still in present in the restricted full export.

I have also combined topics that were highlight related, like pro/con versions of the same topic.
If do this, must combine the metadata csvs as well.

## Package DIPs

Package the script output into DIPs according to the standard born-digital workflow.
This is in development, but rename to add access number, maybe zip.

### Form Letters

Copy the entire form letter folder form the export.
For exports with multiple files, use the combined form letter metadata.
If the export has a form letter DAT file, convert to CSV (just for access copy)

### Redacted Metadata

Full redacted metadata and by_year folder are in one DIP together.

### Letters by Topic

Each topic folder is a separate DIP.

## ArchivesSpace  

Include an explanation of the export and how it has been altered during processing in each DIP
and summarize that information in the finding aid as a processing note. 

I had been expanding on acronyms and abbreviations (from looking at the form letter to be sure) for better search
within the folder name, but that does cause problems with path length.
Instead, wait until they are in the inventory and expand only there.
