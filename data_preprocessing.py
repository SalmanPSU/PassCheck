import pandas as pd
import numpy as np

def password_features(password):
    length = len(password)
    unique_chars = len(set(password))
    digit_ratio = sum(c.isdigit() for c in password) / max(1, length)  # prevent division by zero
    upper_ratio = sum(c.isupper() for c in password) / max(1, length)
    lower_ratio = sum(c.islower() for c in password) / max(1, length)
    special_ratio = sum(not c.isalnum() for c in password) / max(1, length)

    # Return a flat list
    return [length, unique_chars, digit_ratio, upper_ratio, lower_ratio, special_ratio]

def preprocess_data(df):
    # Extract features for each password
    features = np.array([password_features(p) for p in df['password']])

    # Create a DataFrame from features
    features_df = pd.DataFrame(features, columns=[
        'length', 'unique_chars', 'digit_ratio', 'upper_ratio', 'lower_ratio', 'special_ratio'
    ])

    # Combine features with labels
    return pd.concat([features_df, df['strength']], axis=1)


# Create a simple dataset of passwords and their strengths
password_data = {
    'password': [
        "12345",  # Weak
        "Password1",  # Medium
        "A1#4r3Q!",  # Strong
        "admin",  # Weak
        "password123",  # Medium
        "5tR0ngP@ss!",  # Strong
        "111111",  # Weak
        "Qwerty2021",  # Medium
        "P@55w0rd#",  # Strong
    ],
    'strength': [
        "weak", "medium", "strong", "weak", "medium", "strong", "weak", "medium", "strong"
    ]
}

# Convert it into a DataFrame
df = pd.DataFrame(password_data)

# Preprocess it
data = preprocess_data(df)
print(data)

# Save it to a CSV file
data.to_csv('password_dataset.csv', index=False)