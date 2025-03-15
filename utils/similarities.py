from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compare_products(feature1, feature2):
    similarity = cosine_similarity(feature1, feature2)
    return similarity[0][0]
