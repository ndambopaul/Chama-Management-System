from django.urls import path


from users.views import (
    user_login,
    user_logout,
    members,
    new_member,
    edit_member,
    delete_member,
    member_details,
)

urlpatterns = [
    # User Authentication URLS
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    # Members Urls
    path("members/", members, name="members"),
    path("<int:member_id>/", member_details, name="member-details"),
    path("new-member/", new_member, name="new-member"),
    path("edit-member/", edit_member, name="edit-member"),
    path("delete-member/", delete_member, name="delete-member"),
]
