from jacare.models import CustomerReviews
from business.tests.conftest import RestaurantFactory
from user.tests.conftest import UserFactory
import factory


class CustomerReviewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerReviews
    
    user_id = factory.SubFactory(UserFactory)
    restaurant_id = factory.SubFactory(RestaurantFactory)
    data = factory.Faker('pydict', value_types=(str, int, float))

