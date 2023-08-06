"""
edx_braze signals.
"""

import logging

import requests
from django.conf import settings

log = logging.getLogger(__name__)


def identify_user_upon_registration(user=None, **_kwargs):
    """
    Identify any alias-only users with the now-real user in Braze.
    """
    try:
        braze_api_key = settings.EDX_BRAZE_API_KEY
        braze_api_server = settings.EDX_BRAZE_API_SERVER
        if not braze_api_key or not braze_api_server or not user:
            return

        response = requests.post(
            url=f'{braze_api_server}/users/identify',
            headers={'Authorization': f'Bearer {braze_api_key}'},
            json={
                'aliases_to_identify': [
                    # This hubspot alias is defined in 'hubspot_leads.py' in the edx-prefectutils repo
                    {
                        'external_id': str(user.id),
                        'user_alias': {
                            'alias_label': 'hubspot',
                            'alias_name': user.email,
                        },
                    },
                    # This enterprise alias is used for Pending Learners before they activate their accounts,
                    # see the license-manager repo event_utils.py file and the ecommerce Braze client files
                    {
                        'external_id': str(user.id),
                        'user_alias': {
                            'alias_label': 'Enterprise',
                            'alias_name': user.email,
                        },
                    },
                    # This alias is used for anonymous users who interact with "save for later" feature
                    # introduced on prospectus
                    {
                        'external_id': str(user.id),
                        'user_alias': {
                            'alias_label': 'save_for_later',
                            'alias_name': user.email,
                        },
                    }
                ],
            },
        )

        # Throw exception which should alert us if things go wrong.
        # Note that this request does not return an error status if the user alias merely doesn't exist, this is for
        # when something truly bad has happened.
        response.raise_for_status()
    except Exception:  # pylint: disable=broad-except
        # Broad except because we definitely don't want to interrupt registration.
        # Just log it.
        log.exception('Could not identify hubspot-alias in Braze for new user')
