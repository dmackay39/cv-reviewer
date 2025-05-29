from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class CvCrew():
    """CvCrew crew"""

    # YAML configuration files
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Agents
    @agent
    def cv_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['cv_reviewer'],
            verbose=True
        )

    @agent
    def cover_letter_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['cover_letter_writer'],
            verbose=True
        )

    # Tasks
    @task
    def cv_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['cv_review_task'],
            tools=[PDFSearchTool(pdf='<path>/knowledge/Current_CV.pdf')],  # Tool to read files, e.g., CVs
        )

    @task
    def cover_letter_task(self) -> Task:
        return Task(
            config=self.tasks_config['cover_letter_task'],
            tools=[PDFSearchTool(pdf='<path>/knowledge/Current_CV.pdf')],  # Tool to read files, e.g., job descriptions
            output_file='output/cover_letter.md',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CvCrew crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks,   # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )