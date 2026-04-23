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
        rating_c = 60
        rating_o = provider.overall_rating
    elif provider.overall_rating >= 3.5:
        rating_o = provider.overall_rating
        rating_c = 60
    else:
        rating_c = 60
        rating_o = 3.5
    
    # Calculate expertise score

    expertise_score += rating_c * (rating_o / 5.0)
    
    expertise_score += provider.badge_count * 0.5

    # Rating score based on price range
    if provider.price_range[1] <= user_needs.user_price_range[1]:
        pricing_score = 1.5    
    elif provider.price_range[1] > user_needs.user_price_range[1]:
        pricing_score = 1.0 
    
    if provider.price_range[0] <= user_needs.user_price_range[0]:
        pricing_score += 1.5
    elif provider.price_range[0] > user_needs.user_price_range[0]:
        pricing_score += 1.0


    # Combine scores with weights
    score += expertise_score/10.0 - user_needs.user_expertise
    if score < 0.0:
        score = 0.0
    score += pricing_score

    if score > 10.0:
        score = 10.0    

    # Additional scoring logic can be added here based on other factors
    return score

# Example usage
user_needs = UserNeeds()
user_needs.user_expertise = 4.0
user_needs.user_price_range = (800, 1000)

providers = []
providers_scores = []

for i in range(25):
    provider = Provider()
    
    provider.overall_rating = round(float(random.uniform(0.0, 5.0)), 2)
    
    provider.rating_count = random.randint(0, 150)
    
    provider.badge_count = random.randint(0, 5)
    
    low = random.randint(400, 1250)
    high = random.randint(650, 2500)

    if low > high:
        low, high = high, low
    
    provider.price_range = (low, high)

    providers.append(provider)
    providers_scores.append(calculate_provider_score(provider, user_needs))

providers_with_scores = list(zip(providers, providers_scores))
providers_with_scores.sort(key=lambda x: x[1], reverse=True)

for i, (provider, score) in enumerate(providers_with_scores):
    print(f"Provider {i+1} with rating {provider.overall_rating}, rating count {provider.rating_count}, badge count {provider.badge_count}, price range {provider.price_range} has a score of {score:.2f}")


