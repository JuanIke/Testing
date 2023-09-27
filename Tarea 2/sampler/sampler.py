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
        self.final_tree = [] # [function_name, seg, pos, parents] 
        
        
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
                
                # agregar los nuevos nodos
                for pos in range(len(stack)):
                    self.usado = False
                    for fun in self.final_tree: 
                        if stack[pos] == fun[0] and pos == fun[2] and fun[3] == stack[0:pos] :
                            self.usado = True
                            fun[1] += 1
                            break
                    if self.usado == False:
                        self.final_tree.append([stack[pos], 1, pos, stack[0:pos]])

                # Desactivar funciones ACA hay que modificar (ver si hacer un mas 1 al pos_tree para dar espacio)
                    
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def printReport(self):
        for i in self.final_tree:
            print(i)
