# Workflow for Constituent Mail: Appraisal

## Review Appraisal Logs

Save an unedited copy of both in "reports and logs" folder.

### Appraisal Delete Log

The appraisal delete log is more likely to be appraisal.
* Delete any rows that are false positives
* !!! Add tips and tricks for what to look for
* !!! Add tips and tricks if cannot open in Excel.
* Summarize decisions in processing plan.

### Appraisal Check Log

The appraisal check log is looking for new terms that indicate appraisal, and will have a lot of false positives.
If the metadata is inconclusive (e.g., don't have enough detail), do not remove for appraisal.
* Watch for big patterns of not appraisal that we might want to add to the script.
* Narrow it down by removing any rows that don't have enough info (no doc or doc is id number and no notes)
* Indicators of casework:
  * Privacy form or PARF referenced
  * Staffer signature in fill shows them responsible for casework
  * Notes about your problem/situation or a family members problem/situation
  * If the note is that it isn't case or casework, still count as casework since it was sensitive enough to be considered
  * Forwarding to another office is not enough, as that could be for more information
* !!! Add more tips and tricks for what to look for
* Add any rows for appraisal to the appraisal delete log
* Summarize decisions in processing plan.

## Run Script in Appraisal Mode

`python accession.py input_directory appraisal`

The script will read the metadata, combine it if there are multiple metadata files, and create:
* Delete letters due to appraisal
* Make restrictions review report

Unless the export is particularly small, this should be done by remoting into Hub.

Prior to running the script, verify:
* The appraisal_delete_log.csv in output_dir with only rows to be deleted (from previous step)
* Add topics for restriction review to restrictions list in restriction_report() and document in processing plan. 
  Get the topics from the topics report. Either need to do exact matches (even when delimiter)
  or change to testing if topic includes instead of equals and get more false positives.
* Check for new path formats and add to update_path()
* Calculate the number of files in the documents folder, to check after that the right number were deleted.

QC of the script
* Number of files in the documents folder decreases by the expected amount (number of files in the deletion log without a path error)
* Number of files in the deletion log matches the number in appraisal delete log
* Check a few files in the log are not in the export

## Folder Level Review

Check the form letter folder for filled in privacy forms, tour lists with social security numbers, and other privacy issues.

Check all other folders except indivletters and objects (huge, rely on metadata) for folders or subfolders that suggest restrictions.
If you decide to delete, documentation TBD.

When checking files, copy a small sample and only open the copy, or it risks metadata changing.
Record in the processing plan which you reviewed, the percent reviewed, and your findings.

## Metadata Review

For exports with multiple metadata files, delete any metadata file that is for casework only.
Document in the processing plan.

## Restriction Review
Requests for assistance on these topics are likely to include highly sensitive information 
and are being restricted from access until we make a determination of if they should be retained 
or restricted for 75 years.

Save a full copy of this in "reports and logs". Work on a copy so can delete as you determine it isn't restricted.
Like with appraisal, has to be clearly about their personal situation and not an opinion or too little info to decide.

Financial and health are personal and can be deleted (like casemail).
TBD on how to do that. Maybe this report does need to be made before I run appraisal?

Criminal justice or immigration could be personal but of historical value.
Haven't encountered any yet. Will decide then if delete or just restrict.

## Complete Accessioning

Continue with the standard accessioning workflow to complete the accession.

Do some QC to compare the original to the appraised copy?
Do less if going to do preservation and access immediately?
