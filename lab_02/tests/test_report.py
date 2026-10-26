from streamstats.report import sort_for_sorted


# проверка, что при одинаковых errors будет правильная сортировка
def test_sorted_determin():
    """
    детерминированной сортировка - проверка
    """
    # у web и api 2 ошибки, db - 0
    data = [
        ("web", {"total": 5, "errors": 2}),
        ("api", {"total": 10, "errors": 2}),
        ("db", {"total": 1, "errors": 0}),
    ]

    sorted_data = sorted(data, key=sort_for_sorted)

    assert sorted_data[0][0] == "api"

    assert sorted_data[1][0] == "web"

    assert sorted_data[2][0] == "db"
