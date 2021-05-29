import enum
import os

# When deploying environment variable should be used or better yet secrets
# should be retrieved from a vault. OAuth2 security would be better
user = os.getenv('USERNAME', 'fake-user')
password = os.getenv('PASSWORD', 'fake-password')

DATABASE_URL = os.environ['DATABASE_URL']


class LanguagesEnum(enum.Enum):
    english = "English"
    french = "French"
    german = "German"
    chinese = "Chinese"
    arabic = "Arabic"
    urdu = "Urdu"
