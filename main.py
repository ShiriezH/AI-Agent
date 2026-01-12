from src.llm import LLM
from src.agent import Agent

def main():
    llm = LLM(model="dummy")
    agent = Agent(llm)
    print("Hello from AI-Agent")

if __name__ == "__main__":
    main()
