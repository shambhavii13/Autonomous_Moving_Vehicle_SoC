from importlib.resources import path
from gym_driving.assets.car import *
from gym_driving.envs.environment import *
from gym_driving.envs.driving_env import *
from gym_driving.assets.terrain import *

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import time
import pygame, sys
from pygame.locals import *
import random
import math
import argparse

# Do NOT change these values
TIMESTEPS = 1000
FPS = 30
NUM_EPISODES = 10

class Task1():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()
        self.target = np.array([350, 0])

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED
        """

        # Replace with your implementation to determine actions to be taken
        x, y, vel, heading = state[0], state[1], state[2], state[3]

        angle = math.atan2(self.target[1] - y, self.target[0] - x) * 180/math.pi
        if heading > 180:
            heading -= 360

        # print(angle, heading)
        
        done = False
        if abs(angle - heading) < 6:
            done = True

        if not done:
            action_acc = 1
            if angle - heading < 0:
                action_steer = 0
            else:
                action_steer = 2
        else:
            action_steer = 1
            action_acc = 4

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task1(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
    
        ######### Do NOT modify these lines ##########
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        simulator = DrivingEnv('T1', render_mode=render_mode, config_filepath=config_filepath)

        time.sleep(3)
        ##############################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):
        
            ######### Do NOT modify these lines ##########
            
            # To keep track of the number of timesteps per epoch
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset()
            
            # Variable representing if you have reached the road
            road_status = False
            ##############################################

            # The following code is a basic example of the usage of the simulator
            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            # Writing the output at each episode to STDOUT
            print(str(road_status) + ' ' + str(cur_time))

class Task2():

    def __init__(self):
        """
        Can modify to include variables as required
        """

        super().__init__()
        self.target = np.array([350, 0])
        self.centers = 0
        self.cutoff = 150

    def next_action(self, state):
        """
        Input: The current state
        Output: Action to be taken
        TO BE FILLED

        You can modify the function to take in extra arguments and return extra quantities apart from the ones specified if required
        """

        # Replace with your implementation to determine actions to be taken
        x, y, vel, heading = state[0], state[1], state[2], state[3]

        angle = math.atan2(self.target[1] - y, self.target[0] - x) * 180/math.pi
        if heading > 180:
            heading -= 360

        angles = np.arctan2(self.centers[:,1] - y, self.centers[:,0] - x) * 180/math.pi
        # print(angles - heading)
        
        done = False
        if abs(angle - heading) < 6:
            done = True

        done2 = abs(angles - angle) < 70
        done3 = any(done2)

        ind = -1
        old_ind = -1
        min_dist = 100000

        if done3:
            if done2[3]:
                ind = 3 
                dist = abs(y - self.centers[ind][1]) + abs(x - self.centers[ind][0]) 
                if dist < min_dist:
                    min_dist = dist
                    old_ind = ind    
                ind = old_ind
            if done2[2]:
                ind = 2
                dist = abs(y - self.centers[ind][1]) + abs(x - self.centers[ind][0]) 
                if dist < min_dist:
                    min_dist = dist
                    old_ind = ind    
                ind = old_ind  
            if done2[1]:
                ind = 1
                dist = abs(y - self.centers[ind][1]) + abs(x - self.centers[ind][0]) 
                if dist < min_dist:
                    min_dist = dist
                    old_ind = ind    
                ind = old_ind
            if done2[0]:
                ind = 0
                dist = abs(y - self.centers[ind][1]) + abs(x - self.centers[ind][0]) 
                if dist < min_dist:
                    min_dist = dist
                    old_ind = ind   
                ind = old_ind

        dist = abs(y - self.centers[ind][1]) + abs(x - self.centers[ind][0]) 

        if done3 and dist < self.cutoff:
            self.cutoff = 170
            angle = angles[ind]
            if abs(heading - angle) < 90:
                if heading - angle < 0:
                    action_steer = 0
                else:
                    action_steer = 2

                action_acc = 0

            else:
                action_steer = 1
                if vel < 10:
                    action_acc = 3
                else:
                    action_acc = 1
        
        else:
            self.cutoff = 150

            if not done:
                action_acc = 0
                if angle - heading < 0:
                    action_steer = 0
                else:
                    action_steer = 2
            else:
                action_steer = 1
                if vel < 10:
                    action_acc = 3
                else:
                    action_acc = 1

        action = np.array([action_steer, action_acc])  

        return action

    def controller_task2(self, config_filepath=None, render_mode=False):
        """
        This is the main controller function. You can modify it as required except for the parts specifically not to be modified.
        Additionally, you can define helper functions within the class if needed for your logic.
        """
        
        ################ Do NOT modify these lines ################
        pygame.init()
        fpsClock = pygame.time.Clock()

        if config_filepath is None:
            config_filepath = '../configs/config.json'

        time.sleep(3)
        ###########################################################

        # e is the number of the current episode, running it for 10 episodes
        for e in range(NUM_EPISODES):

            ################ Setting up the environment, do NOT modify these lines ################
            # To randomly initialize centers of the traps within a determined range
            ran_cen_1x = random.randint(120, 230)
            ran_cen_1y = random.randint(120, 230)
            ran_cen_1 = [ran_cen_1x, ran_cen_1y]

            ran_cen_2x = random.randint(120, 230)
            ran_cen_2y = random.randint(-230, -120)
            ran_cen_2 = [ran_cen_2x, ran_cen_2y]

            ran_cen_3x = random.randint(-230, -120)
            ran_cen_3y = random.randint(120, 230)
            ran_cen_3 = [ran_cen_3x, ran_cen_3y]

            ran_cen_4x = random.randint(-230, -120)
            ran_cen_4y = random.randint(-230, -120)
            ran_cen_4 = [ran_cen_4x, ran_cen_4y]

            ran_cen_list = [ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4]            
            eligible_list = []

            # To randomly initialize the car within a determined range
            for x in range(-300, 300):
                for y in range(-300, 300):

                    if x >= (ran_cen_1x - 110) and x <= (ran_cen_1x + 110) and y >= (ran_cen_1y - 110) and y <= (ran_cen_1y + 110):
                        continue

                    if x >= (ran_cen_2x - 110) and x <= (ran_cen_2x + 110) and y >= (ran_cen_2y - 110) and y <= (ran_cen_2y + 110):
                        continue

                    if x >= (ran_cen_3x - 110) and x <= (ran_cen_3x + 110) and y >= (ran_cen_3y - 110) and y <= (ran_cen_3y + 110):
                        continue

                    if x >= (ran_cen_4x - 110) and x <= (ran_cen_4x + 110) and y >= (ran_cen_4y - 110) and y <= (ran_cen_4y + 110):
                        continue

                    eligible_list.append((x,y))

            simulator = DrivingEnv('T2', eligible_list, render_mode=render_mode, config_filepath=config_filepath, ran_cen_list=ran_cen_list)
        
            # To keep track of the number of timesteps per episode
            cur_time = 0

            # To reset the simulator at the beginning of each episode
            state = simulator._reset(eligible_list=eligible_list)
            ###########################################################

            # The following code is a basic example of the usage of the simulator
            road_status = False

            centers = np.array([ran_cen_1, ran_cen_2, ran_cen_3, ran_cen_4])
            self.centers = centers

            for t in range(TIMESTEPS):
        
                # Checks for quit
                if render_mode:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                action = self.next_action(state)
                state, reward, terminate, reached_road, info_dict = simulator._step(action)
                fpsClock.tick(FPS)

                cur_time += 1

                if terminate:
                    road_status = reached_road
                    break

            print(str(road_status) + ' ' + str(cur_time))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="config filepath", default=None)
    parser.add_argument("-t", "--task", help="task number", choices=['T1', 'T2'])
    parser.add_argument("-r", "--random_seed", help="random seed", type=int, default=0)
    parser.add_argument("-m", "--render_mode", action='store_true')
    parser.add_argument("-f", "--frames_per_sec", help="fps", type=int, default=30) # Keep this as the default while running your simulation to visualize results
    args = parser.parse_args()

    config_filepath = args.config
    task = args.task
    random_seed = args.random_seed
    render_mode = args.render_mode
    fps = args.frames_per_sec

    FPS = fps

    random.seed(random_seed)
    np.random.seed(random_seed)

    if task == 'T1':
        
        agent = Task1()
        agent.controller_task1(config_filepath=config_filepath, render_mode=render_mode)

    else:

        agent = Task2()
        agent.controller_task2(config_filepath=config_filepath, render_mode=render_mode)
