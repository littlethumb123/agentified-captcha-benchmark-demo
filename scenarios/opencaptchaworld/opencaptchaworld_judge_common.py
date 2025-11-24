from pydantic import BaseModel
from typing import Optional, Any

from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)


class OpenCaptchaPuzzle(BaseModel):
    """Metadata for a single CAPTCHA puzzle."""
    puzzle_type: str
    puzzle_id: str
    prompt: str
    input_type: str
    ground_truth_answer: Any


class OpenCaptchaAttempt(BaseModel):
    """Result of a single CAPTCHA puzzle solving attempt."""
    puzzle_type: str
    puzzle_id: str
    user_answer: Any
    correct_answer: Any
    correct: bool
    elapsed_time: float


class TypeMetrics(BaseModel):
    """Metrics for a specific puzzle type."""
    puzzle_type: str
    total_attempts: int
    correct_predictions: int
    accuracy: float
    average_solve_time: float


class OpenCaptchaEval(BaseModel):
    """Complete evaluation result for OpenCaptcha benchmark."""
    total_attempts: int
    correct_predictions: int
    overall_accuracy: float
    average_solve_time: float
    type_metrics: list[TypeMetrics]
    attempts: list[OpenCaptchaAttempt]


def opencaptchaworld_judge_agent_card(agent_name: str, card_url: str) -> AgentCard:
    """Generate agent card for OpenCaptchaWorld judge."""
    skill = AgentSkill(
        id='evaluate_opencaptcha_solving',
        name='Evaluates OpenCaptcha solving capability',
        description='Evaluate an agent\'s ability to solve various interactive CAPTCHA puzzles from the OpenCaptchaWorld dataset.',
        tags=['captcha', 'vision', 'interactive', 'benchmark', 'opencaptchaworld'],
        examples=["""
{
  "participants": {
    "opencaptcha_solver": "https://opencaptcha-solver.example.com:443"
  },
  "config": {
    "puzzle_types": ["Dice_Count", "Geometry_Click", "Image_Recognition"]
  }
}
"""]
    )
    agent_card = AgentCard(
        name=agent_name,
        description='Evaluate an agent\'s ability to solve interactive CAPTCHA puzzles from the OpenCaptchaWorld dataset. Tests various puzzle types including dice counting, geometry clicking, image recognition, and more.',
        url=card_url,
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )
    return agent_card

