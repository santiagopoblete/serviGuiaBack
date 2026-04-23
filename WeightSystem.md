# Weight System for Provider Matching
For the ServiGuia app we need to define a system for weighing providers and giving a desired weight to the needs of the user.

## Variables
We have identified the next weighable variables.

- user_expertise: Integer ranging from 0 to 10. Level of expertise that user is looking for.

- overall_rating: Float ranging from 0.0 to 5.0, when rating count is 0 it defaults to 3.5 (not viewable in front, only used for calculations in the Backend).

- rating_count: Integer that represents the ammount of user reviews.

- badge_count: Integer that represents count of badges obtained by provider from user reviews.

- user_price_range: [u_price_from, u_price_to] 

- price_range: [price_from, price_to]

- user_due_date : The date in which the user expects the task to be finalized. 

- currently_available : Is the selected provider available in the requested time frame? If not, weight is multiplied by 0.5, otherwise 1.0