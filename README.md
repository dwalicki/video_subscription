# Video Subscription Service

User

## Content via Vimeo

Video
    - vimeo_id

Content
    - content: video /
    - data:
        video: { vimeo_video_id: 12345678 }
    - Pricing (ManyToMany)

## Subscription via Stripe

Pricing
    - price per month
    - currency
    - id
    - name (base/pro/enterprise)

Merchant / Subscription
    - User (FK)
    - stripe_subscription_id
    - status (active / canceled / past_due / trialing )
    - pricing options (FK)

## Export Env Variable
export DJANGO_READ_DOT_ENV_FILE=True
