"""
edx_braze Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins.constants import PluginSettings, PluginSignals


class EdxBrazeConfig(AppConfig):
    """
    Configuration for the edx_braze Django application.
    """

    name = 'edx_braze'

    plugin_app = {
        PluginSettings.CONFIG: {
            'lms.djangoapp': {
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
                'production': {
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
            }
        },
        PluginSignals.CONFIG: {
            'lms.djangoapp': {
                PluginSignals.RECEIVERS: [
                    {
                        PluginSignals.SIGNAL_PATH: 'openedx.core.djangoapps.user_authn.views.register.REGISTER_USER',
                        PluginSignals.RECEIVER_FUNC_NAME: 'identify_user_upon_registration',
                    },
                ],
            },
        },
    }
