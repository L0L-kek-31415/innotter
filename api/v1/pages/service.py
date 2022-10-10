class PageActions:
    def __init__(self, page, user=None, unblock_date=None):
        self.user = user
        self.page = page
        self.unblock_date = unblock_date

    def start_follow(self):
        if self.is_user_follower() or self.is_user_send_follow_request():
            return "You are already sent follow request"
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
        return self.page.followers.filter(id=self.user.id).exists()

    def is_user_send_follow_request(self):
        return self.page.follow_requests.filter(id=self.user.id).exists()
