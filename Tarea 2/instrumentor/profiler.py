import time
from function_record import *
from abstract_profiler import AbstractProfiler


class Profiler(AbstractProfiler):

    def __init__(self):
        self.records = {}
        self.funcion_anterior = None
        self.funcion_actual = None
        self.cacheable_dict = {} # nombre_funct : [si es cacheable (bool), args, resultados]
    
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
        if functionName in self.cacheable_dict and self.cacheable_dict[functionName][0]: # si esta en el dict y sigue siendo posible un cache
            if args != self.cacheable_dict[functionName][1]: # al tiro vemos si no es cache
                self.cacheable_dict[functionName][0] = False
                # agregar a function record
                record.funCache = 0
        else: 
            self.cacheable_dict[functionName] = [True, args, "no hay :c"]


       
    def fun_call_end(self, functionName, returnValue):
        record = self.get_record(functionName)
        record.time_inicio_fin[1] = time.time()
        record.calculo_tiempo_ejecucion()
        if self.funcion_anterior != None:
            self.funcion_actual = self.funcion_anterior
            self.funcion_anterior = self.funcion_actual.recent_caller
        else:
            self.funcion_actual = None

        if self.cacheable_dict[functionName][2] == "no hay :c": # es nuevo
            self.cacheable_dict[functionName][2] = returnValue
        else: 
            if self.cacheable_dict[functionName][0] and self.cacheable_dict[functionName][2] != returnValue:
                self.cacheable_dict[functionName][0] = False
                # agregar a function record
                record.funCache = 0
        

    
    # print report
    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('fun', 'freq', 'avg', 'max', 'min',
                                                                        'cache', 'callers'))
        for record in self.records.values():
            record.print_report()


