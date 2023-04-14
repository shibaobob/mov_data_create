#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import time

# Version 1
# ~~~~~~~~~~~~~~~~~~~~~
# class JointRecorder:
#     def __init__(self):
#         self.joint_states = []
#         self.timestamps = []

#     def record_joint_state(self, joint_state):
#         self.joint_states.append(joint_state)
#         self.timestamps.append(time.time())

#     def save_to_npz(self, filename):
#         np.savez_compressed(
#             filename,
#             time1=np.array(self.timestamps),
#             Q1=np.vstack(self.joint_states)
#         )

# # Create an instance of JointRecorder
# recorder = JointRecorder()

# # Simulate recording joint states over time
# for i in range(10):
#     joint_state = np.random.rand(6)
#     recorder.record_joint_state(joint_state)
#     time.sleep(1)

# # Save the recorded joint states to a compressed NPZ file
# recorder.save_to_npz("test.npz")



# Version 2
# ~~~~~~~~~~~~~~~
# class JointRecorder:
#     def __init__(self):
#         self.joint_states = []
#         self.timestamps = []

#     def record_joint_state(self, joint_state):
#         self.joint_states.append(joint_state)
#         self.timestamps.append(time.time())

#     def save_to_npz(self, filename):
#         np.savez_compressed(
#             filename,
#             time2=np.array(self.timestamps),
#             Q2=np.vstack(self.joint_states)[:10] # make sure Q is at most (10, x)
#         )

# # Create an instance of JointRecorder
# recorder = JointRecorder()

# # Simulate recording joint states over time
# for i in range(10):
#     joint_state = np.random.rand(6)
#     recorder.record_joint_state(joint_state)
#     time.sleep(1)

# # Save the recorded joint states to a compressed NPZ file
# recorder.save_to_npz("test.npz")


# Load the saved joint states from the NPZ file
with open('test.npz','r') as f:
    data = np.load(f)
    time = data["time2"][:10]
    Q = data["Q2"][:10]

print "time shape:", time.shape # should output (10,)
print "Q shape:", Q.shape # should output (10, 6)

