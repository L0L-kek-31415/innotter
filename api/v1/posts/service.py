from main.models import Page


class PostService:
    def __init__(self, post, user=None):
        self.post = post
        self.user = user

    @staticmethod
    def check_page_owner(page_id, user_id):
        page_owner_id = Page.objects.get(id=page_id).owner.id
        if user_id == page_owner_id:
            return True
        return False

    def add_like(self):
        if self.is_like_from_user_exist():
            return "This post already has your Like"
        else:
            self.post.like.add(self.user)
            return "Like has been added"

    def remove_like(self):
        if self.is_like_from_user_exist():
            self.post.like.remove(self.user)
            return "Like has been removed"
        else:
            return "This post does not have your Like"

    def is_like_from_user_exist(self, user_id=None):
        if user_id is None:
            user_id = self.user.id
        return self.post.like.filter(id=user_id).exists()