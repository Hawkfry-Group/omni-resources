# Omni Data Modeling Best Practices

## Overview

This guide provides recommendations for effective data modeling in Omni. Following these practices will help you create maintainable, performant, and user-friendly data models.

## Promoting Logic to Shared Models

- **When to promote logic**: Promote common or frequently used logic to the shared model when:
  - The logic is used across multiple workbooks
  - The logic is non-trivial
  - The pattern is repeatable

- **When to keep logic in workbooks**: Keep logic in workbooks when:
  - It's specific to a single dashboard
  - It's a one-off use case
  - It would unnecessarily complicate the shared model

## Field Definitions and References

- Use Omni field references (e.g., `${field_name}`) rather than raw table names whenever possible
- This simplifies maintenance by requiring updates in only one place when underlying column names or logic changes
- Define default drill fields for each view to enable consistent exploration

## Measures and Calculations

- **Optimal number of measures**: Keep measures focused and purposeful
  - Too many similar named measures can overwhelm users and the AI 
  - Users are able to create their own, less is more when you first deploy, encourage users to create new ones which you can then promote.


- **Use filtered measures** instead of writing CASE WHEN statements directly in measure SQL
  - Aim for measures that answer key business questions with fitlers, over requiring the user to select right dimension filters and measure combinations. This is a better UX.
  - This allows Omni to pass through filters on drill fields
  - Improves query performance
  - Quicker loading of filter drop downs

- **Promote calculations judiciously**:
  - Promote workbook calculations that are frequently used
  - Keep one-off calculations in their specific workbooks (promote to workbook only)

## Managing Relationships

The whole point in omni model is to manage the query layer. If you have many complex joins it suggests there is improvements to make in your warehouse architecture to materilise tables. Many complex joins are hard for data warehouse services to query plan. Else consider using view_queries to simplify any complex joins.

### Global vs Topic-Specific Relationships

- **Global relationships** (defined in the relationships file):
  - Available for use across any topic
  - Best for common joins that will be reused in many places
  - Example: joining products to orders on products.id = orders.product_id

- **Topic-specific relationships** (defined in the topic file):  
  - Relevant only in a specific context
  - Useful for single-use fact tables or aliased joins
  - Ideal when the same table serves different roles in different contexts
  - Example: Salesforce contacts table used as Account Manager, Account Executive, and Customer in different topics

### Relationship Types and Join Selection

- Choose the appropriate relationship type to ensure metrics are calculated correctly:
  - **one_to_one**: Each record in table A matches exactly one record in table B (and vice versa)
  - **many_to_one**: Multiple records in the join_from_view can match a single record in join_to_view
  - **one_to_many**: A single record in join_from_view can match multiple records in join_to_view
  - **many_to_many**: Multiple records in each table can match multiple records in the other

- Select the appropriate join type based on data requirements:
  - **always_left** (default): Returns all records from the left table with matching records from the right
  - **inner**: Returns only records that have matches in both tables
  - **full_outer**: Returns all records from both tables
  - **cross**: Returns the Cartesian product of both tables

### Managing Fan-out and Bi-directional Joins

- **Understand fan-out implications**:
  - By default, Omni curates the workbook UI to avoid unexpected join relationships
  - Joins that "fan out" the dataset (add multiple rows) are filtered from the UI by default if no PKs defined
  - Omni will correctly compute aggregates without the Fanouts if primary keys are defined in views (unique key)

- **Use reversible flag mindfully**:
  - Set `reversible: true` when a join should function bi-directionally
  - One-to-one joins are always reversible
  - Many-to-many joins are reversible by default
  - For one-to-many relationships, consider the impact on metrics before making reversible

### Advanced Join Techniques

- **Aliasing joins** for clarity and multiple use cases:
  - Use `join_to_view_as` to alias the joined table with a new name
  - Use `join_to_view_as_label` to control the view label when using this join
  - Helpful when joining the same table multiple times with different contexts
  - Avoids the issues of a dev using the wrong join
  - Renames the default view name in the topics UI, useful for end users

### Best Practices for Join Management

- Use Omni field references (`${field_name}`) in join conditions rather than raw table names (DRY code). Manages field definitions in one place over having to manage across muliple files.
- Leverage Omni's UI to build joins when possible for simple relationships, this can be pushed down to all or single topics
- Joins can be made in both workbook model or/and shared model
- Document complex join logic with comments in the model
- Setup data tests for joins outside omni to ensure they still reflect current data structure

## Templated Filters

Omni allows parameterization of SQL using the mustache template engine. This can be applied anywhere you see ```sql:``` by injecting dynamic text into a SQL query. This syntax can be used to reference most objects in the IDE, but in this example (templated filters) it would reference a filter_only field ```filters:```


- Where possible, use dashboard and workbook controls to avoid unnessary templated filters in the shared model (such as perod over period, or data granularity fields).
- Templated filters are very powerful, but can be hard for developers to wrap their heads around. It's also easier to create silent errors if data changes (validator will only pick up if the sql is not valid). They should be used only when there isnt a less complex solution.
- Examples include injection a filter only field value into another fields sql (e.g. setting a custom currency rate which injects the rate into price fields/measures)



## Performance Optimization

- Push heavy queries into the database using transformation tools like DBT
- Use `ignored_schemas`, `included_schemas`, and `ignored_views` to limit the scope of views in Omni, this helps the validator performance.
- For complex calculations used frequently, test performance against hitting your warehouse vs hitting omnis duckdb engine. 
- Set up appropriate indexing and partitions on frequently queried fields within your data warehouse.
  - Setup ```default_filter``` at topic level to encourage users to use partition and clustered fields.
  - Consider enforcing use of parition/cluster fields as filters using  ```always_where_sql``` at topic level

## Model Organization

- Structure your model logically using topics. Topics can be grouped into folders using ```group_label``` in the topic
- Create a clear hierarchy that matches your business domains. Topic names and folders are sign posts for users AND AI context.
- Use consistent naming conventions for fields and measures for both the object names (to assist developers) and label based on business user context
    example
    
    ```count_california_seniors:
    label: Number of California Seniors
    aggregate_type: count
    filters:
      age:
        greater_than_or_equal_to: 65
      state:
        is: California
    ```
    
    
- Add descriptions to fields, measures, and views to improve user and AI understanding

## Integration with DBT

- Set up the DBT integration if you're using DBT to:
  - Pull through existing descriptions
  - Import table configuration
  - Enable bi-directional workflow
  - Push new models from Omni back to DBT
  - Wish to select dbt environments to aide in development and testing in omni
