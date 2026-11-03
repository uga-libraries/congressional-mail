# Workflow for Constituent Mail: Appraisal

Requires appraisal_delete_log.csv, created in accession mode.
This CSV may be manually edited (remove rows to not delete, add rows from appraisal_check_log.csv to delete).
For casework, delete even if the phrase indicates it is not a case or casework, 
because the fact they considered it suggests it includes sensitive personal information. 

1. Check the appraisal reports made during review for errors (based on file names) in what will be deleted or not deleted. Double check no form letters are being deleted.
2. Refine the script to catch new patterns, but some errors are acceptable given the scale.
3. Update the function update_path() for transforming the metadata path into the directory path, if needed.
4. Run the script in "accession" mode again to check your changes. It takes a long time to recopy an export if there are mistakes with deletion (next step).
5. Review the topics report and update the restrictions list in restriction_report() with additional highly sensitive topics.
6. Run the script in "appraisal" mode to delete letters flagged for appraisal. The metadata is not changed.
7. Delete any folders that are labeled casework and document those deleted files (probably with accessioning script).
8. Delete any metadata files that are just for casework.

Continue with the standard accessioning workflow to complete the accession.
