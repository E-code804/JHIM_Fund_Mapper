import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# e85ad8822059b4fae3a57f2f095f42cbaebfdaab


def get_funds_data():
    with open('funds_data.json', 'r') as funds_data:
        data = json.load(funds_data)
    
    return data


def asset_dataframe(funds_data, asset):
    data = funds_data[asset]
    rows = []

    for fund_name, attributes in data.items():
        # combined_text = ' '.join(attributes['fund_values'] + attributes['fund_captions'])
        # rows.append({'fund_name' : fund_name, 'combined_text' : combined_text})
        combined_values = ' '.join(attributes['fund_values'])
        combined_captions = ' '.join(attributes['fund_captions'])
        rows.append({'fund_name' : fund_name, 'combined_values' : combined_values, 'combined_captions' : combined_captions})

    return pd.DataFrame(rows)


def find_closest_funds(vectorizer, tfidf_matrix, user_input):
    user_input_tfidf = vectorizer.transform([user_input])
    similarity_scores = cosine_similarity(user_input_tfidf, tfidf_matrix)
    top_match_indices = similarity_scores.argsort()[0][-3:][::-1]

    return top_match_indices, similarity_scores[0]

def get_top_funds(funds_data, user_input):
    top_funds = pd.DataFrame()
    vectorizer = TfidfVectorizer()
    name_vectorizer =  TfidfVectorizer()
    values_vectorizer =  TfidfVectorizer()
    captions_vectorizer =  TfidfVectorizer()

    for fund_type in funds_data:
        fund_df = asset_dataframe(funds_data, fund_type)

        # matrices for a fund_type's name, values, and captions, need vectorizor for each
        tfidf_matrix_name = name_vectorizer.fit_transform(fund_df['fund_name'])
        tfidf_matrix_values = values_vectorizer.fit_transform(fund_df['combined_values'])
        tfidf_matrix_captions = captions_vectorizer.fit_transform(fund_df['combined_captions'])

        # Top names, values, and captions
        top_name_indices, sim_scores_name = find_closest_funds(name_vectorizer, tfidf_matrix_name, user_input)
        top_values_indices, sim_scores_values = find_closest_funds(values_vectorizer, tfidf_matrix_values, user_input)
        top_captions_indices, sim_scores_captions = find_closest_funds(captions_vectorizer, tfidf_matrix_captions, user_input)

        # Add score to the df
        fund_df['Name Similarity Scores'] = sim_scores_name
        fund_df['Values Similarity Scores'] = sim_scores_values
        fund_df['Captions Similarity Scores'] = sim_scores_captions
        top_funds_indices = np.concatenate((top_name_indices, top_captions_indices, top_values_indices), axis=None)
        top_funds_indices = np.unique(top_funds_indices)
        print(fund_type)
        print(top_name_indices)
        print(top_values_indices)
        print(top_captions_indices)

        # tfidf_matrix = vectorizer.fit_transform(fund_df['combined_text'])
        # top_funds_indices, sim_scores = find_closest_funds(vectorizer, tfidf_matrix, user_input)
        # fund_df['Similarity Scores'] = sim_scores
        top_funds_df = fund_df.iloc[top_funds_indices]

        top_funds = pd.concat([top_funds, top_funds_df])

    top_funds.reset_index(inplace=True, drop=True)
    return top_funds

def main():
    funds_data = get_funds_data()
    user_input = "One-stop alternative allocation solution"
    top_funds = get_top_funds(funds_data, user_input)

    print(top_funds.nlargest(5, 'Name Similarity Scores'))


if __name__ == '__main__':
    main()