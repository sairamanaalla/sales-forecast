# ADR-001: Architecture Decisions

## Status

Accepted

---

## Context

The objective of this project is to build an end-to-end sales forecasting platform that demonstrates modern data engineering, machine learning, API development, dashboarding, AI integration, containerization, testing, and CI practices.

The solution is required to:

* Ingest and process sales data using a layered architecture.
* Generate revenue forecasts for future periods.
* Expose forecast and analytics data through APIs.
* Provide a user-friendly dashboard for business users.
* Generate AI-powered business insights from forecast results.
* Support containerized deployment and automated quality checks.

The architecture should remain modular, maintainable, and extensible to support future enhancements.

---

## Decision 1: Medallion Architecture (Bronze and Silver Layers)

### Decision

Use a Medallion-style architecture consisting of Bronze and Silver layers for data processing.

### Rationale

* Bronze layer stores raw ingested data.
* Silver layer stores validated and cleaned data.
* Provides clear separation between ingestion and transformation.
* Improves traceability and data quality.

### Consequences

* Easier debugging and auditing.
* Better maintainability.
* Supports future expansion to a Gold layer for business aggregations.

---

## Decision 2: Random Forest for Forecasting

### Decision

Use RandomForestRegressor as the forecasting model.

### Rationale

* Performs well on structured business datasets.
* Handles non-linear relationships effectively.
* Requires minimal feature engineering and preprocessing.
* Easy to train and evaluate.
* Suitable for demonstrating an end-to-end machine learning workflow.

### Consequences

* Faster implementation compared to advanced forecasting approaches.
* Model remains interpretable through feature importance analysis.
* Can be replaced with more sophisticated forecasting models in the future.

---

## Decision 3: FastAPI for API Layer

### Decision

Use FastAPI to expose forecast, summary, and AI insight endpoints.

### Rationale

* High-performance Python web framework.
* Automatic OpenAPI and Swagger documentation.
* Strong integration with machine learning workflows.
* Simple and lightweight architecture.

### Consequences

* Rapid API development.
* Interactive API documentation available through Swagger UI.
* Easy integration with frontend applications and external consumers.

---

## Decision 4: Streamlit for Dashboard

### Decision

Use Streamlit to build the analytics dashboard.

### Rationale

* Enables rapid dashboard development.
* Native integration with pandas and Python analytics workflows.
* Requires minimal frontend development effort.
* Provides interactive filtering and visualization capabilities.

### Consequences

* Faster delivery compared to building a custom frontend.
* Simplified maintenance and deployment.
* Suitable for analytical and proof-of-concept applications.

---

## Decision 5: LLM Integration Using DeepSeek

### Decision

Use the DeepSeek API to generate AI-powered business insights from forecast outputs.

### Rationale

* Converts forecast metrics into business-friendly explanations.
* Demonstrates practical integration of Large Language Models (LLMs).
* Enhances usability for non-technical stakeholders.
* Adds an AI-assisted decision support layer to the platform.

### Consequences

* Requires external API credentials and service availability.
* Introduces dependency on an external LLM provider.
* Provides richer insights beyond numerical forecasts.

---

## Decision 6: Docker Containerization

### Decision

Containerize FastAPI and Streamlit services using Docker and Docker Compose.

### Rationale

* Ensures consistent execution across environments.
* Simplifies onboarding and deployment.
* Supports environment isolation.
* Enables reproducible builds.

### Consequences

* Additional container configuration and maintenance.
* Improved portability across development and deployment environments.
* Easier migration to cloud-native platforms.

---

## Decision 7: Continuous Integration Using GitHub Actions

### Decision

Use GitHub Actions to automate testing and validation of code changes.

### Rationale

* Automatically executes test suites on code changes.
* Detects issues early in the development lifecycle.
* Improves overall code quality and reliability.
* Integrates directly with the GitHub development workflow.

### Consequences

* Faster feedback for developers.
* Reduced risk of introducing regressions.
* Current implementation provides Continuous Integration (CI). Continuous Deployment (CD) can be introduced in future iterations to automate deployment workflows.

---

## Summary

The selected architecture emphasizes simplicity, modularity, and maintainability while demonstrating modern engineering practices across:

* Data Engineering
* Machine Learning
* API Development
* Dashboarding
* AI Integration
* Containerization
* Automated Testing
* Continuous Integration

The design also provides clear extension points for future enhancements including advanced forecasting models, additional data sources, cloud-native deployment, and automated deployment pipelines.
