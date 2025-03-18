# Tecartbot - Telegram AI Bot  

Tecartbot is a Telegram bot that assists users with various tasks, including AI-based question answering, handling assignment files, and receiving user feedback.  

## Features  
- **AI Interaction**: The bot can respond to user messages with answers retrieved from an external API.  
- **Logging System**: All user messages, bot responses, and feedback are stored in log files.  
- **Telegram Commands**:  
  - `/start` : Starts the bot and displays a welcome message.  
  - `/help` : Displays a list of available commands.  
  - `/assignment` : Prompts users to submit assignments they want the bot to complete.  
  - `/feedback <message>` : Sends feedback to the bot developer.  
- **File Management**:  
  - The bot can receive and store photos or documents submitted by users as assignments.  
  - Submitted assignments can be processed and returned to the user.  

## Technologies Used  
- **Python** for bot development.  
- **Telegram Bot API** using `telebot` to manage user interactions.  
- **Requests** for fetching data from an external API.  
- **OS and datetime** for file management and logging timestamps.  
