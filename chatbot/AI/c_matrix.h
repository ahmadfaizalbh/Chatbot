#ifndef C_MATRIX_H
#define C_MATRIX_H

#include <stdlib.h>
#include <math.h>
#include <stdio.h>

typedef struct {
    float *data;
    int rows;
    int cols;
} Matrix;

// Memory Management
Matrix* mat_create(int rows, int cols);
void mat_free(Matrix *m);
void mat_print(Matrix *m);

// Basic Operations
void mat_add(Matrix *A, Matrix *B, Matrix *C); // C = A + B
void mat_sub(Matrix *A, Matrix *B, Matrix *C); // C = A - B
void mat_mul(Matrix *A, Matrix *B, Matrix *C); // C = A * B (Element-wise)
void mat_dot(Matrix *A, Matrix *B, Matrix *C); // C = A . B (Dot Product)
void mat_scale(Matrix *A, float scalar, Matrix *C); // C = A * scalar
void mat_transpose(Matrix *A, Matrix *C);      // C = A^T

// Activation Functions (Applied in-place or to target)
void mat_apply_sigmoid(Matrix *A, Matrix *C);
void mat_apply_relu(Matrix *A, Matrix *C);
void mat_apply_tanh(Matrix *A, Matrix *C);
void mat_apply_softmax(Matrix *A, Matrix *C);

// Derivatives
void mat_apply_sigmoid_derivative(Matrix *A, Matrix *C);
void mat_apply_relu_derivative(Matrix *A, Matrix *C);
void mat_apply_tanh_derivative(Matrix *A, Matrix *C);

// Randomization
void mat_randomize(Matrix *m, float min, float max);

#endif
