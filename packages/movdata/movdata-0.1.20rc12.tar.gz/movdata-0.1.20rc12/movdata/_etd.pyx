from libc.math cimport pow, exp, sqrt
from libc.stdio cimport printf

cdef double expected_fn(int n, double[5] args):
    cdef double speed       =     args[0]
    cdef double shape       =     args[1]
    cdef double scale       =     args[2]
    cdef double time        =     args[3]
    cdef double distance    =     args[4]
    # time-density expectation function for two-parameter weibull distribution
    return (4 * shape / (3.142 * scale * speed)) * pow(speed / scale, shape - 1) * exp(
        -1 * pow(speed / scale, shape)) / sqrt(speed * speed * time * time - distance * distance)