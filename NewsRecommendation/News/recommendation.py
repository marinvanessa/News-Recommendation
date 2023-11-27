import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Read the CSV file
df_news = pd.read_csv("E:/sac2/NewsRecommendation/Dataset/bbc_news.csv")

# Drop duplicates
df_without_duplicated_guid = df_news.drop_duplicates('guid')
df_news_without_duplicates = df_without_duplicated_guid.drop_duplicates(subset=['title', 'description', 'guid']).copy()


# If there are NaN values, complete them with an empty string
news_titles = df_news_without_duplicates['title'].fillna("")
news_descriptions = df_news_without_duplicates['description'].fillna("")

# Concatenate 'title' and 'description'
df_news_without_duplicates['together'] = news_titles + ' ' + news_descriptions

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df_news_without_duplicates['together'])

# calculate cos similarity
similarity = linear_kernel(tfidf_matrix, tfidf_matrix)


def recomanda_stiri(id_știre, cosine_sim=similarity, df=df_news_without_duplicates):
    idx = df[df['guid'] == id_știre].index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    top_3_news = sim_scores[1:4]

    recomandation_index = [i[0] for i in top_3_news]

    return df['guid'].iloc[recomandation_index].values


test = recomanda_stiri(df_news_without_duplicates.iloc[2]['guid'])
print(test)