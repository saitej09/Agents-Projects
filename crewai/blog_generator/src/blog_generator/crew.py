from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class BlogGenerator:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, temperature=0.7, model="GPT-4o Mini"):
        self.temperature = temperature
        self.model = model

    @agent
    def researcher(self) -> Agent:

        return Agent(
            config=self.agents_config["researcher"],
            tools=[SerperDevTool()],
            verbose=True,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        # Add other models
        if self.model == "Deepseek":
            ollama_llm = LLM(
                model="ollama/deepseek-r1:1.5b",
                base_url="http://localhost:11434",
                temperature=self.temperature,
            )
            return Agent(
                llm=ollama_llm,
                config=self.agents_config["reporting_analyst"],
                verbose=True,
            )
        elif self.model == "GPT-4o Mini":
            return Agent(
                config=self.agents_config["reporting_analyst"],
                verbose=True,
            )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(config=self.tasks_config["reporting_task"], output_file="report.md")

    @crew
    def crew(self) -> Crew:
        """Creates the BlogGenerator crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
