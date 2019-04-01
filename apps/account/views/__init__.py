from .bashInfo.login_and_logout import BaseViews
from .bashInfo.register import RegisterView
from .userInfo.reset_password import ResetView
from .userInfo.userInfo import UserDashBoardView
from .userInfo.user_detail import MeView
from .userInfo.user_visit_log import UserLogView
from .userInfo.userEsCheck import ESCheckView
from .roleInfo.active_user import ActiveView
from .roleInfo.send_email import SendView
from .Notification.notificationInfo import NotificationView

__all__ = [
    'BaseViews', 'UserDashBoardView', 'MeView', 'RegisterView', 'SendView', 'ActiveView', 'ResetView', 'UserLogView',
    'ESCheckView', 'NotificationView'
]
