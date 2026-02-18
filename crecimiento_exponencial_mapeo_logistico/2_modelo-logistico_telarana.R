################################################################################

# Al igual que en el modelo exponencial podemos iterar nuestro modelo para simular lo que sucede. 
# En este caso usaremos R = 2 y una poblacio ́n inicial
# x0 = 0.1, es decir una poblaci ́on del 10% del ma ́ximo posible

# Funcion que describe el modelo logistico: N_{t+1} = R*N_t*(1-N_t)
mod.logistico <- function(x, r) {
  return(r*x*(1-x))
} 

# Parametros
valor.inicial <- .1
r <- 2
tiempo.max <- 10

# Iterar
# generar lista de valores
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))
resultados$N[1] <- valor.inicial # r indexa desde 1, hay que correr en indice
resultados

for (i in 1:(length(resultados$N)-1) ) { #correr para todos los valores menos el ultimo
  resultados$N[i+1] <- mod.logistico(resultados$N[i],r)
}
print(resultados)

# Graficar tiempo contra poblacion
plot(resultados, main="Modelo logistico")

# Graficar N_t contra N_{t+1}
# generar cuadratica
x = seq(0,1, length.out = 25)
y = sapply(x, mod.logistico, r) #generate function
#par(pty="s") #make plot square
plot(x,y, type="l", col="red", #plot the function
     xlim=c(0,1), ylim=c(0,1), 
     main="Modelo logistico" ) #make axis equal
lines(x,x) # plot identity line

# Metodo de telaraña
t0 <- valor.inicial #definimos en punto n_t
for (i in resultados$N) { #iteramos sobre todos los tiempos
  t1 <- mod.logistico(t0,r) # calculamos valor en modelo
  lines(t0,t1, type="p") #punto (n_t, n_{t+1})
  lines(c(t0,t0,t1), c(t0,t1,t1),lty=2) #lineas de iteracion
  t0 <- t1
}

############################################################################

# otro emplo mas
# Qué podeis interpretar?

# Funcion que describe el modelo logistico: N_{t+1} = R*N_t*(1-N_t)
mod.logistico <- function(x, r) {
  return(r*x*(1-x))
} 

# Parametros
valor.inicial <- .95
r <- 2.5
tiempo.max <- 10

# Iterar
# generar lista de valores
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))
resultados$N[1] <- valor.inicial # r indexa desde 1, hay que correr en indice
resultados

for (i in 1:(length(resultados$N)-1) ) { #correr para todos los valores menos el ultimo
  resultados$N[i+1] <- mod.logistico(resultados$N[i],r)
}
print(resultados)

# Graficar tiempo contra poblacion
plot(resultados, main="Modelo logistico")

# Graficar N_t contra N_{t+1}
# generar cuadratica
x = seq(0,1, length.out = 25)
y = sapply(x, mod.logistico, r) #generate function
#par(pty="s") #make plot square
plot(x,y, type="l", col="red", #plot the function
     xlim=c(0,1), ylim=c(0,1), 
     main="Modelo logistico" ) #make axis equal
lines(x,x) # plot identity line

# Metodo de telaraña
t0 <- valor.inicial #definimos en punto n_t
for (i in resultados$N) { #iteramos sobre todos los tiempos
  t1 <- mod.logistico(t0,r) # calculamos valor en modelo
  lines(t0,t1, type="p") #punto (n_t, n_{t+1})
  lines(c(t0,t0,t1), c(t0,t1,t1),lty=2) #lineas de iteracion
  t0 <- t1
}

