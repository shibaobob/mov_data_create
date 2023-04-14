#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from sensor_msgs.msg import JointState
import copy  # Import the copy module

class JointStateRecorder:
    def __init__(self):
        self.joint_states = []
        self.timestamps = []

        rospy.init_node('joint_state_recorder', anonymous=True)
        rospy.Subscriber("/joint_states", JointState, self.joint_state_callback)

    def joint_state_callback(self, msg):
        self.joint_states.append(np.array(msg.position[:7]))
        # print(self.joint_states)
        self.timestamps.append(msg.header.stamp.to_sec())

    def load_existing_npz(self, filename):
        data = np.load(filename, allow_pickle=True)
        self.timestamps = data['time'].tolist()
        self.joint_states = data['Q'].tolist()

    def save_to_npz(self, filename):
        np.savez_compressed(
            filename,
            time=np.array(self.timestamps, dtype=object),
            Q=np.array(self.joint_states, dtype=object)
        )

def main():
    recorder = JointStateRecorder()
    new_demo_timestamps = []
    new_demo_joint_states = []

    # Collect data for a specific duration
    duration = 10.0
    rospy.loginfo("Recording joint states...")
    rospy.sleep(duration)

    # Copy the recorded data
    new_demo_timestamps = copy.copy(recorder.timestamps)  # Use copy.copy() instead of .copy()
    new_demo_joint_states = copy.copy(recorder.joint_states)  # Use copy.copy() instead of .copy()

    # Load existing .npz file if it exists
    output_filename = 'joint_states_data.npz'
    try:
        recorder.load_existing_npz(output_filename)
        rospy.loginfo("Loaded existing data from %s" % output_filename)
    except FileNotFoundError:
        rospy.loginfo("No existing data found, starting a new recording")
        recorder.timestamps = [new_demo_timestamps]
        recorder.joint_states = [new_demo_joint_states]
    else:
        recorder.timestamps.append(new_demo_timestamps)
        recorder.joint_states.append(new_demo_joint_states)

    # Save recorded data to a .npz file
    rospy.loginfo("Saving data to %s" % output_filename)
    recorder.save_to_npz(output_filename)
    rospy.loginfo("Data saved successfully!")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass