# Install Requirements

Install the required dependencies from the requirements.txt file in rest_server

Navigate to rest_server and run the following command.

`pip install -r requirements.txt`

# Usage


Before export: `export PYTHONPATH="$PYTHONPATH:$(pwd)"` from the **rest_server** sub_folder.

Start with `python3 -m swagger_server -d <is_debug_on>`

Per default you can access the web gui over http://localhost:8080/v1/
