"""
edx_braze production settings.
"""


def plugin_settings(settings):
    """Simply map environment variables to settings values."""
    settings.EDX_BRAZE_API_KEY = settings.ENV_TOKENS.get('EDX_BRAZE_API_KEY')
    settings.EDX_BRAZE_API_SERVER = settings.ENV_TOKENS.get('EDX_BRAZE_API_SERVER')
