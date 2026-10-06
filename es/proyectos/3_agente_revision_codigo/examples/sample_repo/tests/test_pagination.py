from app.pagination import paginate


def test_first_page():
    assert paginate(list(range(10)), 1, 3) == [0, 1, 2]
