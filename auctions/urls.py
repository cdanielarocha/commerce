from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create2", views.create, name="create"),
    path("create", views.loadFormCreate, name="createForm"),
    path("listing/<str:id>", views.listing_view, name="listing_view"),
    path("remove/<str:id>", views.removeWatchlist, name="removeWatchlist"),
    path("add/<str:id>", views.addWatchlist, name="addWatchlist"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("close/<str:id>", views.close, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"), 
    path("categories/<str:name>", views.listingInCat, name="listingInCat")
]
