from oscopilot import ToolManager
from oscopilot.utils import setup_config

args = setup_config()
tool_manager = ToolManager(args.generated_tool_repo_path)
print(tool_manager.get_all_db_contents()['ids'])