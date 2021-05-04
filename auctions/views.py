from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime

from .models import User, Category, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html",{
        "listings":listings        
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def loadFormCreate(request):
    categories = Category.objects.all()
    return render(request, "auctions/create.html", {
            "categories": categories
        })

@login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        photo = request.POST["photo"]
        description = request.POST["description"]
        price = request.POST["price"]
        available = True
        seller = request.user
        print(title,category,photo,description,available, price,seller)
        ins = Listing(title = title, category = category, photo = photo, description = description, price = price, available = available, seller = seller)
        ins.save()
    return HttpResponseRedirect(reverse("createForm"))

def listing_view(request, id):
    listing = Listing.objects.get(pk = id)
    inWatchlist = listing.wachtlist.all()
    seller = listing.seller
    isAvailable = listing.available
    buyer = winner(id)
    comments = Comment.objects.filter(listing=listing).all() 
    return render(request, "auctions/listing.html", {
            "listing" : listing,
            "inWatchlist" : inWatchlist,
            "seller": seller,
            "isAvailable" : isAvailable,
            "buyer" : buyer,
            "comments" : comments
        })

@login_required
def watchlist(request):
    user = request.user
    print(user)
    listings = Listing.objects.filter(wachtlist=user).all()
    print(listings)
    return render(request, "auctions/watchlist.html", {
            "listings" : listings
        })

def categories(request):
    categoryList = Category.objects.all()
    print(categoryList)
    return render(request, "auctions/categories.html", {
            "categoryList" : categoryList
        })

@login_required
def removeWatchlist(request, id):
    listing=Listing.objects.get(pk=id)
    listing.wachtlist.remove(request.user)
    return HttpResponseRedirect(reverse("listing_view", args=[str(id)]))

@login_required
def addWatchlist(request, id):
    listing=Listing.objects.get(pk=id)
    listing.wachtlist.add(request.user)
    return HttpResponseRedirect(reverse("listing_view", args=[str(id)]))

def newPrice(newprice, id):
    listing = Listing.objects.get(pk=id)
    listing.price = newprice
    listing.save() 

@login_required
def bid(request, id):
    price = int(request.POST['price'])
    listing = Listing.objects.get(pk=id)
    isAvailable = listing.available
    comments = Comment.objects.filter(listing=listing).all()
    if (price > listing.price):
        date = datetime.datetime.now()
        buyer = request.user
        ins = Bid(price=price, date=date, buyer=buyer, listing=listing)        
        ins.save()
        newPrice(price, id)
        return HttpResponseRedirect(reverse("listing_view", args=[str(id)]))
    else:
        return render(request, "auctions/listing.html", {
                "message": "Error. The bid must be greater than the price",
                "listing" : listing,
                "isAvailable" : isAvailable,
                "comments": comments
            })

@login_required
def close(request, id):
    listing = Listing.objects.get(pk = id)
    seller = listing.seller
    user=request.user
    if (user==seller):
        listing = Listing.objects.get(pk=id)
        listing.available = False
        listing.save() 
    return HttpResponseRedirect(reverse("listing_view", args=[str(id)])) 

def winner(id):
    listing = Listing.objects.get(pk=id)
    if (listing.available == False):
        buyer = Bid.objects.filter(listing=listing).last().buyer
        return buyer

@login_required
def comment(request, id):
    if request.method == "POST":
        text = request.POST["text"]
        user = request.user
        listing=Listing.objects.get(pk=id)
        print(text,listing,user)
        ins = Comment(text=text, listing=listing, user=user)        
        ins.save()
    return HttpResponseRedirect(reverse("listing_view", args=[str(id)]))

def listingInCat(request,name):
    print(name)
    id = Category.objects.get(name=name).id
    print(id)
    listings = Listing.objects.filter(category=id).all()
    return render(request, "auctions/listingInCat.html", {
            "listings" : listings,
            "category" : name
        })