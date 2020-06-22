import threading
import pickle
from QLARK.qlark_class import Qlark

class QlarkThread(threading.Thread):
    threadIDcounter = 1

    def __init__(self, truthtable, trainingsetnum):
        super().__init__()
        self.id = QlarkThread.threadIDcounter
        QlarkThread.threadIDcounter +=1
        self.truthtable = truthtable
        self.trainingsetnum = trainingsetnum
        self.qtable = None
        self.success_flag = False
        self.success_counter = 0

    def run(self):
        print(f"Starting Thread : {self.id}")
        Q_AI = self.TrainQlark()
        self.qtable = Q_AI.q_table
        self.success_flag = Q_AI.success_flag
        self.success_counter = Q_AI.success_counter
        print(f"Exiting Thread: {self.id}")

    def TrainQlark(self):
        Qlearningai = Qlark(self.truthtable,self.id)
        for i in range(self.trainingsetnum):
            print(f"Thread: {self.id} - Number of training sets remaining: {self.trainingsetnum-i}")
            Qlearningai.train()
            if Qlearningai.success_flag == True:
                print(f"THREAD: {self.thread_ID} QLARK SUCCESSFULLY LEARNED on set: {i}")
                break
        # Qlearingai.runBest()
        return Qlearningai



def saveqtable(q_table):
    print("\nSAVING Q-table")
    with open("qtable.pickle", "wb") as f:  # every once in a while autosave just in case
        pickle.dump(q_table, f)

def Needlethreading(thread_num,desired_truth,trainingsetnum):
    qtablelist = []
    thread_list = []

    for i in range(thread_num):
        tempthread = QlarkThread(desired_truth,trainingsetnum)
        tempthread.start()
        thread_list.append(tempthread)
    for thread in thread_list:
        thread.join()
    print("Threads Should Be Finished now")
    # print(f"Qtablelist check: {qtablelist}")
    print("Averaging Q-tables Now")

    max_success = 0
    thread_winner_index = 0
    for i, thread in enumerate(thread_list):
        if thread.success_flag:
            if thread.success_counter >= max_success:
                max_success = thread.success_counter
                thread_winner_index = i
    print(f"max success count: {max_success}")
    print(f"thread winner id: {thread_list[thread_winner_index].id}")
    best_qtable = thread_list[thread_winner_index].qtable


    saveqtable(best_qtable)
    BestAI = Qlark(desired_truth,99)
    BestAI.runBest()

