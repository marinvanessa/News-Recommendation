import numpy as np


def matrix_factorization(R, K=10, steps=5000, alpha=0.0002, beta=0.02):
    num_users, num_items = R.shape
    P = np.random.rand(num_users, K)
    Q = np.random.rand(num_items, K)

    print(f"num_users: {num_users}, num_items: {num_items}")
    print(f"Shape of P: {P.shape}, Shape of Q: {Q.shape}")

    for step in range(steps):
        for i in range(num_users):
            for j in range(num_items):
                if R[i][j] > 0:
                    eij = R[i][j] - np.dot(P[i, :], Q[j, :].T)
                    for k in range(K):
                        P[i][k] += alpha * (2 * eij * Q[j][k] - beta * P[i][k])
                        Q[j][k] += alpha * (2 * eij * P[i][k] - beta * Q[j][k])

    return P, Q

