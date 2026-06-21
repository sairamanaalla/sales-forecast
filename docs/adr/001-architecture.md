# ADR-001: Architecture Decisions

## Status

Accepted

---

## Context

The objective of this project is to build an end-to-end sales forecasting platform that demonstrates modern data engineering, machine learning, API development, dashboarding, AI integration, containerization, testing, and CI practices.

The solution is required to:

* Ingest Sales Transactions, Product Master, and Store Reference datasets.
* Apply data quality validations including null checks, duplicate removal, invalid date detection, and reference-data validation.
* Generate future revenue forecasts using machine learning.
* Expose forecast and analytics data through APIs.
* Provide an interactive dashboard for business users.
* Generate AI-powered business insights from forecast results.
* Support containerized deployment, testing, and automated validation.

The architecture should remain modular, maintainable, and extensible to support future enhancements.

---

## Decision 1: Medallion Architecture (Bronze and Silver Layers)

### Decision

Use a Medallion-style architecture consisting of Bronze and Silver layers to integrate Sales Transactions, Product Master, and Store Reference datasets.

### Rationale

* Bronze layer stores raw ingested data.
* Silver layer stores validated and cleaned data.
* Provides clear separation between ingestion and transformation.
* Improves traceability and data quality.
* Supports enrichment of transactional sales data with product and store reference attributes.
* Enables implementation of data-quality validation and rejection workflows.

### Trade-offs

* Chosen over a single-stage data processing pipeline to provide clearer separation between raw ingestion and validated business-ready data.
* Introduces additional storage and transformation layers in exchange for improved traceability, maintainability, and data quality management.

### Consequences

* Easier debugging and auditing.
* Better maintainability.
* Supports future expansion to a Gold layer for business aggregations.
* Provides a foundation for master-data-driven forecasting.
* Supports future integration of additional business reference datasets.

---

## Decision 2: Data Quality Validation

### Decision

Implement data-quality validation during Silver layer processing.

### Rationale

* Detect and reject invalid records before forecasting.
* Improve forecast reliability and trustworthiness.
* Simulate real-world data engineering challenges.

### Implemented Validations

* Null value checks
* Invalid date detection
* Duplicate transaction removal
* Negative quantity rejection
* Negative price rejection
* Unknown SKU rejection
* Unknown Store rejection

### Consequences

* Improved forecast accuracy and data consistency.
* Additional processing logic during ingestion.
* Better alignment with enterprise data engineering practices.

---

## Decision 3: Random Forest for Forecasting

### Decision

Use RandomForestRegressor as the forecasting model.

### Rationale

* Utilizes category, brand, region, and temporal features for forecasting.
* Performs well on structured business datasets.
* Handles non-linear relationships effectively.
* Requires minimal feature engineering and preprocessing.
* Supports feature importance analysis to understand demand drivers.
* Easy to train and evaluate.
* Suitable for demonstrating an end-to-end machine learning workflow.

### Trade-offs

* Chosen over more specialized forecasting approaches such as Prophet and LSTM to balance implementation simplicity, interpretability, and development effort.
* Sacrifices some advanced time-series modeling capabilities in exchange for faster development, easier training, and straightforward feature importance analysis.

### Consequences

* Faster implementation compared to advanced forecasting approaches.
* Forecasts incorporate master-data attributes and regional demand patterns.
* Model remains interpretable through feature importance analysis.
* Can be replaced with more sophisticated forecasting models in the future.

---

## Decision 4: FastAPI for API Layer

### Decision

Use FastAPI to expose forecast, summary, and AI insight endpoints.

### Rationale

* High-performance Python web framework.
* Automatic OpenAPI and Swagger documentation.
* Strong integration with machine learning workflows.
* Simple and lightweight architecture.

### Trade-offs

* Chosen over lightweight frameworks such as Flask due to built-in OpenAPI documentation, strong typing support, and modern API development features.
* Introduces slightly more framework structure in exchange for improved developer productivity, API maintainability, and automatic documentation generation.

### Consequences

* Rapid API development.
* Interactive API documentation available through Swagger UI.
* Easy integration with frontend applications and external consumers.

---

## Decision 5: Streamlit for Dashboard

### Decision

Use Streamlit to build the analytics dashboard.

### Rationale

* Enables rapid dashboard development.
* Native integration with pandas and Python analytics workflows.
* Requires minimal frontend development effort.
* Provides interactive filtering and visualization capabilities.

### Trade-offs

* Chosen over custom frontend frameworks such as React or Angular to accelerate dashboard development and reduce frontend implementation complexity.
* Sacrifices some UI customization flexibility in exchange for faster delivery, simpler maintenance, and tight integration with Python analytics workflows.

### Consequences

* Faster delivery compared to building a custom frontend.
* Simplified maintenance and deployment.
* Suitable for analytical and proof-of-concept applications.

---

## Decision 6: LLM Integration Using DeepSeek

### Decision

Use the DeepSeek API to generate AI-powered business insights from forecast outputs.

### Rationale

* Converts forecast metrics into business-friendly explanations.
* Demonstrates practical integration of Large Language Models (LLMs).
* Enhances usability for non-technical stakeholders.
* Adds an AI-assisted decision support layer to the platform.

### Trade-offs

* Chosen over building a custom NLP solution to quickly provide business-friendly insights from forecast outputs.
* Introduces dependency on an external AI service in exchange for significantly reduced implementation effort and richer natural language explanations.

### Consequences

* Requires external API credentials and service availability.
* Introduces dependency on an external LLM provider.
* Provides richer insights beyond numerical forecasts.

---

## Decision 7: Docker Containerization

### Decision

Containerize FastAPI and Streamlit services using Docker and Docker Compose.

### Rationale

* Ensures consistent execution across environments.
* Simplifies onboarding and deployment.
* Supports environment isolation.
* Enables reproducible builds.

### Trade-offs

* Chosen to ensure consistent execution across development and deployment environments and simplify project onboarding.
* Introduces container configuration and image management responsibilities in exchange for reproducible deployments and environment portability.

### Consequences

* Additional container configuration and maintenance.
* Improved portability across development and deployment environments.
* Easier migration to cloud-native platforms.

---

## Decision 8: Continuous Integration Using GitHub Actions

### Decision

Use GitHub Actions to automate testing and validation of code changes.

### Rationale

* Automatically executes test suites on code changes.
* Detects issues early in the development lifecycle.
* Improves overall code quality and reliability.
* Integrates directly with the GitHub development workflow.

### Trade-offs

* Chosen over manual testing processes to provide automated validation of code changes and faster feedback cycles.
* Requires pipeline maintenance and configuration effort in exchange for improved code quality, reliability, and early defect detection.

### Consequences

* Faster feedback for developers.
* Reduced risk of introducing regressions.
* Current implementation provides Continuous Integration (CI). Continuous Deployment (CD) can be introduced in future iterations to automate deployment workflows.

---

## Summary

The selected architecture emphasizes simplicity, modularity, and maintainability while demonstrating modern engineering practices across:

* Data Ingestion and Quality Engineering
* Master Data Management
* Machine Learning Forecasting
* API Development
* Dashboarding and Analytics
* LLM-Powered Business Insights
* Containerization
* Automated Testing
* Continuous Integration

The design provides clear extension points for future enhancements including:

* Advanced forecasting models (XGBoost, Prophet, LSTM)
* Additional business data sources such as promotions, marketing campaigns, and weather signals
* Gold-layer business aggregations
* Cloud-native deployment platforms
* Automated deployment pipelines (CD)
* Real-time data ingestion and forecasting
