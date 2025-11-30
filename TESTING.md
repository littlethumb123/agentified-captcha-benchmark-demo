# Test Mode for OpenCaptchaWorld

This document explains how to use the interactive "test mode" for the OpenCaptchaWorld scenario. This mode allows you to run specific puzzles, view them in a browser, and save their data representation to a file.

## How to Use Test Mode

To run the test mode, use the following command from the root of the project:

```bash
uv run agentbeats-run scenarios/opencaptchaworld/scenario.toml --test "PUZZLE_LIST"
```

### `PUZZLE_LIST` Argument

Replace `PUZZLE_LIST` with a comma-separated list of puzzles you want to test. Each puzzle is identified by its `type` and `id` in the format `type:id`.

**Example:**

```bash
uv run agentbeats-run scenarios/opencaptchaworld/scenario.toml --test "Dice_Count:dice1.png,Geometry_Click:xiaodun_000001.png"
```

This command will start a test session with two puzzles: `dice1.png` from the `Dice_Count` category and `xiaodun_000001.png` from the `Geometry_Click` category.

## What Happens

When you run the command:

1.  The necessary agent servers for the `opencaptchaworld` scenario will be started.
2.  A new tab will automatically open in your default web browser, pointing to the test mode URL.
3.  The first puzzle in your list will be displayed.

## Interacting with Puzzles

On the puzzle page, you will see a "Print & Next" button. When you click this button:

1.  The JSON data for the current puzzle is saved to the output directory.
2.  The next puzzle in your list is loaded and displayed.

This process continues until all puzzles in the list have been shown.

## Output

The puzzle data is saved in the `scenarios/opencaptchaworld/output/` directory. The files are organized into subdirectories based on the puzzle type.

For example, the output for the `Dice_Count:dice1.png` puzzle will be saved at:

`scenarios/opencaptchaworld/output/Dice_Count/dice1.png.json`
