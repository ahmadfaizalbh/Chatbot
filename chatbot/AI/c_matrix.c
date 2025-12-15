#include "c_matrix.h"

Matrix* mat_create(int rows, int cols) {
    Matrix *m = (Matrix*)malloc(sizeof(Matrix));
    m->rows = rows;
    m->cols = cols;
    m->data = (float*)calloc(rows * cols, sizeof(float));
    return m;
}

void mat_free(Matrix *m) {
    if (m) {
        if (m->data) free(m->data);
        free(m);
    }
}

void mat_print(Matrix *m) {
    printf("Matrix (%d x %d):\n", m->rows, m->cols);
    for (int i = 0; i < m->rows; i++) {
        for (int j = 0; j < m->cols; j++) {
            printf("%f ", m->data[i * m->cols + j]);
        }
        printf("\n");
    }
}

void mat_randomize(Matrix *m, float min, float max) {
    for (int i = 0; i < m->rows * m->cols; i++) {
        m->data[i] = min + (rand() / (float)RAND_MAX) * (max - min);
    }
}

void mat_add(Matrix *A, Matrix *B, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = A->data[i] + B->data[i];
    }
}

void mat_sub(Matrix *A, Matrix *B, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = A->data[i] - B->data[i];
    }
}

void mat_mul(Matrix *A, Matrix *B, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = A->data[i] * B->data[i];
    }
}

void mat_dot(Matrix *A, Matrix *B, Matrix *C) {
    if (A->cols != B->rows) {
        // Error handling should be better, but for now simple check
        return;
    }
    for (int i = 0; i < A->rows; i++) {
        for (int j = 0; j < B->cols; j++) {
            float sum = 0;
            for (int k = 0; k < A->cols; k++) {
                sum += A->data[i * A->cols + k] * B->data[k * B->cols + j];
            }
            C->data[i * C->cols + j] = sum;
        }
    }
}

void mat_scale(Matrix *A, float scalar, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = A->data[i] * scalar;
    }
}

void mat_transpose(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows; i++) {
        for (int j = 0; j < A->cols; j++) {
            C->data[j * C->cols + i] = A->data[i * A->cols + j];
        }
    }
}

// Activation Functions

void mat_apply_sigmoid(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = 1.0f / (1.0f + expf(-A->data[i]));
    }
}

void mat_apply_sigmoid_derivative(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        float sig = 1.0f / (1.0f + expf(-A->data[i]));
        C->data[i] = sig * (1.0f - sig);
    }
}

void mat_apply_relu(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = A->data[i] > 0 ? A->data[i] : 0;
    }
}

void mat_apply_relu_derivative(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = A->data[i] > 0 ? 1 : 0;
    }
}

void mat_apply_tanh(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        C->data[i] = tanhf(A->data[i]);
    }
}

void mat_apply_tanh_derivative(Matrix *A, Matrix *C) {
    for (int i = 0; i < A->rows * A->cols; i++) {
        float t = tanhf(A->data[i]);
        C->data[i] = 1.0f - t * t;
    }
}

void mat_apply_softmax(Matrix *A, Matrix *C) {
    // Softmax per row
    for (int i = 0; i < A->rows; i++) {
        float max_val = -1.0e30f; // Something small
        for(int j=0; j < A->cols; j++) {
            if(A->data[i * A->cols + j] > max_val) max_val = A->data[i * A->cols + j];
        }
        
        float sum = 0;
        for (int j = 0; j < A->cols; j++) {
            // Shift values for numerical stability
            float val = expf(A->data[i * A->cols + j] - max_val);
            C->data[i * C->cols + j] = val;
            sum += val;
        }
        for (int j = 0; j < A->cols; j++) {
            C->data[i * C->cols + j] /= sum;
        }
    }
}
