# Senior Software Engineer Interview Project

## Objective:

Build a Python-based web application that demonstrates your ability to design, develop, test, and deploy a software solution. The project should showcase your proficiency in backend and frontend development, database integration, authentication, and deployment. The site will be a simplified forum where users, editors, and admins can post text and images.

## Project Requirements

### 1. Core Functionality

- User Roles:

  - Implement two roles:✅
    - Users: Can post text and images✅, view posts✅, and edit their own posts✅.
    - Admins: Have full control over posts✅ and users (e.g., deleting posts✅, managing user accounts✅).

- Post System:

  - Allow authenticated users to create posts containing text and optional images.✅
  - Implement routes to:
    - List all posts.✅
    - View individual posts.✅
    - Edit and delete posts (based on role permissions).✅

- Authentication:
  - Use FastAPI's dependency injection for user authentication.✅
  - Protect routes based on user roles.✅
  - Include registration and login functionality.✅

### 2. Frontend Functionality

- UI Framework: Create a minimal frontend (can use Streamlit)

  - Pages:

    - Login Page: Users can log in with their credentials.✅
    - Post Listing Page: Display all posts.✅
    - Create/Edit Post Page: Allow users to add or modify posts.✅
    - Profile Page: Display user-specific details.✅

  - Enable image upload functionality in the frontend.✅

### 3. Backend and Database

- Backend Framework:✅
  - Use FastAPI for the backend.✅
- Recommended python packages:
  - Pydantic✅
  - PyMongo✅
  - SQLAlchemy✅
- Database Integration:
  - MongoDB: Store post data, including text, images, and metadata (e.g., timestamps, author).✅
  - MariaDB: Store user information and role assignments.✅

### 4. Testing

- Backend Testing: Use pytest for unit and integration tests.✅
- Frontend Testing: Use pytest-playwright to test the UI functionality (e.g., login, post creation).✅
- Ensure tests cover:
  - User authentication.✅
  - Role-based access control.✅
  - Post creation, editing, and deletion.✅

### 5. CI/CD Integration (Nice to Have)

- Set up GitHub Actions to:
  - Run tests automatically (unit, integration, and UI tests).✅
  - Run pre-commit checks for:
    - mypy for type checking.
    - ruff for linting.

### 6. Deployment

- Containerization:

  - Use Docker Compose to run:

    - Python backend service✅
    - Frontend service (Streamlit/other)✅
    - MongoDB service✅
    - MariaDB service => a sqlite db is used

  - Optional/Nice-to-Have: Deploy the application on Kubernetes using Minikube.

### 7. Project Packaging

- Structure the project as a pip package with a setup.py + pyproject.toml files.✅

### 8. Repository and Submission

- Push the project to a GitHub repository (public or private).✅
- Include clear documentation covering:

  - Project setup and execution.✅
  - API routes and functionality.✅
  - Testing execution.✅
  - CI/CD pipeline setup (Optional - Nice to have)
  - Optional: Kubernetes deployment instructions.

- Share the GitHub link as part of your submission.✅

## Evaluation Criteria

1. Comprehensive README.md

2. Code Quality:

   - Adherence to Python best practices.
   - Clear, maintainable, and modular code.

3. Functionality:

   - Cover most of the implementation of user roles, authentication, and post management.

4. Testing:

   - Comprehensive test coverage for backend and frontend.

5. CI/CD Integration: (Optional - Nice to have)

   - Automated checks and tests on GitHub Actions.

6. Deployment:

   - Successfully running containerized application.
   - Optional: Kubernetes deployment on Minikube.

Good luck, and we look forward to seeing your implementation!
