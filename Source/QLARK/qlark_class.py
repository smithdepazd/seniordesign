import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import pickle
import time

style.use("ggplot")

# from QLARK.qlark_cvs_interface import QlarkCircuitInterface
from QLARK.cvs_qlark_interface import QlarkCircuitInterface, CircuitStatus


def square(val):
    return val * val


class Qlark:
    def __init__(self, desired_logic):
        # AI constants
        self.EPISODE_NUM = 100000    # number of circuit Attempts
        self.EPS_DECAY = .9998  # Rate of random probability decay
        self.LEARNING_RATE = 0.1  # How much a q-value will change
        self.DISCOUNT = 0.95
        self.QRANDOMINIT = -1  # The range of random starting values
        self.EPSILONSTART = 1
        self.NUM_STEPS = 12# self.environment.ACTION_SPACE*3-6  # number of tries to complete a circuit
        print(self.NUM_STEPS)
        self.DESIREDLOGIC = desired_logic


        # AI Variables
        self.epsilon = self.EPSILONSTART  # probability of randomness. Goes down over time
        self.episode_rewards = []  # list of rewards for every episode

        try:
            with open("qtable.pickle", "rb") as f:
                self.q_table = pickle.load(f)
        except:
            self.q_table = dict()

        # Space for AI to play and get feedback from
        self.environment = QlarkCircuitInterface(DESIRED_LOGIC=self.DESIREDLOGIC, C_IN_CT=2, C_OUT_CT=2, MAX_GATE_NUM=2, NUM_OF_GATE_TYPES=6)


    def runBest(self):
        self.environment.reset_environment()
        for step in range(0, 20):

            # get state for q-table
            index_q = self.environment.get_state()
            action = np.argmax(self.q_table[index_q])
            # Update the environment and find out how it did
            reward = self.environment.attempt_action(action)
            # get future q
            new_index_q = self.environment.get_state()
            if self.environment.getcircuitstatus() != CircuitStatus.Valid:
                self.environment.printout()
                self.environment.parseLogic()
                break


    # Train The AI on an Environment
    def train(self):

        # Each episode is an attempt from nothing
        for episode in range(self.EPISODE_NUM):

            self.environment.reset_environment()
            episode_reward = 0

            # number of times the ai tries to add to the q table something
            for step in range(0, self.NUM_STEPS):
                # get state for q-table
                index_q = self.environment.get_state()
                # IF STATE DOESNT EXIST MAKE IT SO
                if index_q in self.q_table:
                    pass
                else:
                    self.q_table[index_q] = [np.random.uniform(self.QRANDOMINIT, 0) for i in range(self.environment.ACTION_SPACE)]

                # ACTION based on EPSILON GREEDY/REWARD
                if np.random.random() > self.epsilon:
                    action = np.argmax(self.q_table[index_q])
                else:
                    action = np.random.randint(len(self.q_table[index_q]))

                # Update the environment and find out how it did
                reward = self.environment.attempt_action(action)
                # get future q
                new_index_q = self.environment.get_state()

                # IF THE NEW STATE DOESNT EXIST MAKE IT SO
                if new_index_q in self.q_table:
                    pass
                else:
                    self.q_table[new_index_q] = [np.random.uniform(self.QRANDOMINIT, 0) for i in range(self.environment.ACTION_SPACE)]

                max_future_q = np.max(self.q_table[new_index_q])

                current_q = self.q_table[index_q][action]

                # Check If environment is in end state
                if step == self.NUM_STEPS - 1:
                    self.environment.breakcircuit()
                    # print("LIMIT REACHED")

                if self.environment.getcircuitstatus() == CircuitStatus.Valid:
                    new_q = (1 - self.LEARNING_RATE) * current_q + self.LEARNING_RATE * (reward.value + self.DISCOUNT * max_future_q)
                else:
                    new_q = self.environment.getspecialreward()

                self.q_table[index_q][action] = new_q
                episode_reward += new_q

                if self.environment.circuitstatus == CircuitStatus.Correct:
                    print(f"SUCCESS ON EPISODE: {episode}")
                    # self.environment.printout()
                    # self.environment.parseLogic()
                    # print(f"SUCCESS ON EPISODE: {episode}")
                    # if episode % 10000 == 0 or episode > self.EPISODE_NUM*.90:
                    #     print(f"SUCCESS ON EPISODE: {episode}")
                    #     self.environment.printout()
                    # return
                    break
                elif self.environment.circuitstatus != CircuitStatus.Valid:
                    break

            self.episode_rewards.append(episode_reward)
            if episode < self.EPISODE_NUM:
                self.epsilon *= self.EPS_DECAY
            if episode % 3000 == 0:
                print(f"REMAINING EPISODES: {self.EPISODE_NUM - episode}")
                self.saveq()

            # if self.epsilon < 0.0001:
            #     self.epsilon = self.EPSILONSTART
            #     break
            #
            #     print("Epsilon RESET")
            #     self.environment.printout()


        self.saveq()
        self.environment.printout()
        self.environment.parseLogic()

        self.showaiadata()

    def saveq(self):
        print("\nSAVING Q-table")
        with open("qtable.pickle", "wb") as f:  # every once in a while autosave just in case
            pickle.dump(self.q_table, f)
        print("SAVING finished")

        # with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
        #     pickle.dump(self.q_table, f)
        # with open("qtable_backup.pickle", "wb") as f:
        #     pickle.dump(self.q_table, f)

    def showaiadata(self):

        GRAPH_GRANULARITY = 1000
        moving_avg = np.convolve(self.episode_rewards, np.ones((GRAPH_GRANULARITY,)) / GRAPH_GRANULARITY, mode='valid')

        plt.plot([i for i in range(len(moving_avg))], moving_avg)
        plt.ylabel(f"Reward {GRAPH_GRANULARITY}ma")
        plt.xlabel("episode #")
        plt.show()
        print(f"epsilon value: {self.epsilon}")







