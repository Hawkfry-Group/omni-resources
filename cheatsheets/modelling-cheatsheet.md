# Omni Modeling Cheatsheet

## Modeling in Omni

 

### Model Layers & Promotion
- **Layered Approach**: Schema -> Shared Model -> Workbook.
- **Shared Model**: Central source of truth. Changes pushed here are accessible to other users and new workbooks.
- **Workbook Model**: Isolated space. Changes made here are *not* reusable by others unless promoted.
- **Promotion**: The action of pushing Workbook model changes to the Shared Model layer.

<img src="https://github.com/user-attachments/assets/d9cd9d8e-f0be-492a-aeca-4598a7eef8b1" alt="Cheatsheet for Modeling in Omni - visual selection" width="500">

### How and Where to Model
- Modeling can be done in the **Workbook Layer** or the **Development IDE**.
- **Workbook Layer**:
    - Users can model and query, keeping content isolated to that workbook.
    - Ideal for initial analysis and experimentation.
    - Supports UI-driven modeling:
        - **Quick Aggregates**: Right-click fields for SUM, AVG, etc.
        - **Custom SQL Fields**: Use "Add Field" feature, use `${field_name}` syntax.
        - **Excel-like Calculations**: Create new fields using spreadsheet calcs, can promote some to workbook
- **Shared Model Layer (IDE)**:
    - Central, shared, reusable business logic.
    - Managed via the IDE or by promoting changes from a Workbook.


### Best Practices

<img src="https://github.com/user-attachments/assets/13400b2e-c9f4-417c-8d92-9a75bc8a19c2" alt="Best Practice" width="500">

- **Promotion**: Promote common, frequently used, non-trivial logic to the Shared Model.
- **Isolation**: Keep logic specific to a single dashboard/analysis in the Workbook.
- **Semantic Model vs. SQL**: Use the semantic model for repeatable patterns; use SQL for one-off, complex queries (use slq views for subqueries, window functions).
- **Field References**: Use Omni field references (`${field_name}`) over raw table names.
- **Filtered Measures**: Use filtered measures instead of `CASE WHEN` in measure SQL when possible (allows filter passthrough on drill fields).
- **Schema Curation**: Use `ignored_schemas`, `included_schemas`, `ignored_views` to define relevant database objects.
- **Database Transformations**: Push heavy transformations (long-running, large data) to the database layer (e.g., using dbt).
- **dbt Integration**: Set up if using dbt to pull descriptions/configs and push back new models.

## Model File

<img src="https://github.com/user-attachments/assets/a2f46334-9adf-4359-ba82-9e580cbb36d7" alt="Model Components" width="500">

- **Purpose**: Defines model-wide configurations.
- **Key Configurations**:
    - Access Grants (for column, view or topic access)
    - Define Cache Policies (and set default)
    - Included/Excluded Schemas (`ignored_schemas`, `included_schemas` mentioned in `best-practices`)
- Acts as the top-level configuration file for the Shared Model.
- Possible to define full views and topics in this file, for niche edge use cases
- Models are version controlled with Git.

## Relationships File / Definitions
- **Purpose**: Define joins between tables.
- **Automation**: Omni automatically adds joinable tables based on column names by default on connection setup.
- **Curation**: Users can curate the list of joinable tables (add/remove).
- **Definition**: New joins can be added via a `relationships` file or as custom joins per-topic.
- **Refinement (UI/IDE)**:
    - Basic joins can be made in the workbook UI
- **Best Practice**: Set primary keys in views to prevent fanouts. 

## Topics Files / Definitions
- **Purpose**: Create curated data sets ("topics") for easier user navigation and self-service.
- **Creation**: Topics can be created in the model IDE or the Workbook UI in the Files panel
- **Configuration & Best Practices**:
    - **Limit Joins**: Limiting joined tables creates a cleaner exploration experience.
    - **Naming**: Apply clear, customized names for easier navigation.
    - **Grouping**: Group related topics using `group_label`.
    - **Field Accessibility**: Limit fields shown in each topic using views (hide/ignore unnecessary fields) or fields: [].
    - **Tagging**: Tagging measures and dimensions makes it easier to curate fields in a topic. `fields: [-tag:pii, -users.id]`
    - **Default Filters**: Set up default filters or `always_where_sql`.
    - **Saving**: Save changes so they are visible in the Workbook view of the topic.
    - **Caching**: Individual caching policy can be applied per topic

## View Files / Definitions
- **Purpose**: Define how tables/fields appear; control visibility and sql logic.
- **Configuration**:
    - **Field Hiding/Ignoring**: Used to limit field accessibility in Topics, hide unnecessary or helper fields.
    - Keeps views refined and relevant for users.
    - Define dimensions and measures sql definitions, formatting, descriptions, link & drill functionality 
    - Can be ignored globally via `ignored_views` setting.
    - dbt integration can pull view descriptions and config information.

## Updating Content (Workbooks)
- **Workflow States**:
    - **View Mode**: Users see the latest *saved* version. Non-interactive.
    - **Draft Mode**: Changes *auto-save* to draft.
    - **Exploration Mode**: Users can explore/iterate without impacting the saved version. Exploration changes are *not* saved. Exit exploration returns to the saved version.
    - **Import**: You can duplicate / copy tiles to a new workbook, make changes and then reimport into a workbook if you wish to avoid draft mode.
- **Saving**: Workbooks can be named and saved; appear in the content system. Unsaved accessible via Activity/URL.
- As of April 2025,"draft mode" changes being track only within a single draft, restrictions on multiple editors in a draft, no built in review/approval workflow for content. This will change in future*
