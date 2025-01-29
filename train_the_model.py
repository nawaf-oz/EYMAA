import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# تحميل البيانات من ملف CSV
df = pd.read_csv('features_labels.csv')
X = df.iloc[:, :-1].values  # الميزات
y = df['label'].values      # التصنيفات

# تقسيم البيانات إلى تدريب واختبار
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# تدريب نموذج RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# اختبار النموذج
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# حفظ النموذج المدرب
import joblib
joblib.dump(model, 'sign_language_model.pkl')
print("Model saved as 'sign_language_model.pkl'")
