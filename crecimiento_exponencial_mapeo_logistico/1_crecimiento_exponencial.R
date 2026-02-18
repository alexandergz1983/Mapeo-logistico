# función que describe el modelo: N_{t+1} = R * N_t
mod.exponencial <- function(x, r) {return(x*r)}

# parametros
tiempo.max <-5
valor.inicial <- 1
r <- 2

# iterar 
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))

# r indexa desde 1
resultados$N[1] <- valor.inicial

# correr para todos los valores menos el ultimo
for (i in 1:(length(resultados$N)-1) ) {resultados$N[i+1] <- mod.exponencial(resultados$N[i],r)}
print(resultados)
plot(resultados)

##########################################################################

mod.logistico <- function(x, r) {return(r*x*(1-x))}

# parametros
tiempo.max <- 10
valor.inicial <- 0.1
r <- 0.5

# iterar 
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))

# r indexa desde 1
resultados$N[1] <- valor.inicial

# correr para todos los valores menos el ultimo
for (i in 1:(length(resultados$N)-1) ) {resultados$N[i+1] <- mod.logistico(resultados$N[i],r)}
print(resultados)
plot(resultados)

#######################################################

# dinamica #

mod.logistico <- function(x, r) {
  return(r * x * (1 - x))
}

# parametros
tiempo.max <- 10
valor.inicial <- 0.9
r <- c(0.5, 2.0, 3.2, 3.7)

# iterar 
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))

# loop a través de cada valor de r
for (j in seq_along(r)) {
  # r indexa desde 1
  resultados$N[1] <- valor.inicial
  
  # correr para todos los valores menos el ultimo
  for (i in 1:(length(resultados$N)-1) ) {
    resultados$N[i+1] <- mod.logistico(resultados$N[i],r[j])
  }
  
  # graficar
  plot(resultados, main = paste0("r = ", r[j]))
}

####################


# Estabilidad #

mod.logistico <- function(x, r) {
  return(r * x * (1 - x))
}

# parametros
tiempo.max <- 10
valor.inicial <- 2
r <- c(0.5, 2.0, 3.2, 3.7)

# iterar 
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))

# loop a través de cada valor de r
for (j in seq_along(r)) {
  # r indexa desde 1
  resultados$N[1] <- valor.inicial
  
  # correr para todos los valores menos el ultimo
  for (i in 1:(length(resultados$N)-1) ) {
    resultados$N[i+1] <- mod.logistico(resultados$N[i],r[j])
  }
  
  # graficar
  plot(resultados, main = paste0("r = ", r[j]))
}

######################################################

mod.logistico <- function(x, r) {return(r*x*(1-x))}

# parametros
tiempo.max <- 10
valor.inicial <- 0.1
r <- 2

# iterar 
resultados <- data.frame(t=0:tiempo.max, N=rep(NA,tiempo.max+1))

# r indexa desde 1
resultados$N[1] <- valor.inicial

# correr para todos los valores menos el ultimo
for (i in 1:(length(resultados$N)-1) ) {resultados$N[i+1] <- mod.logistico(resultados$N[i],r)}
print(resultados)
plot(resultados)

