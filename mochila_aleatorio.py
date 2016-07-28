from random import randint
import sys
import time
Dados=[0,0,0,0,0,0,0,0,0,0];
Pesos=[1,2,3,5,4,6,8,7,9,10];
Valores=[2,3,4,5,6,7,8,9,10,11]
NmaxEntradas=10;
NmaxParticulas=3;
Geracoes=3;
PesoMaximo=17;
Maximo=0; #melhor mochila encontrada
MelhorIndice=0;#Indice da melhor particula encontrada
MelhorEpoca=0;#Epoca da melhor particula encontrada
MelhorPeso=0; #
Dados = [[0 for i in xrange(NmaxEntradas)] for i in xrange(NmaxParticulas)]
Objetivo= 25; #peso maximo

inicio_execucao = time.time()
for h in range(Geracoes):
    for i in range(NmaxParticulas):
        Total=0;
        Peso=0;
        for j in range(NmaxEntradas):
            Dados[i][j]=randint(0,1);
            Total+=Dados[i][j]*Pesos[j];
            Peso+=Dados[i][j]*Pesos[j];
        
            if j < NmaxEntradas - 1:
                sys.stdout.write("(")
                sys.stdout.write(str(Dados[i][j]) + " * "+ str(Valores[j]) + ") + ")
            else:
                sys.stdout.write("(")
                sys.stdout.write(str(Dados[i][j]) + " * "+ str(Valores[j]) + ") = ")
                    
        if Total>=Maximo and Peso<=PesoMaximo:
            Maximo=Total;
            MelhorIndice=i;
            MelhorEpoca=h;
            MelhorPeso=Peso;
        


        sys.stdout.write(str(Total)+ "\n")
    sys.stdout.write("\n Numero de epocas: " + str(h)+"\n");
sys.stdout.write("\n Melhor resultado encontrado na epoca " + str(MelhorEpoca)+" e no indice "+ str(MelhorIndice)+ " com valor "+ str(Maximo)+" e peso "+str(MelhorPeso)+"\n");

duracao = time.time() - inicio_execucao;
print duracao


