from jacare.models import CustomerReviews
import factory


class CustomerReviewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomerReviews
    
    user_id = factory.SubFactory("user.tests.factories.UserFactory")
    restaurant_id = factory.SubFactory("business.tests.factories.RestaurantFactory")
    data = factory.Faker('pydict', value_types=(str, int, float))

