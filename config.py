# Database Configuration
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "chatbot_db"
DB_USER = "BRAHIM"
DB_PASS = "0000"

DATABASE_URL = "postgresql://{0}:{1}@{2}:{3}/{4}?sslmode=disable&gssencmode=disable".format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
