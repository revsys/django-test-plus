def test_something(tp):
    response = tp.get('view-200')
    assert response.status_code == 200
