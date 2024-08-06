import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json


def get_funds_data():
    with open('funds_data.json', 'r') as funds_data:
        data = json.load(funds_data)
    
    return data


def asset_dataframe(funds_data, asset):
    data = funds_data[asset]
    rows = []

    for fund_name, attributes in data.items():
        combined_text = ' '.join(attributes['fund_values'] + attributes['fund_captions'])
        rows.append({'fund_name' : fund_name, 'combined_text' : combined_text})

    return pd.DataFrame(rows)


def find_closest_funds(vectorizer, tfidf_matrix, user_input):
    user_input_tfidf = vectorizer.transform([user_input])
    similarity_scores = cosine_similarity(user_input_tfidf, tfidf_matrix)
    top_match_indices = similarity_scores.argsort()[0][-3:][::-1]

    return top_match_indices, similarity_scores[0]

def get_top_funds(funds_data, user_input):
    top_funds = pd.DataFrame()
    vectorizer = TfidfVectorizer()

    for fund_type in funds_data:
        fund_df = asset_dataframe(funds_data, fund_type)
        tfidf_matrix = vectorizer.fit_transform(fund_df['combined_text'])

        top_funds_indices, sim_scores = find_closest_funds(vectorizer, tfidf_matrix, user_input)
        fund_df['Similarity Scores'] = sim_scores
        top_funds_df = fund_df.iloc[top_funds_indices]

        top_funds = pd.concat([top_funds, top_funds_df])

    top_funds.reset_index(inplace=True, drop=True)
    return top_funds

def main():
    funds_data = get_funds_data()
    # df = asset_dataframe(funds_data, 'Alternative funds')

    # vectorizer = TfidfVectorizer()
    # tfidf_matrix = vectorizer.fit_transform(df['combined_text'])
    # top_funds, sim_scores = find_closest_funds(vectorizer, tfidf_matrix, "One-stop alternative allocation solution")
    # df['Similarity Scores'] = sim_scores

    # print(df)
    user_input = "One-stop alternative allocation solution"
    top_funds = get_top_funds(funds_data, user_input)
    print(top_funds.nlargest(5, 'Similarity Scores'))


if __name__ == '__main__':
    main()