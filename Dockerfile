FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Copy your script
COPY send_receive_bot_message.py /app/send_receive_bot_message.py

# Install dependencies
RUN pip install --no-cache-dir flask requests python-telegram-bot httpx

# Expose Flask default port
EXPOSE 5000

# Run the script
CMD ["python", "send_receive_bot_message.py"]