import tensorflow as tf
import numpy as np
import cv2

class AppleClassifier:
    def __init__(self, model_path):
        # Load model once during initialization
        self.model = tf.keras.models.load_model(model_path)
        self.classes = ['Blotch Apple', 'Normal Apple', 'Rot Apple', 'Scab Apple']

    def process_and_predict(self, image_data):
        """
        Works for both file paths and numpy arrays (OpenCV frames)
        """
        if isinstance(image_data, str):
            img = tf.keras.preprocessing.image.load_img(image_data, target_size=(224, 224))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
        else:
            img_array = cv2.resize(image_data, (224, 224))

        img_array = np.expand_dims(img_array / 255.0, axis=0)
        predictions = self.model.predict(img_array)[0]
        
        top_index = np.argmax(predictions)
        return {
            "label": self.classes[top_index],
            "confidence": float(predictions[top_index]),
            "all_scores": dict(zip(self.classes, map(float, predictions)))
        }