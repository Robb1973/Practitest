import requests
import pandas as pd

# Your API token and authentication
api_token = 'your token'
email = 'your email'
auth = (email, api_token)
project_id = 'project id'

# API endpoint
url = f"https://api.practitest.com/api/v2/projects/{project_id}/issues.json?relationships=true"

# Make the API request
response = requests.get(url, auth=auth)
data = response.json()['data']

# Parse the JSON data and prepare the data structure for the DataFrame
issues_data = []
for issue in data:
    issue_data = {
        'ID': issue['id'],
        'Display ID': issue['attributes']['display-id'],
        'Title': issue['attributes']['title'],
        'Description': issue['attributes']['description'],
        'Status Name': issue['attributes']['status-name'],
        'Created At': issue['attributes']['created-at'],
        'Updated At': issue['attributes']['updated-at'],
        # Add custom fields here as needed
        'Number of Related Tests': len(issue['relationships']['tests']['data']),
        'Number of Related Requirements': len(issue['relationships']['requirements']['data'])
    }
    issues_data.append(issue_data)

# Convert the list of dicts into a DataFrame
df = pd.DataFrame(issues_data)

# Save the DataFrame to an Excel file
excel_filename = 'issues_report.xlsx'
df.to_excel(excel_filename, index=False)

print(f'Excel file "{excel_filename}" has been created successfully.')
