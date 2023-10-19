from request import Request

class UpdateRequest(Request):
    def __init__(self, request_type, request_data, database_type):
        super().__init__(request_type, request_data)
        self.database_type = database_type
        
        def do_operation():
            pass