from trello import TrelloClient
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging
import os

load_dotenv()
log = logging.getLogger(__name__)


GCP_SCOPES = ['https://www.googleapis.com/auth/calendar']
LIST_TODO = "A Fazer"                                    
LIST_IN_PROGRESS = "Em Progresso"
LIST_DONE = "Feito"
BOARD_NAME = "Tarefas"       

# ---------------------
# |   INIT CLIENTS    |
# ---------------------
_trello_client: TrelloClient | None = None
_calendar_client = None

def _get_trello_client() -> TrelloClient:
    global _trello_client
    if _trello_client is None:
        _trello_client = TrelloClient(
            api_key=os.getenv("TRELLO_API_KEY"),               
            api_secret=os.getenv("TRELLO_SECRET"),             
            token=os.getenv("TRELLO_TOKEN") 
            )
    return _trello_client

def _get_calendar_creds():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', GCP_SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', GCP_SCOPES)
            credentials = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
    return credentials

def _get_calendar_client():
    global _calendar_client                            
    if _calendar_client is None:                       
        _calendar_client = build('calendar', 'v3', credentials=_get_calendar_creds())
    return _calendar_client


# ---------------------
# |   TRELLO TOOLS    |
# ---------------------
def add_task(name: str, desc: str, due: str, list_name: str = LIST_TODO, board_name: str = BOARD_NAME):
    """Add a task to a Trello board.
    
    Use this function to add a task to a trello list.

    Args
        name: task name.
        desc: task description.
        due: task's due date.
        list_name: name of the list the task is contained in.
    
    Returns
        confirmation (str): confirmation of task addition.
    """
    try:
        log.info("[AGENT] Using add_task tool...")
        client = _get_trello_client()
        board = next((board for board in client.list_boards() if board.name == board_name), None)
        if not board:
            return f'Board "{board_name}" not found.'

        todo_list = next((l for l in board.list_lists() if l.name == list_name), None)
        if not todo_list:
            return f'List "{list_name}" not found.'

        todo_list.add_card(
            name=name,
            desc=desc,
            due=due
        )
        confirmation = f"""
        Task added to: {list_name}
        Name: {name}
        Description: {desc}
        Due Date: {due}
        """
        return confirmation
    except Exception as e:
        log.error(f"Failed to add task: {e}", exc_info=True)
        raise

# TODO
# ---------------------
# |  CALENDAR TOOLS   |
# ---------------------


# TODO
# ---------------------
# |   GITHUB TOOLS    |
# ---------------------