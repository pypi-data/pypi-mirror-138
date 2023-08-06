
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.activity_api import ActivityApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from traq.api.activity_api import ActivityApi
from traq.api.authentication_api import AuthenticationApi
from traq.api.bot_api import BotApi
from traq.api.channel_api import ChannelApi
from traq.api.clip_api import ClipApi
from traq.api.file_api import FileApi
from traq.api.group_api import GroupApi
from traq.api.me_api import MeApi
from traq.api.message_api import MessageApi
from traq.api.notification_api import NotificationApi
from traq.api.oauth2_api import Oauth2Api
from traq.api.ogp_api import OgpApi
from traq.api.pin_api import PinApi
from traq.api.public_api import PublicApi
from traq.api.stamp_api import StampApi
from traq.api.star_api import StarApi
from traq.api.user_api import UserApi
from traq.api.user_tag_api import UserTagApi
from traq.api.webhook_api import WebhookApi
from traq.api.webrtc_api import WebrtcApi
