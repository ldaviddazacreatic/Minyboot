# app.py
import tkinter as tk
import asyncio
from assistant import query_assistant

# Function to handle the user's query
async def execute_query():
    user_message = entry_user.get().strip()
    if user_message:
        try:
            label_response.config(text="Loading...")
            response = await asyncio.to_thread(query_assistant, user_message)
            label_response.config(text=response)
            entry_user.delete(0, tk.END)
            # Hide examples after the query
            label_examples.pack_forget()
        except Exception as e:
            label_response.config(text=f"Error: {e}")
    else:
        label_response.config(text="Please enter a query.")

def start_asyncio():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_query())

# Create the main window
window = tk.Tk()
window.title("Hello, I'm MinyBot, Your Virtual Gaming Product Assistant")
window.geometry("500x400")  # Adjust size for more space

# Label for the user to enter their query
label_user = tk.Label(window, text="Enter your query:")
label_user.pack(pady=10)

# Entry field for the query
entry_user = tk.Entry(window, width=50)
entry_user.pack(pady=10)

# Button to execute the query
button_query = tk.Button(window, text="Query", command=start_asyncio)
button_query.pack(pady=10)

# Label to display the response
label_response = tk.Label(window, text="The response will appear here", wraplength=400, justify="left")
label_response.pack(pady=20)

# Example questions
example_questions = """
Examples of what you can ask:
- "Give me information about the RGB mechanical keyboard."
- "Is the RGB mechanical keyboard available?"
- "How many units are there of the wireless mouse?"
- "Is there stock of the gaming laptop?"
"""
label_examples = tk.Label(window, text=example_questions, wraplength=400, justify="left", fg="gray")
label_examples.pack(pady=10)

# Run the window
window.mainloop()
