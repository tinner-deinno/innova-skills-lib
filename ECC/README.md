# ECC Skill Registry

> Source: `~/.claude/skills/ecc/` — Everything Claude Code skill library
> Indexed: 2026-05-24 | Total skills: 181

This registry catalogs all ECC skills grouped into logical categories. Each skill resides in a subdirectory of `~/.claude/skills/ecc/<name>/SKILL.md` and is installable into Claude Code.

---

## Categories

1. [Agentic & Multi-Agent](#1-agentic--multi-agent)
2. [AI Engineering & Eval](#2-ai-engineering--eval)
3. [Testing](#3-testing)
4. [Security](#4-security)
5. [DevOps & Infrastructure](#5-devops--infrastructure)
6. [Backend Patterns (Language-Specific)](#6-backend-patterns-language-specific)
7. [Frontend & UI](#7-frontend--ui)
8. [Database & Data](#8-database--data)
9. [Cost & Token Management](#9-cost--token-management)
10. [Research & Knowledge Ops](#10-research--knowledge-ops)
11. [Content & Media](#11-content--media)
12. [Business Ops & Domain](#12-business-ops--domain)
13. [Science & Specialized](#13-science--specialized)
14. [ECC Meta & Tooling](#14-ecc-meta--tooling)

---

## 1. Agentic & Multi-Agent

Skills for building, operating, and debugging autonomous agent systems.

| Skill | Description |
|-------|-------------|
| `agentic-engineering` | Operate as an agentic engineer using eval-first execution, decomposition, and cost-aware model routing. |
| `agentic-os` | Build persistent multi-agent operating systems on Claude Code. Covers kernel architecture, specialist agents, file-based memory, and scheduled automation. |
| `agent-architecture-audit` | Full-stack diagnostic for agent and LLM applications. Audits the 12-layer agent stack for regression, memory pollution, and tool discipline failures. |
| `agent-harness-construction` | Design and optimize AI agent action spaces, tool definitions, and observation formatting for higher completion rates. |
| `agent-introspection-debugging` | Structured self-debugging workflow for AI agent failures using capture, diagnosis, contained recovery, and introspection reports. |
| `agent-sort` | Build an evidence-backed ECC install plan by sorting skills into DAILY vs LIBRARY buckets using parallel repo-aware review passes. |
| `autonomous-loops` | Patterns and architectures for autonomous Claude Code loops — from simple sequential pipelines to RFC-driven multi-agent DAG systems. |
| `continuous-agent-loop` | Patterns for continuous autonomous agent loops with quality gates, evals, and recovery controls. |
| `claude-devfleet` | Orchestrate multi-agent coding tasks via Claude DevFleet — plan projects, dispatch parallel agents in isolated worktrees, monitor progress. |
| `council` | Convene a four-voice council for ambiguous decisions, tradeoffs, and go/no-go calls. |
| `dmux-workflows` | Multi-agent orchestration using dmux (tmux pane manager for AI agents). Patterns for parallel agent workflows. |
| `enterprise-agent-ops` | Operate long-lived agent workloads with observability, security boundaries, and lifecycle management. |
| `iterative-retrieval` | Pattern for progressively refining context retrieval to solve the subagent context problem. |
| `nanoclaw-repl` | Operate and extend NanoClaw v2, ECC's zero-dependency session-aware REPL built on claude -p. |
| `ralphinho-rfc-pipeline` | RFC-driven multi-agent DAG execution pattern with quality gates, merge queues, and work unit orchestration. |
| `team-builder` | Interactive agent picker for composing and dispatching parallel teams. |

---

## 2. AI Engineering & Eval

Skills for AI-first development workflows, evaluation, and regression testing.

| Skill | Description |
|-------|-------------|
| `ai-first-engineering` | Engineering operating model for teams where AI agents generate a large share of implementation output. |
| `ai-regression-testing` | Regression testing strategies for AI-assisted development. Sandbox-mode API testing and patterns to catch AI blind spots. |
| `eval-harness` | Formal evaluation framework for Claude Code sessions implementing eval-driven development (EDD) principles. |
| `continuous-learning` | Legacy v1 stop-hook skill extractor. (Deprecated — use continuous-learning-v2.) |
| `continuous-learning-v2` | Instinct-based learning system that observes sessions via hooks, creates atomic instincts with confidence scoring. |
| `cost-aware-llm-pipeline` | Cost optimization patterns for LLM API usage — model routing by task complexity, budget tracking, retry logic. |
| `foundation-models-on-device` | Apple FoundationModels framework for on-device LLM — text generation, guided generation, tool calling in iOS 26+. |
| `mle-workflow` | Production machine-learning engineering workflow for data contracts, reproducible training, model evaluation, deployment. |
| `prompt-optimizer` | Optimize prompts for efficiency, clarity, and model performance. |
| `regex-vs-llm-structured-text` | Decision framework for choosing between regex and LLM when parsing structured text. |
| `search-first` | Research-before-coding workflow — search for existing tools, libraries, and patterns before writing custom code. |
| `strategic-compact` | Suggests manual context compaction at logical intervals to preserve context through task phases. |
| `token-budget-advisor` | Offers the user an informed choice about how much response depth to consume before answering. |
| `verification-loop` | A comprehensive verification system for Claude Code sessions. |

---

## 3. Testing

Skills for TDD, E2E testing, and language-specific test patterns.

| Skill | Description |
|-------|-------------|
| `tdd-workflow` | Enforces test-driven development with 80%+ coverage including unit, integration, and E2E tests. |
| `e2e-testing` | Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management. |
| `cpp-testing` | Writing/updating/fixing C++ tests with GoogleTest/CTest, coverage, and sanitizers. |
| `csharp-testing` | C# and .NET testing patterns with xUnit, FluentAssertions, mocking, and integration tests. |
| `django-tdd` | Django testing strategies with pytest-django, TDD methodology, factory_boy, mocking, and coverage. |
| `django-verification` | Verification loop for Django projects: migrations, linting, tests, security scans, and deployment readiness. |
| `fsharp-testing` | F# testing patterns with xUnit, FsUnit, Unquote, FsCheck property-based testing. |
| `golang-testing` | Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and coverage. |
| `kotlin-testing` | Kotlin testing with Kotest, MockK, coroutine testing, property-based testing, and Kover coverage. |
| `laravel-tdd` | Test-driven development for Laravel with PHPUnit and Pest, factories, database testing, fakes. |
| `laravel-verification` | Verification loop for Laravel: env checks, linting, static analysis, tests, security scans. |
| `perl-testing` | Perl testing patterns using Test2::V0, Test::More, prove runner, mocking, coverage. |
| `python-testing` | Python testing strategies using pytest, TDD methodology, fixtures, mocking, parametrization. |
| `quarkus-tdd` | TDD for Quarkus 3.x LTS using JUnit 5, Mockito, REST Assured, Camel testing, and JaCoCo. |
| `quarkus-verification` | Verification loop for Quarkus: build, static analysis, tests, security scans, native compilation. |
| `rust-testing` | Rust testing including unit tests, integration tests, async testing, property-based testing. |
| `springboot-tdd` | TDD for Spring Boot using JUnit 5, Mockito, MockMvc, Testcontainers, and JaCoCo. |
| `springboot-verification` | Verification loop for Spring Boot: build, static analysis, tests, security scans, and diff review. |
| `swift-protocol-di-testing` | Protocol-based dependency injection for testable Swift code — mock file system, network, and external APIs. |
| `windows-desktop-e2e` | E2E testing for Windows native desktop apps (WPF, WinForms, Win32/MFC, Qt) using pywinauto. |

---

## 4. Security

Skills for security review, scanning, compliance, and vulnerability analysis.

| Skill | Description |
|-------|-------------|
| `security-review` | Comprehensive security checklist and patterns for auth, user input, secrets, API endpoints, and payment features. |
| `security-scan` | Scan Claude Code configuration (.claude/ directory) for security vulnerabilities and injection risks using AgentShield. |
| `security-bounty-hunter` | Hunt for exploitable, bounty-worthy security issues focusing on remotely reachable vulnerabilities. |
| `defi-amm-security` | Security checklist for Solidity AMM contracts, liquidity pools, and swap flows. |
| `django-security` | Django security best practices, authentication, authorization, CSRF, SQL injection prevention. |
| `healthcare-phi-compliance` | PHI and PII compliance patterns for healthcare applications — access control, audit trails, encryption. |
| `hipaa-compliance` | HIPAA-specific entrypoint for healthcare privacy, PHI handling, covered entities, and BAAs. |
| `laravel-security` | Laravel security best practices for authn/authz, validation, CSRF, mass assignment, file uploads. |
| `llm-trading-agent-security` | Security patterns for autonomous trading agents with wallet or transaction authority. |
| `nodejs-keccak256` | Prevent Ethereum hashing bugs in JavaScript/TypeScript — Node's sha3-256 vs Keccak-256. |
| `perl-security` | Perl security covering taint mode, input validation, safe process execution, DBI parameterized queries. |
| `quarkus-security` | Quarkus Security best practices for authentication, authorization, JWT/OIDC, RBAC, CSRF. |
| `springboot-security` | Spring Security best practices for authn/authz, validation, CSRF, secrets, headers, rate limiting. |

---

## 5. DevOps & Infrastructure

Skills for deployment, CI/CD, containers, and infrastructure automation.

| Skill | Description |
|-------|-------------|
| `deployment-patterns` | Deployment workflows, CI/CD pipeline patterns, Docker containerization, health checks, rollback strategies. |
| `docker-patterns` | Docker and Docker Compose patterns for local development, container security, networking, volume strategies. |
| `github-ops` | GitHub repository operations: issue triage, PR management, CI/CD operations, release management, security monitoring. |
| `automation-audit-ops` | Evidence-first automation inventory and overlap audit workflow for ECC. |
| `database-migrations` | Database migration best practices for schema changes, data migrations, rollbacks, and zero-downtime deployments. |
| `homelab-network-readiness` | Readiness checklist for homelab VLAN segmentation, local DNS filtering, and WireGuard-style remote access. |
| `homelab-network-setup` | Practical home and homelab network planning for gateways, switches, IP ranges, DHCP, DNS. |
| `terminal-ops` | Evidence-first repo execution workflow — run commands, debug CI failures, push narrow fixes with exact proof. |
| `plankton-code-quality` | Write-time code quality enforcement using Plankton — auto-formatting, linting, and Claude-powered fixes on every edit. |

---

## 6. Backend Patterns (Language-Specific)

Language and framework patterns for backend development.

| Skill | Description |
|-------|-------------|
| `backend-patterns` | Backend architecture patterns, API design, database optimization for Node.js, Express, and Next.js API routes. |
| `api-design` | REST API design patterns including resource naming, status codes, pagination, filtering, error responses. |
| `api-connector-builder` | Build a new API connector by matching the target repo's existing integration pattern exactly. |
| `coding-standards` | Baseline cross-project coding conventions for naming, readability, immutability, and code-quality review. |
| `error-handling` | Patterns for robust error handling across TypeScript, Python, and Go. Covers typed errors, retries, circuit breakers. |
| `android-clean-architecture` | Clean Architecture patterns for Android and Kotlin Multiplatform projects. |
| `angular-developer` | Angular code generation and architectural guidance — signals, forms, DI, routing, SSR, accessibility. |
| `compose-multiplatform-patterns` | Compose Multiplatform and Jetpack Compose patterns for KMP — state management, navigation, theming. |
| `cpp-coding-standards` | C++ coding standards based on the C++ Core Guidelines for modern, safe, idiomatic practices. |
| `dart-flutter-patterns` | Production-ready Dart and Flutter patterns covering null safety, state management (BLoC, Riverpod), GoRouter. |
| `django-patterns` | Django architecture patterns, REST API design with DRF, ORM best practices, caching, signals, middleware. |
| `dotnet-patterns` | Idiomatic C# and .NET patterns, conventions, dependency injection, async/await best practices. |
| `fastapi-patterns` | FastAPI patterns for async APIs, dependency injection, Pydantic models, OpenAPI docs, tests, security. |
| `golang-patterns` | Idiomatic Go patterns, best practices, and conventions for building robust Go applications. |
| `java-coding-standards` | Java coding standards for Spring Boot and Quarkus services — naming, Optional, streams, generics, CDI. |
| `jpa-patterns` | JPA/Hibernate patterns for entity design, relationships, query optimization, transactions, pagination. |
| `kotlin-coroutines-flows` | Kotlin Coroutines and Flow patterns for Android and KMP — structured concurrency, Flow operators, StateFlow. |
| `kotlin-exposed-patterns` | JetBrains Exposed ORM patterns including DSL queries, DAO pattern, transactions, HikariCP pooling. |
| `kotlin-ktor-patterns` | Ktor server patterns including routing DSL, plugins, authentication, Koin DI, WebSockets. |
| `kotlin-patterns` | Idiomatic Kotlin patterns for coroutines, null safety, and DSL builders. |
| `laravel-patterns` | Laravel architecture patterns, routing/controllers, Eloquent ORM, service layers, queues, events. |
| `laravel-plugin-discovery` | Discover and evaluate Laravel packages via LaraPlugins.io MCP. |
| `mcp-server-patterns` | Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation. |
| `nestjs-patterns` | NestJS architecture patterns for modules, controllers, providers, DTO validation, guards, interceptors. |
| `perl-patterns` | Modern Perl 5.36+ idioms, best practices, and conventions. |
| `python-patterns` | Pythonic idioms, PEP 8, type hints, and best practices for Python applications. |
| `quarkus-patterns` | Quarkus 3.x LTS architecture patterns with Camel for messaging, RESTful API design, Panache. |
| `rust-patterns` | Idiomatic Rust patterns — ownership, error handling, traits, concurrency, and performance. |
| `springboot-patterns` | Spring Boot architecture patterns, REST API design, layered services, data access, caching. |
| `swift-actor-persistence` | Thread-safe data persistence in Swift using actors — in-memory cache with file-backed storage. |
| `swift-concurrency-6-2` | Swift 6.2 Approachable Concurrency — single-threaded by default, @concurrent for background offloading. |
| `swiftui-patterns` | SwiftUI architecture patterns, state management with @Observable, navigation, performance optimization. |

---

## 7. Frontend & UI

Skills for frontend development, design, motion, and UI quality.

| Skill | Description |
|-------|-------------|
| `frontend-patterns` | Frontend development patterns for React, Next.js, state management, performance optimization. |
| `frontend-design-direction` | Set an ECC-specific frontend design direction for production UI work — websites, dashboards, applications. |
| `frontend-slides` | Create animation-rich HTML presentations from scratch or by converting PowerPoint files. |
| `liquid-glass-design` | iOS 26 Liquid Glass design system — dynamic glass material with blur, reflection, and interactive morphing. |
| `make-interfaces-feel-better` | Apply design-engineering details for polish: spacing, typography, borders, shadows, motion, hit areas. |
| `motion-ui` | Production-ready UI motion system for React/Next.js — animations, transitions, motion patterns. |
| `seo` | Audit, plan, and implement SEO improvements: technical SEO, on-page optimization, structured data, Core Web Vitals. |
| `ui-demo` | Record polished UI demo videos using Playwright — demos, walkthroughs, screen recordings. |
| `ui-to-vue` | Batch conversion of UI screenshots or design exports into Vue 3 components. |

---

## 8. Database & Data

Skills for database patterns, query optimization, and data pipelines.

| Skill | Description |
|-------|-------------|
| `postgres-patterns` | PostgreSQL patterns for query optimization, schema design, indexing, and security. |
| `mysql-patterns` | MySQL and MariaDB schema, query, indexing, transaction, replication, and connection-pool patterns. |
| `clickhouse-io` | ClickHouse database patterns, query optimization, analytics, and data engineering best practices. |
| `prisma-patterns` | Prisma ORM patterns for TypeScript — schema design, query optimization, transactions, pagination. |
| `content-hash-cache-pattern` | Cache expensive file processing results using SHA-256 content hashes — path-independent, auto-invalidating. |
| `data-scraper-agent` | Build a fully automated AI-powered data collection agent for any public source — job boards, prices, news. |

---

## 9. Cost & Token Management

Skills for tracking and optimizing Claude and LLM usage costs.

| Skill | Description |
|-------|-------------|
| `cost-tracking` | Track and report Claude Code token usage, spending, and budgets from a local cost-tracking database. |
| `cost-aware-llm-pipeline` | Cost optimization patterns for LLM API usage — model routing, budget tracking, retry logic, prompt caching. |
| `token-budget-advisor` | Offers informed choice about response depth to control token consumption. |
| `ecc-tools-cost-audit` | Evidence-first ECC Tools burn and billing audit workflow — runaway PR creation, quota bypass, premium-model leakage. |

---

## 10. Research & Knowledge Ops

Skills for research workflows, knowledge management, and discovery.

| Skill | Description |
|-------|-------------|
| `deep-research` | Multi-source deep research using firecrawl and exa MCPs — searches the web, synthesizes findings, delivers cited reports. |
| `exa-search` | Neural search via Exa MCP for web, code, and company research. |
| `knowledge-ops` | Knowledge base management, ingestion, sync, and retrieval across multiple storage layers. |
| `market-research` | Conduct market research, competitive analysis, investor due diligence, and industry intelligence. |
| `research-ops` | Evidence-first current-state research workflow — fresh facts, comparisons, enrichment, recommendations. |
| `scientific-thinking-literature-review` | Systematic literature-review workflow for academic, biomedical, technical, and scientific topics. |
| `scientific-thinking-scholar-evaluation` | Structured scholarly-work evaluation for papers, proposals, methods sections, and evidence quality. |
| `blueprint` | Blueprint planning and structured design for complex tasks. |

---

## 11. Content & Media

Skills for content creation, social media, video, and media generation.

| Skill | Description |
|-------|-------------|
| `article-writing` | Write articles, guides, blog posts, tutorials, and long-form content in a distinctive voice. |
| `brand-voice` | Build a source-derived writing style profile from real posts, then reuse it across content workflows. |
| `content-engine` | Create platform-native content systems for X, LinkedIn, TikTok, YouTube, newsletters. |
| `crosspost` | Multi-platform content distribution across X, LinkedIn, Threads, and Bluesky. |
| `fal-ai-media` | Unified media generation via fal.ai MCP — image, video, and audio (text-to-image, video, TTS). |
| `frontend-slides` | Create stunning animation-rich HTML presentations from scratch or by converting PowerPoint files. |
| `manim-video` | Build reusable Manim explainers for technical concepts, graphs, system diagrams, and product walkthroughs. |
| `remotion-video-creation` | Best practices for Remotion — video creation in React with 3D, animations, audio, captions, charts. |
| `video-editing` | AI-assisted video editing workflows: cutting, structuring, augmenting footage via FFmpeg, Remotion, ElevenLabs. |
| `videodb` | See, understand, and act on video and audio — ingest, index, search, edit, generate media assets. |
| `x-api` | X/Twitter API integration for posting tweets, threads, reading timelines, search, and analytics. |

---

## 12. Business Ops & Domain

Skills for business workflows, operations, and specialized domain expertise.

| Skill | Description |
|-------|-------------|
| `carrier-relationship-management` | Codified expertise for managing carrier portfolios and negotiating freight rates. |
| `customer-billing-ops` | Operate customer billing workflows — subscriptions, refunds, churn triage, billing-portal recovery. |
| `customs-trade-compliance` | Codified expertise for customs documentation, tariff classification, and duty management. |
| `email-ops` | Evidence-first mailbox triage, drafting, send verification, and follow-up workflow. |
| `energy-procurement` | Codified expertise for electricity and gas procurement and tariff optimization. |
| `finance-billing-ops` | Evidence-first revenue, pricing, refunds, team-billing, and billing-model truth workflow. |
| `google-workspace-ops` | Operate across Google Drive, Docs, Sheets, and Slides as one workflow surface. |
| `inventory-demand-planning` | Codified expertise for demand forecasting and safety stock optimization. |
| `investor-materials` | Create and update pitch decks, one-pagers, investor memos, accelerator applications, financial models. |
| `investor-outreach` | Draft cold emails, warm intro blurbs, follow-ups, and investor communications for fundraising. |
| `jira-integration` | Retrieve Jira tickets, analyze requirements, update status, add comments, or transition issues. |
| `lead-intelligence` | AI-native lead intelligence and outreach pipeline — replaces Apollo, Clay, ZoomInfo. |
| `logistics-exception-management` | Codified expertise for handling freight exceptions and shipment delays. |
| `messages-ops` | Evidence-first live messaging workflow — read texts/DMs, recover one-time codes, inspect threads. |
| `nutrient-document-processing` | Process, convert, OCR, extract, redact, sign, and fill documents using the Nutrient DWS API. |
| `production-audit` | Local-evidence production readiness audit for shipped apps, pre-launch reviews, post-merge checks. |
| `production-scheduling` | Codified expertise for production scheduling, job sequencing, and line balancing. |
| `product-capability` | Translate PRD intent into an implementation-ready capability plan with constraints and invariants. |
| `project-flow-ops` | Operate execution flow across GitHub and Linear — issue triage, PR triage, GitHub-to-Linear coordination. |
| `quality-nonconformance` | Codified expertise for quality control and non-conformance investigation. |
| `returns-reverse-logistics` | Codified expertise for returns authorization, receipt and inspection. |
| `social-graph-ranker` | Weighted social-graph ranking for warm intro discovery and network gap analysis across X and LinkedIn. |
| `connections-optimizer` | Reorganize X and LinkedIn networks with pruning, recommendations, and warm outreach. |
| `strategic-compact` | Suggests manual context compaction at logical intervals to preserve context through task phases. |
| `unified-notifications-ops` | Operate notifications across GitHub, Linear, desktop alerts, hooks, and communication surfaces. |
| `workspace-surface-audit` | Audit the active repo, MCP servers, plugins, connectors, and harness setup for ECC skill recommendations. |

---

## 13. Science & Specialized

Skills for scientific databases, network engineering, and specialized domains.

| Skill | Description |
|-------|-------------|
| `blender-motion-state-inspection` | Inspect Blender characters, rigs, poses, animation retargeting, and model-vs-motion alignment. |
| `cisco-ios-patterns` | Cisco IOS and IOS-XE review patterns for show commands, config hierarchy, ACL placement. |
| `evm-token-decimals` | Prevent silent decimal mismatch bugs across EVM chains — runtime decimal lookup, chain-aware caching. |
| `netmiko-ssh-automation` | Safe Python Netmiko patterns for read-only collection, bounded batch SSH, TextFSM parsing. |
| `network-bgp-diagnostics` | Diagnostics-only BGP troubleshooting for neighbor state, route exchange, prefix policy. |
| `network-config-validation` | Pre-deployment checks for router and switch configuration — dangerous commands, subnet overlaps. |
| `network-interface-health` | Diagnose interface errors, drops, CRCs, duplex mismatches, and counter trends. |
| `scientific-db-pubmed-database` | Direct PubMed and NCBI E-utilities search workflows for biomedical literature. |
| `scientific-db-uspto-database` | USPTO patent and trademark data workflow for official record lookup and IP research. |
| `scientific-pkg-gget` | gget CLI and Python workflow for genomic database queries, sequence lookup, and BLAST-style searches. |
| `visa-doc-translate` | Translate visa application documents (images) to English and create a bilingual PDF. |

---

## 14. ECC Meta & Tooling

Skills for managing, configuring, and auditing ECC itself.

| Skill | Description |
|-------|-------------|
| `configure-ecc` | Interactive installer for Everything Claude Code — guides users through selecting and installing skills and rules. |
| `hookify-rules` | Create hookify rules, write hook rules, configure hookify, and add hookify rules. |
| `skill-scout` | Search existing local, marketplace, GitHub, and web skill sources before creating a new skill. |
| `skill-stocktake` | Audit Claude skills and commands for quality — Quick Scan or Full Stocktake modes. |
| `code-tour` | Create CodeTour `.tour` files — persona-targeted step-by-step walkthroughs with file and line anchors. |
| `dashboard-builder` | Build monitoring dashboards that answer real operator questions for Grafana, SigNoz, and similar platforms. |

---

## Quick Reference

- **Total skills indexed**: 181
- **Top skills for multi-agent work**: `agentic-os`, `agentic-engineering`, `continuous-agent-loop`, `eval-harness`, `dmux-workflows`
- **Top skills for AI quality**: `tdd-workflow`, `ai-regression-testing`, `verification-loop`, `eval-harness`
- **Top skills for cost control**: `cost-tracking`, `cost-aware-llm-pipeline`, `token-budget-advisor`
- **Source directory**: `~/.claude/skills/ecc/`
- **Full catalog**: See [CATALOG.md](./CATALOG.md)
