#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from cv_crew.crew import CvCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'job_description': """Job Title: Software Engineer

        We are seeking a talented and motivated Software Engineer to join our dynamic development team. The ideal candidate will have experience designing, developing, and maintaining scalable web applications.

        Responsibilities:
        - Design, develop, test, and deploy high-quality software solutions
        - Collaborate with cross-functional teams to define, design, and ship new features
        - Write clean, maintainable, and efficient code
        - Participate in code reviews and contribute to team best practices
        - Troubleshoot, debug, and upgrade existing systems

        Requirements:
        - Bachelors degree in Computer Science or related field, or equivalent experience
        - Proficiency in Python, JavaScript, or similar programming languages
        - Experience with web frameworks such as Django, Flask, or React
        - Familiarity with version control systems (e.g., Git)
        - Strong problem-solving skills and attention to detail
        - Excellent communication and teamwork abilities

        Preferred:
        - Experience with cloud platforms (AWS, Azure, or GCP)
        - Knowledge of CI/CD pipelines and DevOps practices""",
    }
    
    try:
        CvCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CvCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CvCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CvCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
