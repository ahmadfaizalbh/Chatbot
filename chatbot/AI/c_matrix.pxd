cdef extern from "c_matrix.h":
    ctypedef struct Matrix:
        float *data
        int rows
        int cols

    Matrix* mat_create(int rows, int cols)
    void mat_free(Matrix *m)
    void mat_print(Matrix *m)
    void mat_randomize(Matrix *m, float min, float max)
    
    void mat_add(Matrix *A, Matrix *B, Matrix *C)
    void mat_sub(Matrix *A, Matrix *B, Matrix *C)
    void mat_mul(Matrix *A, Matrix *B, Matrix *C)
    void mat_dot(Matrix *A, Matrix *B, Matrix *C)
    void mat_scale(Matrix *A, float scalar, Matrix *C)
    void mat_transpose(Matrix *A, Matrix *C)
    
    void mat_apply_sigmoid(Matrix *A, Matrix *C)
    void mat_apply_relu(Matrix *A, Matrix *C)
    void mat_apply_tanh(Matrix *A, Matrix *C)
    void mat_apply_softmax(Matrix *A, Matrix *C)
    
    void mat_apply_sigmoid_derivative(Matrix *A, Matrix *C)
    void mat_apply_relu_derivative(Matrix *A, Matrix *C)
    void mat_apply_tanh_derivative(Matrix *A, Matrix *C)
