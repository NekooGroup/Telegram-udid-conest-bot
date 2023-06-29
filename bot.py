from pyrogram import Client, filters
from pyrogram.types import Message

# Initialize the Pyrogram client
api_id = YOUR_API_KEY
api_hash = 'YOUR_HASH'
bot_token = 'YOUR_BOT_TOKEN'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Initialize a dictionary to keep track of users who have submitted a valid UDiD
submitted_udids = {}

# Define a command handler
@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    chat_id = message.chat.id

    lang_code = message.from_user.language_code
    if lang_code == 'ru':
        response_message = "Привет! Пожалуйста, отправь нам свой правильный UDiD."
        flag_emoji = "\U0001F1F7\U0001F1FA"  # Russian flag emoji
    else:
        response_message = "Hello! Please send us your valid UDiD."
        flag_emoji = "\U0001F1FA\U0001F1F8"  # United States flag emoji

    # Add the flag emoji to the response message
    response_message = f"{flag_emoji} {response_message}"

    client.send_message(chat_id=chat_id, text=response_message)

# Define a filter to handle all incoming messages
@app.on_message(filters.private)
def handle_message(client: Client, message: Message):
    chat_id = message.chat.id
    text = message.text

    if chat_id in submitted_udids:
        lang_code = message.from_user.language_code
        if lang_code == 'ru':
            response_message = "Привет! Ты уже отправил нам свой правильный UDiD. " \
                               "Ты не можешь отправить еще один UDiD."
            flag_emoji = "\U0001F1F7\U0001F1FA"  # Russian flag emoji
        else:
            response_message = "You have already submitted a valid UDiD. " \
                               "You cannot submit another UDiD."
            flag_emoji = "\U0001F1FA\U0001F1F8"  # United States flag emoji

        # Add the flag emoji to the response message
        response_message = f"{flag_emoji} {response_message}"

        client.send_message(chat_id=chat_id, text=response_message)
        return

    if text is None or len(text) > 40 or len(text) < 25:
        lang_code = message.from_user.language_code
        if lang_code == 'ru':
            response_message = "Привет! UDiD, который ты отправил, не является правильным UDiD."
            flag_emoji = "\U0001F1F7\U0001F1FA"  # Russian flag emoji
        else:
            response_message = "The UDiD you sent is not a valid UDiD."
            flag_emoji = "\U0001F1FA\U0001F1F8"  # United States flag emoji

        # Add the flag emoji to the response message
        response_message = f"{flag_emoji} {response_message}"

        client.send_message(chat_id=chat_id, text=response_message)
    else:
        # Save the message to a text file
        save_message(chat_id, text)

        lang_code = message.from_user.language_code
        if lang_code == 'ru':
            response_message = "Привет! Мы получили твой UDiD. Он будет зарегистрирован в ближайшее время. " \
                               "Однако, ты можешь проверить статус своего UDiD с помощью нашего бота @ipawind_bot.\n\n Подпишитесь, чтобы узнать больше о розыгрыше: @NekooEco"
            flag_emoji = "\U0001F1F7\U0001F1FA"  # Russian flag emoji
        else:
            response_message = "Hello! We have received your UDiD. It will be registered as soon as possible. " \
                               "However, you can check the status of your UDiD using our bot @ipawind_bot.\n\n Follow for More giveway: @NekooEco"
            flag_emoji = "\U0001F1FA\U0001F1F8"  # United States flag emoji

        # Add the flag emoji to the response message
        response_message = f"{flag_emoji} {response_message}"

        client.send_message(chat_id=chat_id, text=response_message)
        submitted_udids[chat_id] = True

# Function to save the message to a text file
def save_message(chat_id, text):
    with open('messages.txt', 'a') as file:
        file.write(f"Chat ID: {chat_id}\n")
        file.write(f"Message: {text}\n")
        file.write("\n")

# Start the bot
app.run()
