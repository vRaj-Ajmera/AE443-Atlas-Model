import random
import numpy as np

# -------------------------------------------
# 1. Effective Throughput Model (Simple Equation)
# -------------------------------------------
def effective_throughput(arrival_rate, power_availability, sensor_accuracy):
    """
    Calculate the number of items successfully processed per day.
    
    Effective Throughput = Arrival Rate × Power Availability × Sensor Accuracy
    
    :param arrival_rate: (float) items arriving per day
    :param power_availability: (float) fraction of the day with adequate power (0–1)
    :param sensor_accuracy: (float) fraction of items correctly identified (0–1)
    :return: (float) effective throughput in items per day
    """
    return arrival_rate * power_availability * sensor_accuracy

def estimate_mission_risk(power_availability, sensor_accuracy, threshold=0.8):
    """
    Simple risk indicator that flags high-risk scenarios based on the combined 
    operational factor (power_availability × sensor_accuracy).
    
    :param power_availability: (float) fraction of the day with adequate power (0–1)
    :param sensor_accuracy: (float) fraction of items correctly identified (0–1)
    :param threshold: (float) critical threshold below which risk is flagged
    :return: (bool) True if system is high-risk, False otherwise
    """
    operational_factor = power_availability * sensor_accuracy
    return operational_factor < threshold


# -------------------------------------------
# 2. Discrete Event Simulation (DES) for Cargo Flow
# -------------------------------------------
def simulate_cargo_flow(arrival_rate, processing_time, delay_probability, simulation_time=24):
    """
    Simulate cargo flow over a given simulation period (in hours).
    Arrivals are modeled via a Poisson process.
    If a shipment is delayed (based on delay_probability), its processing time doubles.
    
    :param arrival_rate: (float) shipments per day
    :param processing_time: (float) base processing time per shipment (hours)
    :param delay_probability: (float) chance that a shipment faces delay
    :param simulation_time: (float) total simulation time in hours (default 24 hours)
    :return: (int) number of shipments processed
    """
    # Convert daily arrival rate to hourly rate
    shipments_per_hour = arrival_rate / 24.0
    total_shipments = np.random.poisson(shipments_per_hour * simulation_time)
    processed_shipments = 0
    time_elapsed = 0.0

    for _ in range(total_shipments):
        # If delayed, processing time doubles
        actual_processing = processing_time * (2 if random.random() < delay_probability else 1)
        if time_elapsed + actual_processing <= simulation_time:
            processed_shipments += 1
            time_elapsed += actual_processing
        else:
            break
    return processed_shipments


# -------------------------------------------
# 3. Agent-Based Model (ABM) for Rover and Crew Tasks (Simplified)
# -------------------------------------------
def simulate_rover_tasks(num_rovers, rover_speed, task_distance, simulation_time=3600):
    """
    Simulate a simplified model where rovers complete round-trip tasks.
    Each rover's task completion is determined by its speed and the round-trip distance.
    
    :param num_rovers: (int) number of rovers available
    :param rover_speed: (float) rover speed in meters per second
    :param task_distance: (float) round-trip distance per task in meters
    :param simulation_time: (float) simulation time in seconds (default 3600 seconds = 1 hour)
    :return: (int) total number of tasks completed by all rovers
    """
    # Time to complete one task (in seconds)
    time_per_task = task_distance / rover_speed
    tasks_completed = 0
    for _ in range(num_rovers):
        tasks_completed += simulation_time // time_per_task
    return int(tasks_completed)


# -------------------------------------------
# 4. Markov Chain for Power Availability (Simplified)
# -------------------------------------------
def simulate_power_availability(mtbf, mttr, simulation_time=720):
    """
    Simulate power system availability using a simple Markov chain.
    The system transitions between 'operational' and 'repair' states.
    
    :param mtbf: (float) Mean Time Between Failures in hours
    :param mttr: (float) Mean Time To Repair in hours
    :param simulation_time: (float) total simulation time in hours (default 720 hours = 30 days)
    :return: (float) fraction of time the power system is operational
    """
    state = "operational"
    t = 0.0
    operational_time = 0.0

    while t < simulation_time:
        if state == "operational":
            time_until_failure = np.random.exponential(mtbf)
            if t + time_until_failure > simulation_time:
                operational_time += (simulation_time - t)
                break
            operational_time += time_until_failure
            t += time_until_failure
            state = "repair"
        else:  # state == "repair"
            repair_time = np.random.exponential(mttr)
            t += repair_time
            state = "operational"
    return operational_time / simulation_time


# -------------------------------------------
# Example usage for all models:
# -------------------------------------------
if __name__ == "__main__":
    # Effective Throughput Model
    arrival_rate = 5          # items per day
    power_avail = 0.90        # fraction (min: 0.70, nominal: 0.90, max: 0.99)
    sensor_acc = 0.95         # fraction (min: 0.85, nominal: 0.95, max: 0.99)
    throughput = effective_throughput(arrival_rate, power_avail, sensor_acc)
    risk_flag = estimate_mission_risk(power_avail, sensor_acc)
    print("Effective Throughput (items/day):", throughput)
    print("Mission Risk (operational factor < 0.8):", risk_flag)

    # DES for Cargo Flow Simulation
    shipments_processed = simulate_cargo_flow(arrival_rate=5,
                                              processing_time=1.5,   # hours per shipment (min: 0.5, nominal: 1–2, max: 4)
                                              delay_probability=0.10, # (min: 5%, nominal: 10%, max: 20%)
                                              simulation_time=24)     # simulate for 24 hours
    print("Shipments processed in 24 hours (DES):", shipments_processed)

    # Agent-Based Model for Rover Tasks Simulation
    tasks_completed = simulate_rover_tasks(num_rovers=2,
                                           rover_speed=1.0,       # m/s (min: 0.3, nominal: 1, max: 2)
                                           task_distance=100,     # meters round-trip distance
                                           simulation_time=3600)  # 1 hour in seconds
    print("Rover tasks completed in 1 hour (ABM):", tasks_completed)

    # Markov Chain for Power Availability Simulation
    availability_sim = simulate_power_availability(mtbf=100,  # hours (min: 50, nominal: 100, max: 200)
                                                     mttr=1,    # hours (min: 0.5, nominal: 1, max: 3)
                                                     simulation_time=720)  # 720 hours = 30 days
    print("Simulated Power Availability over 30 days:", availability_sim)
