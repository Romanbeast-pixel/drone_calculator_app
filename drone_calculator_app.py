import streamlit as st

def quadcopter_calculator(prop_size_inch, drone_weight_g, thrust_per_motor_g,
                          battery_voltage, battery_capacity_mah,
                          motor_kv, rotor_count):

    prop_size_mm = prop_size_inch * 25.4
    arm_length_mm = (prop_size_mm * 1.1) / 2
    diag_frame_size = arm_length_mm * 2
    center_plate = arm_length_mm * 0.72
    total_diag = diag_frame_size + center_plate

    total_thrust = thrust_per_motor_g * rotor_count
    twr = total_thrust / drone_weight_g

    power_per_motor = motor_kv * battery_voltage * 0.001
    total_power = power_per_motor * rotor_count
    current_draw = total_power / battery_voltage
    battery_capacity_ah = battery_capacity_mah / 1000
    flight_time = (battery_capacity_ah / current_draw) * 60 * 0.8
    esc_rating = round(current_draw / rotor_count * 1.3)

    return {
        "Propeller Size (mm)": round(prop_size_mm, 2),
        "Arm Length (mm)": round(arm_length_mm, 2),
        "Total Diagonal Frame (mm)": round(diag_frame_size, 2),
        "Center Plate Length (mm)": round(center_plate, 2),
        "Total Diagonal Length (mm)": round(total_diag, 2),
        "Total Thrust (g)": total_thrust,
        "Thrust-to-Weight Ratio": round(twr, 2),
        "Power per Motor (W)": round(power_per_motor, 2),
        "Total Power (W)": round(total_power, 2),
        "Total Current Draw (A)": round(current_draw, 2),
        "Estimated Flight Time (min)": round(flight_time, 2),
        "ESC Rating Recommendation (A)": esc_rating
    }

# Streamlit UI
st.title("🛩️ Drone Design Calculator")

prop_size = st.number_input("Propeller Size (inches)", min_value=1.0, value=10.0)
drone_weight = st.number_input("Drone Weight (g)", min_value=100, value=1500)
thrust_per_motor = st.number_input("Thrust per Motor (g)", min_value=100, value=1000)
battery_voltage = st.number_input("Battery Voltage (V)", min_value=3.0, value=14.8)
battery_capacity = st.number_input("Battery Capacity (mAh)", min_value=500, value=5200)
motor_kv = st.number_input("Motor KV Rating", min_value=100, value=1000)
rotor_count = st.selectbox("Number of Rotors", [4, 6, 8], index=0)

if st.button("Calculate"):
    results = quadcopter_calculator(prop_size, drone_weight, thrust_per_motor,
                                    battery_voltage, battery_capacity,
                                    motor_kv, rotor_count)
    st.subheader("✅ Results")
    for key, val in results.items():
        st.write(f"**{key}**: {val}")
