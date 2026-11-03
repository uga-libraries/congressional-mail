# Workflow for Constituent Mail: Preservation

Create AIPs with the original metadata and with each subfolder within documents (minus letters deleted for appraisal).
1. Reorganize the export in ProcessingCopy using TeraCopy. It is not worth the time to make a PreservationCopy.
   - Rename the "documents" folder to "aips_dir"
   - Add "documents_" to the front of all folder titles within "aips_dir"
   - Move all metadata files to a new folder named "export_metadata" within the "documents" folder.
2. Create the [metadata.csv](https://github.com/uga-libraries/general-aip/blob/main/documentation/metadata.csv) 
for the general_aip.py script, saved in "aips_dir".
   - Department: russell
   - Collection: collection_id
   - Folder: folder names
   - AIP_ID: rbrl-coll#-er-######, continuing the sequential number from other digital content for this collection, if any
   - Title: Name Constituent Email: Details, where Details is documents/foldername or metadata
   - Rights: http://rightsstatements.org/vocab/InC/1.0/
   - Version: 1
3. Follow the [preservation steps of the born-digital processing workflow](https://github.com/uga-libraries/born-digital-processing/blob/main/preservation.md), using the "general" AIP type and "no-file-info" workflow. 
