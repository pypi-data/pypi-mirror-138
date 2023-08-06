import pandas as pd
import logging
import spacy
import re
from takeusecases.ml.preprocessing.preprocessing_messages import Vectorizer


def pad_data(json_list: str) -> pd.DataFrame:
    """
    Turns a list of JSON strings into a dataframe by adding dummy values to
    columns 'Caller' and 'mgsg'. This makes the input compatible with the 
    rest of the code.

    :param json_list: the input list of intelligent contact json.
    :return: a pandas dataframe with 3 columns, in which the json is stored
    """
    assert json_list, 'Please provide a non-empty list of strings (JSONs).'
    assert type(json_list) == list, 'Please provide a non-empty list of strings (JSONs).'
    assert type(json_list[0]) == str, 'Please provide a non-empty list of strings (JSONs).'
    dummy_df = pd.DataFrame(json_list, columns=['Json'])
    dummy_df['Caller'] = [str(x) for x in range(len(dummy_df))]
    dummy_df['msgs'] = 10 
    return dummy_df


def clean_data(df: pd.DataFrame, stopwords, selected):
    """
    Perform data cleansing.

    Parameters
    ----------
    df  :   pd.Dataframe
            Dataframe to be processed
    stopwords : pickle loaded file of stopwords
    selected : pickle loaded file of selected words

    Returns
    -------
    pd.Dataframe
        Clean Data Frame
    """
    logging.info("Cleaning data")
    df_copy = df.copy()
    df_copy['Message'] = df_copy['Message'].apply(lambda x: re.sub(r'[^\w\s]','',x) )
    nlp = spacy.load('pt_core_news_sm')
    df_copy['Message'] = df_copy['Message'].apply(lambda x: [word.lemma_ for word in nlp(x) ] )
    df_copy['Message'] = df_copy['Message'].apply(lambda x: [word for word in x if word in selected] )
    df_copy.Message = df_copy.Message.apply(lambda x: [word for word in x if word not in stopwords])
    df_copy = df_copy[df_copy['Message'].map(len) > 0]
    return df_copy


def get_vectors(df: pd.DataFrame):
    """
    Perform vectorizer of the textual data

    Parameters
    ----------
    df  :   pd.Dataframe
            Dataframe to be processed

    Returns
    -------
    pd.Dataframe
        Vectorized Data Frame
    """
    path = '../output/fasttext/titan_v2_after_correction_fasttext_window4_mincount20_cbow.kv'
    preprocessing = Vectorizer(path)
    df = preprocessing.process(df)
