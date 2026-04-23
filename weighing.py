import datetime as dt
import random

class Provider:
    overall_rating = 0.0
    rating_count = 0
    badge_count = 0
    price_range = (0, 0)

class UserNeeds:
    user_expertise = 0
    user_price_range = (0, 0)
    user_due_date = dt.datetime.now()

def calculate_provider_score(provider: Provider, user_needs: UserNeeds) -> float:
    # Placeholder for the actual scoring logic
    expertise_score = 0.0
    pricing_score = 0.0
    score = 0.0

    # Rating score based on overall rating and rating count
    rating_c = 0
    rating_o = 0.0

    if provider.rating_count >= 100:
        rating_c = 100
        rating_o = provider.overall_rating
    elif provider.rating_count > 75 and provider.rating_count < 100:
        rating_c = 90
        rating_o = provider.overall_rating
    elif provider.rating_count > 25 and provider.rating_count < 75:
        rating_c = 70
        rating_o = provider.overall_rating
    elif provider.rating_count > 10 and provider.rating_count < 25:
        rating_c = 50
        rating_o = provider.overall_rating
    else:
        rating_o = 2.5
        rating_c = 40
    
    # Calculate expertise score

    expertise_score += rating_c * (rating_o / 5.0)
    
    expertise_score += provider.badge_count * 0.5

    # Rating score based on price range
    if provider.price_range[1] <= user_needs.user_price_range[1]:
        pricing_score = 5.0    
    elif provider.price_range[1] > user_needs.user_price_range[1]:
        pricing_score = 2.5 
    
    if provider.price_range[0] <= user_needs.user_price_range[0]:
        pricing_score += 5.0
    elif provider.price_range[0] > user_needs.user_price_range[0]:
        pricing_score += 2.5


    # Combine scores with weights
    score += abs(user_needs.user_expertise - expertise_score)
    score += pricing_score * 0.3

    if user_needs.user_due_date < dt.datetime.now() + dt.timedelta(days=3):
        score += 5.0  # Higher score for providers that can meet tight deadlines
    elif user_needs.user_due_date < dt.datetime.now() + dt.timedelta(days=7):
        score += 3.0  # Moderate score for providers that can meet medium deadlines
    else:
        score += 1.0  # Lower score for providers that cannot meet the deadline

    # Additional scoring logic can be added here based on other factors
    return score

# Example usage
user_needs = UserNeeds()
user_needs.user_expertise = 4.0
user_needs.user_price_range = (1000, 3000)
user_needs.user_due_date = dt.datetime.now() + dt.timedelta(days=6)

providers = []
providersScores = []

for i in range(100):
    provider = Provider()
    provider.overall_rating = random.uniform(1.0, 5.0)
    provider.rating_count = random.randint(0, 150)
    provider.badge_count = random.randint(0, 5)
    provider.price_range = (random.randint(500, 2000), random.randint(1500, 5000))

    providers.append(provider)
    providersScores.append(calculate_provider_score(provider, user_needs))

providers_with_scores = list(zip(providers, providersScores))
providers_with_scores.sort(key=lambda x: x[1], reverse=True)

for provider, score in providers_with_scores[:10]:  # Top 10 providers
    print(f"Provider: {provider}, Score: {score}")



