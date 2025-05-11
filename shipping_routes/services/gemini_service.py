import os
import google.generativeai as genai


class GeminiService:
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def get_shipping_route_points(self, origin, destination, product):
        prompt = f"""
        I need to identify the exact shipping route points for transporting {product} from {origin} to {destination}.

        DO NOT provide generic descriptions like "Major port in [Country]". Instead, select the MOST LIKELY SPECIFIC ports, airports, or transit points based on standard shipping routes for this type of product.

        For the origin and destination points especially, you MUST select a specific named port or airport - not a generic description.

        Please determine:
        1. The most appropriate transportation method for {product} (sea freight, air freight, or multimodal)
        2. The specific starting port/airport in {origin} (select the single most appropriate one)
        3. The specific destination port/airport in {destination} (select the single most appropriate one)
        4. All major transit points along the route

        Format the response as JSON with this structure:
        {{
            "transport_method": "sea freight|air freight|multimodal",
            "route_points": [
                {{
                    "name": "Exact facility name",
                    "description": "Brief description including why this specific point was selected",
                    "type": "origin|transit|destination",
                    "location": {{
                        "country": "Country name",
                        "city": "City name"
                    }}
                }},
                ...
            ]
        }}

        For example, use "Port of Shanghai" rather than "Major Chinese Port", or "Port of Rotterdam" rather than "Major European Port".

        Focus on well-known, specific locations that would be easily identifiable in news and reports about disruptions. Order the points in the sequence they would be encountered during the journey.
        """

        response = self.model.generate_content(prompt)

        return response.text
