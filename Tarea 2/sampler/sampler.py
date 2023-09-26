from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames


class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.final_tree = [] # [function_name, seg, activa(bool), pos] 
        
        
    def start(self):
        self.active = True
        self.t.start()

    
    def stop(self):
        self.active = False
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                print(stack)  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
                
                for pos in range(len(stack)):
                    self.usado = False
                    for fun in self.final_tree: 
                        if stack[pos] == fun[0] and fun[2]:
                            self.usado = True
                            fun[1] += 1
                            break
                    if self.usado == False:
                        self.final_tree.append([stack[pos], 1, True, pos])

                contador_pos_stack = 0
                contador_pos_tree = 0
                for item in self.final_tree:
                    if contador_pos_stack == len(stack):
                        break
                    if item[2] and item[0] == stack[contador_pos_stack]:
                        contador_pos_stack += 1
                    else:
                        break
                    contador_pos_tree += 1

                for item_num in range(contador_pos_tree, len(self.final_tree)):
                    self.final_tree[item_num][2] = False
                    
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def printReport(self):
        print("\nFinal: ",self.final_tree, "\n")
