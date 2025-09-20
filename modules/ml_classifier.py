# modules/ml_classifier.py

def predict_risk_profile(risk_score: float) -> str:
    """
    Simula la predicción de un modelo de Machine Learning para clasificar
    el perfil de riesgo de un subdominio basado en su puntuación de riesgo.

    En una implementación real, aquí se cargararía un modelo entrenado
    (ej: de scikit-learn o TensorFlow) y se llamaría a model.predict().

    Args:
        risk_score (float): La puntuación de riesgo final calculada en el paso anterior.

    Returns:
        str: El perfil de riesgo predicho ('Bajo', 'Medio', 'Alto').
    """
    
    # Lógica de decisión simple para simular el modelo
    if risk_score > 75:
        return "Alto Riesgo"
    elif risk_score > 40:
        return "Riesgo Medio"
    else:
        return "Bajo Riesgo"