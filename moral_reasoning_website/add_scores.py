#!/usr/bin/env python3
"""
Script to add scores to each model's thinking_trace and model_resp in comparison_data.json
Uses the scoring logic from rubric_scoring.py
"""

import json
from pathlib import Path


def calculate_score_for_a_task(criteria):
    """
    Calculate score based on rubric criteria.
    Imported from rubric_scoring.py
    """
    max_score = 0
    achieved_score = 0

    for criterion in criteria:
        weight = criterion.get("weight")

        # our way 
        max_score += abs(weight)
        # only award credit in these cases
        if "yes" in criterion["judgement"].strip().lower() and weight > 0:
            achieved_score += weight
        elif "no" in criterion["judgement"].strip().lower() and weight < 0:
            achieved_score -= weight

    return max(min(100 * achieved_score / max_score, 100), 0)


def add_scores_to_comparison_data(json_file_path):
    """
    Read comparison_data.json, add scores to each model's thinking_trace and model_resp,
    and save the updated data back to the file.
    """
    # Read the JSON file
    print(f"Reading {json_file_path}...")
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_tasks = len(data)
    total_models = 0
    scores_added = 0
    
    # Process each task
    for task_idx, task in enumerate(data):
        print(f"\nProcessing task {task_idx + 1}/{total_tasks} (ID: {task['metadata']['task_id']})")
        
        # Process each model in the task
        for model in task.get('models'):
            total_models += 1
            model_name = model.get('model_name')
            print(f"  Processing model: {model_name}")
            
            # Add score to thinking_trace if it exists and has rubrics
            if 'thinking_trace' in model and 'rubrics' in model['thinking_trace']:
                rubrics = model['thinking_trace']['rubrics']
                score = calculate_score_for_a_task(rubrics)
                model['thinking_trace']['score'] = round(score, 2)
                scores_added += 1
                print(f"    Added thinking_trace score: {score:.2f}")
            
            # Add score to model_resp if it exists and has rubrics
            if 'model_resp' in model and 'rubrics' in model['model_resp']:
                rubrics = model['model_resp']['rubrics']
                score = calculate_score_for_a_task(rubrics)
                model['model_resp']['score'] = round(score, 2)
                scores_added += 1
                print(f"    Added model_resp score: {score:.2f}")
    
    # Save the updated data back to the file
    print(f"\n\nSaving updated data to {json_file_path}...")
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total tasks processed: {total_tasks}")
    print(f"  Total models processed: {total_models}")
    print(f"  Total scores added: {scores_added}")
    print(f"{'='*60}")
    print(f"\nSuccessfully updated {json_file_path}")


if __name__ == "__main__":
    # Path to the comparison_data.json file
    json_file = Path(__file__).parent / "comparison_data.json"
    
    # Add scores to the data
    add_scores_to_comparison_data(json_file)

