from db import collection

class GPTServiceMixin:
    @classmethod
    def get_keywords(cls, text):
        pass
    
class RegisterService():
    @classmethod
    def get_user_by_id(cls, user_tg_id):
        user = collection.find_one("user_id", user_tg_id)
        return user
        
    @classmethod
    def create_user(cls, user_data):
        #Get keywords by GPT here soon
        collection.insert_one(user_data)
        
class SearchService(GPTServiceMixin):
    pass