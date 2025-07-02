import pandas as pd
from jira import JIRA
import json
import sys, os
sys.path.append('./')
import PhaseTwo.getIssues as getIssues
import createissuescsv
# --- Configuration ---
JIRA_URL = "https://tomergngn.atlassian.net"
EMAIL = 'tomer.gal.netser@gmail.com'
API_TOKEN = 'ATATT3xFfGF0RNn7nze2AKpMLEmx_ub5wJRDnE2REwTXg8AFWBQRqvjqdoP4cseH_ufUMKynSceEK8bGD1feYdQN4zL93A5pQejprt7mIROvUTL-HCD8vszSawLtZVmZeUpfpaUPDLrezQ83gHVR1K3rHgZIIyMz_R3leZPkxHE0upaRFfVO75Y=87ADD768'
PROJECT_KEY = 'TDECP'
# --- Connect to Jira ---
jira = JIRA(
    server=JIRA_URL,
    basic_auth=(EMAIL, API_TOKEN)
)

total_issues = getIssues.count()

# --- Load CSV and Config ---
if not os.path.exists("jira_issues.csv"):
    createissuescsv.main()
df = pd.read_csv("jira_issues.csv")

with open("config.json") as f:
    config = json.load(f)

# Build mapping from field name (like "Severity") to its custom field ID (like "customfield_10039")
custom_fields = {}
for key, value in config.items():
    if isinstance(value, dict) and "id" in value:
        field_name = key.replace("_distribution", "").capitalize()
        custom_fields[value["id"]] = field_name

# Reverse mapping for easy lookup: {field_name: field_id}
field_name_to_id = {v: k for k, v in custom_fields.items()}

# --- Create Issues ---
for i, row in df.iterrows():
    if i < total_issues:
        print(f"Skipping row {i} as it already exists in Jira.")
        continue
    if i >= 5000:
        print("Reached the limit of 5000 issues. Stopping creation.")
        break

    issue_dict = {
        'project': {'key': PROJECT_KEY},
        'summary': row['Summary'],
        'description': row['Description'],
        'issuetype': {'name': 'Task'}
    }

    # Add custom fields
    for field_name in df.columns:
        if field_name != "Status" and field_name in field_name_to_id:
            field_id = field_name_to_id[field_name]
            issue_dict[field_id] = {"value": row[field_name], "name": row[field_name]}

    # Create the issue
    try:
        new_issue = jira.create_issue(fields=issue_dict)
        if 'Status' in row:
            jira.transition_issue(new_issue, row['Status'])
        print(f"Issue {new_issue.key} created.")
    except Exception as e:
        print(f"Error creating issue from row {i}: {e}")