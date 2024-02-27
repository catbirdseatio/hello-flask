class TestUser:
    def test_new_user(self, new_user):
        assert new_user.email == "roderick@email.com"
        assert new_user.password_hashed != "testpass1234"
    
    def test_new_user_password_correct(self, new_user):
        assert new_user.is_password_correct("testpass1234")
    
    def test_new_user_password_incorrect(self, new_user):
        assert not new_user.is_password_correct("FakePasswerd")