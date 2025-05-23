# @document_migration.py
# This script should be used to migrate document content to a new model in your Omni instance.
# Set your API key, new model ID, and instance name as described below.
import subprocess
import os

# Set your Omni API key as an environment variable
OMNI_API_KEY = os.getenv('T_OMNI_API_KEY')
# Set your model ID and instance URL here
new_model_id = os.getenv('OMNI_MODEL_ID', '[your-model-id]')  # or set directly as a string
instance_name = os.getenv('OMNI_INSTANCE_NAME', '[your-instance-NAME]')  # or set directly as a string

# List of document IDs
document_ids = [
    "23456789",
    "12345678"
]

# Base URL for the API
base_url = f"https://{instance_name}.omniapp.co/api/v0/documents"

# Function to export a document
def export_document(doc_id):
    export_command = [
        "curl.exe",
        "-H", f"Authorization: Bearer {OMNI_API_KEY}",
        "-H", "Content-Type: application/json",
        f"{base_url}/{doc_id}/export"
    ]
    output_file = f"{doc_id}_sales.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        subprocess.run(export_command, stdout=f)

    return output_file

# Function to import a document
def import_document(file_path):
    import_command = [
        "curl.exe",
        "-X", "POST",
        "-H", f"Authorization: Bearer {OMNI_API_KEY}",
        "-H", "Content-Type: application/json",
        "--data-binary", f"@{file_path}",
        f"{base_url}/import"
    ]
    subprocess.run(import_command)

# Main loop to export and import documents
for doc_id in document_ids:
    print(f"Exporting document: {doc_id}")
    exported_file = export_document(doc_id)

    # Add baseModelId to the exported JSON file
    with open(exported_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        modified_content = content.replace(
            '{"dashboard":{',
            f'{{"baseModelId":"{new_model_id}","dashboard":{{'
        )
        f.seek(0)
        f.write(modified_content)
        f.truncate()

    print(f"Importing document: {doc_id}")
    import_document(exported_file)

print("Document transfer completed.")