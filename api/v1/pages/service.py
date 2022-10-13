from rest_framework import status

from user.models import User


class PageService:
    def __init__(self, page, user=None, unblock_date=None, user_id=None):
        self.user = user
        self.page = page
        self.unblock_date = unblock_date
        self.user_id = user_id

    def deny_follow_request(self, users):
        follow_requests = list(self.page._prefetched_objects_cache.get("follow_requests"))
        follow_request = [item for item in follow_requests if item.id in users]
        for i in follow_request:
            self.page.follow_requests.remove(i)
        if follow_request:
            return status.HTTP_200_OK
        return status.HTTP_400_BAD_REQUEST

    def accept_follow_request(self, users):
        follow_requests = list(self.page._prefetched_objects_cache.get("follow_requests"))
        follow_request = [item for item in follow_requests if item.id in users]
        for i in follow_request:
            self.page.follow_requests.remove(i)
            self.page.followers.add(i)
        if follow_request:
            return status.HTTP_200_OK
        return status.HTTP_400_BAD_REQUEST

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

    def is_user_follower(self):
        return self.page.followers.filter(id=self.user_id).exists()

    def is_user_send_follow_request(self):
        return self.page.follow_requests.filter(id=self.user_id).exists()

