import time
from function_record import *
from abstract_profiler import AbstractProfiler


class Profiler(AbstractProfiler):

    def __init__(self):
        self.records = {}
        self.funcion_anterior = None
        self.funcion_actual = None
    
    # search a record by name
    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    # metodo se llama cada vez que se ejecuta una funcion    
    def fun_call_start(self, functionName, args):
        record = self.get_record(functionName)
        record.time_inicio_fin[0] = time.time()
        record.freq += 1
        if self.funcion_actual != None:
            record.caller.append(self.funcion_actual.functionName)
            record.recent_caller = record
        self.funcion_anterior = self.funcion_actual
        self.funcion_actual = record

       
    def fun_call_end(self, functionName, returnValue):
        record = self.get_record(functionName)
        record.time_inicio_fin[1] = time.time()
        record.calculo_tiempo_ejecucion()
        if self.funcion_anterior != None:
            self.funcion_actual = self.funcion_anterior
            self.funcion_anterior = self.funcion_actual.recent_caller
        else:
            self.funcion_actual = None

    
    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.print_report()


