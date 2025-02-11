class LunarLogisticsModel:
    def payload_maneuverability(self, payload_mass, robot_power_output, terrain_complexity):
        # Check if inputs are valid
        if payload_mass <= 0 or robot_power_output <= 0:
            raise ValueError("Payload mass and robot power output must be positive values.")
        if terrain_complexity < 0:
            raise ValueError("Terrain complexity cannot be negative.")
        
        # Calculate maneuverability
        efficiency = (robot_power_output / (payload_mass * (1 + terrain_complexity)))
        return max(0, min(1, efficiency))

    def crew_time_requirements(self, payload_complexity, system_automation_level):
        # Check if inputs are valid
        if payload_complexity < 0:
            raise ValueError("Payload complexity cannot be negative.")
        if not (0 <= system_automation_level <= 1):
            raise ValueError("System automation level must be between 0 and 1.")
        
        # Calculate time with automation
        base_time = payload_complexity * 10
        time_with_automation = base_time * (1 - system_automation_level)
        return max(0, time_with_automation)

    def position_location_accuracy(self, power_usage, environmental_noise, robot_path_variability):
        # Check if inputs are valid
        if power_usage <= 0:
            raise ValueError("Power usage must be a positive value.")
        if environmental_noise < 0 or robot_path_variability < 0:
            raise ValueError("Environmental noise and robot path variability cannot be negative.")
        
        # Calculate accuracy
        accuracy = power_usage / (1 + environmental_noise + robot_path_variability)
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
