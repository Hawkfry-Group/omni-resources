# Omni Branch Strategies Guide

## Overview
This guide outlines three practical branching strategies for Omni model development, considering Omni's unique workbook-to-model promotion workflow and Git integration.

## Strategy 1: Basic Workflow
Best for small teams or those new to Omni.

### Structure
```
main
└── feature branches
```

### Workflow
1. Create feature branch from `main`
2. Make changes in workbook layer
3. Test changes thoroughly
4. Promote to shared model
5. Check Content Validator
6. Create merge request (PR)
7. Merge to `main`

### Best Practices
- Keep changes small and focused
- Test in workbook before promotion
- Regular commits with clear messages
- Avoid stale branches

## Strategy 2: Multi-Instance Workflow
Best for teams working across development and production Omni instances in the same region.

### Structure
```
Instance 1 (Development)          Instance 2 (Production)
main --------------------------> staging/from-dev-YYYY-MM-DD
└── feature branches             └── main
```

### Workflow
1. Create feature branch in Instance 1
2. Develop in workbook layer or model IDE
3. Test changes thoroughly
4. Promote to shared model (if developed in workbook model)
5. Raise PR, Review, Merge to main in Instance 1
6. Use model migrate API to sync to Instance 2:
   ```
   POST /api/v1/models/{modelId}/migrate/target/upload
   
   Headers:
   - Authorization: Bearer {token}
   - Content-Type: multipart/form-data
   
   Form Data:
   - branch: "staging/from-dev-YYYY-MM-DD"
   - gitReference: "origin/main"
   - targetModelId: "{instance_2_model_id}"
   ```
7. Test in Instance 2 staging branch
8. Merge to main in Instance 2

### Key Components
- Two Omni instances in same region
- Model migration API for sync
- Use a CI runner to automate
- Automated branch creation
- Version-tracked migrations

### Best Practices
- Use dated staging branches
- Validate before migration
- Run content validator in both instances
- Document model IDs and endpoints
- Keep instances in sync
- Regular migration schedule

### Migration Process
1. Pre-migration Checklist:
   - [ ] Changes tested in Instance 1
   - [ ] Content validator passed
   - [ ] All dependencies included
   - [ ] Model IDs documented
   
2. Migration Steps:
   - [ ] Create new staging branch name
   - [ ] Prepare API call parameters
   - [ ] Execute migration
   - [ ] Verify branch creation
   - [ ] Test migrated changes
   
3. Post-migration:
   - [ ] Run content validator
   - [ ] Test critical paths
   - [ ] Document migration
   - [ ] Update stakeholders

## Strategy 3: Feature-Based Workflow
Best for larger teams working on multiple features simultaneously.

### Structure
```
main
├── model/customer-metrics
├── model/sales-analytics
└── model/inventory
```

### Workflow
1. Create feature-specific branch
2. Develop in isolated workbooks
3. Collect related changes
4. Promote to shared model
5. Review and test
6. Raise PR, Merge to main

### Organization
- Group related model changes
- Topic-based branches
- Feature-specific workbooks
- Collective promotions

## Omni-Specific Considerations

### Workbook Layer
- Use workbooks as development environment
- Test changes before promotion
- Keep experimental work isolated

### Shared Model Promotion
1. Validate changes in workbook
2. Check dependencies
3. Review impact on existing models using content validator
4. Promote
5. Test after promotion

### Branch Naming Conventions
```
model/OM-123-customer-metrics
topic/OM-456-sales-analytics
hotfix/OM-789-join-fix
```