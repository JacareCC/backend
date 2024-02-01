from pytest_factoryboy import register

from .factories import RestaurantFactory, TierRewardFactory, RegistrationRequestFactory

register(RestaurantFactory)
register(TierRewardFactory)
register(RegistrationRequestFactory)