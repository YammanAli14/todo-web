<!--
SYNC IMPACT REPORT
==================
Amendment Date: 2026-01-02
Version Change: 1.0.0 → 1.1.0 (MINOR - Phase II technology additions)

Modified Sections:
- Article III, Section 3.1: Phase Definitions updated
  * Phase I: Changed to "in-memory only (no persistence)" (was "local SQLite")
  * Phase II: Changed to "Full-Stack Web App | Python REST API, Neon PostgreSQL, Next.js frontend, Better Auth" (was "API Layer | FastAPI backend, Neon PostgreSQL, REST API")
  * Phase IV: Changed to "Advanced Features" (was "Frontend | Next.js web application, user authentication")
  * Phase V: Added "AI orchestration" to scope

- Article IV, Section 4.1: Mandatory Technologies updated
  * Backend Framework: Changed from "FastAPI" to "Python REST API (framework TBD)" for Phase II–V
  * ORM: Changed from "SQLModel | All" to "SQLModel or equivalent | II–V"
  * Database: Split into two rows - Phase I (None/in-memory) and Phase II–V (Neon Serverless PostgreSQL)
  * Frontend: Changed from "Next.js | IV–V" to "Next.js (React, TypeScript) | II–V"
  * Authentication: Added new row "Better Auth (signup/signin) | II–V"

- Article IV, Section 4.2: Technology Prohibitions updated
  * Removed prohibitions on alternative ORMs and web frameworks (now flexible)
  * Added: "AI frameworks, agent frameworks, or orchestration tools before Phase III"
  * Added: "Authentication systems other than Better Auth (Phase II+)"
  * Added: "Databases or persistence layers in Phase I (in-memory only)"

- Article IV, Section 4.4: Version Requirements updated
  * Removed FastAPI minimum version requirement
  * Changed SQLModel to "SQLModel or equivalent ORM"
  * Added TypeScript 5.0+ requirement
  * Added Better Auth latest stable version requirement

Added Sections:
- None

Removed Sections:
- None

Templates Requiring Updates:
⚠ PENDING: .specify/templates/plan-template.md - Review constitution alignment
⚠ PENDING: .specify/templates/spec-template.md - Review phase technology constraints
⚠ PENDING: .specify/templates/tasks-template.md - Review task categorization for Phase II

Follow-up TODOs:
- Review all Phase II specifications for compliance with new technology matrix
- Update any existing Phase I specs to clarify "in-memory only" constraint
- Ensure Better Auth is specified for all Phase II+ features requiring authentication

Rationale for MINOR version bump:
This amendment adds new technology capabilities for Phase II (Next.js frontend, Better Auth,
Neon PostgreSQL) and clarifies phase boundaries. It does not remove or fundamentally redefine
existing principles, nor does it break backward compatibility with Phase I specifications.
The changes are additive and clarifying, warranting a MINOR version increment.
-->

# Evolution of Todo — Global Constitution

**Version:** 1.1.0
**Effective:** All Phases (I–V)
**Authority:** This constitution governs all development activities across the entire Evolution of Todo project.

---

## Preamble

This constitution establishes the foundational laws, constraints, and principles that govern the Evolution of Todo project from inception through completion. No agent, human, or automated process may violate these rules. All work must align with this constitution or be rejected.

---

## Article I: Spec-Driven Development

### Section 1.1 — Mandatory Specification Approval

No code shall be written without an approved specification. This is absolute and non-negotiable.

### Section 1.2 — The Development Hierarchy

All work must flow through the following hierarchy, in strict order:

```
Constitution
    ↓
Specification
    ↓
Plan
    ↓
Tasks
    ↓
Implementation
```

Each level must be completed and approved before proceeding to the next.

### Section 1.3 — Specification Requirements

Every specification must define:

1. **Scope** — What is included and explicitly excluded
2. **Requirements** — Functional and non-functional requirements
3. **Interfaces** — APIs, data models, contracts
4. **Acceptance Criteria** — Measurable conditions for completion
5. **Dependencies** — What must exist before work begins

### Section 1.4 — Plan Requirements

Every plan must:

1. Reference an approved specification
2. Break work into discrete, verifiable tasks
3. Define the order of execution
4. Identify files to be created or modified
5. Specify testing approach

### Section 1.5 — Task Requirements

Every task must:

1. Reference its parent plan
2. Be atomic and independently verifiable
3. Have clear completion criteria
4. Produce testable output

---

## Article II: Agent Behavior Rules

### Section 2.1 — Prohibition of Manual Human Coding

Humans shall not write production code directly. The human role is limited to:

- Defining specifications
- Reviewing and approving specifications
- Reviewing and approving plans
- Reviewing agent-generated code
- Accepting or rejecting deliverables

### Section 2.2 — Prohibition of Feature Invention

Agents shall not invent, suggest, or implement features not explicitly defined in approved specifications. If an agent identifies a potential improvement:

1. It must halt implementation
2. Document the suggestion
3. Request specification amendment
4. Await approval before proceeding

### Section 2.3 — Prohibition of Specification Deviation

Agents shall implement exactly what specifications define. Deviations include:

- Adding functionality not specified
- Omitting specified functionality
- Changing interfaces without approval
- Altering data models without approval
- Modifying behavior beyond specification scope

All deviations are violations of this constitution.

### Section 2.4 — Refinement at Specification Level

When implementation reveals issues:

1. **Do not** fix issues by modifying code beyond specification
2. **Do** document the issue
3. **Do** propose specification amendments
4. **Do** await approval before implementing changes

Code-level refinement without specification amendment is prohibited.

### Section 2.5 — Agent Declaration

Before beginning any task, agents must declare:

1. Which specification they are implementing
2. Which plan they are following
3. Which specific task they are executing

Work without declaration is prohibited.

---

## Article III: Phase Governance

### Section 3.1 — Phase Definitions

| Phase | Name | Scope |
|-------|------|-------|
| I | Foundation | CLI todo app, single-user, in-memory only (no persistence) |
| II | Full-Stack Web App | Python REST API, Neon PostgreSQL, Next.js frontend, Better Auth |
| III | Agent Integration | OpenAI Agents SDK, MCP, agent-driven operations |
| IV | Advanced Features | Additional capabilities built on Phase II foundation |
| V | Scale | Docker, Kubernetes, Kafka, Dapr, multi-tenant, AI orchestration |

### Section 3.2 — Phase Isolation

Each phase is strictly bounded by its specification. The following rules apply:

1. **No Forward Leakage** — Features defined for Phase N+1 shall not appear in Phase N
2. **No Premature Optimization** — Infrastructure for future phases shall not be built early
3. **No Speculative Architecture** — Design only for current phase requirements

### Section 3.3 — Phase Completion Criteria

A phase is complete only when:

1. All specifications for that phase are implemented
2. All acceptance criteria are met
3. All tests pass
4. Documentation is complete
5. Human review approves the deliverable

### Section 3.4 — Architecture Evolution

Architecture may evolve only through:

1. Updated specifications approved for a new phase
2. Explicit refactoring tasks in approved plans
3. Migration paths defined in specifications

Ad-hoc architectural changes are prohibited.

### Section 3.5 — Inter-Phase Dependencies

Later phases may depend on earlier phases. Earlier phases shall not depend on later phases. Circular dependencies between phases are prohibited.

---

## Article IV: Technology Constraints

### Section 4.1 — Mandatory Technologies

The following technologies are mandatory for their respective domains:

| Domain | Technology | Phases |
|--------|------------|--------|
| Backend Language | Python 3.11+ | All |
| Backend Framework | Python REST API (framework TBD) | II–V |
| ORM/Data Layer | SQLModel or equivalent | II–V |
| Database | None (in-memory only) | I |
| Database | Neon Serverless PostgreSQL | II–V |
| Frontend Framework | Next.js (React, TypeScript) | II–V |
| Authentication | Better Auth (signup/signin) | II–V |
| Agent SDK | OpenAI Agents SDK | III–V |
| Tool Protocol | MCP (Model Context Protocol) | III–V |
| Containerization | Docker | V |
| Orchestration | Kubernetes | V |
| Messaging | Kafka | V |
| Distributed Runtime | Dapr | V |

### Section 4.2 — Technology Prohibitions

The following are prohibited without explicit specification approval:

- Alternative frontend frameworks (Vue, Angular, React without Next.js, etc.)
- NoSQL databases as primary storage
- GraphQL (unless specified)
- AI frameworks, agent frameworks, or orchestration tools before Phase III
- Authentication systems other than Better Auth (Phase II+)
- Databases or persistence layers in Phase I (in-memory only)

### Section 4.3 — Dependency Management

All dependencies must be:

1. Explicitly listed in requirements files
2. Version-pinned for reproducibility
3. Justified by specification requirements
4. Reviewed for security vulnerabilities

### Section 4.4 — Version Requirements

Minimum versions required:

- Python: 3.11
- SQLModel: 0.0.14+ (or equivalent ORM)
- Next.js: 14+
- Node.js: 20+ (for frontend)
- TypeScript: 5.0+ (for frontend)
- Better Auth: Latest stable version

---

## Article V: Quality Principles

### Section 5.1 — Clean Architecture

All code must adhere to clean architecture principles:

1. **Separation of Concerns** — Each module has one responsibility
2. **Dependency Inversion** — High-level modules do not depend on low-level modules
3. **Interface Segregation** — No module is forced to depend on interfaces it doesn't use
4. **Single Responsibility** — Each class/function does one thing

### Section 5.2 — Project Structure

```
project/
├── src/
│   ├── domain/          # Business entities, no external dependencies
│   ├── application/     # Use cases, orchestration
│   ├── infrastructure/  # Database, external services
│   └── presentation/    # API routes, CLI commands
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── specs/               # Approved specifications
├── plans/               # Approved plans
└── docs/                # Documentation
```

### Section 5.3 — Stateless Services

Where specifications require stateless services:

1. No in-memory state between requests
2. All state persisted to database
3. Session data externalized
4. Services horizontally scalable

### Section 5.4 — Code Quality Standards

All code must meet:

1. **Type Hints** — All function signatures typed
2. **Documentation** — Public APIs documented
3. **Testing** — Minimum 80% coverage for business logic
4. **Linting** — Pass ruff or equivalent
5. **Formatting** — Consistent with black or equivalent

### Section 5.5 — Error Handling

1. Exceptions must be specific, not generic
2. Error messages must be actionable
3. Failures must not leak sensitive information
4. All errors must be logged appropriately

### Section 5.6 — Security Requirements

1. No secrets in code
2. Input validation on all boundaries
3. SQL injection prevention (parameterized queries via ORM)
4. Authentication/authorization where specified
5. HTTPS in production

---

## Article VI: Documentation Requirements

### Section 6.1 — Required Documentation

Each phase must produce:

1. **Specification** — What will be built
2. **Plan** — How it will be built
3. **API Documentation** — OpenAPI/Swagger for all endpoints
4. **README** — Setup and usage instructions
5. **Changelog** — What changed and why

### Section 6.2 — Documentation Standards

1. Written in Markdown
2. Stored in version control
3. Updated with each change
4. Reviewed with code

---

## Article VII: Amendment Process

### Section 7.1 — Constitution Amendments

This constitution may only be amended through:

1. Written proposal documenting the change
2. Justification for the change
3. Impact analysis
4. Human approval

### Section 7.2 — Specification Amendments

Specifications may be amended through:

1. Change request documenting the modification
2. Updated specification document
3. Updated plan if required
4. Human approval

### Section 7.3 — Emergency Amendments

In case of blocking issues:

1. Document the emergency
2. Propose minimal change
3. Obtain approval
4. Implement change
5. Conduct post-incident review

---

## Article VIII: Enforcement

### Section 8.1 — Violation Detection

Violations are detected through:

1. Code review
2. Automated checks
3. Testing
4. Human inspection

### Section 8.2 — Violation Response

When a violation is detected:

1. Work must stop immediately
2. Violation must be documented
3. Violating code must be reverted or corrected
4. Root cause must be identified
5. Prevention measures must be implemented

### Section 8.3 — Agent Accountability

Agents must:

1. Self-report potential violations
2. Request clarification when uncertain
3. Never proceed when in doubt

---

## Article IX: Definitions

| Term | Definition |
|------|------------|
| Agent | Any AI system performing development tasks |
| Human | The project owner or authorized reviewer |
| Specification | Approved document defining what to build |
| Plan | Approved document defining how to build |
| Task | Atomic unit of work derived from a plan |
| Phase | Major project milestone with defined scope |
| Constitution | This document; supreme authority |

---

## Article X: Supremacy

### Section 10.1 — Constitutional Supremacy

This constitution is the supreme governing document. In case of conflict:

1. Constitution overrides specifications
2. Specifications override plans
3. Plans override task interpretations
4. Earlier approved documents override later assumptions

### Section 10.2 — Precedence

When facing ambiguity:

1. Consult this constitution first
2. Then consult the relevant specification
3. Then consult the relevant plan
4. If still ambiguous, halt and request clarification

---

## Signatures

This constitution is effective upon creation and governs all work on the Evolution of Todo project.

**Established:** 2025-12-28
**Last Amended:** 2026-01-02
**Authority:** Project Owner
**Version:** 1.1.0

---

*End of Constitution*
