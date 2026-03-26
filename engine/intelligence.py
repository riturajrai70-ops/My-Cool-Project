class AppleExpert:
    def __init__(self, api_key=AIzaSyCN2SsQBpOgsvKOmUap1c1x_PHopXEIs1MM):
        self.api_key = api_key

    def get_treatment_plan(self, disease_name):
        if not self.api_key:
            # Fallback local database
            plans = {
                "Blotch Apple": "Increase pruning to improve sunlight and air circulation.",
                "Rot Apple": "Immediately remove and burn infected fruit to prevent spread.",
                "Scab Apple": "Apply sulfur-based fungicides during the rainy season.",
                "Normal Apple": "Continue standard irrigation and nutrient monitoring."
            }
            return plans.get(disease_name, "Keep monitoring for changes.")
        
        # If API Key is provided, you would call Gemini/OpenAI here:
        # response = call_llm(f"Write a 3-step organic treatment for {disease_name}")
        # return response