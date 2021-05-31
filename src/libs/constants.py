import os

# Sensitive secrets injected as env variable (e.g. through Kubernetes secrets or retrieved from vault)
DATABASE_URL = os.environ['DATABASE_URL']

SECRET_KEY = os.getenv('SECRET_KEY', 'de4d36b1c5605f70c8aab59216e4261ad8b984b75e23b978c07c22bedc14215e')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

username = 'talal'
name = 'Talal Mahmood Chaudhry'
email = 'talalmahmood@example.com'
fake_users_db = {
    username: {
        'username': username,
        'full_name': name,
        'email': email,
        'hashed_password': '$2b$12$6q.fUkNAab6oqULb1uS8VO.zfpXQbcpEjxYhyR7QEXdafx9fKt7Km',
        'disabled': False,
    },
}