from c_matrix cimport Matrix

cdef class PyMatrix:
    cdef Matrix *ptr
    cdef public int rows
    cdef public int cols
