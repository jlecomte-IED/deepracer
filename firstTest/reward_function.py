import math


def reward_function(params):
    """
    Example of penalize steering, which helps mitigate zig-zag behaviors
    """

    # Read input parameters
    distance_from_center = params["distance_from_center"]
    track_width = params["track_width"]
    abs_steering = abs(params["steering_angle"])  # Only need the absolute steering angle
    waypoints = params["waypoints"]
    closest_waypoints = params["closest_waypoints"]
    heading = params["heading"]
    x = params["x"]
    y = params["y"]

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    marker_4 = 0.75 * track_width
    marker_5 = 0.95 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.9
    elif distance_from_center <= marker_3:
        reward = 0.8
    elif distance_from_center <= marker_4:
        reward = 0.5
    elif distance_from_center <= marker_5:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 25

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    rabbit = [0, 0]
    pointing = [0, 0]

    # Reward when yaw (car_orientation) is pointed to the next waypoint IN FRONT.

    # Find nearest waypoint coordinates
    rabbit = waypoints[closest_waypoints[1]]

    radius = math.hypot(x - rabbit[0], y - rabbit[1])

    pointing[0] = x + (radius * math.cos(heading))
    pointing[1] = y + (radius * math.sin(heading))

    vector_delta = math.hypot(pointing[0] - rabbit[0], pointing[1] - rabbit[1])

    # Max distance for pointing away will be the radius * 2
    # Min distance means we are pointing directly at the next waypoint
    # We can setup a reward that is a ratio to this max.

    if vector_delta == 0:
        reward *= 1
    else:
        reward *= 1 - (vector_delta / (radius * 2))

    return float(reward)
