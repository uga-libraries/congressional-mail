# Workflow for Constituent Mail: Appraisal

See the processing plan (started during accessioning) for what to document from this stage.

## Review Appraisal Logs

Save an unedited copy of both in "reports and logs" folder.

### Appraisal Delete Log

The appraisal delete log is more likely to be appraisal.
* Delete any rows that are false positives
* !!! Add tips and tricks for what to look for
* !!! Add tips and tricks if cannot open in Excel.

### Appraisal Check Log

The appraisal check log is looking for new terms that indicate appraisal, and will have a lot of false positives.
If the metadata is inconclusive (e.g., don't have enough detail), do not remove for appraisal.
* Watch for big patterns of not appraisal that we might want to add to the script.
* Narrow it down by removing any rows that don't have enough info (no doc or doc is id number and no notes)
* Indicators of casework:
  * Privacy form or PARF referenced
  * Staffer signature shows them only responsible for casework (may be part of fill column)
  * Notes about your problem/situation or a family members problem/situation
  * If the note is that it isn't case or casework, still count as casework since it was sensitive enough to be considered
  * Forwarding to another office is not enough, as that could be for more information
* Some label a row "intern" because it was written by the intern, so it isn't enough on its own to be a job application
* Do not delete recommendations for public office
* Do not delete requests for interviews if it likely to be an interview of the congressperson
* Do not review further if it is related to a piece of legislation
* Do not review further if it has pro/con/neutral position
* Do delete individual help with finding a job , which is casework-like (likely to come up as possible job application)
* !!!Any more tips and tricks?
* Add any rows for appraisal to the appraisal delete log

## Select topics for routine office appraisal

Review the topic report for any topic related to routine office interactions, such as 
requests for flags, tours, congratulations, thank you’s, scouts, invitations, and holidays (Christmas cards, etc.)
We do want to keep replies to students writing for class.

Process is TBD, but need to add this to the appraisal delete log somehow.
The file level deletion does need to be logged and these files should not be in the preservation or access copies.
The metadata will also not be in the access copies.

## Select topics for restriction review

We are doing additional review for topics related to criminal justice, finances, health, and immigration.
Requests for assistance on these topics are likely to include highly sensitive information.

Review the topics report and update the list in the restriction_report() function with the exact topics to review.
Include any delimited versions of these topics.

## Run Script in Appraisal Mode

`python accession.py input_directory appraisal`

The script will read the metadata, combine it if there are multiple metadata files, and create:
* Delete letters due to appraisal
* Make restrictions review report

Unless the export is particularly small, this should be done by remoting into Hub.

Prior to running the script, verify:
* The appraisal_delete_log.csv in output_dir with only rows to be deleted (from previous step)
* Add topics for restriction review to restrictions list in restriction_report() 
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

Even if the file is casework, check it. If it is just form letters or other templates, it is ok to keep.
Only delete if it is about an individual's situation.

When checking files, copy a small sample and only open the copy, or it risks metadata changing.

## Metadata Review

For exports with multiple metadata files, delete any metadata file that is for casework only.

## Restriction Review
We are doing additional review for topics related to criminal justice, finances, health, and immigration.
Requests for assistance on these topics are likely to include highly sensitive information.

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
