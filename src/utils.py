import pandas as pd

def preprocess_input(data, encoder, model_features):
    df = pd.DataFrame([data])

    # Encode Type
    encoded = encoder.transform(df[['Type']])
    encoded_cols = encoder.get_feature_names_out(['Type'])

    df = df.drop('Type', axis=1)
    df = pd.concat([df, pd.DataFrame(encoded, columns=encoded_cols)], axis=1)

    # Align features
    df = df.reindex(columns=model_features, fill_value=0)

    return df