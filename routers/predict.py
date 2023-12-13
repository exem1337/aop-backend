from fastapi import APIRouter
from typing import List
import numpy as np
import json
import tensorflow as tf
from pydantic import BaseModel

router = APIRouter()

# Определение моделей данных с помощью Pydantic
class InputData(BaseModel):
    computer_literacy: float
    visual_acuity: float
    age: float
    emotional_state: float
    memory: float
    attention_concentration: float

class PredictionResult(BaseModel):
    prediction: List[float]

# Генерация простой нейронной сети
def create_model(input_shape, output_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_shape,)),
        tf.keras.layers.Dense(64, input_shape=(input_shape,), activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(output_shape, activation='linear')
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Загрузка данных из файла JSON
def load_dataset(file_path):
    with open(file_path, 'r') as json_file:
        dataset = json.load(json_file)
    return dataset

# Загрузка или обучение модели
def load_or_train_model(dataset_file):
    try:
        # Загрузка обученной модели, если она существует
        model = tf.keras.models.load_model('perceptron_model')
    except:
        # Загрузка датасета из файла JSON
        dataset = load_dataset(dataset_file)

        # Преобразование данных в numpy массивы для обучения
        inputs = np.array([[data["computer_literacy"], data["visual_acuity"], data["age"], data["memory"], data["attention_concentration"]] for data in dataset])
        outputs = np.array([[data["font_size"], data["color_scheme"], 1 if data["icon_presence"] else 0] for data in dataset])

        # Создание и обучение модели
        model = create_model(len(inputs[0]), len(outputs[0]))
        model.fit(inputs, outputs, epochs=100, batch_size=32, verbose=0)
        
        # Сохранение обученной модели
        model.save('perceptron_model')
    
    return model

@router.post("/predict/", response_model=PredictionResult, tags=["Predictions"])
async def predict(data: InputData):
    model = load_or_train_model('constants/dataset.json')

    inputs = np.array([[data.computer_literacy, data.visual_acuity, data.age, data.memory, data.attention_concentration]])
    prediction = model.predict(inputs)
    print(prediction)
    # Предположим, у вас есть два предсказанных значения, например, размер шрифта и цветовая схема
    predicted_font_size = prediction[0][0]  # Предсказанное значение размера шрифта
    predicted_color_scheme = prediction[0][1]  # Предсказанное значение цветовой схемы
    predicted_icon_presence = prediction[0][2]  # Предсказанное значение наличия иконок

    return {"prediction": [predicted_font_size, predicted_color_scheme, predicted_icon_presence]}

@router.get("/model_info/", tags=["Model"])
async def model_info():
    model = load_or_train_model('constants/dataset.json')
    model_summary = []
    # Получаем информацию о входном слое
    input_shape = model.layers[0].input_shape[1:]  # Извлекаем форму без первой размерности (None)
    layer_info = [
        {
            "Название_слоя": "Input",
            "Тип_слоя": "InputLayer",
            "Параметры_слоя": {"input_shape": input_shape}
        }
    ]

    model.summary(print_fn=lambda x: model_summary.append(x))

    translated_summary = [summary.replace("dense", "Полносвязный").replace("sequential", "Последовательный") for summary in model_summary[1:]]

    for layer in model.layers:
        layer_config = layer.get_config()
        layer_info.append({
            "Название_слоя": layer.__class__.__name__,
            "Параметры_слоя": layer_config
        })

    hidden_layers = len(model.layers) - 1  # Вычитаем входной и выходной слои
    total_params = model.count_params()

    return {
        "информация_о_модели": translated_summary,
        "информация_о_слоях": layer_info,
        "общее_количество_параметров": total_params,
        "количество_скрытых_слоев": hidden_layers
    }