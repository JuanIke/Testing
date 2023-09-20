class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.freq = 0
        self.avg = 0
        self.min = 0
        self.max = 0
        self.functionCache = 0
        
        self.recent_caller = None
        self.caller = []

        self.time_inicio_fin = [0, 0]
        self.tiempos_todos = []

    def calculo_tiempo_ejecucion(self):
        resta = self.time_inicio_fin[1] - self.time_inicio_fin[0]
        self.tiempos_todos.append(resta)

    def calculo_min_max_avg(self):
        self.min = "{:.4f}".format(min(self.tiempos_todos))
        self.max = "{:.4f}".format(max(self.tiempos_todos))
        self.avg = "{:.4f}".format(sum(self.tiempos_todos) / len(self.tiempos_todos))



    def print_report(self):
        self.calculo_min_max_avg()
        self.caller_no_repete = list(set(self.caller))
        print("{:<30} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(self.functionName, self.freq,
                                                                         self.avg, self.min, self.max, self.functionCache, str(self.caller_no_repete)))
