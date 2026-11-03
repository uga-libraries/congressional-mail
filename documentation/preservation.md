# Workflow for Constituent Mail: Preservation

Appraisal must be fully complete prior to making the AIPs.
For exports that cannot be open, we haven't decided if we will make AIPs during accessioning
or if we'll wait until they can open to implement any additional appraisal criteria added during the restriction period.

## AIP Boundaries

For exports under 100,000 files (not sure if this is the right maximum), make one AIP for the entire export.

Otherwise, do one AIP per subfolder within "documents" and an AIP for the metadata.
Reorganize the export in ProcessingCopy using TeraCopy. It is not worth the time to make a PreservationCopy.
  * Rename the "documents" folder to "aips_dir"
  * Add "documents_" to the front of all folder titles within "aips_dir"
  * Move all metadata files to a new folder named "export_metadata" within the "aips_dir" folder.

## Metadata CSV

Following the template [metadata.csv](https://github.com/uga-libraries/general-aip/blob/main/documentation/metadata.csv) for the general_aip.py script, make a metadata.csv file in "aips_dir".
  * Department: russell
  * Collection: collection_id
  * Folder: folder names
  * AIP_ID: rbrl-coll#-er-######, continuing the sequential number from other digital content for this collection, if any
  * Title: Name Constituent Email: Details, where Details is documents/foldername or metadata
  * Rights: http://rightsstatements.org/vocab/InC/1.0/
  * Version: 1

## Create and Ingest AIPs

Follow the [preservation steps of the born-digital processing workflow](https://github.com/uga-libraries/born-digital-processing/blob/main/preservation.md).
For the general_aip.py script arguments, use the "general" AIP type and "no-file-info" workflow. 

This will make AIPs without a filelist, 
so that the enormous number of files in an export do not overwhelm the ARCHive application's metadata capacity.

TBD: Does the AIP to accession fixity comparison scale?
Is there even accession fixity information for the files, or is it just their zips?

Once in ARCHive, add Special Access Policy restriction. 
And maybe make a Russell restriction related to these? Constituent Mail or more generic Privacy?

## ArchivesSpace

Add as the last thing within the constituent mail export.
Include a closure of 75 years.
