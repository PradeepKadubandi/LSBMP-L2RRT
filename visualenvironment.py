from shapely.geometry import box
from shapely.geometry import Point
import numpy as np
import matplotlib.pyplot as plt

class VisualEnvironment:
    def __init__(self, size=32, includeRobot=True, shouldInit=True):
        self.size = size
        self.includeRobot = includeRobot
        self.robot_hl = 0.5
        self.world = None
        self.data = None
        if shouldInit:
            self.initialize()

    def initialize(self):
        self.num_obstacles = np.random.randint(low=2, high=7)
        self.type_obstacle = np.random.randint(0, 2, size=self.num_obstacles)
        self.center_obstacles = self.size * np.random.rand(self.num_obstacles, 2)
        # spec: Radius for circle and half_length for square
        # Min value is 2 and maximum 8
        self.spec_obstacle = 2 + 6 * np.random.rand(self.num_obstacles)
        # Clip the obstacle size not to exceed boundaries
        upper_bounds = self.size - self.center_obstacles
        self.spec_obstacle = np.min(np.stack((self.spec_obstacle,
                                              self.center_obstacles[:,0],
                                              self.center_obstacles[:,1],
                                              upper_bounds[:,0],
                                              upper_bounds[:,1]),axis=1), axis=1)
        self.robot_center = self.size * np.random.rand(2)
        
    def with_new_robot_position(self, new_robot_center):
        '''
        Returns a new object with all other things being shared except robot_position
        '''
        result = VisualEnvironment(self.size, includeRobot=True, shouldInit=False)
        result.num_obstacles = self.num_obstacles
        # Intentionally sharing the obstacle arrays as these should be common across copies
        result.type_obstacle = self.type_obstacle
        result.center_obstacles = self.center_obstacles
        result.spec_obstacle = self.spec_obstacle
        result.robot_center = new_robot_center
        return result
        
    def build_geometry(self):
        '''
        Builds the shapely objects corresponding to this environment
        '''
        self.world = box(0.0, 0.0, self.size, self.size)
        self.obstacles = []
        for i in range(self.num_obstacles):
            if self.type_obstacle[i] == 0:
                obs = self.make_box(self.center_obstacles[i, :], self.spec_obstacle[i])
            else:
                obs = self.make_circle(self.center_obstacles[i, :], self.spec_obstacle[i])
            self.obstacles.append(obs)
        self.robot = None
        if self.includeRobot:
            self.robot = self.make_box(self.robot_center, self.robot_hl)

    def build_data(self):
        '''
        Builds a numpy array with different integer range values for empty space, obstacles, robot
        '''
        self.data = np.array([[self.value_for_position([x, y]) for y in range(self.size)] for x in range(self.size)])
        # if self.world is None:
        #     self.build_geometry()
        # self.build_empty()
        # if self.includeRobot:
        #     for x in range(self.size):
        #         for y in range(self.size):
        #             p = Point(x, y)
        #             if self.robot.contains(p):
        #                 self.data[x, y] += np.random.randint(43, 47)
    
    def build_empty(self):
        self.data = np.random.randint(0, 30, size=(self.size,self.size))
        for x in range(self.size):
            for y in range(self.size):
                p = Point(x, y)
                for obs in self.obstacles:
                    if obs.contains(p):
                        self.data[x, y] += np.random.randint(80, 90)
                        break
    
    def generate_trajectory(self, length):
        envs = []
        stepsize = 3
        delta_t = 1
        direction = np.random.choice([-1, +1], size=(2))
        current_env = self
        for i in range(length):
            control = np.random.uniform(0.0, stepsize, size=(2)) * direction
            new_robot_pos = current_env.robot_center + delta_t * control
            current_env = current_env.with_new_robot_position(new_robot_pos)
            envs.append(current_env)
        return envs

    def value_for_position(self, pos):
        world_center = np.array([self.size/2, self.size/2])
        world_center_value = 30.0
        world_gradient = 1.0
        value_from_world = world_center_value - self.square_obs_distance(world_center, pos) * world_gradient

        obs_center_value = 70.0
        obs_gradient = 2.0
        min_distance_from_any_obs_center = None
        value_from_obstacle = 0.0
        for i in range(self.num_obstacles):
            if self.type_obstacle[i] == 0:
                dist = self.square_obs_distance(self.center_obstacles[i, :], pos)
            else:
                dist = self.circular_obs_distance(self.center_obstacles[i, :], pos)
            if dist < self.spec_obstacle[i]:
                if min_distance_from_any_obs_center is None:
                    min_distance_from_any_obs_center = dist
                else:
                    min_distance_from_any_obs_center = min(min_distance_from_any_obs_center, dist)
        if min_distance_from_any_obs_center is not None:
            value_from_obstacle = obs_center_value - obs_gradient * min_distance_from_any_obs_center

        robot_center_value = 50.0
        robot_gradient = 3.0
        value_from_robot = 0.0
        if self.includeRobot:
            dist = self.square_obs_distance(self.robot_center, pos)
            if dist <= self.robot_hl:
                value_from_robot = robot_center_value - robot_gradient * dist

        return int(value_from_world + value_from_obstacle + value_from_robot)
        
    def circular_obs_distance(self, center, point):
        return np.linalg.norm(center-point)
    
    def square_obs_distance(self, center, point):
        return np.max(np.abs(center-point))
    
    def plot_geometry(self):
        '''
        Uses matplotlib to plot directly shapely objects.
        '''
        if self.world is None:
            self.build_geometry()
        fig = plt.figure()
        plt.fill(*self.world.exterior.xy, 'g')
        for obs in self.obstacles:
            plt.fill(*obs.exterior.xy, 'b')
        if self.robot is not None:
            plt.fill(*self.robot.exterior.xy, 'y')
        plt.show()
    
    def plot_data(self):
        '''
        Plots the raw data generated after build_array
        '''
        if self.data is None:
            self.build_data()
        plt.imshow(self.data)
        
    def make_box(self, center, half_length):
        return box(center[0]-half_length, center[1]-half_length, center[0]+half_length, center[1]+half_length)

    def make_circle(self, center, radius):
        return Point(center[0], center[1]).buffer(radius)