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
    auth = HTTPBasicAuth("tomer.gal.netser@gmail.com", "ATATT3xFfGF0qVcfXlup2I_BDd92MhXWto0vz46OLquwrs37wq7hhjB_SYG27nP9vJ6-DwzDYw_wFRQqAiDM1IsBo55tmHJmgDVDVnaUkQUpB7I2BU0tQluY7CPf0uLhyaIIIupJCFE1jg2NBx9g3yXjKraFS3QGf-YyGmonSBGAS9hreOHR9D4=47D22949")
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
        basic_auth=("tomer.gal.netser@gmail.com", "ATATT3xFfGF0qVcfXlup2I_BDd92MhXWto0vz46OLquwrs37wq7hhjB_SYG27nP9vJ6-DwzDYw_wFRQqAiDM1IsBo55tmHJmgDVDVnaUkQUpB7I2BU0tQluY7CPf0uLhyaIIIupJCFE1jg2NBx9g3yXjKraFS3QGf-YyGmonSBGAS9hreOHR9D4=47D22949")
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
