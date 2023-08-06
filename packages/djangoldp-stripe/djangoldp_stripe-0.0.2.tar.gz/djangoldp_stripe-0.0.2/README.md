# djangoldp-stripe

A DjangoLDP package supporting Stripe payments. Uses dependency [dj-stripe](https://github.com/dj-stripe/dj-stripe) to achieve much of the functionality, a library for handling Stripe payments in Django

# Requirements

* djangoldp 2.1
* Python 3.6.5

* Requires the installation of a [DjangoLDP server](https://docs.startinblox.com/import_documentation/djangoldp_guide/install-djangoldp-server.html)

* You will need to set up a [Stripe client](https://dashboard.stripe.com/test/dashboard)

# Installation

* You will need to set the following settings to your settings.yml:

```yaml
dependencies:
   # ...
   - djangoldp-stripe

ldp_packages:
   # ...
   - djangoldp_stripe

server:
   # ...
   STRIPE_LIVE_MODE: True  # Should be False when testing, True in production
   DJSTRIPE_USE_NATIVE_JSONFIELD: True  # if using SQLite, set this to False
   DJSTRIPE_FOREIGN_KEY_TO_FIELD: "id"
```

* Set `STRIPE_LIVE_SECRET_KEY` and `STRIPE_TEST_SECRET_KEY` in your OS environment variables where the server is run. These settings will then be securely imported when you next configure. Alternatively, you can add them to the settings.yml:

```yaml
server:
    # ...
    STRIPE_LIVE_SECRET_KEY: ""
    STRIPE_TEST_SECRET_KEY: ""
```

You can find these settings via the [Stripe dashboard](https://dashboard.stripe.com/)

* In the Stripe dashboard, add your first webhook

* In the created webhooks, find your webhook secret, and set this in the OS variable (or server setting) `DJSTRIPE_WEBHOOK_SECRET`. It is a string which will start `whsec_`

* Run `djangoldp install`

* Run `djangoldp configure`

* Run `python manage.py djstripe_sync_models`

## Migrating existing customers

After configuration, you can do this by running:

```
djangoldp configure
python manage.py djstripe_init_customers
python manage.py djstripe_sync_plans_from_stripe
```

## Optional Configuration Options

* `LDP_STRIPE_URL_PATH`: the path where Django Stripe's urls will be accessible. By default `"stripe/"`

# StripeSubscriptionPermissions

This package can be used to provide custom permissions on your models and views. To do this you can use the permissions class `StripeSubscriptionPermissions` or the utility functions in `permissions.py`

* Set up the required product permissions on your model:

```python
class MyModel(Model):
    # ...

    class Meta(Model.Meta):
       # ...
       PERMS_REQUIRED_STRIPE_SUBSCRIPTIONS = ['prod_xxxx',]
```

When applying either the permission class to a `LDPViewSet` or the utility function, you can now control access based on the products a requesting user is subscribed to
