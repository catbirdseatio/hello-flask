class TestErrorPages:
    def test_error_403(self, client):
        response = client.get("/admin")
        assert response.status_code == 403

    def test_error_404(self, client):
        response = client.get("/green")
        assert response.status_code == 404

    def test_error_405(self, client):
        response = client.post("/")
        assert response.status_code == 405

    def test_error_500(self, client):
        response = client.get("/error")
        assert response.status_code == 500
