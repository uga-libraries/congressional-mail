# Workflow for Constituent Mail: Preservation

Appraisal must be fully complete prior to making the AIPs.
For closed collections, we haven't decided if we will make AIPs during accessioning
or if we'll wait until they can open to implement any additional appraisal criteria added while the collection was closed.

## Make a Preservation Copy

Within the collection folder, make a folder named CMSPreservationCopy or CSSPreservationCopy.
The rest of making a copy depends on how large the export is.

### Smaller Exports
For exports under 100,000 files 
(TBD on if this is the correct boundary - depends on how long it takes to make the copy and run the script)
   1. Make a folder named "aips_directory" within PreservationCopy
   2. Copy the export folder from AppraisalCopy into aips_directory with TeraCopy

### Larger (more typical) Exports
For exports over 100,000 files
   1. Copy the export folder from AppraisalCopy into PreservationCopy with robocopy remoted into Hub: see [accession.md](accession.md)'s Appraisal Copy section for instructions
   2. Rename the "documents" folder to "aips_directory"
   3. Add "documents_" to the front of all folder titles within aips_directory
   4. Move all metadata files to a new folder named "export_metadata" within aips_directory

Note: if there is a ProcessingCopy, use that instead of the AppraisalCopy.

I was originally not going to make a separate PreservationCopy to save time,
since most AIP creation errors can be resolved by moving files (e.g., out of incomplete bags).
However, the appraisal process would be even more time-consuming to replicate if we could not recover from an AIP creation error,
so we'll stick with our standard practice of working on a copy.

## Metadata CSV

Following the template [metadata.csv](https://github.com/uga-libraries/general-aip/blob/main/documentation/metadata.csv) for the general_aip.py script, make a metadata.csv file in aips_directory.

| Field      | Information to Use                                                               |
|:-----------|:---------------------------------------------------------------------------------|
| Department | russell                                                                          |
| Collection | rbrl-###                                                                         |
| Folder     | folder name                                                                      |
| AIP_ID     | collid-er-###### <br/>Continue sequential number from other born-digital, if any |
| Title      | Constituent Mail Export: Folder Name                                             |
| Rights     | http://rightsstatements.org/vocab/InC/1.0/                                       |
| Version    | 1                                                                                |

## Create and Ingest AIPs

Run the [general_aip script](https://github.com/uga-libraries/general-aip) with the following arguments:
- aips_directory: path to aips_directory
- aip_type: general
- zip_method: tar-bz2
- workflow: no-file-info

This will make AIPs without a filelist, 
so that the enormous number of files in an export do not overwhelm the ARCHive application's metadata capacity.
This is acceptable since the vast majority of these are plain text files and not a preservation risk.
The formats will still be in ARCHive for risk analsyis, but underrepresented since they will only be counted once per AIP.

Follow the quality control and documentation portions of the [born-digital processing workflow](https://github.com/uga-libraries/born-digital-processing/blob/main/preservation.md),
except for checking bag size, since these AIPs are purposefully much larger.

TBD: Does the AIP to accession fixity comparison scale?
Is there even accession fixity information for the files, or is it just their zips?

After ingesting into ARCHive, add the Special Access Policy restriction to each AIP. 
TBD: make a Russell restriction related to these? Constituent Mail or more generic Privacy?

## ArchivesSpace

The constituent mail original export will already be in the finding aid, with a closure of 75 years.

Add the AIP ID(s) to the folder. 
These should potentially be a staff-only field to prevent someone requesting it.
It is needed for extra tracking that this exists, rather than just relying on ARCHive metadata.
