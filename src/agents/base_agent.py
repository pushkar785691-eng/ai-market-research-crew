class BaseAgent:
    name = "BaseAgent"

    def __init__(self, llm_client, verbose: bool = True):
        self.llm = llm_client
        self.verbose = verbose

    def log(self, message: str):
        if self.verbose:
            print(f"[{self.name}] {message}")
