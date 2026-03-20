from google.adk.agents.llm_agent import Agent

from .tools import (
add_task,
list_tasks, 
move_task, 
archive_task, 
complete_task
)

from datetime import datetime

import logging
from dotenv import load_dotenv
import os

log = logging.getLogger(__name__)

load_dotenv()

BOARD_NAME = "Tarefas"

# Loader function
def _load_prompt(filename:str) -> str:
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()

try:
    INSTRUCTIONS = _load_prompt("instructions.md")
except FileNotFoundError as e:
    log.error(e)
    raise

tools = [add_task, list_tasks, move_task, archive_task, complete_task]

current_date = datetime.now()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Trello task management agent.',
    instruction=INSTRUCTIONS.format(current_date=current_date, board_name=BOARD_NAME),
    tools=tools
)

