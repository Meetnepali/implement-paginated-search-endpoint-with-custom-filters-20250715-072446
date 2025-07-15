# Guidance for Task

This is an intermediate FastAPI backend assessment for building an order management API module.

## Your Task

- Complete the API implementation so that it fully supports:
  - Creating orders (with at least one item; each item having positive price and quantity)
  - Retrieving single and multiple orders (with pagination and filtering by customer)
  - Updating and deleting orders
  - Properly structured, OpenAPI-documented endpoints using APIRouter under `/orders`
  - In-memory storage (dependency-injected dictionary)
  - Consistent, structured error responses for all input/validation failures
  - Model validation with Pydantic

You are expected to:
- Build out or enhance the FastAPI endpoints and Pydantic models as described.
- Ensure ALL validation and error handling is robust and consistent.
- Ensure endpoint documentation is clear and helpful. Responses and examples should support OpenAPI/Swagger UI.
- Maintain clean code organization for maintainability and extensibility.

## Verifying Your Solution

- Start the application and use a tool like Swagger UI to create, retrieve, update, and delete orders.
- Verify that validation rules (e.g., min item count, positive price/quantity) are enforced, and errors are consistently structured.
- Confirm that endpoints return OpenAPI documentation as intended.

*Do NOT include instructions for building or running the environment here. Focus strictly on the implementation requirements and API contract.*
