def add_block(page, date):
    page.unblock_date.update(date)


def is_user_follower(user, page):
    return page.followers.get(id=user.id).exists()


def is_user_send_follow_request(user, page):
    return page.follow_requests.get(id=user.id).exists()


def del_user_from_followers(user, page):
    page.followers.filter(id=user.id).delete()


def del_user_from_follow_request(user, page):
    page.follow_requests.filter(id=user.id).delete()


def add_user_to_follow_request(user, page):
    page.follow_requests.add(user)


def add_user_to_followers(user, page):
    page.followers.add(user)
