from random import randint
import sys
import time
Dados=  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
Pesos=  [10,22,3,46,58,6,75,8,9,101,11,122,13,10,15,76,17,10,19,20,10,22,3,46,58,6,75,8,9,101,11,122,13,10,15,76,17,10,19,20]
Valores=[10,22,3,46,58,6,75,8,9,101,11,122,13,10,15,76,17,10,19,20,10,22,3,46,58,6,75,8,9,101,11,122,13,10,15,76,17,10,19,20]
NmaxEntradas=50;
NmaxParticulas=10;
Geracoes=100;
PesoMaximo=9000;
Maximo=0; #melhor mochila encontrada
MelhorIndice=0;#Indice da melhor particula encontrada
MelhorEpoca=0;#Epoca da melhor particula encontrada
MelhorPeso=0; #
Dados = [[0 for i in xrange(NmaxEntradas)] for i in xrange(NmaxParticulas)]
Objetivo= 100000; #peso maximo

inicio_execucao = time.time()
for h in range(Geracoes):
    for i in range(NmaxParticulas):
        Total=0;
        Peso=0;
        for j in range(NmaxEntradas):
            Dados[i][j]=randint(0,1);
            Total+=Dados[i][j]*Valores[j];
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


