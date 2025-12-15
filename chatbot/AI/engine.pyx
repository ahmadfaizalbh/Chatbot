# cython: language_level=3
from c_matrix cimport Matrix, mat_create, mat_free, mat_print, mat_randomize, mat_add, mat_sub, mat_mul, mat_dot, mat_scale, mat_transpose, mat_apply_sigmoid, mat_apply_relu, mat_apply_tanh, mat_apply_softmax, mat_apply_sigmoid_derivative, mat_apply_relu_derivative, mat_apply_tanh_derivative
from libc.stdlib cimport malloc, free

cdef class PyMatrix:

    def __cinit__(self, int rows, int cols):
        self.ptr = mat_create(rows, cols)
        self.rows = rows
        self.cols = cols

    def __dealloc__(self):
        if self.ptr is not NULL:
            mat_free(self.ptr)

    @property
    def data(self):
        # Only for debugging, returns a list copy
        cdef list res = []
        for i in range(self.rows * self.cols):
            res.append(self.ptr.data[i])
        return res

    def randomize(self, float min_val, float max_val):
        mat_randomize(self.ptr, min_val, max_val)

    def dot(self, PyMatrix other):
        if self.cols != other.rows:
            raise ValueError(f"Shape mismatch: {self.rows}x{self.cols} . {other.rows}x{other.cols}")
        cdef PyMatrix res = PyMatrix(self.rows, other.cols)
        mat_dot(self.ptr, other.ptr, res.ptr)
        return res

    def add(self, PyMatrix other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Shape mismatch for add")
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_add(self.ptr, other.ptr, res.ptr)
        return res

    def sub(self, PyMatrix other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Shape mismatch for sub")
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_sub(self.ptr, other.ptr, res.ptr)
        return res

    def mul(self, PyMatrix other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Shape mismatch for mul")
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_mul(self.ptr, other.ptr, res.ptr)
        return res

    def scale(self, float scalar):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_scale(self.ptr, scalar, res.ptr)
        return res
    
    def transpose(self):
        cdef PyMatrix res = PyMatrix(self.cols, self.rows)
        mat_transpose(self.ptr, res.ptr)
        return res

    def apply_sigmoid(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_sigmoid(self.ptr, res.ptr)
        return res
    
    def apply_relu(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_relu(self.ptr, res.ptr)
        return res
    
    def apply_tanh(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_tanh(self.ptr, res.ptr)
        return res

    def apply_softmax(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_softmax(self.ptr, res.ptr)
        return res

    def apply_sigmoid_derivative(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_sigmoid_derivative(self.ptr, res.ptr)
        return res
    
    def apply_relu_derivative(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_relu_derivative(self.ptr, res.ptr)
        return res
    
    def apply_tanh_derivative(self):
        cdef PyMatrix res = PyMatrix(self.rows, self.cols)
        mat_apply_tanh_derivative(self.ptr, res.ptr)
        return res
    
    def print_mat(self):
        mat_print(self.ptr)

    def to_list(self):
        result = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.ptr.data[i * self.cols + j])
            result.append(row)
        return result
    
    @staticmethod
    def from_list(list data):
        if not data:
            return PyMatrix(0, 0)
        cdef int rows = len(data)
        cdef int cols = len(data[0])
        cdef PyMatrix m = PyMatrix(rows, cols)
        for i in range(rows):
            for j in range(cols):
                m.ptr.data[i * cols + j] = float(data[i][j])
        return m
