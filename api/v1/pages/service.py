from rest_framework import status
from core.producer import publish


class PageService:
    def __init__(self, page, user=None, unblock_date=None, user_id=None):
        self.user = user
        self.page = page
        self.unblock_date = unblock_date
        self.user_id = user_id

    def deny_follow_request(self, users):
        follow_request = self.page.follow_requests.filter(id__in=users)
        if follow_request:
            publish(method="del_follow_requests", body={"page_id": self.page.uuid, "count": len(follow_request)})
            self.page.follow_requests.remove(*follow_request)
            return status.HTTP_200_OK
        return status.HTTP_400_BAD_REQUEST

    def accept_follow_request(self, users):
        follow_request = self.page.follow_requests.filter(id__in=users)
        if follow_request:
            publish(body={"page_id": self.page.uuid, "count": len(follow_request), "method": "add_followers"})
            publish(body={"page_id": self.page.uuid, "count": len(follow_request), "method": "del_follow_requests"})
            self.page.follow_requests.remove(*follow_request)
            self.page.followers.add(*follow_request)
            return status.HTTP_200_OK
        return status.HTTP_400_BAD_REQUEST

    def start_follow(self):
        if self.is_user_follower() or self.is_user_send_follow_request():
            return "You are already sent follow request or you are already in followers"
        if self.user == self.page.owner:
            return "Your are the owner of this page, You cant follow your own page"
        if self.page.is_private:
            self.page.follow_requests.add(self.user)
            publish(body={"page_id": self.page.uuid,
                                                        "count": 1,
                                                        "method": "add_follow_requests"})
            return "You are in follow requests"
        else:
            publish(body={"page_id": self.page.uuid,
                                                  "count": 1,
                                                  "method": "add_followers"})
            self.page.followers.add(self.user)
            return "You are in followers"

    def stop_follow(self):
        if self.is_user_follower():
            self.page.followers.remove(self.user)
            publish(body={"page_id": self.page.uuid,
                                                  "count": 1,
                                                  "method": "del_followers"})
            return "You're not in followers"
        if self.is_user_send_follow_request():
            self.page.follow_requests.remove(self.user)
            publish(body={"page_id": self.page.uuid,
                                                        "count": 1,
                                                        "method": "del_follow_requests"})
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
