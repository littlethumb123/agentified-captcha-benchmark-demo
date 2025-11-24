# Agentified CAPTCHA Benchmark

A prototype of agent-based CAPTCHA solving benchmark using the A2A (Agent-to-Agent) protocol.

## Overview

This project demonstrates an agentified approach to benchmarking CAPTCHA-solving capabilities using AI agents. It leverages the [A2A protocol](https://a2a-protocol.org/latest/) for agent interoperability and provides a standardized evaluation framework.

It was forked from https://github.com/agentbeats/tutorial.

The benchmark consists of:
- **Green Agent (Judge)**: Orchestrates the CAPTCHA solving assessment and evaluates results
- **Purple Agent (Solver)**: Attempts to solve CAPTCHA challenges using vision-enabled LLMs

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- [Git LFS](https://git-lfs.github.com/) (required for dataset files)
- Google Gemini API key (or other vision-enabled LLM API)

## Quick Start

### 1. Install Git LFS

This repository uses Git LFS to store large dataset files (images). You must install Git LFS before cloning.

**macOS:**
```bash
brew install git-lfs
```

**Ubuntu/Debian:**
```bash
sudo apt-get install git-lfs
```

**Windows:**
Download and install from [git-lfs.github.com](https://git-lfs.github.com/)

**Initialize Git LFS:**
```bash
git lfs install
```

### 2. Clone the Repository

```bash
git clone https://github.com/gmsh/agentified-captcha-benchmark-demo.git
cd agentified-captcha-benchmark-demo
```

**Verify LFS files were downloaded:**
```bash
# Check if image files are properly downloaded (should show actual file sizes, not small pointer files)
ls -lh assets/opencaptchaworld/data/Dice_Count/dice1.png
```

If you see a very small file size (< 1KB), LFS files weren't downloaded. Run:
```bash
git lfs pull
```

### 3. Install Dependencies

```bash
uv sync
```

### 4. Setup Environment Variables

Copy the sample environment file and add your API key:

```bash
cp sample.env .env
```

Edit `.env` and configure the following:

```bash
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-google-api-key-here
```

**To get a Google Gemini API key:**
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Create a new API key or use an existing one
3. Copy the key and paste it into your `.env` file

**Note:** Keep your `.env` file secure and never commit it to version control.

### 5. Run a Scenario

#### Simple CAPTCHA Scenario

```bash
uv run agentbeats-run scenarios/captcha/scenario.toml
```

Here is the [example output](example_output.txt):

This command will:
- Start the green agent (CAPTCHA judge) on `http://127.0.0.1:9009`
- Start the purple agent (CAPTCHA solver) on `http://127.0.0.1:9019`
- Run the assessment with 10 CAPTCHA samples from the dataset
- Display real-time progress and final results

#### OpenCaptchaWorld Scenario

```bash
uv run agentbeats-run scenarios/opencaptchaworld/scenario.toml
```

This advanced scenario uses the [OpenCaptchaWorld dataset](https://github.com/MetaAgentX/OpenCaptchaWorld) with 20 different interactive puzzle types:

This command will:
- Start the green agent (judge) on `http://127.0.0.1:9010` with an embedded puzzle server
- Start the purple agent (solver) on `http://127.0.0.1:9020`
- Test **463 interactive puzzles** across 20 different types
- Display per-type accuracy and overall metrics

**Puzzle Types:**
OpenCaptchaWorld includes 20 distinct CAPTCHA types, each testing different visual reasoning capabilities:

- **Dice_Count**: Count and sum numbers on dice
- **Geometry_Click**: Click on a specific geometric shape
- **Rotation_Match**: Rotate an object to match a reference orientation
- **Slide_Puzzle**: Drag a component to a target position
- **Unusual_Detection**: Identify unusual items in a grid
- **Image_Recognition**: Select images matching a description
- **Bingo**: Swap positions to create a line of matching images
- **Image_Matching**: Match similar images
- **Patch_Select**: Select grid squares containing specific objects
- **Dart_Count**: Select an image where darts sum to a target number
- **Object_Match**: Match the number of objects to a reference
- **Select_Animal**: Identify a specific animal in a grid
- **Coordinates**: Move an object to specified coordinates
- **Path_Finder**: Navigate to a target position
- **Place_Dot**: Place a dot at a specific location
- **Connect_icon**: Connect matching icons
- **Click_Order**: Click items in a specific sequence
- **Hold_Button**: Hold a button for a specified duration
- **Misleading_Click**: Click in the correct area, avoiding distractions
- **Pick_Area**: Select a specific area in an image

**Note:** The current implementation includes a **pseudo purple agent** with two modes:
- **Ground Truth Mode** (default): Returns correct answers for all puzzles (100% accuracy for debugging)
- **Fixed Mode**: Returns the same answer for all puzzles of each type (~13% accuracy baseline)

This serves as a baseline for testing the infrastructure before implementing real LLM-based solvers.

**Optional flags:**
- `--show-logs`: Display agent outputs during the assessment
- `--serve-only`: Start agents without running the assessment (useful for debugging)

## Datasets

### Simple CAPTCHA Dataset

The benchmark uses a sample of the [Kaggle CAPTCHA v2 Images dataset](https://www.kaggle.com/datasets/fournierp/captcha-version-2-images) located in `assets/kaggle-captcha-v2-images/`.

- **Location**: `assets/kaggle-captcha-v2-images/`
- **Format**: PNG images with CAPTCHA text
- **Labels**: Filenames contain the ground truth text

See `assets/kaggle-captcha-v2-images.md` for more details about the dataset.

### OpenCaptchaWorld Dataset

The advanced benchmark uses the [OpenCaptchaWorld dataset](https://github.com/MetaAgentX/OpenCaptchaWorld), a comprehensive collection of 20 interactive CAPTCHA puzzle types.

- **Location**: `assets/opencaptchaworld/data/`
- **Format**: Images (PNG/JPG) with structured ground truth in JSON files
- **Labels**: `ground_truth.json` in each puzzle type folder
- **Total Puzzles**: 463 across 20 different types
- **Source**: [MetaAgentX/OpenCaptchaWorld](https://github.com/MetaAgentX/OpenCaptchaWorld)

Each puzzle type tests different cognitive capabilities:
- Visual perception and recognition
- Spatial reasoning and geometry
- Pattern matching and logic
- Interactive problem-solving

## Configuration

### Simple CAPTCHA Scenario

You can customize the assessment by editing `scenarios/captcha/scenario.toml`:

```toml
[config]
num_samples = 10                              # Number of CAPTCHAs to test
dataset_path = "assets/kaggle-captcha-v2-images"  # Path to dataset
```

### OpenCaptchaWorld Scenario

You can customize the assessment by editing `scenarios/opencaptchaworld/scenario.toml`:

**Select puzzle types:**
```toml
[config]
# List of puzzle types to test (empty list means test all types)
puzzle_types = []

# Example: Test only specific types
# puzzle_types = ["Dice_Count", "Geometry_Click", "Image_Recognition"]
```

**Switch solver mode:**
```toml
[[participants]]
role = "opencaptcha_solver"
endpoint = "http://127.0.0.1:9020"
# Ground truth mode (100% accuracy):
cmd = "python3 scenarios/opencaptchaworld/opencaptchaworld_solver.py --host 127.0.0.1 --port 9020 --mode ground_truth"
# Fixed mode (~13% accuracy):
# cmd = "python3 scenarios/opencaptchaworld/opencaptchaworld_solver.py --host 127.0.0.1 --port 9020 --mode fixed"
```

**Available puzzle types:**
`Dice_Count`, `Geometry_Click`, `Rotation_Match`, `Slide_Puzzle`, `Unusual_Detection`, `Image_Recognition`, `Bingo`, `Image_Matching`, `Patch_Select`, `Dart_Count`, `Object_Match`, `Select_Animal`, `Coordinates`, `Path_Finder`, `Place_Dot`, `Connect_icon`, `Click_Order`, `Hold_Button`, `Misleading_Click`, `Pick_Area`

## Project Structure

```
agentified-captcha-benchmark/
├── src/agentbeats/              # Core framework
│   ├── green_executor.py        # Base green agent executor
│   ├── models.py                # Pydantic models for evaluation
│   ├── client.py                # A2A messaging utilities
│   ├── client_cli.py            # CLI client
│   └── run_scenario.py          # Scenario orchestration
│
├── scenarios/
│   ├── captcha/                 # Simple CAPTCHA scenario
│   │   ├── captcha_judge.py     # Green agent (judge)
│   │   ├── captcha_solver.py    # Purple agent (solver)
│   │   ├── captcha_judge_common.py  # Shared models
│   │   └── scenario.toml        # Configuration
│   │
│   └── opencaptchaworld/        # OpenCaptchaWorld scenario
│       ├── opencaptchaworld_judge.py         # Green agent with puzzle server
│       ├── opencaptchaworld_solver.py        # Pseudo purple agent
│       ├── opencaptchaworld_judge_common.py  # Shared models
│       ├── extract_ground_truth.py           # Ground truth extraction script
│       ├── pseudo_purple_data/               # Extracted answers for testing
│       └── scenario.toml                     # Configuration
│
├── assets/                      # Datasets and resources
│   ├── kaggle-captcha-v2-images/    # Simple CAPTCHA dataset
│   └── opencaptchaworld/            # OpenCaptchaWorld dataset
│       ├── data/                    # 20 puzzle types with ground truth
│       ├── templates/               # HTML templates for puzzle UI
│       └── static/                  # CSS and JavaScript assets
│
├── README.md                    # This file
├── README.agentbeats.md         # Original Agentbeats tutorial
├── sample.env                   # Environment variable template
└── pyproject.toml               # Project configuration
```

## How It Works

### Simple CAPTCHA Scenario

1. **Assessment Request**: The client sends an assessment request to the green agent with:
   - The solver agent's endpoint
   - Configuration (number of samples, dataset path)

2. **CAPTCHA Distribution**: The green agent:
   - Loads CAPTCHA images from the dataset
   - Sends each image to the purple agent for solving
   - Tracks responses in real-time

3. **Solving**: The purple agent:
   - Receives CAPTCHA images
   - Uses a vision-enabled LLM (e.g., Google Gemini) to analyze the image
   - Returns the predicted text

4. **Evaluation**: The green agent:
   - Compares predictions against ground truth labels
   - Calculates accuracy metrics
   - Generates a detailed evaluation report

5. **Results**: The assessment produces:
   - Real-time task updates showing progress
   - Final accuracy score
   - Detailed per-sample results as artifacts

### OpenCaptchaWorld Scenario

1. **Assessment Request**: The client sends an assessment request to the green agent with:
   - The solver agent's endpoint
   - Configuration (puzzle types to test)

2. **Puzzle Server**: The green agent:
   - Starts an embedded Starlette web server serving interactive puzzles
   - Loads ground truth data for all puzzle types
   - Prepares to evaluate each puzzle type

3. **Puzzle Distribution**: For each puzzle:
   - Green agent constructs a unique URL: `http://127.0.0.1:9010/get_puzzle?type=<type>&id=<id>`
   - Sends the URL to the purple agent via A2A protocol
   - The URL serves an interactive HTML/JavaScript puzzle interface

4. **Solving**: The purple agent:
   - Receives the puzzle URL
   - For a real solver: Would interact with the web page using browser automation
   - For the pseudo agent: Retrieves the pre-extracted ground truth answer
   - Returns a structured JSON response with the answer

5. **Evaluation**: The green agent:
   - Validates answers using type-specific logic (coordinates, indices, patterns, etc.)
   - Tracks per-type metrics (accuracy, solve time)
   - Calculates overall accuracy across all 463 puzzles

6. **Results**: The assessment produces:
   - Per-type accuracy metrics (e.g., "Dice_Count: 100.0% (20/20)")
   - Overall accuracy (e.g., "100.00% (463/463)")
   - Detailed breakdown as artifacts

### Pseudo Purple Agent Modes

The OpenCaptchaWorld scenario includes a pseudo purple agent with two operating modes:

#### Ground Truth Mode (Default)
```bash
--mode ground_truth
```
- **Purpose**: Infrastructure validation and baseline establishment
- **Accuracy**: 100% (463/463 puzzles)
- **How it works**: Pre-extracts correct answers from ground truth JSON files
- **Use cases**: 
  - Verify the judge's evaluation logic is correct
  - Test the A2A communication pipeline
  - Establish a perfect baseline for comparison
  - Debug puzzle-specific issues

#### Fixed Mode
```bash
--mode fixed
```
- **Purpose**: Realistic baseline without ground truth access
- **Accuracy**: ~13% (62/463 puzzles)
- **How it works**: Returns the same valid answer for all puzzles of each type (based on the first puzzle's correct answer)
- **Guarantees**: At least 1 correct answer per puzzle type (all 20 types)
- **Use cases**:
  - Simulate a naive solver that doesn't adapt to puzzle variations
  - Establish a lower-bound baseline for comparison
  - Test solver performance without ground truth dependency
  - Benchmark real solvers against a simple strategy

**Performance breakdown (fixed mode):**
- Best performing types: Path_Finder (50%), Hold_Button (40%), Misleading_Click (40%)
- Moderate performing types: Object_Match (30%), Image_Matching (26%), Connect_icon (20%)
- Challenging types: Most other types (3-17%)

This demonstrates that while some puzzles in a type may share similar solutions, most require puzzle-specific analysis.

## Development

### Running Agents Manually

For debugging, you can start agents manually in separate terminals:

**Simple CAPTCHA Scenario:**
```bash
# Terminal 1: Start green agent
python scenarios/captcha/captcha_judge.py --host 127.0.0.1 --port 9009

# Terminal 2: Start purple agent
python scenarios/captcha/captcha_solver.py --host 127.0.0.1 --port 9019

# Terminal 3: Run client
python -m agentbeats.client_cli scenarios/captcha/scenario.toml
```

**OpenCaptchaWorld Scenario:**
```bash
# Terminal 1: Start green agent (with puzzle server)
python scenarios/opencaptchaworld/opencaptchaworld_judge.py --host 127.0.0.1 --port 9010

# Terminal 2: Start pseudo purple agent
python scenarios/opencaptchaworld/opencaptchaworld_solver.py --host 127.0.0.1 --port 9020 --mode ground_truth

# Terminal 3: Run client
python -m agentbeats.client_cli scenarios/opencaptchaworld/scenario.toml

# Optional: View puzzle server in browser
# Open http://127.0.0.1:9010/get_puzzle?type=Dice_Count&id=dice1.png
```

### Modifying the Solver

**Simple CAPTCHA:**
The solver agent (`scenarios/captcha/captcha_solver.py`) can be modified to:
- Use different LLM providers (OpenAI, Anthropic, etc.)
- Implement custom preprocessing
- Add retry logic or fallback strategies
- Enhance prompting techniques

**OpenCaptchaWorld:**
The pseudo solver (`scenarios/opencaptchaworld/opencaptchaworld_solver.py`) supports two modes:

**Ground Truth Mode** (default):
```bash
python scenarios/opencaptchaworld/opencaptchaworld_solver.py --host 127.0.0.1 --port 9020 --mode ground_truth
```
- Returns correct answers from pre-extracted ground truth data
- Achieves 100% accuracy (463/463 puzzles)
- Useful for validating the infrastructure and judge logic

**Fixed Mode**:
```bash
python scenarios/opencaptchaworld/opencaptchaworld_solver.py --host 127.0.0.1 --port 9020 --mode fixed
```
- Returns the same answer for all puzzles of each type
- Achieves ~13% accuracy (62/463 puzzles)
- Guarantees at least 1 correct answer per puzzle type
- Useful as a baseline for comparing real solver performance

To use fixed mode by default, edit `scenarios/opencaptchaworld/scenario.toml`:
```toml
[[participants]]
role = "opencaptcha_solver"
endpoint = "http://127.0.0.1:9020"
cmd = "python3 scenarios/opencaptchaworld/opencaptchaworld_solver.py --host 127.0.0.1 --port 9020 --mode fixed"
```

The pseudo solver can be replaced with a real solver that:
- Uses browser automation (Playwright, Selenium) to interact with puzzles
- Employs vision-enabled LLMs to analyze puzzle images
- Implements puzzle-specific solving strategies
- Handles different interaction types (clicks, swaps, rotations, etc.)

### Extracting Ground Truth

For OpenCaptchaWorld, ground truth answers are pre-extracted for the pseudo agent:

```bash
# Regenerate ground truth data
python scenarios/opencaptchaworld/extract_ground_truth.py
```

This creates `scenarios/opencaptchaworld/pseudo_purple_data/` with answer files for each puzzle.

### Adding New Scenarios

See `README.agentbeats.md` for detailed instructions on creating new assessment scenarios using the Agentbeats framework.

## Troubleshooting

**Issue**: Git LFS files not downloaded (small placeholder files instead of images)
- **Solution**: Install Git LFS and pull the files:
  ```bash
  git lfs install
  git lfs pull
  ```
- **Verification**: Check file sizes - images should be several KB, not just ~100 bytes
  ```bash
  ls -lh assets/opencaptchaworld/data/Dice_Count/
  ```

**Issue**: `ImportError` or missing dependencies
- **Solution**: Run `uv sync` to install all dependencies

**Issue**: API key errors
- **Solution**: Ensure your `.env` file has a valid `GOOGLE_API_KEY` set

**Issue**: Dataset not found
- **Solution**: 
  - Verify that dataset directories exist: `assets/kaggle-captcha-v2-images/` and `assets/opencaptchaworld/data/`
  - If missing, ensure Git LFS files were downloaded (see above)

**Issue**: Connection errors
- **Solution**: Ensure ports 9009, 9010, 9019, and 9020 are not in use by other applications

**Issue**: OpenCaptchaWorld shows 0% accuracy
- **Solution**: Check if you're using the correct mode. Ground truth mode requires running the extraction script first:
  ```bash
  python scenarios/opencaptchaworld/extract_ground_truth.py
  ```
- **Alternative**: Switch to fixed mode which doesn't require pre-extracted data

**Issue**: Pseudo purple data not found
- **Solution**: Run the extraction script to generate ground truth data:
  ```bash
  python scenarios/opencaptchaworld/extract_ground_truth.py
  ```

## Cost Considerations

- Each CAPTCHA image requires one vision API call to the LLM
- Default configuration tests 10 samples
- Consider using cheaper/free models during development (e.g., Gemini Flash)

## Next Steps

### Simple CAPTCHA Scenario
- **Expand the dataset**: Add more CAPTCHA samples for robust evaluation
- **Advanced CAPTCHAs**: Include more challenging variants (distorted text, noise, etc.)
- **Improve prompting**: Experiment with different prompting strategies for better accuracy

### OpenCaptchaWorld Scenario
- **Real browser-based solver**: Replace the pseudo agent with a real LLM-powered solver using:
  - Browser automation (Playwright/Selenium) for interaction
  - Vision models for puzzle analysis
  - Multi-modal reasoning for complex puzzles
- **Optimize solving strategies**: Develop puzzle-specific solving approaches
- **Benchmark comparison**: 
  - Compare different LLM models' performance across puzzle types
  - Use fixed mode (13% accuracy) as a lower-bound baseline
  - Use ground truth mode (100% accuracy) to validate infrastructure
  - Target: Real solvers should exceed 13% to demonstrate learning capability
- **Human baseline**: Establish human performance metrics for comparison
- **Progressive difficulty**: Identify which puzzle types are easiest/hardest for AI models

### General
- **Deploy to platform**: Publish agents to [agentbeats.org](https://agentbeats.org) for public benchmarking
- **Cost optimization**: Implement efficient caching and batching strategies
- **Continuous evaluation**: Set up automated testing for tracking model improvements

## References

- [A2A Protocol Documentation](https://a2a-protocol.org/latest/)
- [Agentbeats Platform](https://agentbeats.org)
- [Original Agentbeats Tutorial](README.agentbeats.md)
- [OpenCaptchaWorld Dataset](https://github.com/MetaAgentX/OpenCaptchaWorld)
- [Kaggle CAPTCHA v2 Dataset](https://www.kaggle.com/datasets/fournierp/captcha-version-2-images)

## License

MIT License - see LICENSE file for details
