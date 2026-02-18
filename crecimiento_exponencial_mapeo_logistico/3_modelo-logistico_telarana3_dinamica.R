#########################################################################################
#                                                                                       #
######################## DINAMICA-DINAMICA-DINAMICA #####################################
#                                                                                       #
#########################################################################################


# Funcion que describe el modelo logistico: N_{t+1} = R*N_t*(1-N_t)
#
mod.logistico <- function(x, r) {
  return(r*x*(1-x))
} 

# Parametros
valor.inicial <- .9
r_vals <- c(0.5, 2.0, 3.2, 3.7)
tiempo.max <- 10

for (r in r_vals) {
  # Iterar
  # generar lista de valores
  resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))
  resultados$N[1] <- valor.inicial # r indexa desde 1, hay que correr en indice
  
  for (i in 1:(length(resultados$N)-1) ) { #correr para todos los valores menos el ultimo
    resultados$N[i+1] <- mod.logistico(resultados$N[i],r)
  }
  
  # Graficar tiempo contra poblacion
  plot(resultados, main=paste0("Modelo logistico, r=",r))
  
  # Graficar N_t contra N_{t+1}
  # generar cuadratica
  x = seq(0,1, length.out = 25)
  y = sapply(x, mod.logistico, r) #generate function
  #par(pty="s") #make plot square
  plot(x,y, type="l", col="red", #plot the function
       xlim=c(0,1), ylim=c(0,1), 
       main=paste0("Modelo logistico, r=",r) ) #make axis equal
  lines(x,x) # plot identity line
  
  # Metodo de telaraña
  t0 <- valor.inicial #definimos en punto n_t
  for (i in resultados$N) { #iteramos sobre todos los tiempos
    t1 <- mod.logistico(t0,r) # calculamos valor en modelo
    lines(t0,t1, type="p") #punto (n_t, n_{t+1})
    lines(c(t0,t0,t1), c(t0,t1,t1),lty=2) #lineas de iteracion
    t0 <- t1
  }
}
