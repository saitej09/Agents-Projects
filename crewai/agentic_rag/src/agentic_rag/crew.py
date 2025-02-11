from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, PDFSearchTool
from tools.document_search_tool import DocumentSearchTool
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class AgenticRag:
    """AgenticRag crew"""

    def __init__(
        self,
        vector_search_tool,
        temperature=0.7,
        model="gpt-4o-mini",
    ):
        self.temperature = temperature
        self.model = model
        self.vector_search_tool = vector_search_tool
        # self.web_search_tool = SerperDevTool()

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def load_llm(self):
        if self.model == "Deepseek":
            llm = LLM(
                model="ollama/deepseek-r1:1.5b",
                base_url="http://localhost:11434",
                temperature=self.temperature,
            )
        elif self.model == "gpt-4o-mini":
            llm = LLM(model=self.model)
        return llm

    @agent
    def retriever_agent(self) -> Agent:
        llm = self.load_llm()
        return Agent(
            llm=llm,
            config=self.agents_config["retriever_agent"],
            tools=[self.vector_search_tool],
            verbose=True,
        )

    @agent
    def response_synthesizer_agent(self) -> Agent:
        llm = self.load_llm()
        return Agent(
            llm=llm,
            config=self.agents_config["response_synthesizer_agent"],
            verbose=True,
        )

    @task
    def retrieve_task(self) -> Task:
        return Task(
            config=self.tasks_config["retrieve_task"],
        )

    @task
    def response_task(self) -> Task:
        return Task(config=self.tasks_config["response_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the AgenticRag crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
