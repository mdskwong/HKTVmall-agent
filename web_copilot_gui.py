import tkinter as tk
from tkinter import scrolledtext, END, font as tkFont, ttk
import threading

from oscopilot import FridayWebAgent
from oscopilot import ToolManager
from oscopilot import FridayWebExecutor, FridayPlanner, FridayRetriever
from oscopilot.utils import setup_config, setup_pre_run
from selenium_utils.create_driver import create_driver
from selenium_utils.reconnect_driver import reconnect_driver
from selenium_utils.json_products_data import clean_json_file

# args = setup_config()
EXIT_COMMANDS = ["exit", "quit", "bye", "goodbye"]
LLM_DROPDOWN = [
    "Meta-Llama-3.1-8B-Instruct",
    "Meta-Llama-3.1-70B-Instruct",
    "Meta-Llama-3.1-405B-Instruct",
    "Doubao-pro-128k"
    ]
PROMPT_TEMPLATE = {
    "1 item: coca cola": "Goto HKTV mall website in 'https://www.hktvmall.com/hktv/en/', search for 'coca cola' products, then add product to cart, finally go to cart page. Give me the cheapest relevant products.",
    "2 items: beef & buns": "Goto HKTV mall website in 'https://www.hktvmall.com/hktv/en/', search for 'beef' and 'buns' products, then add both products to cart, finally go to cart page. Give me the relevant products.",
    "Recipe: hamburger": "I want to make 'hamburger', tell me the recipe, just return the names of ingredients to me only, output the ingredients to ['ingredient 1 ','ingredient 2',...]. If the output is ['ingredient 1','ingredient 2',...], then goto HKTV mall website 'https://www.hktvmall.com/hktv/en/', search for ingredients, and add all products to cart, finally go to cart page. Give me the cheapest relevant products.",
    "Recipe: lemonade": "I want to make 'lemonade', tell me the recipe, just return the names of ingredients to me only, output the ingredients to ['ingredient 1 ','ingredient 2',...]. If the output is ['ingredient 1','ingredient 2',...], then goto HKTV mall website 'https://www.hktvmall.com/hktv/en/', search for ingredients, and add all products to cart, finally go to cart page. Give me the cheapest relevant products.",
    "Recipe with budget: steamed egg": "I want to make 'steamed egg', tell me the recipe, just return the names of ingredients to me only, output the ingredients to ['ingredient 1 ','ingredient 2',...]. If the output is ['ingredient 1','ingredient 2',...], then goto HKTV mall website 'https://www.hktvmall.com/hktv/en/', search for ingredients, and add all products to cart, finally go to cart page. Give me the relevant products within budget. I only have $88 budget."
}

def web_copilot_agent(input_text):
    try:
        # if not args.query:
        reconnect_driver()
        args = setup_config()
        args.query = input_text

        task = setup_pre_run(args)
        
        selected_llm_index = dropdown_llm.current() + 1

        agent = FridayWebAgent(FridayPlanner, FridayRetriever, FridayWebExecutor, ToolManager, config=args, selected_llm_index=selected_llm_index)
        
        agent.run(task=task)
        qa_history_str = "\n".join(agent.qa_history)
        insert_chat_log(f"Web Copilot: {qa_history_str}\n")

        # if FridayWebAgent.stop_agent_event.is_set():  # Check if stop event is set
        #     return "Your task was stopped."

        return "Your task was completed."
    except Exception as e:
        print(f"Error in web_copilot_agent: {e}")
        return "An error occurred while processing your request."

# Function to display the copilot response in the GUI
def show_copilot_response():
    user_input = user_input_box.get("1.0", END).strip()
    user_input_box.delete("1.0", END)

    if user_input.lower() in EXIT_COMMANDS:
        insert_chat_log("Web Copilot: Goodbye!\n")
        cleanup_driver()
        windows.destroy()
        return

    insert_chat_log(f"You: {user_input}\n")
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)  # Enable the Stop button

    # response_text = web_copilot_agent(user_input)
    # insert_chat_log(f"Web Copilot: {response_text}\n")
    # send_button.config(state=tk.NORMAL)
    
    # Start the web_copilot_agent in a separate thread
    threading.Thread(target=run_agent, args=(user_input,), daemon=True).start()

def run_agent(input_text):
    clean_json_file()
    response_text = web_copilot_agent(input_text)
    insert_chat_log(f"Web Copilot: {response_text}\n")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)  # Disable the Stop button

def stop_agent():
    # FridayWebAgent.stop_agent_event.set()  # Set the stop event to stop the agent
    pass

def insert_chat_log(message):
    chat_log.config(state=tk.NORMAL)  # Enable editing to insert text
    chat_log.insert(tk.END, message)   # Insert the message
    chat_log.config(state=tk.DISABLED)  # Disable editing again
    chat_log.see(tk.END)  # Auto-scroll to the latest message

def insert_user_input_box():
    user_input_box.delete("1.0", tk.END)
    user_input_box.insert(tk.END, PROMPT_TEMPLATE[dropdown_template.get()])   # Insert the message

def clear_user_input_box():
    user_input_box.delete("1.0", tk.END)

# Function to handle key press events
def handle_keypress(event):
    # 12 is the state for Ctrl key pressed
    if (event.state & 0x0004) and event.keysym == 'Return':
        show_copilot_response()

def cleanup_driver():
    driver = reconnect_driver()
    if driver:
        driver.close()
        driver.quit()  # Quit the driver if it exists
        driver = None

def on_closing():
    cleanup_driver()  # Clean up the driver before closing the window
    windows.destroy()

# Main GUI window
windows = tk.Tk()
windows.title("Web Copilot")
windows.geometry("600x500")
windows.grid_columnconfigure(0, weight=1)
windows.grid_rowconfigure(0, weight=1)

# Create a font object
custom_font = tkFont.Font(family="Arial", size=12)  # Change "Helvetica" and size as needed

# Chat log
chat_log = scrolledtext.ScrolledText(windows, width=60, height=20, wrap=tk.WORD, font=custom_font)
# chat_log.insert(tk.END, f"Current args: {args}\n")
chat_log.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky=tk.W)
chat_log.config(state=tk.DISABLED)  # Make chat_log non-editable

# User input box
user_input_box = scrolledtext.ScrolledText(windows, width=50, height=5, wrap=tk.WORD, font=custom_font)
# user_input_box.insert(tk.END, PROMPT_TEMPLATE["1 item: coca cola"])
user_input_box.grid(row=1, column=0, rowspan=2, columnspan=3, padx=10, pady=10, sticky=tk.W)

# Dropdown list (Combobox) for LLM selection
llm_label = tk.Label(windows, text="Select LLM:", font=custom_font)
llm_label.grid(row=1, column=3, padx=10, sticky=tk.W)

dropdown_llm = ttk.Combobox(windows, height=1, values=LLM_DROPDOWN)
dropdown_llm.grid(row=2, column=3, padx=10, sticky=tk.NW)
dropdown_llm.current(1)  # Set the default selected item

template_label = tk.Label(windows, text="Select Template:", font=custom_font)
template_label.grid(row=3, column=0, padx=10, sticky=tk.W)

run_label = tk.Label(windows, text="Run:", font=custom_font)
run_label.grid(row=3, column=3, padx=10, sticky=tk.W)

# Dropdown list (Combobox) for template selection
dropdown_template = ttk.Combobox(windows, width=30, height=1, values=list(PROMPT_TEMPLATE))
dropdown_template.grid(row=4, column=0, padx=10, sticky=tk.W)
dropdown_template.current(0)  # Set the default selected item

# Select button
select_button = tk.Button(windows, width=5, height=1, text="Select", command=insert_user_input_box)
select_button.grid(row=4, column=1, sticky=tk.W)

# Clear button
clear_button = tk.Button(windows, width=5, height=1, text="Clear", command=clear_user_input_box)
clear_button.grid(row=4, column=2, sticky=tk.W)

# Start button
start_button = tk.Button(windows, width=5, height=1, text="Start", command=show_copilot_response)
start_button.grid(row=4, column=3, padx=10, sticky=tk.W)

# Stop button
stop_button = tk.Button(windows, width=5, height=1, text="Stop", command=stop_agent, state=tk.DISABLED)
stop_button.grid(row=4, column=3, sticky=tk.E)

# Bind the Ctrl + Enter key event
windows.bind('<KeyRelease>', handle_keypress)

# Bind the window close event to the cleanup function
windows.protocol("WM_DELETE_WINDOW", on_closing)

# Create the driver when the application starts
create_driver()

# Start the GUI event loop
windows.mainloop()