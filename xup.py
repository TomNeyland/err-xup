from errbot import BotPlugin, botcmd
from errbot.utils import get_sender_username
from datetime import datetime
import ago


class Xup(BotPlugin):
    min_err_version = '1.6.0' # Optional, but recommended
    #max_err_version = '2.0.0' # Optional, but recommended

    def activate(self):
        super(Xup, self).activate()

        if not hasattr(self.shelf, 'users'):
            self['users'] = {}

    @botcmd(split_args_with=None)
    def xup(self, mess, args):
        """Add yourself to the ready list, you can include an optional message."""

        user = get_sender_username(mess)
        xup_args = {'user': user, 'args': args, 'message': mess.getBody(), 'time': datetime.utcnow()}

        self['users'][user] = xup_args

        return "Done."

    @botcmd(template="xup_list")
    def xup_list(self, mess, args):
        """Show everyone who is on the ready list."""
        now = datetime.utcnow()

        members = self['users'].values()

        members = sorted(members, key=lambda member: member['time'])

        for member in members:
            if ((now - member['time']).seconds//3600) < 2:
                member['message'] = " ".join(member['args'])
                member['time_ago'] = ago.human(now - member['time'], 1)

        return {'members': members}

    @botcmd(split_args_with=None)
    def xup_ping(self, mess, args):
        """Ping everyone who has xed-up"""
        return " ".join(sorted(self['users'].keys()))

    @botcmd(split_args_with=None)
    def xup_remove(self, mess, args):
        """Remove yourself from the ready list"""
        user = get_sender_username(mess)

        del self['users'][user]

        return "Done."
