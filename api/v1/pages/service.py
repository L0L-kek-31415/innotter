from user.models import User


class PageService:
    def __init__(self, page, user=None, unblock_date=None):
        self.user = user
        self.page = page
        self.unblock_date = unblock_date

    def deny_follow_request(self, users):
        message = []
        for id_user in users:
            try:
                user = User.objects.get(id=id_user)
            except User.DoesNotExist:
                message.append(f"User {id_user} does not exist")
            else:
                if self.is_user_send_follow_request(user.id):
                    self.page.follow_requests.remove(user)
                    message.append(f"User {user.id} was removed from follower requests")
                elif self.is_user_follower(user.id):
                    self.page.followers.remove(user)
                    message.append(f"User {user.id} was removed from followers")
                else:
                    message.append(f"User {user.id} does not send follow request")
        return message

    def accept_follow_request(self, users):
        message = []
        for id_user in users:
            try:
                user = User.objects.get(id=id_user)
            except User.DoesNotExist:
                message.append(f"User {id_user} does not exist")
            else:
                if self.is_user_send_follow_request(user.id):
                    self.page.follow_requests.remove(user)
                    self.page.followers.add(user)
                    message.append(f"User {user.id} was added to followers")
                elif self.is_user_follower(user.id):
                    message.append(f"User {user.id} is already in your followers")
                else:
                    message.append(f"User {user.id} does not send follow request")
        return message

    def start_follow(self):
        if self.is_user_follower() or self.is_user_send_follow_request():
            return "You are already sent follow request or you are already in followers"
        if self.user == self.page.owner:
            return "Your are the owner of this page, You cant follow your own page"
        if self.page.is_private:
            self.page.follow_requests.add(self.user)
            return "You are in follow requests"
        else:
            self.page.followers.add(self.user)
            return "You are in followers"

    def stop_follow(self):
        if self.is_user_follower():
            self.page.followers.remove(self.user)
            return "You're not in followers"
        if self.is_user_send_follow_request():
            self.page.follow_requests.remove(self.user)
            return "You're not in follow requests"
        return "You're not in followers/follow requests"

    def block_page(self):
        self.page.unblock_date = self.unblock_date
        self.page.save()
        return f"Unblock date - {self.page.unblock_date}"

    def is_user_follower(self, user_id=None):
        if user_id is None:
            user_id = self.user.id
        return self.page.followers.filter(id=user_id).exists()

    def is_user_send_follow_request(self, user_id=None):
        if user_id is None:
            user_id = self.user.id
        return self.page.follow_requests.filter(id=user_id).exists()

