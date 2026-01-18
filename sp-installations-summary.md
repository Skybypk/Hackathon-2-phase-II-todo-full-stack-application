# SP (Spec-Plus) Tools Installation Summary

## Available SP Commands in Claude Code

The following SP (Spec-Plus) tools are already installed and available for use:

1. **sp.adr** - Create Architectural Decision Records
   - Description: Review planning artifacts for architecturally significant decisions and create ADRs

2. **sp.analyze** - Perform consistency analysis
   - Description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation

3. **sp.checklist** - Generate custom checklists
   - Description: Generate a custom checklist for the current feature based on user requirements

4. **sp.clarify** - Identify underspecified areas
   - Description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec

5. **sp.constitution** - Create/update project constitution
   - Description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync

6. **sp.git.commit_pr** - Git workflow automation
   - Description: An autonomous Git agent that intelligently executes git workflows to commit the work and create PR

7. **sp.implement** - Execute implementation plan
   - Description: Execute the implementation plan by processing and executing all tasks defined in tasks.md

8. **sp.phr** - Create Prompt History Records
   - Description: Record an AI exchange as a Prompt History Record (PHR) for learning and traceability

9. **sp.plan** - Create implementation plans
   - Description: Execute the implementation planning workflow using the plan template to generate design artifacts

10. **sp.reverse-engineer** - Reverse engineer codebase
    - Description: Reverse engineer a codebase into SDD-RI artifacts (spec, plan, tasks, intelligence)

11. **sp.specify** - Create/update feature specifications
    - Description: Create or update the feature specification from a natural language feature description

12. **sp.tasks** - Generate actionable tasks
    - Description: Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts

13. **sp.taskstoissues** - Convert tasks to GitHub issues
    - Description: Convert existing tasks into actionable, dependency-ordered GitHub issues for the feature based on available design artifacts

## Usage Instructions

To use any of these commands, simply type `/sp.<command>` followed by any required arguments in Claude Code.

Example usage:
- `/sp.plan feature-name` - Create a plan for a specific feature
- `/sp.specify feature-name` - Create a specification for a feature
- `/sp.tasks` - Generate tasks from existing specifications
- `/sp.implement` - Execute the implementation plan
- `/sp.adr "Decision Title"` - Create an architectural decision record

## Directory Structure

The SP tools are organized as follows:
- Templates: `.specify/templates/`
- Scripts: `.specify/scripts/`
- Memory (Constitution): `.specify/memory/`
- Feature specs: `specs/features/`
- API specs: `specs/api/`
- Database specs: `specs/database/`
- Commands: `.claude/commands/`

## Integration Status

✅ All SP tools are properly installed and integrated with Claude Code
✅ Ready to use for full spec-driven development workflow
✅ Compatible with the established project structure