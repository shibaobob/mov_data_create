#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from sensor_msgs.msg import JointState

class JointStateRecorder:
    def __init__(self):
        self.joint_states = []
        self.timestamps = []

        rospy.init_node('joint_state_recorder', anonymous=True)
        rospy.Subscriber("/joint_states", JointState, self.joint_state_callback)

    def joint_state_callback(self, msg):
        self.joint_states.append(np.array(msg.position[:7]).reshape(1, -1))
        # print(self.joint_states)
        self.timestamps.append(msg.header.stamp.to_sec())

    def load_existing_npz(self, filename):
        data = np.load(filename)
        self.timestamps = data['time'].tolist()
        self.joint_states = data['Q'].tolist()

    def save_to_npz(self, filename):
        np.savez_compressed(
            filename,
            time=np.array(self.timestamps),
            Q=np.vstack(self.joint_states)
        )

def main():
    recorder = JointStateRecorder()

    # Load existing .npz file if it exists
    output_filename = 'joint_states_data.npz'
    try:
        recorder.load_existing_npz(output_filename)
        rospy.loginfo("Loaded existing data from %s" % output_filename)
    except FileNotFoundError:
        rospy.loginfo("No existing data found, starting a new recording")

    rospy.loginfo("Recording joint states...")

    # Collect data for a specific duration
    duration = 10.0
    rospy.sleep(duration)

    # Save recorded data to a .npz file
    rospy.loginfo("Saving data to %s" % output_filename)
    recorder.save_to_npz(output_filename)
    rospy.loginfo("Data saved successfully!")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass