import cv2
import numpy as np

class PaletteTools:

    @staticmethod
    def available_tools():
        return ["Skala szarości", "Sepia", "Negatyw"]

    @staticmethod
    def apply(tool_name, image, params=None):
        if tool_name == "Skala szarości":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        
        elif tool_name == "Sepia":
            kernel = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])
            sepia = cv2.transform(image, kernel)
            return np.clip(sepia, 0, 255).astype(np.uint8)

        elif tool_name == "Negatyw":
            return cv2.bitwise_not(image)
        
        return image  # fallback
