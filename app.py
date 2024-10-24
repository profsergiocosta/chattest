import chainlit as cl


@cl.on_chat_start
def on_chat_start():
    print("A new chat session has started!")

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Verifica o usuário e senha
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...

    # Send a response back to the user
    await cl.Message(
        content=f"Received: {message.content}",
    ).send()
