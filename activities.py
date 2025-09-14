from temporalio import activity

@activity.defn
async def say_hello(name: str) -> str:
    print("Executing say_hello activity")
    return f"Hello, {name}!"
