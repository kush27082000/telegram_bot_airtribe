# telegram_bot_airtribe

Here are the step-by-step instructions to run your Flask Telegram bot project:

1. **Install Python**  
    Make sure Python 3.x is installed on your system.

2. **Create a Virtual Environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Required Packages:**  
    Install Flask and requests:
    ```bash
    pip install flask python-telegram-bot requests httpx
    ```

4. **Save Your Code:**  
    Ensure your code is saved in the file:
    ```
    /Users/kushagra.soni/github_projects/self_learnings/airtribe_hackathon/telegram_bot_airtribe/bot.py
    ```

5. **Run the Flask App:**  
    In your terminal, navigate to the project directory and run:
    ```bash
    python bot.py
    ```

6. **Send a Request to the Bot:**  
    Use a tool like Postman or curl to send a POST request to your Flask server:
    - URL: `http://127.0.0.1:5000/send`
    - Method: POST
    - Form Data:
      - `message`: (your message text)
      - `image`: (optional, attach an image file)

    Example using curl:
    ```bash
    curl -F "message=Hello from Flask!" http://127.0.0.1:5000/send
    ```

    To send an image:
    ```bash
    curl -F "message=Here is an image" -F "image=@/path/to/image.jpg" http://127.0.0.1:5000/send
    ```

7. **Check Telegram:**  
    The message or image should appear in your Telegram chat with the specified chat ID.

**Note:**  
- Make sure your bot token and chat ID are correct.
- Your bot must be able to message the chat (add it to the group or start a chat with it).