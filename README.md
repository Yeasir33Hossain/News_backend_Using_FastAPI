# News_backend_Using_FastAPI

## Features

- OAuth2 client credentials-based authentication
- Fetch top headlines (NewsAPI)
- Save top 3 latest news to database
- PostgreSQL integration
- Secured API endpoints
- Dockerized
- 72%+ test coverage with Pytest

## Setup Instructions
1. Clone the repo:
   ```bash
   git clone https://github.com/Yeasir33Hossain/News_backend_Using_FastAPI.git
   cd News_backend_Using_FastAPI

2. Create .env
    DATABASE_URL=postgresql://username:password@localhost:5432/newsdb
    NEWS_API_KEY=your_newsapi_key
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret

3. Create_Virtual_env 
    python -m venv env
    source env/bin/activate  
    # On Windows use `env\\Scripts\\activate`

4. Install Requiremts for the project
    pip install -r requirements.txt


5. Run the Project
    uvicorn app.main:app --reload
 
6. Run Tests
    pytest --cov=app tests/

7. Run with Docker
    docker-compose up --build



