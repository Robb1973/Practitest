import csv
import requests


class CustomField:
    def __init__(self, id, name, field_format, project_id, possible_values, possible_values_parent_cf_id, parent_list_id,
                 created_at, updated_at):
        self.id = id
        self.type = "custom-fields"  # Assuming it's always "custom-fields"
        self.attributes = {
            "name": name,
            "field-format": field_format,
            "project-id": project_id,
            "possible-values": possible_values,
            "parent-list-id": parent_list_id,
            "possible-values-parent-cf-id": possible_values_parent_cf_id,
            "created-at": created_at,
            "updated-at": updated_at
        }


def make_api_call(custom_field_instance, email, token):
    # Replace the following URL with your actual API endpoint
    api_url = f"https://api.practitest.com/api/v2/projects/{custom_field_instance.attributes['project-id']}/custom_fields/{custom_field_instance.id}.json"

    # Convert the CustomField instance to a dictionary
    custom_field_data = {
        "data": {
            "id": custom_field_instance.id,
            "type": custom_field_instance.type,
            "attributes": custom_field_instance.attributes
        }
    }

    # Extract 'id' and 'project-id' from the data
    field_id = custom_field_data['data'].pop('id', None)
    project_id = custom_field_data['data']['attributes'].pop('project-id', None)

    # Set up authentication with email and token
    auth = (email, token)

    # Make the API call with authentication
    response = requests.put(api_url, json=custom_field_data, auth=auth)

    if response.status_code == 200:
        print(f"API call successful for CustomField ID {field_id} in Project ID {project_id}")
    else:
        print(f"Error in API call for CustomField ID {field_id} in Project ID {project_id}: {response.status_code}")


def populate_json_and_make_api_calls(csv_file_path, email, token):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            custom_field_instance = CustomField(
                id=row['id'],
                name=row['name'],
                field_format=row['field_format'],
                project_id=row['project_id'],
                possible_values=row['possible_values'],
                parent_list_id=row['parent_list_id'],
                possible_values_parent_cf_id=row['possible_values_parent-cf-id'],
                created_at=row['created_at'],
                updated_at=row['updated_at'],
            )

            # Make the API call for each CustomField instance
            make_api_call(custom_field_instance, email, token)


# Example usage:
csv_file_path = 'File.csv'
your_email = 'myemail@yahoo.com'
your_token = '123456'
populate_json_and_make_api_calls(csv_file_path, your_email, your_token)

