from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess
import os
import sys

app = FastAPI()

@app.get("/run-test-predict")
async def run_test_predict():
    # Путь к текущей директории, где находится api.py
    current_dir = os.path.dirname(__file__)

    # Полный путь к python.exe внутри venv
    python_path = os.path.join(current_dir, 'venv', 'Scripts', 'python.exe')

    # Путь к test_predict.py
    script_path = os.path.join(current_dir, 'test_predict.py')

    # Отладочный вывод
    print(f"[DEBUG] Python path: {python_path}")
    print(f"[DEBUG] Script path: {script_path}")

    # Проверка, существует ли python.exe
    if not os.path.exists(python_path):
        return JSONResponse(
            status_code=500,
            content={"error": f"Python executable не найден по пути: {python_path}"}
        )

    # Проверка, существует ли скрипт
    if not os.path.exists(script_path):
        return JSONResponse(
            status_code=500,
            content={"error": f"Скрипт test_predict.py не найден по пути: {script_path}"}
        )

    try:
        # Запуск скрипта через subprocess
        result = subprocess.run(
            [python_path, script_path],
            capture_output=True,  # захватываем stdout и stderr
            text=True,            # работаем с текстом, а не байтами
            check=True            # выбрасывать исключение при ошибке
        )
        output = result.stdout

    except subprocess.CalledProcessError as e:
        print("[ERROR] Ошибка выполнения скрипта:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)

        return JSONResponse(
            status_code=500,
            content={
                "error": "Ошибка при выполнении test_predict.py",
                "stderr": e.stderr,
                "stdout": e.stdout
            }
        )

    # Успешный ответ с выводом скрипта
    return JSONResponse(
        content={
            "message": "Скрипт успешно выполнен",
            "output": output
        }
    )