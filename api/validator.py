class Validator:
    def __init__(self, request):
        self.request = request

    def redflag_is_valid(self):
        try:
            redflag = self.request.get_json()
            self.ensure_no_empty_fields(redflag)
            self.ensure_valid_data_types(redflag)
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields(self, redflag):
        # assert 'createdOn' in redflag, 'createdOn field not specified.'
        assert 'createdBy' in redflag, 'createdBy field not specified.'
        assert 'types' in redflag, 'types field not specified.'
        assert 'location' in redflag, 'location field not specified.'
        assert 'images' in redflag, 'images field not specified.'
        assert 'videos' in redflag, 'videos field not specified.'
        assert 'comment' in redflag, 'comment field not specified.'

    def ensure_valid_data_types(self, redflag):
        assert isinstance(redflag['createdBy'], int), (
            'createdBy should be an integer'
        )

    def validate_user_data(self):
        try:
            user_data = self.request.get_json()
            assert isinstance(user_data, dict),'Ensure to enter registration details in json format'
            self.ensure_no_empty_fields_user(user_data)
            self.ensure_items_correct_datatype(user_data)
            return True
        except Exception as e:
            self.error = str(e)
            return False

    def ensure_no_empty_fields_user(self, user_data):
        assert 'firstname' in user_data, 'Firstname not specified'
        assert 'lastname' in user_data, 'lastname not specified'
        assert 'firstname' in user_data, 'firstname not specified'
        assert 'email' in user_data, 'Please provide an email'
        assert 'phoneNumber' in user_data, 'phoneNumber not specified'
        assert 'username' in user_data, 'username not specified'
        assert 'password' in user_data, 'password not specified'

    def ensure_items_correct_datatype(self, user_data):
        assert isinstance(user_data["phoneNumber"], str), 'phoneNumber should be a string!'
        assert isinstance(user_data["email"], str), 'Email should be a string!!'
        assert isinstance(user_data["username"], str), 'Username should be a string'
        assert isinstance(user_data["firstname"], str), 'Firstname should be a string!!'
        assert isinstance(user_data["lastname"], str), 'Lastname should be string'
        assert isinstance(user_data["othernames"], str), 'Othernames should be a string'



    # def user_not_exist(self, id):
    #     user = self.request.get_json()


        