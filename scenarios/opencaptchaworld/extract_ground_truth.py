#!/usr/bin/env python3
"""
Extract ground truth data from OpenCaptchaWorld dataset and prepare it
for the pseudo purple agent to use.
"""

import json
import os
from pathlib import Path
from datetime import datetime


def get_answer_field(puzzle_type: str, puzzle_data: dict):
    """
    Extract the appropriate answer field based on puzzle type.
    Different puzzle types store answers in different fields.
    
    IMPORTANT: Check special cases FIRST before the generic 'answer' field!
    """
    # Special cases - CHECK THESE FIRST!
    if puzzle_type == 'Dice_Count' and 'sum' in puzzle_data:
        return puzzle_data['sum']
    
    elif puzzle_type == 'Hold_Button' and 'hold_time' in puzzle_data:
        return puzzle_data['hold_time']
    
    elif puzzle_type == 'Geometry_Click' and 'answer' in puzzle_data:
        # For Geometry_Click, return the center of the clickable area
        answer = puzzle_data['answer']
        if isinstance(answer, dict) and 'area' in answer:
            area = answer['area']
            # Calculate center point
            center_x = (area[0][0] + area[1][0]) // 2
            center_y = (area[0][1] + area[1][1]) // 2
            return [center_x, center_y]
        return answer
    
    elif puzzle_type == 'Pick_Area' and 'answer' in puzzle_data:
        # Similar to Geometry_Click - return center of the area
        answer = puzzle_data['answer']
        if isinstance(answer, dict) and 'area' in answer:
            area = answer['area']
            # Calculate center point
            center_x = (area[0][0] + area[1][0]) // 2
            center_y = (area[0][1] + area[1][1]) // 2
            return [center_x, center_y]
        return answer
    
    elif puzzle_type == 'Rotation_Match' and 'correct_angle' in puzzle_data:
        return puzzle_data['correct_angle']
    
    elif puzzle_type == 'Slide_Puzzle' and 'target_position' in puzzle_data:
        return puzzle_data['target_position']
    
    elif puzzle_type == 'Image_Recognition' and 'correct_selections' in puzzle_data:
        return puzzle_data['correct_selections']
    
    elif puzzle_type == 'Image_Matching':
        # For Image_Matching, return the index (as expected by check_answer)
        if 'correct_option_index' in puzzle_data:
            return puzzle_data['correct_option_index']
        # Fallback to answer if index not present
        elif 'answer' in puzzle_data:
            return puzzle_data['answer']
    
    elif puzzle_type == 'Dart_Count' and 'correct_option_index' in puzzle_data:
        return puzzle_data['correct_option_index']
    
    elif puzzle_type == 'Object_Match' and 'correct_option_index' in puzzle_data:
        return puzzle_data['correct_option_index']
    
    elif puzzle_type == 'Coordinates' and 'correct_option_index' in puzzle_data:
        return puzzle_data['correct_option_index']
    
    elif puzzle_type == 'Path_Finder' and 'correct_option' in puzzle_data:
        return puzzle_data['correct_option']
    
    elif puzzle_type == 'Connect_icon' and 'correct_option' in puzzle_data:
        return puzzle_data['correct_option']
    
    elif puzzle_type == 'Patch_Select' and 'correct_patches' in puzzle_data:
        return puzzle_data['correct_patches']
    
    elif puzzle_type == 'Select_Animal' and 'correct_patches' in puzzle_data:
        return puzzle_data['correct_patches']
    
    elif puzzle_type == 'Place_Dot' and 'target_position' in puzzle_data:
        return puzzle_data['target_position']
    
    elif puzzle_type == 'Bingo' and 'answer' in puzzle_data:
        # For Bingo, return the FIRST valid swap pair from the list
        answer = puzzle_data['answer']
        if isinstance(answer, list) and len(answer) > 0:
            # Return the first swap pair
            return answer[0]
        return answer
    
    elif puzzle_type == 'Click_Order' and 'answer' in puzzle_data:
        return puzzle_data['answer']
    
    elif puzzle_type == 'Misleading_Click':
        # For misleading click, calculate coordinates outside the avoid area
        avoid_area = puzzle_data.get('avoid_area', {})
        if avoid_area:
            # Get avoid area bounds
            avoid_x = avoid_area.get('x', 0)
            avoid_y = avoid_area.get('y', 0)
            avoid_width = avoid_area.get('width', 0)
            avoid_height = avoid_area.get('height', 0)
            
            # Image bounds (typically 500x500)
            img_width = 500
            img_height = 500
            
            # Helper function to check if a point is outside the avoid area
            def is_safe(x, y):
                return not (avoid_x <= x <= avoid_x + avoid_width and 
                           avoid_y <= y <= avoid_y + avoid_height)
            
            # Try multiple candidate positions (in order of preference)
            candidates = [
                # To the right of avoid area
                (avoid_x + avoid_width + 30, avoid_y + avoid_height // 2),
                # To the left of avoid area
                (max(30, avoid_x - 30), avoid_y + avoid_height // 2),
                # Below the avoid area
                (avoid_x + avoid_width // 2, avoid_y + avoid_height + 30),
                # Above the avoid area
                (avoid_x + avoid_width // 2, max(30, avoid_y - 30)),
                # Top-left corner
                (30, 30),
                # Top-right corner
                (img_width - 30, 30),
                # Bottom-left corner
                (30, img_height - 30),
                # Bottom-right corner
                (img_width - 30, img_height - 30),
                # Center (last resort)
                (img_width // 2, img_height // 2),
            ]
            
            # Find the first safe candidate that's within bounds
            for x, y in candidates:
                if (0 <= x < img_width and 0 <= y < img_height and is_safe(x, y)):
                    return [x, y]
            
            # Fallback (should never reach here)
            return [30, 30]
        # If no avoid area, click center
        return [250, 250]
    
    # Generic case - most puzzle types use 'answer' field
    if 'answer' in puzzle_data:
        return puzzle_data['answer']
    
    # Default fallback
    return None


def extract_ground_truth():
    """Extract ground truth from all puzzle types."""
    
    # Base paths
    data_dir = Path(__file__).parent.parent.parent / 'assets' / 'opencaptchaworld' / 'data'
    output_dir = Path(__file__).parent / 'pseudo_purple_data'
    
    if not data_dir.exists():
        print(f"Error: Data directory not found: {data_dir}")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each puzzle type
    puzzle_types = [d for d in data_dir.iterdir() if d.is_dir()]
    
    total_puzzles = 0
    
    for puzzle_type_dir in puzzle_types:
        puzzle_type = puzzle_type_dir.name
        ground_truth_file = puzzle_type_dir / 'ground_truth.json'
        
        if not ground_truth_file.exists():
            print(f"Warning: No ground_truth.json found for {puzzle_type}")
            continue
        
        # Load ground truth
        with open(ground_truth_file, 'r') as f:
            ground_truth = json.load(f)
        
        # Create output directory for this type
        type_output_dir = output_dir / puzzle_type
        type_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract answer for each puzzle
        for puzzle_id, puzzle_data in ground_truth.items():
            answer = get_answer_field(puzzle_type, puzzle_data)
            
            # Create result in the format expected by the solver
            result = {
                "puzzle_type": puzzle_type,
                "puzzle_id": puzzle_id,
                "answer": answer,
                "elapsed_time": 0.5,  # Dummy time
                "timestamp": datetime.now().isoformat()
            }
            
            # Save to file
            output_file = type_output_dir / f"{puzzle_id}.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            total_puzzles += 1
        
        print(f"Processed {len(ground_truth)} puzzles for {puzzle_type}")
    
    print(f"\nTotal: Extracted {total_puzzles} puzzle ground truths")
    print(f"Output directory: {output_dir}")


if __name__ == '__main__':
    extract_ground_truth()

