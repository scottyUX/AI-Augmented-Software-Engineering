<!--
Sync Impact Report
Version change: no prior constitution -> 1.0.0 (initial ratification)
Modified principles: none
Added sections: Core Principles, Quality Standards, Development Workflow, Governance
Removed sections: none
Follow-up TODOs: none
This report is temporary review material and should be removed before commit.
-->

# Spec Kit Week 2 Constitution

## Core Principles

### I. Clear, Correct Implementation
Code MUST express the intended behavior directly and use names, structure, and
comments that make non-obvious decisions understandable. Changes MUST follow the
project's existing conventions and avoid unrelated edits. This keeps behavior
reviewable and makes defects easier to locate.

### II. Behavior-Focused Testing
Each user-visible behavior and important edge case MUST have a repeatable check.
Changes MUST add or update tests for affected behavior, and all relevant checks
MUST pass before the work is considered complete. Tests MUST assert outcomes
rather than mirror implementation details, so they remain useful through refactors.

### III. Simple, Maintainable Design
Implementations MUST use the smallest design that satisfies the approved
requirements. New dependencies, abstractions, and duplicated logic MUST be
avoided unless they provide a clear, explainable benefit. A refactor MUST preserve
observable behavior and be covered by the same relevant checks.

### IV. Accessible and Resilient Interaction
Interactive controls MUST use appropriate native semantics and remain usable with
keyboard input. User-facing state MUST be represented clearly, and persistence or
browser APIs MUST handle unavailable or invalid stored data without breaking the
primary experience.

### V. Traceable Scope and Decisions
Implementation MUST match the reviewed specification and plan. Ambiguity or a
conflict with an approved requirement MUST be raised for clarification rather than
silently resolved through extra features. Material changes to scope MUST first be
reflected in the relevant spec artifact.

## Quality Standards

The project MUST remain within its approved technology and feature scope. Runtime
dependencies MUST be justified by a concrete requirement. Changes MUST preserve
existing user data where applicable and MUST NOT claim completion when required
validation has not run or has failed.

## Development Workflow

Work MUST proceed through reviewed specification artifacts before implementation.
For each change, identify the relevant acceptance criteria, implement the smallest
conforming change, run focused checks, and review the result against the spec.
When validation exposes a mismatch, update the spec or implementation as
appropriate and repeat the relevant checks until the behavior conforms.

## Governance

This constitution governs project decisions and takes precedence over conflicting
local conventions. Changes to principles or quality gates MUST be made explicitly
in this file and reviewed before implementation proceeds. Version changes follow
semantic versioning: MAJOR for incompatible governance changes, MINOR for new or
materially expanded requirements, and PATCH for clarifications that do not change
obligations. Contributors and reviewers MUST check proposed changes against these
principles and record any justified exception in the relevant spec artifact.

**Version**: 1.0.0 | **Ratified**: 2026-10-14 | **Last Amended**: 2026-10-14
