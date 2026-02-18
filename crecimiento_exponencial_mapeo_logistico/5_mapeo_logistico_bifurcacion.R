### code to plot the bifurcation diagram for logistic map
n<-1
R <- seq(2.5,4,length=1000)
f <- expression(a*x*(1-x))
data <- matrix(0,200,1001)
for(a in R){
  x <- runif(1) # random initial condition
  ## first converge to attractor
  for(i in 1:200){
    x <- eval(f)
  } # collect points on attractor
  for(i in 1:200){
    x <- eval(f)
    data[i,n] <- x
  }
  n <- n+1
}
data <- data[,1:1000]
plot(R,data[1,], pch=".", xlab="a", ylab="X")

