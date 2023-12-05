import factory
from user.models import User, UserTier, Points, VisitedHistory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    user_uid = "test_uid"
    email = "test@test.com"
    birthday = birthday = factory.Faker('date_of_birth')

class VisitedHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VisitedHistory
    
    user_id = factory.SubFactory(UserFactory)
    restaurant_id = factory.SubFactory("business.tests.factories.RestaurantFactory")





