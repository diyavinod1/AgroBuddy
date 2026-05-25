DISEASE_KNOWLEDGE: dict[str, dict[str, object]] = {
    "Tomato___Late_blight": {
        "crop": "tomato",
        "disease": "Late blight",
        "symptoms": ["Dark water-soaked leaf spots", "White fungal growth in humid weather", "Rapid leaf drying"],
        "remedies": ["Remove severely infected leaves", "Use copper-based fungicide as per label", "Avoid overhead irrigation"],
        "fertilizer": ["Use balanced NPK", "Add compost for soil health", "Avoid excess nitrogen during humid periods"],
        "prevention": ["Keep plant spacing for airflow", "Mulch to reduce soil splash", "Rotate tomato crops for 2-3 seasons"],
    },
    "Tomato___Early_blight": {
        "crop": "tomato",
        "disease": "Early blight",
        "symptoms": ["Brown rings on older leaves", "Yellowing around spots", "Lower leaves dropping"],
        "remedies": ["Prune infected lower leaves", "Apply approved fungicide", "Water near the roots only"],
        "fertilizer": ["Maintain potassium levels", "Use compost tea or organic manure", "Avoid nitrogen overdose"],
        "prevention": ["Stake plants", "Clean crop debris", "Use disease-free seedlings"],
    },
    "Potato___Late_blight": {
        "crop": "potato",
        "disease": "Late blight",
        "symptoms": ["Irregular dark lesions", "Leaf collapse after wet weather", "Brown patches on stems"],
        "remedies": ["Destroy infected foliage away from field", "Spray recommended fungicide", "Improve drainage"],
        "fertilizer": ["Apply potassium-rich fertilizer", "Use well-rotted farmyard manure", "Avoid excessive nitrogen"],
        "prevention": ["Use certified seed tubers", "Hill soil around plants", "Rotate with non-solanaceous crops"],
    },
    "Corn___Common_rust": {
        "crop": "corn",
        "disease": "Common rust",
        "symptoms": ["Small reddish-brown pustules", "Pustules on both leaf surfaces", "Reduced green leaf area"],
        "remedies": ["Use fungicide if infection is heavy", "Remove volunteer maize plants", "Monitor young crops closely"],
        "fertilizer": ["Maintain balanced NPK", "Ensure zinc if local soil is deficient", "Add organic matter"],
        "prevention": ["Plant resistant varieties", "Avoid late sowing in high-risk areas", "Keep field sanitation"],
    },
    "Rice___Brown_spot": {
        "crop": "rice",
        "disease": "Brown spot",
        "symptoms": ["Oval brown leaf spots", "Seedling weakness", "Poor grain filling in severe cases"],
        "remedies": ["Use seed treatment next season", "Correct nutrient deficiency", "Drain stagnant water when needed"],
        "fertilizer": ["Apply balanced NPK", "Correct potassium and silica deficiency", "Use zinc where recommended"],
        "prevention": ["Use healthy seed", "Improve field leveling", "Avoid drought stress"],
    },
    "Wheat___Leaf_rust": {
        "crop": "wheat",
        "disease": "Leaf rust",
        "symptoms": ["Orange-brown powdery pustules", "Scattered spots on leaves", "Premature leaf drying"],
        "remedies": ["Apply triazole fungicide if severe", "Remove alternate hosts near field", "Monitor after cool humid weather"],
        "fertilizer": ["Use balanced nitrogen", "Add phosphorus and potassium as per soil test", "Avoid lush excessive growth"],
        "prevention": ["Choose resistant varieties", "Sow at recommended time", "Practice crop rotation"],
    },
    "Generic___Healthy": {
        "crop": "generic leaves",
        "disease": "Healthy or low visible disease",
        "symptoms": ["No strong disease pattern detected", "Leaf color appears mostly normal"],
        "remedies": ["Continue regular monitoring", "Remove damaged leaves if present", "Use clean irrigation water"],
        "fertilizer": ["Follow local soil test recommendation", "Use compost or farmyard manure", "Do not over-fertilize"],
        "prevention": ["Keep field clean", "Inspect leaves weekly", "Maintain proper spacing and watering"],
    },
}

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "ml": "Malayalam",
    "kn": "Kannada",
}

SUPPORTED_LANGUAGES = set(LANGUAGE_NAMES)
