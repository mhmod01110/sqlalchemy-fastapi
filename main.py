"""
    Golden Rules for building practical api : 
        1 - Split Endpoints into Routers: Organize your API endpoints into logical routers or modules. This modular approach makes your codebase easier to navigate and maintain, allowing for better scalability and separation of concerns.

        2 - Move Operation Implementations Out of Endpoints: Keep your endpoint definitions clean by moving the business logic and operations to separate service or utility functions. This makes your endpoints focused on handling HTTP requests and responses, while the actual logic is handled elsewhere.

        3 - Consider Deployment Applications (Docker, Environment, Resources): Plan for how your API will be deployed. Use Docker to containerize your application, ensuring consistency across different environments. Manage environment variables properly and consider resource allocation (CPU, memory) to optimize performance and scalability.

        4 - Control Access with Authentication Flow or Rate Limiting: Implement security measures such as authentication and authorization to control who can access your API. Use rate limiting to prevent abuse and ensure fair usage of resources.

        5 - Write Software Testing Code: Develop comprehensive test cases for your API, including unit tests, integration tests, and end-to-end tests. This ensures that your API behaves as expected and helps catch bugs early in the development process.
"""

from fastapi import FastAPI, Response
import models
from database import engine
from routers import post_routes, user_routes
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)


app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


models.Base.metadata.create_all(bind=engine)

app.include_router(post_routes.router, prefix="/posts", tags=["Posts"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

@app.get("/")
def read_root():
    return Response("Server is running")

