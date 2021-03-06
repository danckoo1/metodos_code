#
#  Código para Descomposición de Benders V2
#
# Autor: Moisés Saavedra
# Modificaciones y comentarios adicionales: Jorge Vera
#

from gurobipy import *
import numpy
import time

# Se setea que opcion de resolucion ocupar
opcion = int(input("Ingresa 0 para resolver el problema completo, \n ingresa 1 para usar Benders: "))
if opcion == 0:
    no_benders = True
else:
    no_benders = False


######################################
#   Invencion de parametros base     #
######################################

#Numero de depositos
NITERACIONES = 150
TOL = 0.000001
BIGM = 5000000000000000

# Parametros
LOG = ["LOG1","LOG2","LOG3", "LOG4","LOG5","LOG6"]
BOARD = ["LU1","LU2","LU3","LU4","LU5","LU6","LU7"]
CUT = ["E1", "E2", "E3", "E4"]
MONTH = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

# Procurement and procesing cost for logs
CTt = {
    ("LOG1","Jan") :	260,
    ("LOG1","Feb") :	260,
    ("LOG1","March") :	260,
    ("LOG1","April") :	260,
    ("LOG1","May") :	260,
    ("LOG1","June") :	260,
    ("LOG1","July") :	260,
    ("LOG1","Aug") :	260,
    ("LOG1","Sept") :	260,
    ("LOG1","Oct") :	260,
    ("LOG1","Nov") :	260,
    ("LOG1","Dec") :	260,
    ("LOG2","Jan") :	265,
    ("LOG2","Feb") :	265,
    ("LOG2","March") :	265,
    ("LOG2","April") :	265,
    ("LOG2","May") :	265,
    ("LOG2","June") :	265,
    ("LOG2","July") :	265,
    ("LOG2","Aug") :	265,
    ("LOG2","Sept") :	265,
    ("LOG2","Oct") :	265,
    ("LOG2","Nov") :	265,
    ("LOG2","Dec") :	265,
    ("LOG3","Jan") :	233,
    ("LOG3","Feb") :	233,
    ("LOG3","March") :	233,
    ("LOG3","April") :	233,
    ("LOG3","May") :	233,
    ("LOG3","June") :	233,
    ("LOG3","July") :	233,
    ("LOG3","Aug") :	233,
    ("LOG3","Sept") :	233,
    ("LOG3","Oct") :	233,
    ("LOG3","Nov") :	233,
    ("LOG3","Dec") :	233,
    ("LOG4","Jan") :	241,
    ("LOG4","Feb") :	241,
    ("LOG4","March") :	241,
    ("LOG4","April") :	241,
    ("LOG4","May") :	241,
    ("LOG4","June") :	241,
    ("LOG4","July") :	241,
    ("LOG4","Aug") :	241,
    ("LOG4","Sept") :	241,
    ("LOG4","Oct") :	241,
    ("LOG4","Nov") :	241,
    ("LOG4","Dec") :	241,
    ("LOG5","Jan") :	102,
    ("LOG5","Feb") :	102,
    ("LOG5","March") :	102,
    ("LOG5","April") :	102,
    ("LOG5","May") :	102,
    ("LOG5","June") :	102,
    ("LOG5","July") :	102,
    ("LOG5","Aug") :	102,
    ("LOG5","Sept") :	102,
    ("LOG5","Oct") :	102,
    ("LOG5","Nov") :	102,
    ("LOG5","Dec") :	102,
    ("LOG6","Jan") :	140,
    ("LOG6","Feb") :	140,
    ("LOG6","March") :	140,
    ("LOG6","April") :	140,
    ("LOG6","May") :	140,
    ("LOG6","June") :	140,
    ("LOG6","July") :	140,
    ("LOG6","Aug") :	140,
    ("LOG6","Sept") :	140,
    ("LOG6","Oct") :	140,
    ("LOG6","Nov") :	140,
    ("LOG6","Dec") :	140,
}
CFt = {
    ("LOG1","Jan") :	2600000	,
    ("LOG1","Feb") :	3120000	,
    ("LOG1","March") :	2080000	,
    ("LOG1","April") :	2600000	,
    ("LOG1","May") :	2600000	,
    ("LOG1","June") :	2600000	,
    ("LOG1","July") :	2600000	,
    ("LOG1","Aug") :	3120000	,
    ("LOG1","Sept") :	2600000	,
    ("LOG1","Oct") :	2600000	,
    ("LOG1","Nov") :	2080000	,
    ("LOG1","Dec") :	3120000	,
    ("LOG2","Jan") :	2650000	,
    ("LOG2","Feb") :	3180000	,
    ("LOG2","March") :	2650000	,
    ("LOG2","April") :	2650000	,
    ("LOG2","May") :	3180000	,
    ("LOG2","June") :	2650000	,
    ("LOG2","July") :	3180000	,
    ("LOG2","Aug") :	3180000	,
    ("LOG2","Sept") :	3180000	,
    ("LOG2","Oct") :	2120000	,
    ("LOG2","Nov") :	2120000	,
    ("LOG2","Dec") :	2120000	,
    ("LOG3","Jan") :	2330000	,
    ("LOG3","Feb") :	2330000	,
    ("LOG3","March") :	1864000	,
    ("LOG3","April") :	2796000	,
    ("LOG3","May") :	2796000	,
    ("LOG3","June") :	2330000	,
    ("LOG3","July") :	2330000	,
    ("LOG3","Aug") :	2330000	,
    ("LOG3","Sept") :	2796000	,
    ("LOG3","Oct") :	2330000	,
    ("LOG3","Nov") :	1864000	,
    ("LOG3","Dec") :	2330000	,
    ("LOG4","Jan") :	2892000	,
    ("LOG4","Feb") :	2892000	,
    ("LOG4","March") :	1928000	,
    ("LOG4","April") :	2410000	,
    ("LOG4","May") :	2410000	,
    ("LOG4","June") :	2410000	,
    ("LOG4","July") :	2892000	,
    ("LOG4","Aug") :	2892000	,
    ("LOG4","Sept") :	2892000	,
    ("LOG4","Oct") :	2410000	,
    ("LOG4","Nov") :	2892000	,
    ("LOG4","Dec") :	1928000	,
    ("LOG5","Jan") :	816000	,
    ("LOG5","Feb") :	1224000	,
    ("LOG5","March") :	1224000	,
    ("LOG5","April") :	816000	,
    ("LOG5","May") :	816000	,
    ("LOG5","June") :	1224000	,
    ("LOG5","July") :	1224000	,
    ("LOG5","Aug") :	816000	,
    ("LOG5","Sept") :	1224000	,
    ("LOG5","Oct") :	1224000	,
    ("LOG5","Nov") :	1224000	,
    ("LOG5","Dec") :	1020000	,
    ("LOG6","Jan") :	1680000	,
    ("LOG6","Feb") :	1120000	,
    ("LOG6","March") :	1400000	,
    ("LOG6","April") :	1120000	,
    ("LOG6","May") :	1120000	,
    ("LOG6","June") :	1400000	,
    ("LOG6","July") :	1680000	,
    ("LOG6","Aug") :	1120000	,
    ("LOG6","Sept") :	1680000	,
    ("LOG6","Oct") :	1120000	,
    ("LOG6","Nov") :	1120000	,
    ("LOG6","Dec") :	1680000	,
}
# Inventory costo for logs
CBt = {
    ("LU1","Jan") :	2,
    ("LU1","Feb") :	2,
    ("LU1","March") :	2,
    ("LU1","April") :	2,
    ("LU1","May") :	2,
    ("LU1","June") :	2,
    ("LU1","July") :	2,
    ("LU1","Aug") :	2,
    ("LU1","Sept") :	2,
    ("LU1","Oct") :	2,
    ("LU1","Nov") :	2,
    ("LU1","Dec") :	2,
    ("LU2","Jan") :	2,
    ("LU2","Feb") :	2,
    ("LU2","March") :	2,
    ("LU2","April") :	2,
    ("LU2","May") :	2,
    ("LU2","June") :	2,
    ("LU2","July") :	2,
    ("LU2","Aug") :	2,
    ("LU2","Sept") :	2,
    ("LU2","Oct") :	2,
    ("LU2","Nov") :	2,
    ("LU2","Dec") :	2,
    ("LU3","Jan") :	2,
    ("LU3","Feb") :	2,
    ("LU3","March") :	2,
    ("LU3","April") :	2,
    ("LU3","May") :	2,
    ("LU3","June") :	2,
    ("LU3","July") :	2,
    ("LU3","Aug") :	2,
    ("LU3","Sept") :	2,
    ("LU3","Oct") :	2,
    ("LU3","Nov") :	2,
    ("LU3","Dec") :	2,
    ("LU4","Jan") :	2,
    ("LU4","Feb") :	2,
    ("LU4","March") :	2,
    ("LU4","April") :	2,
    ("LU4","May") :	2,
    ("LU4","June") :	2,
    ("LU4","July") :	2,
    ("LU4","Aug") :	2,
    ("LU4","Sept") :	2,
    ("LU4","Oct") :	2,
    ("LU4","Nov") :	2,
    ("LU4","Dec") :	2,
    ("LU5","Jan") :	2,
    ("LU5","Feb") :	2,
    ("LU5","March") :	2,
    ("LU5","April") :	2,
    ("LU5","May") :	2,
    ("LU5","June") :	2,
    ("LU5","July") :	2,
    ("LU5","Aug") :	2,
    ("LU5","Sept") :	2,
    ("LU5","Oct") :	2,
    ("LU5","Nov") :	2,
    ("LU5","Dec") :	2,
    ("LU6","Jan") :	2,
    ("LU6","Feb") :	2,
    ("LU6","March") :	2,
    ("LU6","April") :	2,
    ("LU6","May") :	2,
    ("LU6","June") :	2,
    ("LU6","July") :	2,
    ("LU6","Aug") :	2,
    ("LU6","Sept") :	2,
    ("LU6","Oct") :	2,
    ("LU6","Nov") :	2,
    ("LU6","Dec") :	2,
    ("LU7","Jan") :	2,
    ("LU7","Feb") : 2,
    ("LU7","March") :	2,
    ("LU7","April") :	2,
    ("LU7","May") :	2,
    ("LU7","June") :	2,
    ("LU7","July") :	2,
    ("LU7","Aug") :	2,
    ("LU7","Sept") :	2,
    ("LU7","Oct") :	2,
    ("LU7","Nov") :	2,
    ("LU7","Dec") :	2,
}
# Processing and inventory capacities
PAt = {
    "Jan" : 28500,		
    "Feb" : 28500,
    "March" : 28500,
    "April" : 28500,
    "May" : 28500,
    "June" : 28500,
    "July" : 28500,
    "Aug" : 28500,
    "Sept" : 28500,
    "Oct" : 28500,
    "Nov" : 28500,
    "Dec" : 28500,
}	
PBt = {
    "Jan" : 40000,		
    "Feb" : 8000,
    "March" : 50000,
    "April" : 50000,
    "May" : 50000,
    "June" : 50000,
    "July" : 50000,
    "Aug" : 50000,
    "Sept" : 35000,
    "Oct" : 50000,
    "Nov" : 50000,
    "Dec" : 50000,
}	
# Demand for final products									
D = {
    "LU1" : {"Jan":2450,"Feb":2558,"March":2708,"April":2208,"May":2433,"June":2354,"July":2359,"Aug":2699,"Sept":2107,"Oct":2309,"Nov":2624,"Dec":2725},
    "LU2" : {"Jan":152,"Feb":176,"March":139,"April":142,"May":167,"June":147,"July":139,"Aug":152,"Sept":156,"Oct":137,"Nov":137,"Dec":126},	
    "LU3" : {"Jan":420,"Feb":346,"March":	371,"April":	360,"May":497,"June":458,"July":	490,"Aug":502,"Sept":441,"Oct":495,"Nov":392,"Dec":396},	
    "LU4" : {"Jan":2100,"Feb":2515,"March":1745,"April":1906,"May":2320,"June":2335,"July":2028,"Aug":2218,"Sept":1931,"Oct":	2465,"Nov":2131,"Dec":2383},	
    "LU5" : {"Jan":1818,"Feb":2108,"March":2015,"April":1471,"May":1956,"June":2063,"July":1473,"Aug":2165,"Sept":2130,"Oct":2166,"Nov":1489,"Dec":1588},	
    "LU6" : {"Jan":1120,"Feb":975,"March":1130,"April":1163,"May":1003,"June":1233,"July":1161,"Aug":1253,"Sept":951,"Oct":1074,"Nov":1244,"Dec":1144},	
    #"LU6" : {"Jan":0,"Feb":0,"March":0,"April":0,"May":0,"June":1233,"July":1161,"Aug":0,"Sept":0,"Oct":0,"Nov":0,"Dec":0},
    "LU7" : {"Jan":342,"Feb":295,"March":310,"April":400,"May":335,"June":334,"July":282,"Aug":277,"Sept":325,"Oct":280,"Nov":308,"Dec":344}
}
# Aggregated yield of the sawing process 
Rt	= {
    "LOG1" : {"LU1":0.0611,"LU2":0.01742,"LU3":0.0611,"LU4":0.13936,"LU5":0.05954,"LU6":0.12194,"LU7":0.05954},		
    "LOG2" : {"LU1":0.08996,"LU2":0.0078,"LU3":0.08996,"LU4":	0.10582,"LU5":0.06422,"LU6":0.09802,"LU7":0.06422},		
    "LOG3" : {"LU1":0.065,"LU2":0.065,"LU3":0.0624,"LU4":0.169,"LU5":0.026,"LU6":0.13,"LU7":	0.0026},		
    "LOG4" : {"LU1":0.091,"LU2":0.0234,"LU3":0.143,"LU4":0.0676,"LU5":0.0494,"LU6":0.104,"LU7":0.0416},		
    "LOG5" : {"LU1":0.155,"LU2":0.055,"LU3":0.045,"LU4":0.105,"LU5":0.0715,"LU6":0.025,"LU7":0.05616},		
    "LOG6" : {"LU1":0.12246,"LU2":0.00286,"LU3":	0.04004,"LU4":0.13546,"LU5":0.09542,"LU6":0.00208,"LU7":0.12168}
}
# Initial log inventory
w0t = {											
    "LU1": 0,													
    "LU2": 0,													
    "LU3": 0,													
    "LU4": 0,													
    "LU5": 0,													
    "LU6": 0,													
    "LU7": 0,
}

if no_benders:
    deterministico = Model()
    deterministico.Params.Threads = 1

    # Generacion de variables
    x = deterministico.addVars(N, N, vtype=GRB.CONTINUOUS, lb=0)
    y = deterministico.addVars(N, N, vtype=GRB.CONTINUOUS, lb=0)

    # Generacion de restricciones
    R1 = deterministico.addConstrs(
        (quicksum(x[ii, jj] for jj in N if jj!=ii) <= s[ii]) for ii in N
    )

    R2 = deterministico.addConstrs(
        (quicksum(y[ii, jj] for jj in N if jj!=ii) <= s[ii] + quicksum(x[ll, ii] for ll in N if ll!=ii) - quicksum(x[ii, ll] for ll in N if ll!=ii)) for ii in N
    )

    R3 = deterministico.addConstrs(
        (y[ii, jj] <= d[ii][jj]) for ii in N for jj in N if jj!=ii
    )

    # Generacion de funcion objetivo
    deterministico.setObjective(
        quicksum(quicksum(q[ii][jj]*y[ii,jj] - c[ii][jj]*x[ii,jj] for jj in N if jj!=ii) for ii in N),
        GRB.MAXIMIZE
    )

    # Optimiza el equivalente
    inicio = time.time()
    deterministico.update()
    deterministico.optimize()
    final = time.time()

    print("Valor objetivo - Tiempo de resolucion ")
    print(deterministico.objVal, "   -   ", deterministico.Runtime)

else: ########################################
    #   Inicia  Descomposicion Benders
    #########################################

    # Define problema maestro
    maestro = Model()
    maestro.Params.DualReductions = 0
    maestro.Params.OutputFlag = 1

    # Generacion de variables
    skt = maestro.addVars(LOG,MONTH, vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, name="skt")
    zkt =  maestro.addVars(LOG,MONTH, vtype=GRB.BINARY ,name="zkt")

    theta = maestro.addVar(vtype=GRB.CONTINUOUS, lb = 0)

    # Generacion de restricciones
    R1m = maestro.addConstrs(
        quicksum(skt[k,t] for k in LOG) <= PAt[t] for t in MONTH
    )

    R2mm = maestro.addConstrs(((skt[k,t] <= BIGM*zkt[k,t]) for t in MONTH for k in LOG), name = "Cargas_fijas")
    
    maestro.setObjective(
        quicksum(quicksum( (CTt[k,t]+4.5)*skt[k,t] for k in LOG) + quicksum(CFt[k,t] * zkt[k,t] for k in LOG) for t in MONTH ),
        GRB.MINIMIZE
    )

    


    # *********************************************************************************

    ##### Definicion de subproblema ####
    # 
    # En este caso el problema satélite se usa en forma primal directamente.
    # Entonces, lo que se usa en la iteración son las VARIABLES DUALES del satélite, esas
    # generan el corte.
    #
    subproblema = Model()
    subproblema.Params.DualReductions = 0
    subproblema.Params.OutputFlag = 0
    subproblema.setParam('InfUnbdInfo', 1)

    # Generacion de variables
    pi = subproblema.addVars(BOARD, MONTH, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="pi")
    v = subproblema.addVars(MONTH, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=0)

    # Generacion de restricciones
    R1sub = subproblema.addConstrs(
       pi[m,t] - pi[m,MONTH[MONTH.index(t)+1]] + v[MONTH[MONTH.index(t)+1]] <= CBt[m,MONTH[MONTH.index(t)+1]] for m in BOARD \
           for t in MONTH if t != MONTH[-1]
    )

    R1subi = subproblema.addConstrs(
        (-pi[m,MONTH[-1]] + v[MONTH[-1]]<= CBt[m, MONTH[-1]] for m in BOARD)
    )

    # Genera funcion objetivo
    #mas arriba

    ##################################
    #         Ciclo Benders          #
    ##################################

    print("")
    print("---------- CICLOS BENDERS-------------")
    print("")
    print("Ciclo - Master - Subproblema")
    inicio = time.time()
    contador = 0
    lista = []

    # Se inician las iteracion controladas
    FOold = 0
    while contador <= NITERACIONES:
        contador += 1
        # Resuelve el modelo maestro
        maestro.update()
        maestro.optimize()

        # Actualizacion de restricciones segun lo calculado en el maestro
        subproblema.setObjective(
        quicksum(quicksum(pi[m,t]*(D[m][t] - quicksum(Rt[k][m]*skt[k,t].X for k in LOG)) for t in MONTH) for m in BOARD) \
            + quicksum(v[t]*PBt[t] for t in MONTH),
        GRB.MAXIMIZE
        )
        subproblema.update()


        # Optimizacion del subproblema satélite.
        # Recordar que se resuleve el primal en las variables y directamente.        subproblema.update()
        subproblema.optimize()
        status = subproblema.Status

        # Acumula el valor en la FO
        FO = maestro.objVal
        if status == 2:
            BOUND = subproblema.objVal + sum(sum( (CTt[k,t]+4.5)*skt[k,t].X for k in LOG) + sum(CFt[k,t] * \
                zkt[k,t].X for k in LOG) for t in MONTH )
            print(contador, "/", maestro.objVal, "/", BOUND)
            
        elif status != 13:
            print(contador, "/", maestro.objVal, "/","infinity" )
        lista.append(FO)

        # Condicion de quiebre de BENDERE
        if ((contador > 1) and (theta.X -TOL >= subproblema.objVal) and status == 2): 
            print("**** Termino por convergencia ****")
            break

        # Si es factible agrega corte de optimalidad
        if status == 2:
            maestro.addConstr(
                quicksum(quicksum(pi[m,t].X*(D[m][t] - quicksum(Rt[k][m]*skt[k,t] for k in LOG)) for t in MONTH) for m in BOARD) + 
                quicksum(v[t].X*PBt[t] for t in MONTH) <= theta
            )
            maestro.setObjective(
            quicksum(quicksum( (CTt[k,t]+4.5)*skt[k,t] for k in LOG) + quicksum(CFt[k,t] * zkt[k,t] for k in LOG) for t in MONTH ) + theta,
            GRB.MINIMIZE
            )

        elif status!= 13:
            h = subproblema.UnbdRay
            pond = 1
            h_1 = {}
            i = 0 
            for m in BOARD:
                h_1[m] = {}
                for t in MONTH:
                    h_1[m][t] = h[i]*pond
                    i += 1
            h_2 = {}
            for t in MONTH:
                h_2[t] = h[i]*pond
                i += 1

            maestro.addConstr(
                quicksum(quicksum(h_1[m][t]*(D[m][t] - quicksum(Rt[k][m]*skt[k,t] for k in LOG)) for t in MONTH) for m in BOARD) 
                + quicksum(h_2[t]*PBt[t] for t in MONTH) <= 0
            )

    final = time.time()
    print("")
    print(" Tiempo de ejecucion:", (final - inicio))