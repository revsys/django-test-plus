import factory.django
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """Used by the test_plus_user_factory pytest option tests."""

    username = factory.Sequence(lambda n: f"factoryuser{n}")
    email = factory.Sequence(lambda n: f"factoryuser{n}@example.com")

    class Meta:
        model = User
