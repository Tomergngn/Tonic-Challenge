from collections import defaultdict
import json
import matplotlib.pyplot as plt
import sys
sys.path.append('./PhaseTwo/')
import getIssues

def listFind(text, char_list):
    min_index = -1
    for char in char_list:
        index = text.find(char)
        if index != -1:
            if min_index == -1 or index < min_index:
                min_index = index
    return min_index

def count_servers(issues):
    server_counts = defaultdict(int)
    end_word = [' ', '.', ',', '!', '?', ':', ';', ')', '(', '-', '_', '/', '\\', '\n']
    for issue in issues:
        desc = issue['description']
        ind = 0
        while ind < len(desc):
            if desc[ind:ind+4] == "srv-":
                found_server = False
                for server in servers:
                    if server == desc[ind:ind+len(server)] and (len(desc) == ind + len(server) - 1 or desc[ind+len(server)] in end_word):
                        found_server = True
                        server_counts[server] += 1
                        ind += len(server)
                        break
                if not found_server:
                    print(f"Issue {issue['key']} contains an unrecognized server name: {desc[ind:listFind(desc, end_word)]}")
            ind += 1
    
    return dict(server_counts)

issues = getIssues.main()

with open("config.json") as f:
    config = json.load(f)

servers = config["servers"]
server_counts = count_servers(issues)


### DISPLAY RESULTS ###

# Plot
plt.figure(figsize=(8, 5))
plt.bar(server_counts.keys(), server_counts.values())

# Labels
plt.title("Number of Tickets per Server")
plt.xlabel("server Name")
plt.ylabel("num tickets")

# Optional: Rotate x labels if needed
plt.xticks(rotation=30)

# Show
plt.tight_layout()
plt.show()