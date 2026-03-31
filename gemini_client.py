import os
import google.generativeai as genai

class GeminiClient:
    def __init__(self, api_key: str = None):
        # Use the provided key if not found in environment
        key = api_key or os.environ.get("GEMINI_API_KEY", "ENTER_YOUR_API_HERE")
        if not key:
            raise ValueError("GEMINI_API_KEY environment variable is not set. Please set it to use the Gemini features.")
        genai.configure(api_key=key)
        # Using Gemini 1.5 Flash
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        
    def interpret_patient_data(self, decrypted_patient_record: dict) -> str:
        """Provides a medical interpretation of a single patient record securely."""
        try:
            # Hide huge base64 strings from text payload to prevent token bloat
            clean_record = {k: v for k, v in decrypted_patient_record.items() if k not in ["attached_file_b64", "attached_mime"]}
            
            prompt = f"""
            You are an expert AI clinical assistant. Below is a securely passed patient record.
            Analyze this patient's data, highlight any critical areas of concern, and provide general 
            medical interpretation without diagnosing or prescribing. 
            
            Patient Data: {clean_record}
            """
            
            contents = [prompt]
            
            if "attached_file_b64" in decrypted_patient_record and "attached_mime" in decrypted_patient_record:
                import base64
                b64_string = decrypted_patient_record["attached_file_b64"]
                mime_type = decrypted_patient_record["attached_mime"]
                raw_bytes = base64.b64decode(b64_string)
                
                # Appending inline data representation for Gemini
                contents.append({
                    "mime_type": mime_type,
                    "data": raw_bytes
                })

            response = self.model.generate_content(contents)
            return response.text
        except Exception as e:
            return f"Error connecting to Gemini 1.5 Flash: {str(e)}"
            
    def interpret_aggregate_stats(self, dp_stats_summary: str) -> str:
        """Interprets anonymized, differentially private demographic/population health stats."""
        prompt = f"""
        You are an epidemiological AI assistant. Review the following summary of public health/demographic
        statistics that have been protected using Differential Privacy (noise has been added for anonymity).
        
        Provide an interpretation of these trends, noting that these are high-level, differentially private aggregates.
        
        DP Statistics: {dp_stats_summary}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error connecting to Gemini 1.5 Flash: {str(e)}"
