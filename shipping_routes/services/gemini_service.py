import os
import google.generativeai as genai


class GeminiService:
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def get_shipping_route_points(self, origin, destination, product):
        prompt = f"""
        I need to identify the key shipping route points for transporting {product} from {origin} to {destination}.

        Please provide a list of the most important geographic points, shipping lanes, canals, straits, oceans, seas, 
        and major ports that the product would likely pass through during shipping.

        Format the response as JSON with this structure:
        {{
            "route_points": [
                {{"name": "Point name", "description": "Brief description"}},
                {{"name": "Point name", "description": "Brief description"}},
                ...
            ]
        }}

        Focus on well-known keywords like "Panama Canal", "Suez Canal", "Strait of Malacca", "Pacific Ocean", etc.
        Order the points in the sequence they would be encountered during the journey.
        """

        response = self.model.generate_content(prompt)

        return response.text
