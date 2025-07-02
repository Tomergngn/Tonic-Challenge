import atexit, pickle, os
import requests
from requests.auth import HTTPBasicAuth

if os.path.exists("issues.pickle"):
    # Load existing issues from the pickle file
    with open("issues.pickle", 'rb') as f:
        issues = pickle.load(f)
else:
    issues = []

def closeIssues():
    global issues
    # Saving what we got from issues to a pickle file for next runs
    with open("issues.pickle", 'wb') as f:
        pickle.dump(issues, f)

atexit.register(closeIssues)

def count():
    auth = HTTPBasicAuth("tomer.gal.netser@gmail.com", "ATATT3xFfGF0RNn7nze2AKpMLEmx_ub5wJRDnE2REwTXg8AFWBQRqvjqdoP4cseH_ufUMKynSceEK8bGD1feYdQN4zL93A5pQejprt7mIROvUTL-HCD8vszSawLtZVmZeUpfpaUPDLrezQ83gHVR1K3rHgZIIyMz_R3leZPkxHE0upaRFfVO75Y=87ADD768")
    headers = {"Accept": "application/json"}

    # Step 1: Search for all issue keys in the project
    search_url = "https://tomergngn.atlassian.net/rest/api/3/search"
    params = {
        "jql": "project=TDECP",
        "fields": "key",
        "maxResults": 5000
    }
    response = requests.get(search_url, headers=headers, auth=auth, params=params)
    return len(response.json().get('issues', []))

def updatePickle():
    global issues
    from jira import JIRA
    # Connect to your Jira instance
    jira = JIRA(
        server="https://tomergngn.atlassian.net",
        basic_auth=("tomer.gal.netser@gmail.com", "ATATT3xFfGF0RNn7nze2AKpMLEmx_ub5wJRDnE2REwTXg8AFWBQRqvjqdoP4cseH_ufUMKynSceEK8bGD1feYdQN4zL93A5pQejprt7mIROvUTL-HCD8vszSawLtZVmZeUpfpaUPDLrezQ83gHVR1K3rHgZIIyMz_R3leZPkxHE0upaRFfVO75Y=87ADD768")
    )

    # Pagination setup
    block_size = 8
    start_index = len(issues)
    while True:
        issuesCur = jira.search_issues(
            "project=TDECP",
            startAt=start_index,
            maxResults=block_size,
            fields="description"
        )
        if not issuesCur:
            break
        start_index += block_size
        issues.extend([{'key': issue.key, 'description': issue.fields.description} for issue in issuesCur])
    
    # Save the issues to a pickle file
    with open("issues.pickle", 'wb') as f:
        pickle.dump(issues, f)
    
    return issues

def main(full_update=False):
    global issues
    if full_update:
        issues = []
    updatePickle()
    return issues
