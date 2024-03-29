<!---
  Use this template when making consequential changes to the `/transform` directory,
  including changes to dbt models, tests, seeds, and docs.
--->

## Issue
<!--- Link the Issue this MR closes --->
Closes #

## Solution

Describe the solution. Include links to any related MRs and/or issues.

## Stakeholder Checklist
<details>
<summary><i>Click to toggle Stakeholder Checklist</i></summary>
If you are the person who will be using this data and/or the dashboard it depends on, please fill out this section.

- [ ] Does the dbt model change provide the requested data? 
- [ ] Does the dbt model change provide accurate data?
</details>

## Submitter Checklist

#### Testing - any exceptions must be noted

- [ ] Every model should be [tested](https://docs.getdbt.com/docs/testing-and-documentation) AND documented in a `schema.yml` file. At minimum, unique, not nullable fields, and foreign key constraints should be tested, if applicable.
- [ ] All models should be integrated into the [trusted data framework](https://about.gitlab.com/handbook/business-technology/data-team/platform/#tdf)
- [ ] Run the appropriate pipeline for the model changes in this MR
  - [ ] If there is an associated MR in the [Data Tests](https://gitlab.com/gitlab-data/data-tests) project, be sure to pass the branch name to the manual job using the `DATA_TEST_BRANCH` environment variable.
- [ ] If the periscope_query job failed, validate that the changes you've made don't affect the grain of the table or the expected output in Periscope.
- [ ] If you are on the Data Team, please paste the output of `dbt test` when run locally below. Any failing tests should be fixed or explained prior to requesting a review.

<summary> dbt test results </summary>

<pre><code>

Paste the results of dbt test here, including the command.

</code></pre>


#### Style & Structure

- [ ] Field names should all be lowercased.
- [ ] Function names should all be capitalized.
- [ ] Ensure source tables/views are only referenced within [base models](https://about.gitlab.com/handbook/business-ops/data-team/platform/sql-style-guide/#base-models).
- [ ] All references to existing tables/views/sources (i.e. `{{ ref('...') }}` statements) should be placed in CTEs at the top of the file.
- [ ] If you are using [custom schemas](https://docs.getdbt.com/docs/using-custom-schemas) or modifying [materializations](https://docs.getdbt.com/docs/materializations), ensure these attributes are specified in the model.


#### Pipelines

* [ ] Run the dbt_models pipeline with the full model selection syntax for all models which have changed
* [ ] Re-run the dbt_models pipeline (you may need to create a new pipeline with the "Run Pipeline" button), running only the models which have changed; e.g: dim_subscription. To remove any un-related pipeline failures.  

**Which pipeline job do I run?** See our [handbook page](https://about.gitlab.com/handbook/business-ops/data-team/platform/ci-jobs/) on our CI jobs to better understand which job to run.

**Provide an explanation here in case of any pipeline failures:**
<!--- explanation per pipeline failure and indicate why this is accepted ---> 


**What to do for failed pipelines** See our [handbook page](https://about.gitlab.com/handbook/business-ops/data-team/platform/ci-jobs/#what-to-do-if-a-pipeline-fails) 

#### Auditing
<details>
<summary><i>Click to toggle Auditing</i></summary>
What are you using to audit your results are accurate If you have an existing report/dashboard/dataset as reference, please provide your query used to validate the results of your model changes. If this is the first iteration of a model or validation is otherwise out of scope, please provide additional context.

- [ ] Have you updated the values in any `dbt_audit` macros that you're referencing?

<details>
<summary> Paste query and results here </summary>

<pre><code>

Example: You might be looking at the count of opportunities before and after, if you're editing the opportunity model.

</code></pre>
</details>
</details>

#### Macros

<details>
<summary><i>Click to toggle Macros</i></summary>

  - [ ] Does this MR utilize [macros](https://docs.getdbt.com/docs/macros)?
  - [ ] This MR contains new macros. Follow the naming convention (file name matches macro name) and document in the `macros.yml` file
</details>

#### Incremental Models

<details>
<summary><i>Click to toggle Incremental Models</i></summary>

- [ ] Does this MR contain an [incremental model](https://docs.getdbt.com/docs/configuring-incremental-models#section-how-do-i-use-the-incremental-materialization-)?
  - [ ] If the MR adds/renames columns to a specific model, a `dbt run --full-refresh` will be needed after merging the MR. Please, add it to the Reviewer Checklist to warn them that this step is required.
</details>

#### Schema or Model Name Changes
<details>
<summary><i>Click to toggle Schema or Model Name Changes</i></summary>

- [ ] Does this MR change the **schema** or **model name** of any existing models?
  - [ ] Create an issue to change all existing periscope reporting to reference the new schema/name.
  - [ ] After merging, ensure the old model is dropped from snowflake. This can be done by creating an issue specifying the tables/models to be dropped and assiging to a snowflake admin. 
</details>

#### Snapshot model
<details>
<summary><i>Click to toggle Snapshot model</i></summary>

- [ ] Is this MR creating or renaming a snapshot model?
- [ ] Does it concern Gitlab.com data?
  - [ ] Make sure its captured into the selection criteria of the [GDPR deletion](https://gitlab.com/gitlab-data/analytics/-/blob/master/transform/snowflake-dbt/macros/warehouse/gdpr_delete_gitlab_dotcom.sql) macro for GitLab.com data.
</details>

## All MRs Checklist
- [ ] This MR follows the coding conventions laid out in the [SQL style guide](https://about.gitlab.com/handbook/business-ops/data-team/platform/sql-style-guide/), including the [dbt guidelines](https://about.gitlab.com/handbook/business-ops/data-team/platform/sql-style-guide/#dbt-guidelines).
- [ ] [Label hygiene](https://about.gitlab.com/handbook/business-ops/data-team/how-we-work/#issue-labeling) on issue.
  - [ ] Apply Label [Business logic change](https://gitlab.com/gitlab-data/analytics/-/labels?subscribed=&search=business+logic+change) for any business logic changes like adding new dimensions, facts, marts, changing joins, adding new calculated fields.
- [ ] Branch set to delete. (Leave commits unsquashed)
- [ ] Latest CI pipeline passes.
  - [ ] If not, an explanation has been provided in testing section of this MR.
  - [ ] If (Sisense)/Periscope pipeline failed, link to the periscope issue/mr or provide an explanation:  
- [ ] This MR is ready for final review and merge.
- [ ] All threads are resolved.
- [ ] Remove the `Draft:` prefix in the MR title before assigning to reviewer.
- [ ] DBT full refresh required post merge?
  - [ ] Yes. Create an issue with the model name which needs to be refreshed and assign it to the Reviewer to run it post merge. 
  - [ ] No.
- [ ] Assigned to reviewer.

## Reviewer Checklist
- [ ]  Check before setting to merge
- [ ]  If DBT Full refresh is required?
  - [ ] Yes. Ensure to get the issue for Full Refresh Request. 
  - [ ] No.

## Further changes requested
* [ ]  AUTHOR: Uncheck all boxes before taking further action.
