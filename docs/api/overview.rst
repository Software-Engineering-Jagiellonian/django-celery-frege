Overview
========

Frege is a system for analyzing source code repositories at scale.

The project was created as a response to growing complexity and fragmentation in the previous architecture. Originally based on multiple microservices, the earlier system suffered from duplicated logic, unnecessary inter-service dependencies, and inconsistent use of programming languages and communication protocols.

Frege aims to simplify the overall architecture while retaining full functionality and scalability. Instead of maintaining separate microservices for indexing, downloading, extracting, and analyzing code, Frege consolidates all essential functionality into a unified, task-driven system based on Celery and Django.

The system's main purpose is to:

- Automatically discover and analyze code repositories,
- Process and extract file-level data from supported source files,
- Store structured analysis results in a central database,
- Expose this data through a clean, secure API for frontend and third-party use,
- Provide developers and researchers with an extensible platform for working with large sets of source code.

Frege is designed to be easy to deploy, maintain, and extend. It uses proven tools like Celery for task orchestration, Django for API and admin interface, PostgreSQL for data storage, and Prometheus/Grafana for monitoring.

By focusing on modularity and developer experience, Frege allows contributors to build and improve features without having to worry about low-level infrastructure or duplicated effort.

Core Objectives
---------------

- Eliminate redundant microservices and reduce codebase size.
- Centralize database schema definition and migrations using Django ORM.
- Unify the technology stack (Python, Celery, Django).
- Improve system scalability and observability.
- Simplify service orchestration and fault recovery.

System Architecture
-------------------

Frege is centered around **Celery** workers that handle all background processing tasks, including repository indexing and source code analysis. Tasks are distributed via **Redis** and results are persisted in a **PostgreSQL** database.

A simplified component breakdown:
- **Indexers**: Discover and enqueue repositories for analysis.
- **Processors**: Fetch and extract repository content.
- **Analyzers**: Perform file-level analysis on known filetypes.
- **Django**: Serves as the main API layer, admin panel, and data interface for external consumers.
- **Prometheus & Grafana**: Provide monitoring and observability.

By consolidating services and relying on well-established frameworks, Frege allows contributors to focus on implementing domain-specific logic without needing to manage low-level infrastructure concerns.
