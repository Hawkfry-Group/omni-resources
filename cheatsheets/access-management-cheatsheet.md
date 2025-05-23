# Access Management in Omni

This can be achieved through both the connection, User roles/permissions and the omni model combined with user attributes.

## Access Management in Model
- **Row-Level Security**: 
    - Topic level: Can be enforced using user attributes combined with access filter

      ```
      access_filters:
      - field: products.brand
        user_attribute: customer
        values_for_unfiltered: [is_admin]
      ```

    - View Level: Has to be done with sql and user attributes combination, e.g.:

      ```
      name:
        sql: ${users.full_name}

      name_hidden:
        sql: |+
          CASE 
            WHEN {{omni_attributes.see_names}} = 'true'
            THEN ${users.name}
            ELSE 'No Access'
          END

      name_hashed:
        sql: |+
          CASE 
            WHEN {{omni_attributes.see_names}} = 'true'
            THEN ${users.state}
            ELSE MD5(${users.name})
          END
      ```

- **Column-Level Security**: 
  - Using `required_access_grants` to limit a user's ability to query a field based on assigned user attributes:
  
    ```
    full_name:
      required_access_grants: region_access    # References an access_grant defined in model file
    ```
    
  - Can be applied to individual fields, entire topics, or view files
  - The referenced access_grant must first be defined in the model file
  - Access grants only affect direct access and queries, not references within the model

## Access Management via Connection
- **Connection-level restrictions**: 
  - Controlled and implemented by administrators
  - Restrict what data users can see at the database level
  - Applied globally across all queries made through that connection
  - Cannot be overridden by model developers
  - Best used for enforcing strict organizational data boundaries and compliance requirements

## Access Management via Model Access
- **Model-level restrictions**:
  - Controlled and implemented by model developers
  - Can be used to restrict developer access to specific parts of the model
  - Useful for creating development sandboxes or limiting access to sensitive model components
  - Administrators can manage which developers have access to which models
  - Provides granular control over who can modify specific parts of the data model

## Access Management of Content via Folders

- Content access is handled via content sharing and folder level permissions
- A workbook owner can share a workbook
- Owners of folders can make all workbooks in a folder available
- Regardless if a workbook is shared,  if the user has data access restrictons the data will not be shown

# Omni User Management Tool

For managing users, groups, and user attributes with Omni from the command line, you can use the [omni-user-manager Python package](https://github.com/Hawkfry-Group/omni-user-manager).

- **Purpose:** Synchronize users, groups, and user attributes with Omni via the command line.
- **Installation:**
  ```bash
  pip install omni-user-manager
  ```
  (Recommended: install in a Python virtual environment)
- **Features:**
  - Sync users, groups, and attributes using Omni APIs
  - Supports JSON and CSV data sources
  - Multiple sync modes (full, groups-only, attributes-only)
  - Easy CLI usage

See the [GitHub repository](https://github.com/Hawkfry-Group/omni-user-manager) for usage instructions and examples.