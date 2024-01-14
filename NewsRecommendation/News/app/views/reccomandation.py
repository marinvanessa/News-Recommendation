import numpy as np
from django.shortcuts import render

from ..models.news import News
from app.models.likes import UserLikes
from sklearn.metrics.pairwise import cosine_similarity

from ..models.user import CustomUser
from ..matrix_factorization import matrix_factorization
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD


def recommend(request, user_id):
    MAX_RECOMMENDATIONS = 10
    NUM_SVD_COMPONENTS = 50

    num_users = CustomUser.objects.count()
    num_items = News.objects.count()

    R = np.zeros((num_users, num_items))
    ratings = UserLikes.objects.filter(user_id=user_id)

    for rating in ratings:
        R[rating.user_id - 1][rating.news_id - 1] = rating.rating

    R_sparse = csr_matrix(R)

    if R_sparse.nnz == 0:
        print("Matrix is too sparse.")
        return render(request, 'recommendations.html', {'recommendations': []})

    svd = TruncatedSVD(n_components=NUM_SVD_COMPONENTS)
    U = svd.fit_transform(R_sparse)
    Sigma = np.diag(svd.singular_values_)
    Vt = svd.components_

    R_reconstructed = U @ Sigma @ Vt

    P, Q = matrix_factorization(R_reconstructed)

    user_similarity = cosine_similarity(P[user_id - 1, :].reshape(1, -1), P).flatten()
    similar_users = np.argsort(user_similarity)[::-1]
    positive_similar_users = similar_users[user_similarity[similar_users] > 0]

    unrated_indices = np.where(R[user_id - 1] == 0)[0]

    N = min(MAX_RECOMMENDATIONS, len(unrated_indices))

    recommended_items_set = set()

    for similar_user in positive_similar_users:
        similar_user_recommendations = np.dot(P[similar_user, :], Q.T)

        top_n_indices = np.argsort(similar_user_recommendations[unrated_indices])[::-1][:N]

        recommended_items_set.update(
            News.objects.filter(id__in=unrated_indices[top_n_indices] + 1, userlikes__rating__gt=0)
        )

    recommended_items = list(recommended_items_set)

    user_ratings = UserLikes.objects.filter(user_id=user_id, news_id__in=[item.id for item in recommended_items])

    recommended_news_data = []

    for recommended_item in recommended_items:
        rating = UserLikes.objects.filter(news=recommended_item, user_id=user_id).first()
        rating_value = rating.rating if rating else 0

        recommended_news_data.append({
            'id': recommended_item.id,
            'title': recommended_item.title,
            'description': recommended_item.description,
            'link': recommended_item.link,
            'rating': rating_value,
        })

    return render(request, 'recommendations.html', {'recommendations': recommended_news_data})