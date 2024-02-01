import factory
from user.models import User, UserTier, Points, VisitedHistory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    user_uid = factory.Sequence(lambda n: "test_%d" % n)
    email = "test@test.com"
    birthday = birthday = factory.Faker('date_of_birth')

    _ITERATOR_VALUE = 1 

class VisitedHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VisitedHistory
    
    user_id = factory.SubFactory(UserFactory)
    restaurant_id = factory.SubFactory("business.tests.factories.RestaurantFactory")

class PointsFactory(factory.django.DjangoModelFactory):
    class Meta: 
        model = Points
    
    user_id = factory.SubFactory(UserFactory)
    value = 1




