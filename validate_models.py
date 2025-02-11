import pandas as pd
import numpy as np
import os
from src.lunar_logistics_models import predict_payload_maneuverability, predict_crew_time, predict_position_accuracy

def compute_error(predicted, actual):
    """Calculate percentage error between predicted and actual values."""
    return abs(predicted - actual) / actual * 100 if actual != 0 else np.nan

def validate_model(validation_file, prediction_function, input_columns, output_column, output_directory="val/"):
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Load the validation data
    df = pd.read_csv(validation_file)
    errors = []

    # Run predictions and compute errors
    for _, row in df.iterrows():
        inputs = [row[col] for col in input_columns]
        predicted = prediction_function(*inputs)
        actual = row[output_column]
        error = compute_error(predicted, actual)
        errors.append(error)

    # Add errors to DataFrame
    df['Predicted'] = [prediction_function(*[row[col] for col in input_columns]) for _, row in df.iterrows()]
    df['Error (%)'] = errors

    # Construct output file path in the "val" directory
    output_file = os.path.join(output_directory, os.path.basename(validation_file))
    
    # Save validation results
    df.to_csv(output_file, index=False)
    print(f"Validation results saved to {output_file}")

    # Summary statistics
    mean_error = np.nanmean(errors)
    print(f"Mean Error for {validation_file}: {mean_error:.2f}%\n")
    return mean_error

def main():
    # Define validation files and corresponding models
    validation_tasks = [
        ("input/payload_maneuverability.csv", predict_payload_maneuverability, ["payload_mass", "robot_power", "terrain_complexity"], "travel_speed"),
        ("input/crew_time.csv", predict_crew_time, ["task_complexity", "automation_level"], "crew_time_minutes"),
        ("input/position_accuracy.csv", predict_position_accuracy, ["power_usage", "environmental_noise", "path_variability"], "positional_error")
    ]

    # Validate each model
    for file_path, model_func, input_cols, output_col in validation_tasks:
        validate_model(file_path, model_func, input_cols, output_col)

if __name__ == "__main__":
    main()
