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
    progress = params["progress"]
    steering_angle = params["steering_angle"]
    heading = heading + steering_angle
    is_offtrack = params["is_offtrack"]
    is_reversed = params["is_reversed"]
    speed = params["speed"]

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
        reward = 8.0
    elif distance_from_center <= marker_2:
        reward = 7.0
    elif distance_from_center <= marker_3:
        reward = 5.5
    elif distance_from_center <= marker_4:
        reward = 1.8
    elif distance_from_center <= marker_5:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    if is_offtrack or is_reversed:
        return 1e-3
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 25

    # Alter the array to make sure the first point is the one just behind the car
    # Then we can identify and target the 9th
    # Compare target point and current x-y coordinates to identify the direction
    waypoints = waypoints[closest_waypoints[0] :] + waypoints[: closest_waypoints[0]]
    if speed > 2.0:
        next_point = waypoints[9]
    elif speed > 0.9:
        next_point = waypoints[5]
    elif speed > 0.4:
        next_point = waypoints[3]
    else:
        next_point = waypoints[2]

    prev_point = (x, y)

    # Now identify the direction that the car should be heading
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    track_direction = math.degrees(track_direction)

    # Get the difference between the ideal and actual.
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Reward or Penalize based on the difference
    if direction_diff > 30:
        reward += 1e-3 / params["speed"]
    elif direction_diff > 15:
        reward += 0.05 / params["speed"]
    elif direction_diff > 7:
        reward += 0.12
    elif direction_diff > 3:
        reward += 0.5 * params["speed"]
    else:
        reward += 1 * params["speed"]

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8

    if progress == 100:
        reward += 50

    return float(reward)
