require 'matrix'

# See http://en.wikipedia.org/wiki/Fibonacci_number#Matrix_form

FIB_MATRIX = Matrix[[1,1],[1,0]]

def fast_fib(n)
  (FIB_MATRIX**(n-1))[0,0]
end
