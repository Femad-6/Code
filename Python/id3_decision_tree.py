import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# 1. Setup Data
dataset = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain', 'Sunny', 'Overcast', 'Overcast', 'Rain'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    'PlayTennis': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
}
df = pd.DataFrame(dataset)

# 2. Preprocessing: Convert strings to numbers
# ID3 handles strings naturally, but sklearn requires numbers
le = LabelEncoder()
df_encoded = df.apply(le.fit_transform)

X = df_encoded.drop('PlayTennis', axis=1)
y = df_encoded['PlayTennis']

# 3. Train Model
# criterion='entropy' makes it behave mathematically like ID3 (minimizing entropy)
clf = DecisionTreeClassifier(criterion='entropy')
clf.fit(X, y)

# 4. Visualization
plt.figure(figsize=(12,8))
plot_tree(clf, feature_names=X.columns.tolist(), class_names=['No', 'Yes'], filled=True)
plt.show()

# 5. Prediction Example
# Outlook=Sunny(2), Temp=Cool(0), Humidity=High(0), Wind=Strong(1) based on encoding
new_data = pd.DataFrame([[2, 0, 0, 1]], columns=X.columns)
prediction = clf.predict(new_data)
print(f"Prediction: {'Yes' if prediction[0] == 1 else 'No'}")

print('202378040607李世奇')