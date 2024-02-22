import csv
import requests


def fetch_project_ids(email, token):
    api_url = "https://api.practitest.com/api/v2/projects.json"
    auth = (email, token)

    response = requests.get(api_url, auth=auth)

    if response.status_code == 200:
        return [{'id': project['id'], 'name': project['attributes']['name']} for project in
                response.json().get('data', [])]
    else:
        print(f"Error in API call: {response.status_code}")
        return []


def fetch_custom_fields_for_project(email, token, project_id):
    api_url = f"https://api.practitest.com/api/v2/projects/{project_id}/custom_fields.json"
    auth = (email, token)

    response = requests.get(api_url, auth=auth)

    if response.status_code == 200:
        return {'project_id': project_id, 'custom_fields': response.json().get('data', [])}
    else:
        print(f"Error in API call for project {project_id}: {response.status_code}")
        return {'project_id': project_id, 'custom_fields': []}


def export_to_csv(custom_fields_data, csv_file_path):
    project_id = custom_fields_data['project_id']
    project_name = project_id_name_mapping.get(project_id, f"Unknown Project {project_id}")

    custom_fields = custom_fields_data['custom_fields']
    if not custom_fields:
        print(f"No custom fields for Project ID {project_id}")
        return

    header = ['project_id', 'project_name', 'id', 'type'] + list(custom_fields[0]['attributes'].keys())

    with open(csv_file_path, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        if csv_file.tell() == 0:
            writer.writeheader()

        for custom_field in custom_fields:
            field_data = custom_field.copy()
            attributes = field_data.pop('attributes', {})
            field_data.update({'project_id': project_id, 'project_name': project_name})
            field_data.update(attributes)
            writer.writerow(field_data)


if __name__ == "__main__":
    your_email = 'yourmail@yahoo.com'
    your_token = '123456'
    # place your Token here
    output_csv_path = 'all_projects_custom_fields_data.csv'

    project_id_name_mapping = {}  # Mapping to store project names based on project IDs
    project_ids = fetch_project_ids(your_email, your_token)

    for project_info in project_ids:
        project_id = project_info['id']
        project_name = project_info['name']

        # Store project name in mapping for later use
        project_id_name_mapping[project_id] = project_name

        custom_fields_data = fetch_custom_fields_for_project(your_email, your_token, project_id)
        export_to_csv(custom_fields_data, output_csv_path)

        print(f"Custom fields data for Project ID {project_id} ('{project_name}') appended to {output_csv_path}")

