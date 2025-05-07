import os
import sys
import pandas as pd
import numpy as np
import joblib

# --- Определение базовой директории ---
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS  # временная папка при запуске .exe
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # обычный запуск .py

print(f"[DEBUG] Базовая директория: {base_dir}")

# --- Пути к файлам относительные ---
model_path = os.path.join(base_dir, 'best_CatBoost_full.pkl')
data_path = os.path.join(base_dir, 'pred2.csv')

print(f"[DEBUG] Путь к модели: {model_path}")
print(f"[DEBUG] Путь к данным: {data_path}")

# --- Загрузка модели ---
try:
    model = joblib.load(model_path)
    print("[INFO] Модель успешно загружена")
except FileNotFoundError:
    raise FileNotFoundError(f"[ERROR] Модель не найдена по пути: {model_path}")

# --- Загрузка данных ---
try:
    df = pd.read_csv(data_path)
    print("[INFO] Данные успешно загружены")
except FileNotFoundError:
    raise FileNotFoundError(f"[ERROR] Файл данных не найден: {data_path}")

# --- Проверка признаков ---
try:
    required_features = model.feature_names_
except AttributeError:
    raise AttributeError("[ERROR] Модель не содержит атрибут feature_names_. Убедитесь, что это обученная модель с поддержкой feature_names.")

missing_features = [f for f in required_features if f not in df.columns]
if missing_features:
    raise ValueError(f"[ERROR] Отсутствуют следующие признаки в данных: {missing_features}")

# --- Выборка 20 случайных строк ---
np.random.seed(42)
sample_indices = np.random.choice(df.index, size=20, replace=False)
df_sample = df.loc[sample_indices]

# --- Предсказания ---
X_sample = df_sample[required_features]
y_prob = model.predict_proba(X_sample)[:, 1]
y_pred = (y_prob >= 0.5).astype(int)

# --- Вывод результатов ---
print("\n[RESULT] Пример данных и предсказаний:")
for i, idx in enumerate(sample_indices):
    print(f"Строка {idx}: Вероятность={y_prob[i]:.4f}, Предсказание={y_pred[i]}")

# Чтобы консоль не закрывалась мгновенно (для Windows .exe)
if getattr(sys, 'frozen', False):
    input("\n[INFO] Нажмите Enter для выхода...")