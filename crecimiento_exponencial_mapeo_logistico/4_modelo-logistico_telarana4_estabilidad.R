#########################################################################################
#                                                                                       #
################################ ESTABILIDAD ############################################
#                                                                                       #
#########################################################################################
# Una pregunta que podemos hacernos es que tan estable es una solución
# Deimos que una solućion es localmente estable si dada una condcíon inicial lo
# suficientemente cercana las iteraciones siguiente se acercan a esta solución

# Una forma intuitiva de ver esto es tomar una serie de puntos y ver si
# convergen a una solucíon o se alejan de el.

# En este caso volveremos a usar los mismos valores de R que ya intentamos,
# pero probaremos distintos valores iniciales X0

# Funcion que describe el modelo logistico: N_{t+1} = R*N_t*(1-N_t)
#
mod.logistico <- function(N,r) {
  N*r*(1-N)
}
# Parámetros
r_vals <- c(0.5, 2.0, 3.2, 3.7)
tiempo.max <- 10
# Iterar para diferentes valores de r
for (r in r_vals) {
  # Iterar para diferentes valores de valor.inicial
  for (valor.inicial in c(0.1, 0.3, 0.7, 0.8, 0.9, 0.95, 1.0, 1.2)) {
    # Generar lista de valores
    resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))
    resultados$N[1] <- valor.inicial
    # Iterar
    for (i in 1:(length(resultados$N)-1)) {
      resultados$N[i+1] <- mod.logistico(resultados$N[i],r)
    }
    # Graficar tiempo contra poblacion
    plot(resultados, main=paste0("Modelo logistico, r=",r, ", valor.inicial=", valor.inicial))
    # Graficar N_t contra N_{t+1}
    x = seq(0,1, length.out = 25)
    y = sapply(x, mod.logistico, r)
    plot(x,y, type="l", col="red", 
         xlim=c(0,1), ylim=c(0,1), 
         main=paste0("Modelo logistico, r=",r, ", valor.inicial=", valor.inicial))
    lines(x,x)
    # Metodo de telaraña
    t0 <- valor.inicial
    for (i in resultados$N) {
      t1 <- mod.logistico(t0,r)
      lines(t0,t1, type="p")
      lines(c(t0,t0,t1), c(t0,t1,t1),lty=2)
      t0 <- t1
    }
  }
}
