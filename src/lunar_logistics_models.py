class LunarLogisticsModel:
    def payload_maneuverability(self, payload_mass, robot_power_output, terrain_complexity):
        """
        Calculates the maneuverability efficiency of a payload-handling robot.

        Inputs:
        - payload_mass (kg): Mass of the payload.
        - robot_power_output (W): Power output of the robot in watts.
        - terrain_complexity (dimensionless): A factor representing terrain difficulty 
        (0 = flat, 1 = rocky, 2 = inclined, etc.).

        Output:
        - travel_speed (m/s): Estimated travel speed in meters per second.
        """

        # Check if inputs are valid
        if payload_mass <= 0 or robot_power_output <= 0:
            raise ValueError("Payload mass and robot power output must be positive values.")
        if terrain_complexity < 0:
            raise ValueError("Terrain complexity cannot be negative.")

        # Scaling factor to normalize output based on dataset trends
        K = 1.05  # Adjust as needed based on data fit

        # Compute maneuverability as a function of power, mass, and terrain resistance
        travel_speed = (robot_power_output / (payload_mass * (1 + terrain_complexity))) *K

        return travel_speed  # Output in m/s (not clipped)


    def crew_time_requirements(self, payload_complexity, system_automation_level):
        """
        Estimates the required crew time for handling a payload.

        Inputs:
        - payload_complexity (dimensionless): Represents task difficulty (e.g., 1 = simple, 2 = moderate, 3 = complex).
        - system_automation_level (dimensionless): A factor from 0 (fully manual) to 1 (fully autonomous).

        Output:
        - time_with_automation (minutes): Estimated crew time in minutes.
        """

        # Check if inputs are valid
        if payload_complexity < 0:
            raise ValueError("Payload complexity cannot be negative.")
        if not (0 <= system_automation_level <= 1):
            raise ValueError("System automation level must be between 0 and 1.")

        # Optimized parameters based on validation data
        scaling_factor = 15.01  # Adjusted to fit actual data (minutes per complexity unit)
        automation_effect = 10.41  # Exponential effect of automation

        # Calculate time with optimized scaling
        time_with_automation = scaling_factor * payload_complexity * (1 - system_automation_level**automation_effect)

        return max(0, time_with_automation)

    def position_location_accuracy(self, power_usage, environmental_noise, robot_path_variability):
        """
        Determines the positional accuracy of a mobile payload system.

        Inputs:
        - power_usage (W): Power allocated to positional updates.
        - environmental_noise (dimensionless): Level of environmental interference (e.g., signal distortion).
        - robot_path_variability (dimensionless): A factor representing deviations in the robot's planned path.

        Output:
        - accuracy (dimensionless): A normalized accuracy metric (0 to 1), where 1 is perfect accuracy.
        """

        # Check if inputs are valid
        if power_usage <= 0:
            raise ValueError("Power usage must be a positive value.")
        if environmental_noise < 0 or robot_path_variability < 0:
            raise ValueError("Environmental noise and robot path variability cannot be negative.")

        # Tuning parameter to balance power usage against environmental factors
        K = 50  # Adjust as needed for better accuracy

        # Calculate accuracy with improved scaling
        accuracy = power_usage / (power_usage + K * (1 + environmental_noise + robot_path_variability))

        return max(0, min(1, accuracy))


# Export functions for easier direct import
def predict_payload_maneuverability(payload_mass, robot_power_output, terrain_complexity):
    model = LunarLogisticsModel()
    return model.payload_maneuverability(payload_mass, robot_power_output, terrain_complexity)

def predict_crew_time(payload_complexity, system_automation_level):
    model = LunarLogisticsModel()
    return model.crew_time_requirements(payload_complexity, system_automation_level)

def predict_position_accuracy(power_usage, environmental_noise, robot_path_variability):
    model = LunarLogisticsModel()
    return model.position_location_accuracy(power_usage, environmental_noise, robot_path_variability)
