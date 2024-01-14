import numpy as np
from django.shortcuts import render, redirect

from ..models.news import News
from app.models.likes import UserLikes
from sklearn.metrics.pairwise import cosine_similarity

from ..models.user import CustomUser
from ..recommendation_new import matrix_factorization
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


def recommend(request, user_id):
    MAX_RECOMMENDATIONS = 10  # Change this value to the desired maximum number of recommendations
    NUM_SVD_COMPONENTS = 50  # Choose an appropriate value for the number of SVD components

    num_users = CustomUser.objects.count()
    num_items = News.objects.count()

    R = np.zeros((num_users, num_items))
    ratings = UserLikes.objects.filter(user_id=user_id)

    for rating in ratings:
        R[rating.user_id - 1][rating.news_id - 1] = rating.rating

    # Convert the user-item interaction matrix to a sparse matrix
    # Convert the user-item interaction matrix to a sparse matrix
    R_sparse = csr_matrix(R)

    # Check for extreme sparsity
    if R_sparse.nnz == 0:
        print("Matrix is too sparse.")
        return render(request, 'recommendations.html', {'recommendations': []})

    # Apply Truncated SVD
    svd = TruncatedSVD(n_components=NUM_SVD_COMPONENTS)
    U = svd.fit_transform(R_sparse)
    Sigma = np.diag(svd.singular_values_)
    Vt = svd.components_

    # Reconstruct the matrix
    R_reconstructed = U @ Sigma @ Vt

    # Perform matrix factorization on the reconstructed matrix
    P, Q = matrix_factorization(R_reconstructed)

    user_similarity = cosine_similarity(P[user_id - 1, :].reshape(1, -1), P).flatten()
    similar_users = np.argsort(user_similarity)[::-1]
    positive_similar_users = similar_users[user_similarity[similar_users] > 0]

    # Get the indices of unrated items for the user
    unrated_indices = np.where(R[user_id - 1] == 0)[0]

    # Use the maximum possible number of recommendations based on unrated items or the set maximum
    N = min(MAX_RECOMMENDATIONS, len(unrated_indices))

    recommended_items_set = set()  # Use a set to avoid duplicates

    for similar_user in positive_similar_users:
        # Calculate recommendations based on the similar user
        similar_user_recommendations = np.dot(P[similar_user, :], Q.T)

        # Sort unrated indices by recommendation scores in descending order
        top_n_indices = np.argsort(similar_user_recommendations[unrated_indices])[::-1][:N]

        # Add unique news articles to the set, considering those rated by both current user and other users
        recommended_items_set.update(
            News.objects.filter(id__in=unrated_indices[top_n_indices] + 1, userlikes__rating__gt=0)
        )

    # Convert the set back to a list
    recommended_items = list(recommended_items_set)
    print(recommended_items)

    print(f"Recommendations for user {user_id} (ID 'b'):")

    for item in recommended_items:
        print(f"ID: {item.id}, Title: {item.title}, Description: {item.description}, Link: {item.link}")

    return render(request, 'recommendations.html', {'recommendations': recommended_items})