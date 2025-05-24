# @content_migration_folder.py
# This script uses the omni SDK to copy content to a new folder in your Omni instance.
# Set your API key, new model ID, and instance name as described below.

from omni_python_sdk import OmniAPI

dashboards_to_move = [
    '5e5dac8e',
]

# Initialize the API with your credentials
api = OmniAPI()

for dashboard in dashboards_to_move:
    try:
        # retrieve the dashboard
        dashboard_export = api.document_export(dashboard)

        # update the export with the new base model ID and folder path
        dashboard_export.update({
            'baseModelId': '2e238a8e-33f8-4a7d-a035-de50022f9961',
            'folderPath': dashboard_export['dashboard']['workbook']['folder']['path']
        })

        # import the modified document
        api.document_import(dashboard_export)

        print(f"✅ Successfully moved dashboard {dashboard}")

    except Exception as e:
        print(f"❌ Failed to move dashboard {dashboard}: {e}")
