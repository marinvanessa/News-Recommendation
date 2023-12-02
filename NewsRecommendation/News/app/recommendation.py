import pandas as pd
from django.http import JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def cleaning_data(news_data):
    df = pd.DataFrame([(item.title, item.description, item.link) for item in news_data],
                      columns=['title', 'description', 'link'])
    df_without_duplicated_link = df.drop_duplicates('link')
    df_without_duplicates = df_without_duplicated_link.drop_duplicates(subset=['title', 'description']).copy()
    news_titles = df_without_duplicates['title'].fillna("")
    news_descriptions = df_without_duplicates['description'].fillna("")
    df_without_duplicates['together'] = news_titles + ' ' + news_descriptions
    return df_without_duplicates


def calculate_matrix_of_similarity(df_without_duplicates):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_without_duplicates['together'])

    return linear_kernel(tfidf_matrix, tfidf_matrix)


def recommend_top_news(news_data, cosine_sim, news_id):
    df = pd.DataFrame([(item.id, item.title, item.description, item.link, item.number_of_likes) for item in news_data],
                      columns=['id', 'title', 'description', 'link', 'number_of_likes'])
    idx = df[df['id'] == news_id].index[0]
    weighted_scores = []
    for i in range(len(df)):
        similarity_score = cosine_sim[idx, i]
        likes_count = df['number_of_likes'].iloc[i]
        weighted_score = similarity_score * (1 + likes_count)
        weighted_scores.append((i, weighted_score))

    weighted_scores = sorted(weighted_scores, key=lambda x: x[1], reverse=True)

    recommended_indices = []
    for i, _ in weighted_scores:
        if i != idx:
            recommended_indices.append(i)

    top_3_recommendations = df['link'].iloc[recommended_indices[:3]].values

    if top_3_recommendations is None or top_3_recommendations.size == 0:
        return JsonResponse({'recommendations': '0 news recommendations'})

    return JsonResponse({'recommendations': list(top_3_recommendations)})
