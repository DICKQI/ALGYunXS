from .bashInfo.login_and_logout import BaseViews
from .bashInfo.register import RegisterView
from .userInfo.send_email import SendView
from .userInfo.reset_password import ResetView
from .userInfo.userInfo import UserDashBoardView
from .userInfo.user_detail import MeView
from .userInfo.user_visit_log import UserLogView
from .roleInfo.active_user import ActiveView

__all__ = [
    'BaseViews', 'UserDashBoardView', 'MeView', 'RegisterView', 'SendView', 'ActiveView', 'ResetView', 'UserLogView'
]
