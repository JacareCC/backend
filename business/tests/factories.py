import factory
from business.models import Restaurant, TierReward, RegistrationRequests
from user.tests.factories import UserFactory

class RestaurantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Restaurant
    place_id = "test_place_id"
    business_name = "test restaurant"
    owner_user_id = factory.SubFactory(UserFactory)

class TierRewardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TierReward
    
    restaurant_id = factory.SubFactory(RestaurantFactory)
    reward_level = 'bronze'
    reward_description = 'free drink'
    points_required = 10

class RegistrationRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RegistrationRequests
    
    user_id = factory.SubFactory(UserFactory)
    first_name = 'test'
    last_name = 'test'
    email = 'test@test.com'
    business_name = 'test restaurant'
    contact_person = 'John Doe'
    address = '123 test st'
    phone_number = "00000000000"
