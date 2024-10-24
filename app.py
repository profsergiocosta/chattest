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
async def on_message(message: cl.Message):
    # Certifique-se de que você está acessando o contexto dentro de eventos.
    try:
        # Acessa o contexto dentro de um bloco onde ele está ativo
        user = cl.user_session.get("user")
        if user:
            print(f"Usuário autenticado: {user}")
        else:
            print("Nenhum usuário encontrado na sessão.")
    except cl.context.ChainlitContextException as e:
        print("Erro: Chainlit context não encontrado.")
        print(e)

