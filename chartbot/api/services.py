import infermedica_api
from django.conf import settings

class InfermedicaService:
    def __init__(self):
        self.api = infermedica_api.API(
            app_id=settings.INFERMEDICA_APP_ID,
            app_key=settings.INFERMEDICA_APP_KEY
        )
    
    def analyze_symptoms(self, symptoms):
        request = infermedica_api.Diagnosis(
            sex='male',  # Default value, should be provided by user
            age=30,     # Default value, should be provided by user
        )
        
        for symptom in symptoms:
            request.add_symptom(symptom['id'], symptom['choice_id'])
            
        return self.api.diagnosis(request)
    
    def get_symptom_details(self, symptom_id):
        return self.api.symptom_details(symptom_id)