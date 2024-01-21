# News Recommendation

The proposed project involves the development of a news recommendation application, centered around user experience and powered by advanced techniques such as collaborative filtering based on matrix factorization and cosine similarity measurement within a user-based framework.

## LoginPage


![Login Page](NewsRecommendation/loginPage.png)

## Register Page

![Register Page](NewsRecommendation/registerPage.png)

## Flow of the Application

![Getting recommendations](NewsRecommendation/NewsRecommendation.gif)

## Data

[Get Dataset (up to date)] https://www.kaggle.com/datasets/gpreda/bbc-news

I used a large dataset from BBC with 25,642 news articles to build a news recommendation app. I saved 1,000 articles in a PostgreSQL database for the app to work with. This approach ensures the app has a solid base for providing accurate recommendations.

**adding_data.py:** (u have to introduce the number of users and news that u want to populate with data)

Generates random ratings for a specified number of users and news articles, simulating user interactions. The generated ratings, ranging between 0 and 5, are then saved in the database through the UserLikes model. This script is useful for populating the database with synthetic data for testing and development purposes, ensuring a diverse set of user preferences and interactions.

## Recommendation Algorithm 

**matrix_factorization.py:**

This function employs stochastic gradient descent to perform matrix factorization on the user-item rating matrix ('R'). By decomposing it into two lower-rank matrices ('P' and 'Q'), the algorithm initializes these matrices with random values. Through iterative updates, the matrices evolve to minimize the reconstruction error. This technique is fundamental for extracting latent features that capture underlying patterns within the user-item interactions.

**recommend.py:**

The recommendation function starts by retrieving user-item ratings and constructing the rating matrix ('R'). It employs singular value decomposition (SVD) to reduce matrix dimensionality, creating a reconstructed version (R_reconstructed). The matrix_factorization function is then called to obtain decomposed matrices 'P' and 'Q'. User similarity is calculated using cosine similarity for identifying similar users. The function recommends news articles based on user preferences and organizes them for personalized presentation, enhancing the user experience through collaborative filtering.
