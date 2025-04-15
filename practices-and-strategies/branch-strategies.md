# Omni Branch Strategies Guide

## Overview
This guide outlines three practical branching strategies for Omni model development, considering Omni's unique workbook-to-model promotion workflow and Git integration.

## Strategy 1: Basic Workflow
Best for small teams or those new to Omni, focusing on **individual, sequential, or isolated development tasks**.

### Structure
```
main
└── development branches (e.g., feature/..., fix/..., user/dev-branch)
```

### Workflow
1. Create a **development branch** from `main` (e.g., `fix/OM-123-correct-calc`, `user/jane-doe/refactor-logic`).
2. **A developer** works on and tests changes within their **workbook**.
3. Promote relevant changes to the **shared model** on the **development branch**.
4. Run the **Content Validator** to check for downstream impacts.
5. Create merge request (PR) for review.
6. Merge to `main` after approval.

### Best Practices
- Keep changes small and focused.
- **Thoroughly test in the workbook before promotion.**
- Use clear commit messages.
- Run the Content Validator after promotion and before merging.
- Avoid letting feature branches become stale.

## Strategy 2: Multi-Instance Workflow
Best for teams needing separate development and production Omni instances (must be in the same region).

### Structure
```
Instance 1 (Development)          Instance 2 (Production)
main --------------------------> staging/from-dev-YYYY-MM-DD
└── feature branches             └── main
```

### Workflow
1. Create feature branch from `main` in Instance 1 (Dev).
2. Develop and test changes (using **workbooks** or the model IDE).
3. Promote changes to the **shared model** feature branch if needed.
4. Run **Content Validator** in Instance 1.
5. Merge feature branch to `main` in Instance 1.
6. **Sync `main` from Instance 1 to a `staging/*` branch in Instance 2 (Prod)** using the model migrate API.
7. Test thoroughly in the Instance 2 staging branch.
8. Run **Content Validator** in Instance 2.
9. Create PR to merge the staging branch into `main` in Instance 2.
10. Merge to `main` in Instance 2 after approval.

### Key Components
- Two Omni instances in the same region.
- Model migration API for syncing (consider CI automation).
- Dated or clearly named staging branches in Production.

### Best Practices
- **Validate changes and run Content Validator in Dev instance *before* migration.**
- **Test and run Content Validator again in Prod instance staging branch *before* merging to main.**
- Maintain consistent configurations between instances where possible.
- Establish a regular migration schedule if applicable.

## Strategy 3: Feature-Based Workflow
Best for larger teams **coordinating multiple related changes for a single larger feature or topic**, often involving contributions from several developers or workbooks.

### Structure
```
main
├── model/ticket-123-customer-metrics
├── model/sales-analytics
└── model/inventory
```
(Branch names are feature/topic-focused)

### Workflow
1. Create a feature-specific branch from `main` (e.g., `model/customer-metrics`).
2. **Multiple developers** work on related changes in their **individual workbooks**.
3. **promote** related changes from multiple workbooks onto the **git feature branch**.
4. Test the integrated changes on the feature branch.
5. Run the **Content Validator**.
6. Create PR to merge the feature branch into `main`.
7. Merge to `main` after review and approval.

### Organization
- Group related model changes onto single feature branches.
- Use topic-based branch names.
- Developers use separate workbooks for initial development.
- Changes are promoted collectively to the feature branch.

## Key Omni Concepts
- **Workbook Layer:** Use workbooks as your primary development and testing environment before impacting the shared model. Test thoroughly here.
- **Shared Model Promotion:** Carefully promote validated logic from workbooks to your shared model branch. This makes logic reusable but also affects downstream content.
- **Content Validator:** Always run the Content Validator after promoting changes to a shared model branch and before merging. It helps catch broken dependencies or downstream issues.

## Branch Naming Conventions
Use clear, descriptive names incorporating type, ticket number (if applicable), and purpose.
```
# Examples
model/OM-123-customer-metrics
topic/OM-456-sales-analytics
hotfix/OM-789-join-fix
feature/new-user-onboarding-flow
```

## Automating Checks with CI/CD

Leverage CI/CD pipelines (e.g., GitHub Actions, GitLab CI) to automate checks on your branches before merging, enhancing reliability and consistency.

Integrate Omni APIs into your CI/CD workflows triggered on Pull Requests:

1.  **Content Validation:** Automatically run the Content Validator API against the branch in the Pull Request to catch potential downstream breakages early.
2.  **Model Migration (for Strategy 2):** If using the Multi-Instance Workflow, automate the process of syncing the development `main` branch to a staging branch in the production instance using the Model Migration API.
3.  **Automated Testing (Advanced):** Potentially trigger automated tests against the PR branch using Omni's query capabilities (if applicable to your setup) to validate key reports or data points.

This automated approach ensures that essential checks are performed consistently for every proposed change, reducing manual effort and the risk of errors.