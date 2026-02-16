# #!/bin/bash

# # 🐳 DOCKER + CHATBOT DATABASE SETUP

# echo "======================================================================"
# echo "🐳 DOCKER + CHATBOT DATABASE SETUP"
# echo "======================================================================"

# # Database configuration (matches docker-compose.yml)
# DB_HOST="localhost"
# DB_PORT="5432"
# DB_USER="postgres"
# DB_PASS="postgres"
# DB_NAME="chatbot_db"
# NEW_USER="BRAHIM"
# NEW_PASS="0000"

# # Colors
# GREEN='\033[0;32m'
# BLUE='\033[0;34m'
# RED='\033[0;31m'
# NC='\033[0m' # No Color

# # ==================== FUNCTIONS ====================

# wait_for_postgres() {
#     echo -e "\n⏳ Waiting for PostgreSQL to start..."
    
#     local max_attempts=30
#     local attempt=1
    
#     while [ $attempt -le $max_attempts ]; do
#         if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "SELECT 1" > /dev/null 2>&1; then
#             echo -e "${GREEN}✅ PostgreSQL is ready!${NC}"
#             return 0
#         fi
        
#         if [ $attempt -lt $max_attempts ]; then
#             echo "   Attempt $attempt/$max_attempts... Retrying in 2 seconds"
#             sleep 2
#         else
#             echo -e "${RED}❌ PostgreSQL failed to start${NC}"
#             return 1
#         fi
        
#         attempt=$((attempt + 1))
#     done
    
#     return 1
# }

# create_database_and_user() {
#     echo -e "\n🗄️  Creating database and user..."
    
#     # Create user if not exists
#     if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "SELECT 1 FROM pg_roles WHERE rolname='$NEW_USER'" 2>/dev/null | grep -q "1 row"; then
#         if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "CREATE USER $NEW_USER WITH PASSWORD '$NEW_PASS';" > /dev/null 2>&1; then
#             echo -e "   ${GREEN}✅${NC} User '$NEW_USER' created"
#         else
#             echo -e "   ${RED}❌ Error creating user${NC}"
#             return 1
#         fi
#     else
#         echo -e "   ℹ️  User '$NEW_USER' already exists"
#     fi
    
#     # Create database if not exists
#     if ! psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" 2>/dev/null | grep -q "1 row"; then
#         if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "postgres" -c "CREATE DATABASE $DB_NAME OWNER $NEW_USER;" > /dev/null 2>&1; then
#             echo -e "   ${GREEN}✅${NC} Database '$DB_NAME' created"
#         else
#             echo -e "   ${RED}❌ Error creating database${NC}"
#             return 1
#         fi
#     else
#         echo -e "   ℹ️  Database '$DB_NAME' already exists"
#     fi
    
#     return 0
# }

# create_tables() {
#     echo -e "\n📊 Creating tables..."
    
#     # Messages table
#     if psql -h "$DB_HOST" -p "$DB_PORT" -U "$NEW_USER" -d "$DB_NAME" -c "
#         CREATE TABLE IF NOT EXISTS messages (
#             id SERIAL PRIMARY KEY,
#             session_id VARCHAR(50) NOT NULL,
#             role VARCHAR(10) NOT NULL,
#             content TEXT NOT NULL,
#             timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#         )
#     " > /dev/null 2>&1; then
#         echo -e "   ${GREEN}✅${NC} Table 'messages' created"
#     else
#         echo -e "   ${RED}❌ Error creating messages table${NC}"
#         return 1
#     fi
    
#     # Chat sessions table
#     if psql -h "$DB_HOST" -p "$DB_PORT" -U "$NEW_USER" -d "$DB_NAME" -c "
#         CREATE TABLE IF NOT EXISTS chat_sessions (
#             id SERIAL PRIMARY KEY,
#             session_id VARCHAR(50) UNIQUE NOT NULL,
#             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             message_count INTEGER DEFAULT 0
#         )
#     " > /dev/null 2>&1; then
#         echo -e "   ${GREEN}✅${NC} Table 'chat_sessions' created"
#     else
#         echo -e "   ${RED}❌ Error creating chat_sessions table${NC}"
#         return 1
#     fi
    
#     # Create indexes
#     if psql -h "$DB_HOST" -p "$DB_PORT" -U "$NEW_USER" -d "$DB_NAME" -c "
#         CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
#         CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
#     " > /dev/null 2>&1; then
#         echo -e "   ${GREEN}✅${NC} Indexes created"
#     else
#         echo -e "   ${RED}❌ Error creating indexes${NC}"
#         return 1
#     fi
    
#     return 0
# }

# create_config() {
#     echo -e "\n⚙️  Creating configuration file..."
    
#     cat > config.py << EOFCONFIG
# # Database Configuration (Docker)
# DB_HOST = "$DB_HOST"
# DB_PORT = "$DB_PORT"
# DB_NAME = "$DB_NAME"
# DB_USER = "$NEW_USER"
# DB_PASS = "$NEW_PASS"

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# EOFCONFIG
    
#     if [ -f config.py ]; then
#         echo -e "   ${GREEN}✅${NC} Created config.py"
#         return 0
#     else
#         echo -e "   ${RED}❌ Error creating config.py${NC}"
#         return 1
#     fi
# }

# # ==================== MAIN ====================

# main() {
#     echo -e "\n📋 Starting Docker PostgreSQL setup...\n"
    
#     # Check if psql is installed
#     if ! command -v psql &> /dev/null; then
#         echo -e "${RED}❌ psql not found! Install PostgreSQL client first:${NC}"
#         echo "   Mac: brew install postgresql"
#         echo "   Linux: sudo apt-get install postgresql-client"
#         return 1
#     fi
    
#     # Step 1: Wait for PostgreSQL
#     if ! wait_for_postgres; then
#         echo -e "\n${RED}❌ PostgreSQL container is not running!${NC}"
#         echo "   Run: docker-compose up -d"
#         return 1
#     fi
    
#     # Step 2: Create database and user
#     echo -e "\n${BLUE}Step 1/4: Creating database and user${NC}"
#     if ! create_database_and_user; then
#         return 1
#     fi
    
#     # Step 3: Create tables
#     echo -e "\n${BLUE}Step 2/4: Creating tables${NC}"
#     if ! create_tables; then
#         return 1
#     fi
    
#     # Step 4: Create config
#     echo -e "\n${BLUE}Step 3/4: Creating configuration${NC}"
#     if ! create_config; then
#         return 1
#     fi
    
#     # Success!
#     echo ""
#     echo "======================================================================"
#     echo -e "${GREEN}✅ DOCKER SETUP COMPLETED SUCCESSFULLY!${NC}"
#     echo "======================================================================"
    
#     echo -e "\n${BLUE}📊 Database Information:${NC}"
#     echo "   Host: $DB_HOST"
#     echo "   Port: $DB_PORT"
#     echo "   Database: $DB_NAME"
#     echo "   User: $NEW_USER"
#     echo "   Password: $NEW_PASS"
    
#     echo -e "\n${BLUE}🚀 Next Steps:${NC}"
#     echo "   1. Ensure Docker container is running: docker-compose ps"
#     echo "   2. Run Flask app: python app.py"
#     echo "   3. Open: http://localhost:6000/chatbot"
    
#     echo -e "\n${BLUE}📁 Files Created:${NC}"
#     echo "   - config.py (database configuration)"
#     echo "   - Database '$DB_NAME'"
#     echo "   - User '$NEW_USER'"
#     echo "   - Tables: messages, chat_sessions"
    
#     echo ""
#     echo "======================================================================"
#     return 0
# }

# # Run main function
# main
# exit $?






















# # import psycopg2
# # from psycopg2 import sql
# # import time
# # import sys

# # print("=" * 70)
# # print("🐳 DOCKER + CHATBOT DATABASE SETUP")
# # print("=" * 70)

# # # Database configuration (matches docker-compose.yml)
# # DB_HOST = "localhost"
# # DB_PORT = "5432"
# # DB_USER = "postgres"
# # DB_PASS = "postgres"
# # DB_NAME = "chatbot_db"
# # NEW_USER = "BRAHIM"
# # NEW_PASS = "0000"

# # def wait_for_postgres(max_attempts=30):
# #     """Wait for PostgreSQL to be ready"""
# #     print("\n⏳ Waiting for PostgreSQL to start...")
    
# #     for attempt in range(max_attempts):
# #         try:
# #             conn = psycopg2.connect(
# #                 dbname="postgres",
# #                 user=DB_USER,
# #                 password=DB_PASS,
# #                 host=DB_HOST,
# #                 port=DB_PORT,
# #                 connect_timeout=1
# #             )
# #             conn.close()
# #             print("✅ PostgreSQL is ready!")
# #             return True
# #         except psycopg2.OperationalError:
# #             if attempt < max_attempts - 1:
# #                 print(f"   Attempt {attempt + 1}/{max_attempts}... Retrying in 2 seconds")
# #                 time.sleep(2)
# #             else:
# #                 print("❌ PostgreSQL failed to start")
# #                 return False
# #     return False

# # def create_database_and_user():
# #     """Create database and user"""
# #     try:
# #         print("\n🗄️  Creating database and user...")
        
# #         conn = psycopg2.connect(
# #             dbname="postgres",
# #             user=DB_USER,
# #             password=DB_PASS,
# #             host=DB_HOST,
# #             port=DB_PORT
# #         )
# #         conn.autocommit = True
# #         cur = conn.cursor()

# #         # Create user if not exists
# #         cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{NEW_USER}'")
# #         if not cur.fetchone():
# #             cur.execute(
# #                 sql.SQL("CREATE USER {} WITH PASSWORD %s").format(
# #                     sql.Identifier(NEW_USER)
# #                 ),
# #                 [NEW_PASS]
# #             )
# #             print(f"   ✅ User '{NEW_USER}' created")
# #         else:
# #             print(f"   ℹ️  User '{NEW_USER}' already exists")

# #         # Create database if not exists
# #         cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'")
# #         if not cur.fetchone():
# #             cur.execute(
# #                 sql.SQL("CREATE DATABASE {} OWNER {}").format(
# #                     sql.Identifier(DB_NAME),
# #                     sql.Identifier(NEW_USER)
# #                 )
# #             )
# #             print(f"   ✅ Database '{DB_NAME}' created")
# #         else:
# #             print(f"   ℹ️  Database '{DB_NAME}' already exists")

# #         cur.close()
# #         conn.close()
# #         return True
# #     except Exception as e:
# #         print(f"   ❌ Error: {e}")
# #         return False

# # def create_tables():
# #     """Create tables in the new database"""
# #     try:
# #         print("\n📊 Creating tables...")
        
# #         conn = psycopg2.connect(
# #             dbname=DB_NAME,
# #             user=NEW_USER,
# #             password=NEW_PASS,
# #             host=DB_HOST,
# #             port=DB_PORT
# #         )
# #         cur = conn.cursor()

# #         # Messages table
# #         cur.execute('''
# #             CREATE TABLE IF NOT EXISTS messages (
# #                 id SERIAL PRIMARY KEY,
# #                 session_id VARCHAR(50) NOT NULL,
# #                 role VARCHAR(10) NOT NULL,
# #                 content TEXT NOT NULL,
# #                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# #             )
# #         ''')
# #         print("   ✅ Table 'messages' created")

# #         # Chat sessions table
# #         cur.execute('''
# #             CREATE TABLE IF NOT EXISTS chat_sessions (
# #                 id SERIAL PRIMARY KEY,
# #                 session_id VARCHAR(50) UNIQUE NOT NULL,
# #                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# #                 updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
# #                 message_count INTEGER DEFAULT 0
# #             )
# #         ''')
# #         print("   ✅ Table 'chat_sessions' created")

# #         # Create indexes
# #         cur.execute('CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id)')
# #         cur.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)')
# #         print("   ✅ Indexes created")

# #         conn.commit()
# #         cur.close()
# #         conn.close()
# #         return True
# #     except Exception as e:
# #         print(f"   ❌ Error: {e}")
# #         return False

# # def create_config():
# #     """Create config file for Flask"""
# #     try:
# #         print("\n⚙️  Creating configuration file...")
        
# #         config_content = f'''# Database Configuration (Docker)
# # DB_HOST = "{DB_HOST}"
# # DB_PORT = "{DB_PORT}"
# # DB_NAME = "{DB_NAME}"
# # DB_USER = "{NEW_USER}"
# # DB_PASS = "{NEW_PASS}"

# # DATABASE_URL = f"postgresql://{NEW_USER}:{NEW_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# # '''
        
# #         with open('config.py', 'w') as f:
# #             f.write(config_content)
# #         print("   ✅ Created config.py")
# #         return True
# #     except Exception as e:
# #         print(f"   ❌ Error: {e}")
# #         return False

# # def main():
# #     print("\n📋 Starting Docker PostgreSQL setup...\n")
    
# #     # Step 1: Wait for PostgreSQL
# #     if not wait_for_postgres():
# #         print("\n❌ PostgreSQL container is not running!")
# #         print("   Run: docker-compose up -d")
# #         return False
    
# #     # Step 2: Create database and user
# #     print("\nStep 1/4: Creating database and user")
# #     if not create_database_and_user():
# #         return False
    
# #     # Step 3: Create tables
# #     print("\nStep 2/4: Creating tables")
# #     if not create_tables():
# #         return False
    
# #     # Step 4: Create config
# #     print("\nStep 3/4: Creating configuration")
# #     if not create_config():
# #         return False
    
# #     # Success!
# #     print("\n" + "=" * 70)
# #     print("✅ DOCKER SETUP COMPLETED SUCCESSFULLY!")
# #     print("=" * 70)
    
# #     print("\n📊 Database Information:")
# #     print(f"   Host: {DB_HOST}")
# #     print(f"   Port: {DB_PORT}")
# #     print(f"   Database: {DB_NAME}")
# #     print(f"   User: {NEW_USER}")
# #     print(f"   Password: {NEW_PASS}")
    
# #     print("\n🚀 Next Steps:")
# #     print("   1. Ensure Docker container is running: docker-compose ps")
# #     print("   2. Run Flask app: python app.py")
# #     print("   3. Open: http://localhost:5000/chatbot")
    
# #     print("\n📁 Files Created:")
# #     print("   - config.py (database configuration)")
# #     print("   - Database 'chatbot_db'")
# #     print("   - User 'BRAHIM'")
# #     print("   - Tables: messages, chat_sessions")
    
# #     print("\n" + "=" * 70)
# #     return True

# # if __name__ == "__main__":
# #     success = main()
# #     sys.exit(0 if success else 1)

    