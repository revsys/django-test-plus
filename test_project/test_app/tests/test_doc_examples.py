"""Guards the pytest examples in docs/usage.rst, auth_helpers.rst and
low_query_counts.rst. If you change those examples, change these too.
"""


def test_the_view(tp):
    tp.get("view-context-with")
    tp.response_200()
    tp.assertInContext("testvalue")


def test_auth(tp, db):
    user = tp.make_user("u1")
    tp.assertLoginRequired("view-needs-login")
    with tp.login(user):
        tp.get_check_200("view-needs-login")


def test_auth_methods(tp):
    tp.assertLoginRequired("view-needs-login")
    tp.assertLoginRequired("view-needs-login", method="post")


def test_restrictions(tp, db):
    user1 = tp.make_user("u1")
    with tp.login(user1):
        tp.get("view-needs-login")


def test_better_than_nothing(tp, db):
    tp.assertGoodView("view-200")


def test_query_ctx(tp, db):
    with tp.assertNumQueriesLessThan(7):
        tp.get("view-200")
