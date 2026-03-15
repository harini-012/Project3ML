import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import time
import random

# Load trained model
model = pickle.load(open("car_model.pkl","rb"))

st.title("🚗 Self Driving Car Route Simulation")

# Sidebar settings
st.sidebar.header("Simulation Settings")

start_position = st.sidebar.slider("Start Position",0,50,0)
destination = st.sidebar.slider("Destination",40,120,90)
speed = st.sidebar.slider("Speed",20,60,30)

if start_position >= destination:
    st.sidebar.error("Destination must be greater than start position")

start_simulation = st.sidebar.button("Start Simulation")

# Route generation
route = list(range(start_position, destination+1))

# Car starts in center lane
car_lane = 1
car_position = start_position

# Generate obstacles
obstacles = {}
for i in range(8):
    pos = random.randint(start_position+5,destination-10)
    lane = random.randint(0,2)
    obstacles[pos] = lane

# Traffic signal
signal_position = random.randint(start_position+20,destination-30)
signal_cycle = ["GREEN","YELLOW","RED"]

# Toll booth
toll_position = random.randint(signal_position+10,destination-5)

plot_area = st.empty()
status = st.empty()

if start_simulation:

    while car_position < destination:

        signal_state = random.choice(signal_cycle)

        obstacle_front = False

        # Detect obstacle
        for pos,lane in obstacles.items():
            if pos == car_position + 1 and lane == car_lane:
                obstacle_front = True

        # Sensor values
        left_sensor = 80
        right_sensor = 80
        front_sensor = 90

        if obstacle_front:
            front_sensor = 10

        input_data = np.array([[left_sensor,right_sensor,front_sensor,speed]])

        action = model.predict(input_data)[0]

        # Stop before signal
        stop_distance = 2

# Stop before red signal
        if car_position >= signal_position - stop_distance and car_position < signal_position:
            if signal_state == "RED":
                status.warning("🚦 Red Signal - Car Stopped")

                while signal_state == "RED":

                    fig,ax = plt.subplots(figsize=(18,5))

                    ax.set_facecolor("black")

                    for lane_line in range(3):
                        ax.axhline(lane_line,color="white",linestyle="--")

                    ax.scatter(car_position,car_lane,color="blue",s=900)

                    ax.scatter(signal_position,2,color="red",s=600,marker="s")

                    ax.set_xlim(start_position,destination)
                    ax.set_ylim(-1,3)

                    plot_area.pyplot(fig)

                    time.sleep(1)

                    # update signal cycle while waiting
                    if signal_state == "RED":
                        signal_state = "GREEN"

                status.success("🟢 Signal Green - Moving")

        # Toll stop
        if car_position == toll_position:

            status.warning("🏦 Toll Booth - Paying Toll")

            time.sleep(2)

        # Lane change logic
        if obstacle_front:

            if car_lane > 0:
                car_lane -= 1

            elif car_lane < 2:
                car_lane += 1

        else:

            if action == "left" and car_lane > 0:
                car_lane -= 1

            elif action == "right" and car_lane < 2:
                car_lane += 1

        # Move along route
        if car_position < destination:
            car_position = route[route.index(car_position)+1]

        # Draw road
        fig,ax = plt.subplots(figsize=(18,5))

        ax.set_facecolor("black")

        # Lane lines
        for lane_line in range(3):
            ax.axhline(lane_line,color="white",linestyle="--")

        # Route path
        ax.plot(route,[1]*len(route),linestyle="dotted",color="white")

        # Obstacles
        for pos,lane in obstacles.items():
            ax.scatter(pos,lane,color="orange",s=500,marker="^")

        # Traffic signal
        if signal_state == "GREEN":
            ax.scatter(signal_position,2,color="lime",s=600,marker="s")
        elif signal_state == "YELLOW":
            ax.scatter(signal_position,2,color="yellow",s=600,marker="s")
        else:
            ax.scatter(signal_position,2,color="red",s=600,marker="s")

        # Toll booth
        ax.scatter(toll_position,2,color="purple",s=600,marker="D")

        # Car
        ax.scatter(car_position,car_lane,color="blue",s=900)

        ax.set_xlim(start_position,destination)
        ax.set_ylim(-1,3)

        ax.set_xlabel("Road Distance")
        ax.set_ylabel("Lane")

        # Legend
        car_legend = plt.Line2D([0],[0],marker='o',color='w',markerfacecolor='blue',markersize=12,label='Car')
        obs_legend = plt.Line2D([0],[0],marker='^',color='w',markerfacecolor='orange',markersize=12,label='Obstacle')
        sig_legend = plt.Line2D([0],[0],marker='s',color='w',markerfacecolor='red',markersize=12,label='Traffic Signal')
        toll_legend = plt.Line2D([0],[0],marker='D',color='w',markerfacecolor='purple',markersize=12,label='Toll Booth')
        route_legend = plt.Line2D([0],[0],color='white',linestyle="dotted",label='Route')

        ax.legend(handles=[car_legend,obs_legend,sig_legend,toll_legend,route_legend],
                  bbox_to_anchor=(1.02,1),
                  loc="upper left")

        plot_area.pyplot(fig)

        status.info(f"🚗 Speed: {speed} km/h | Lane: {car_lane}")

        time.sleep(0.4)

    st.success("🏁 Car reached destination!")