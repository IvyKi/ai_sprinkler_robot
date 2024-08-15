import time

ANGLE = {1: 0, 2: 90, 3: 180, 4: 270}  # Mapping of sensor numbers to motor angles


def motor_angle(sensor_list):
    current_position = 0

    for sensor_number in sensor_list:
        target_angle = ANGLE[sensor_number]
        movement = target_angle - current_position
        print(f"Moving motor from {current_position}° to {target_angle}° ({movement}° movement)")

        time.sleep(abs(movement) / 90)
        current_position = target_angle
