from app.clients.ai_client import AiClient


def main():
    client = AiClient()
    print("model:", client.model)
    result = client.generate_text(
        system_prompt="你是一个测试助手。",
        user_prompt="请只回复：OK",
    )
    print("result:", result)


if __name__ == "__main__":
    main()
