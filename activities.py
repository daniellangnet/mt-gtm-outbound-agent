from temporalio import activity
from utils.openai_utils import create_openai_client


@activity.defn
async def say_hello(name: str) -> str:
    print("Executing say_hello activity")

    client = create_openai_client()
    response = client.responses.create(
        model="gpt-5-nano",
        input="Tell me a joke about Python."
    )

    return f"Hello, {name}!\n\nHere's a joke:\n{response.output_text}"
