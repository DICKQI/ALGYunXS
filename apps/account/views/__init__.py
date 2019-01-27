from .register import RegisterView
from .login_and_logout import LoginViews
from .send_email import SendView
from .active_user import ActiveView
from .userInfo import UserDashBoardView
from .reset_password import ResetView
from .user_detail import MeView

__all__ = [
    'LoginViews', 'UserDashBoardView', 'MeView', 'RegisterView', 'SendView', 'ActiveView', 'ResetView'
]