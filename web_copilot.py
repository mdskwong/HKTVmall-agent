from oscopilot import FridayWebAgent
from oscopilot import ToolManager
from oscopilot import FridayWebExecutor, FridayPlanner, FridayRetriever
from oscopilot.utils import setup_config, setup_pre_run
from selenium_utils.create_driver import create_driver
import time

start_time = time.gmtime()

args = setup_config()
if not args.query:
    # args.query = "Goto HKTV mall website in 'https://www.hktvmall.com/hktv/en/', search for 'coca cola' products, then add product to cart. Give me the cheapest relevant products."
    args.query = "Goto HKTV mall website in 'https://www.hktvmall.com/hktv/en/', search for 'beef' and 'buns' products, then add both products to cart. Give me the relevant products. I have $80 budget for all items."
    # args.query = "Goto HKTV mall website in 'https://www.hktvmall.com/hktv/en/', search for 'xbox', 'ps5' and 'switch' products, then add all products to cart."
    # args.query = "Goto HKTV mall website in 'https://www.hktvmall.com/hktv/en/', search for 'xbox', 'basketball', 'rice' and 'fanta' products, then add all products to cart."
    # args.query = "I want to cook 'hamburger', tell me the recipe, just return the names of ingredients to me only, output the ingredients to ['ingredient 1 ','ingredient 2',...]. If the output is ['ingredient 1','ingredient 2',...], then goto HKTV mall website 'https://www.hktvmall.com/hktv/en/', search for ingredients, and add all products to cart. Give me the cheapest relevant products."
task = setup_pre_run(args)

driver = create_driver()

agent = FridayWebAgent(FridayPlanner, FridayRetriever, FridayWebExecutor, ToolManager, config=args)
# agent.run(task=task)

tool_manager = ToolManager(args.generated_tool_repo_path)
print(tool_manager.get_all_db_contents())

end_time = time.gmtime()
# running_time = end_time - start_time
# print(f"Running time: {time.strftime('%H:%M:%S', running_time)} seconds")
