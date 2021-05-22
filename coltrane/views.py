from django.shortcuts import render
from django.shortcuts import get_object_or_404, render_to_response
from coltrane.models import Entry, Category, Comments, User_Likes, User_Profile, Hashtag
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import datetime

# create forms for database model
from forms import EntryForm, CommentForm, User_ProfileForm, EntryFormText, EntryFormURL
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# user login csrf token
from django.template import RequestContext

from tagging.models import Tag, TaggedItem


# a view is simply a Python function that accepts an HttpRequest object, and returns an HttpResponse object.


def home_page(request):
    return HttpResponseRedirect('/weblog/')


def password_reset(request):
    return render_to_response('coltrane/forgot.html')


def send_password(request):
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['entry1'] = Entry.objects.all()
    args['tag_list'] = Hashtag.objects.all()
    args['category_list'] = Category.objects.all()
    args['recent'] = Hashtag.objects.order_by('-last_used')[:10]
    args['most_used'] = Hashtag.objects.order_by('-num_used')[:10]

    return render_to_response('coltrane/tag_index.html', args)


def tags(request):
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['entry1'] = Entry.objects.all()
    args['tag_list'] = Hashtag.objects.all()
    args['category_list'] = Category.objects.all()
    args['recent'] = Hashtag.objects.order_by('-last_used')[:10]
    args['most_used'] = Hashtag.objects.order_by('-num_used')[:10]

    return render_to_response('coltrane/tag_index.html', args)


def tag_detail(request, id):
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id

    tag = get_object_or_404(Hashtag, id=id)

    args['tag'] = Hashtag.objects.get(id=id)
    args['object_list'] = tag.entry_set.all()

    tag = get_object_or_404(Hashtag, id=id)
    return render_to_response('coltrane/tag_detail.html', args)


# ajax search function for ENTRIES
def search_titles(request):
    if request.method == "GET":
        search_text = request.GET['search_text']
    else:
        search_text = ''

    args = {}
    args['entries'] = Entry.objects.filter(title__contains=search_text)[:35]

    return render_to_response('coltrane/ajax_search.html', args)


# ajax search function for HASHTAGS
def search_hashes(request):
    if request.method == "GET":
        search_text_hash = request.GET['search_text_hash']
    else:
        search_text_hash = ''

    args = {}
    args['hashtags'] = Hashtag.objects.filter(title__contains=search_text_hash)[:35]

    return render_to_response('coltrane/ajax_search_hash.html', args)


def user_index(request, user_id):
    args = {}
    args['username'] = request.user
    args['uid'] = request.user.id
    args['this_user'] = User.objects.get(id=user_id)
    args['entry_list'] = Entry.objects.all().filter(author_id=user_id)[:35]

    e_comments = Entry.objects.all()
    args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()

    return render_to_response('coltrane/user_index.html', args)


def entries_index(request):
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['entry_list'] = Entry.objects.all().order_by('-id')[:35]
    # args['entry_list'] = Entry.objects.all().filter(author_id=request.user.id)[:35]

    e_comments = Entry.objects.all()
    args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()

    return render_to_response('coltrane/entry_index.html', args)


def entry_detail(request, entry_id):
    # if a comment is trying to get posted, these if statements will be called
    a = Entry.objects.get(id=entry_id)
    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            obj = f.save(commit=False)
            obj.parent_entry_id = a.id
            obj.save()

            c = f.save(commit=False)
            a.comments += 1
            c.entry = a
            c.save()

            return HttpResponseRedirect('/weblog/%s' % entry_id)

    # else the entry detail page is loaded
    else:
        args = {}
        # args['entry'] = Entry.objects.get(id=entry_id)
        e_comments = Entry.objects.get(id=entry_id)

        # all code related to counting the total number of this entry's views
        e_views = Entry.objects.get(id=entry_id)
        if request.user.id != e_views.author_id:
            e_views.num_views += 1
            e_views.save()

        # this code counts the total views for each post done by this author
        author_id = e_views.author_id
        setviews = User_Profile.objects.get(uid_id=author_id)
        if request.user.id != e_views.author_id:
            setviews.num_views += 1
            setviews.save()

        varComments = Comments.objects.all().filter(parent_entry_id=e_comments)

        # used for the navigation bar to show currently logged in user
        args['username'] = request.user.username
        args['uid'] = request.user.id

        args['comments'] = varComments

        args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()

        basic = Comments.objects.all()
        args['basic'] = basic
        advanced = User_Profile.objects.all()
        args['avatar'] = advanced

        f = CommentForm()

        # args = {}
        args.update(csrf(request))

        args['entry'] = a
        args['form'] = f
        return render_to_response('coltrane/entry_detail.html', args)


# return render_to_response('coltrane/newcomment.html', args)


def category_list(request):
    args = {}
    args['entry1'] = Entry.objects.all()
    args['category_list'] = Category.objects.all()
    args['username'] = request.user.username
    args['uid'] = request.user.id
    # entry_list = entry.get([entry])
    return render_to_response('coltrane/category_list.html', args)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)

    args = {}
    args['category_list'] = Category.objects.all()
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['cat'] = category

    category = get_object_or_404(Category, slug=slug)

    args['object_list'] = category.entry_set.all().order_by('-num_views')
    return render_to_response('coltrane/category_detail.html', args)


def category_views(request, slug):
    category = get_object_or_404(Category, slug=slug)

    args = {}
    args['category_list'] = Category.objects.all()
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['cat'] = category

    category = get_object_or_404(Category, slug=slug)

    args['object_list'] = category.entry_set.all().order_by('-num_views', '-pub_date')
    return render_to_response('coltrane/category_detail.html', args)


def category_likes(request, slug):
    category = get_object_or_404(Category, slug=slug)

    args = {}
    args['category_list'] = Category.objects.all()
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['cat'] = category

    category = get_object_or_404(Category, slug=slug)

    args['object_list'] = category.entry_set.all().order_by('-likes', '-pub_date')
    return render_to_response('coltrane/category_detail.html', args)


def category_comments(request, slug):
    category = get_object_or_404(Category, slug=slug)

    args = {}
    args['category_list'] = Category.objects.all()
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['cat'] = category

    category = get_object_or_404(Category, slug=slug)

    args['object_list'] = category.entry_set.all().order_by('-num_comments', '-pub_date')
    return render_to_response('coltrane/category_detail.html', args)


def user_register(request):
    return render_to_response('coltrane/registration_page.html')


def register(request):
    username = request.GET.get('username', '')
    password_get = request.GET.get('password', '')
    repassword = request.GET.get('repassword', '')
    email_get = request.GET.get('email_get', '')
    first_name = request.GET.get('first_name', '')
    last_name = request.GET.get('last_name', '')

    if not username:
        args = {}
        args['error'] = "Please enter a user name."
        return render_to_response('coltrane/registration_page.html', args)

    if password_get != repassword:
        args = {}
        args['error'] = "The passwords you've entered do not match."
        return render_to_response('coltrane/registration_page.html', args)

    if password_get == "":
        args = {}
        args['error'] = "Invalid password."
        return render_to_response('coltrane/registration_page.html', args)

    if len(password_get) < 6:
        args = {}
        args['error'] = "Your password must contain at least 6 characters."
        return render_to_response('coltrane/registration_page.html', args)

    if email_get.find("@") == -1:
        args = {}
        args['error'] = "Please enter a valid email address."
        return render_to_response('coltrane/registration_page.html', args)

    check4dupe = User.objects.filter(username=username)
    if not check4dupe:
        user = User.objects.create_user(username, email_get, password_get)
        user.last_name = last_name
        user.first_name = first_name
        user.save()
        user_profile = User_Profile(uid=user)
        user_profile.save()
    else:
        args = {}
        args['error'] = "That user name has already been taken."
        return render_to_response('coltrane/registration_page.html', args)
    args = {}
    args['notice'] = "Thanks for signing up!"
    return render_to_response('coltrane/login_page.html', args)


def user_login(request, entry_id=1):
    return render_to_response('coltrane/login_page.html')


def user_auth(request, entry_id=1):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')

    user = authenticate(username=username, password=password)

    # Get current username that's logged in
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['error'] = "Please check if your user name and password are correct."

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/weblog')
        else:
            return render_to_response('coltrane/login_page.html', args)
    else:
        return render_to_response('coltrane/login_page.html', args)


from django.contrib.auth import logout
from django.http import HttpResponseRedirect


def user_logout(request, entry_id=1):
    logout(request)
    return HttpResponseRedirect('/weblog')


def create_pick(request):
    args = {}
    args['username'] = request.user.username
    args['uid'] = request.user.id
    if request.user.is_authenticated() is False:
        args['entry_list'] = Entry.objects.all()
        args['error'] = 'You must be signed in before creating a new post.'

        return render_to_response('coltrane/entry_index.html', args)

    return render_to_response('coltrane/entry_type.html', args)


def create(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['entry_list'] = Entry.objects.all()
        args['error'] = 'You must be signed in before creating a new post.'
        return render_to_response('coltrane/entry_index.html', args)
    if request.POST:
        # post_values = request.POST.copy()
        # post_values['author'] = 4
        post_values = request.POST.copy()
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            obj = form.save(commit=False)
            obj.author = request.user
            # get entry and category id:
            e1 = obj.id
            c1 = post_values['categories']
            c2 = Category.objects.get(id=c1)
            # save entry to category
            obj.save()
            # add the hashtags from the post into the database:
            getHashtags = obj.body + " " + obj.title
            s = {tag.strip("#") for tag in getHashtags.split() if tag.startswith("#")}
            for item in s:
                h = Hashtag.objects.filter(title=item)
                if not h:
                    item = item.lower()
                    newhash = Hashtag(title=item, num_used=1)
                    newhash.save()
                    obj.tags.add(newhash)
                # obj.save()
                else:
                    # oldh = Hashtag.objects.get(title=item)
                    for item2 in h:
                        item2.num_used += 1
                        item2.save()
                        obj.tags.add(item2)
            # obj.save()
            # this code increments each time a specific user creates a post
            inc_post = request.user.id
            count_post = User_Profile.objects.get(uid_id=inc_post)
            count_post.num_posts += 1
            count_post.save()

            obj.categories.add(c1)
            return HttpResponseRedirect('/weblog')
    else:
        form = EntryForm()
        form.author = request.user
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('coltrane/newpost.html', args)


def create_text(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['entry_list'] = Entry.objects.all()
        args['error'] = 'You must be signed in before creating a new post.'
        return render_to_response('coltrane/entry_index.html', args)
    if request.POST:
        post_values = request.POST.copy()
        form = EntryFormText(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            e1 = obj.id
            c1 = post_values['categories']
            c2 = Category.objects.get(id=c1)
            obj.save()
            getHashtags = obj.body + " " + obj.title
            s = {tag.strip("#") for tag in getHashtags.split() if tag.startswith("#")}
            for item in s:
                h = Hashtag.objects.filter(title=item)
                if not h:
                    item = item.lower()
                    newhash = Hashtag(title=item, num_used=1)
                    newhash.save()
                    obj.tags.add(newhash)
                else:
                    for item2 in h:
                        item2.num_used += 1
                        item2.save()
                        obj.tags.add(item2)
            inc_post = request.user.id
            count_post = User_Profile.objects.get(uid_id=inc_post)
            count_post.num_posts += 1
            count_post.save()
            obj.categories.add(c1)
            return HttpResponseRedirect('/weblog')
    else:
        form = EntryFormText()
        form.author = request.user
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('coltrane/newpostText.html', args)


def create_url(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['entry_list'] = Entry.objects.all()
        args['error'] = 'You must be signed in before creating a new post.'
        return render_to_response('coltrane/entry_index.html', args)
    if request.POST:
        post_values = request.POST.copy()
        form = EntryFormURL(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            e1 = obj.id
            c1 = post_values['categories']
            c2 = Category.objects.get(id=c1)
            obj.save()
            getHashtags = obj.body + " " + obj.title
            s = {tag.strip("#") for tag in getHashtags.split() if tag.startswith("#")}
            for item in s:
                h = Hashtag.objects.filter(title=item)
                if not h:
                    item = item.lower()
                    newhash = Hashtag(title=item, num_used=1)
                    newhash.save()
                    obj.tags.add(newhash)
                else:
                    for item2 in h:
                        item2.num_used += 1
                        item2.save()
                        obj.tags.add(item2)
            inc_post = request.user.id
            count_post = User_Profile.objects.get(uid_id=inc_post)
            count_post.num_posts += 1
            count_post.save()
            obj.categories.add(c1)
            return HttpResponseRedirect('/weblog')
    else:
        form = EntryFormURL()
        form.author = request.user
    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['username'] = request.user.username
    args['uid'] = request.user.id
    return render_to_response('coltrane/newpostURL.html', args)


def add_comment(request, entry_id):
    a = Entry.objects.get(id=entry_id)

    # prevent the post from getting an additional view since COMMENT causes the page to refresh
    e_views = Entry.objects.get(id=entry_id)
    e_views.num_views -= 1
    e_views.save()

    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            obj = f.save(commit=False)
            obj.parent_entry_id = a.id
            obj.author = request.user.username
            obj.author_id = request.user.id
            obj.save()

            c = f.save(commit=False)
            a.num_comments += 1
            a.save()
            c.entry = a
            c.save()

            # this code increments each time a specific user adds a comment
            inc_comment = request.user.id
            count_comment = User_Profile.objects.get(uid_id=inc_comment)
            count_comment.num_comments += 1
            count_comment.save()

            return HttpResponseRedirect('/weblog/%s' % entry_id)

    else:
        f = CommentForm()

    args = {}
    args.update(csrf(request))

    args['entry'] = a
    args['form'] = f

    return render_to_response('coltrane/newcomment.html', args)


def like_entry1(request, entry_id):
    uid = request.user.id

    # verify that the user does not like this entry already
    check = User_Likes.objects.filter(user=uid, liked_entry=entry_id)
    if not check:
        # it's empty, like it
        liked_entry = User_Likes(user=uid, liked_entry=entry_id)
        liked_entry.save()

        # if entry_id:
        e = Entry.objects.get(id=entry_id)
        count = e.likes
        count += 1
        e.likes = count
        e.rating_sum += 1
        e.rating_current = e.rating_sum / e.likes
        e.save()

        # increment the total likes the author recieves
        inc_likes = e.author_id
        count_likes = User_Profile.objects.get(uid_id=inc_likes)
        count_likes.likes += 1
        count_likes.save()

        # prevent the post from getting an additional view since LIKE causes refresh
        e_views = Entry.objects.get(id=entry_id)
        e_views.num_views -= 1
        e_views.save()

        return HttpResponseRedirect('/weblog/%s' % entry_id)

    else:
        args = {}
        args['error'] = "You've already given that post a rating."
        args['username'] = request.user.username
        args['uid'] = request.user.id
        args['entry_list'] = Entry.objects.all().order_by('-id')[:35]
        # args['entry_list'] = Entry.objects.all().filter(author_id=request.user.id)[:35]

        e_comments = Entry.objects.all()
        args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()
        return render_to_response('coltrane/entry_index.html', args)


def like_entry2(request, entry_id):
    uid = request.user.id

    # verify that the user does not like this entry already
    check = User_Likes.objects.filter(user=uid, liked_entry=entry_id)
    if not check:
        # it's empty, like it
        liked_entry = User_Likes(user=uid, liked_entry=entry_id)
        liked_entry.save()

        # if entry_id:
        e = Entry.objects.get(id=entry_id)
        count = e.likes
        count += 1
        e.likes = count
        e.rating_sum += 2
        e.rating_current = e.rating_sum / e.likes
        e.save()

        # increment the total likes the author recieves
        inc_likes = e.author_id
        count_likes = User_Profile.objects.get(uid_id=inc_likes)
        count_likes.likes += 1
        count_likes.save()

        # prevent the post from getting an additional view since LIKE causes refresh
        e_views = Entry.objects.get(id=entry_id)
        e_views.num_views -= 1
        e_views.save()

        return HttpResponseRedirect('/weblog/%s' % entry_id)

    else:
        args = {}
        args['error'] = "You've already given that post a rating."
        args['username'] = request.user.username
        args['uid'] = request.user.id
        args['entry_list'] = Entry.objects.all().order_by('-id')[:35]
        # args['entry_list'] = Entry.objects.all().filter(author_id=request.user.id)[:35]

        e_comments = Entry.objects.all()
        args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()
        return render_to_response('coltrane/entry_index.html', args)


def like_entry3(request, entry_id):
    uid = request.user.id

    # verify that the user does not like this entry already
    check = User_Likes.objects.filter(user=uid, liked_entry=entry_id)
    if not check:
        # it's empty, like it
        liked_entry = User_Likes(user=uid, liked_entry=entry_id)
        liked_entry.save()

        # if entry_id:
        e = Entry.objects.get(id=entry_id)
        count = e.likes
        count += 1
        e.likes = count
        e.rating_sum += 3
        e.rating_current = e.rating_sum / e.likes
        e.save()

        # increment the total likes the author recieves
        inc_likes = e.author_id
        count_likes = User_Profile.objects.get(uid_id=inc_likes)
        count_likes.likes += 1
        count_likes.save()

        # prevent the post from getting an additional view since LIKE causes refresh
        e_views = Entry.objects.get(id=entry_id)
        e_views.num_views -= 1
        e_views.save()

        return HttpResponseRedirect('/weblog/%s' % entry_id)

    else:
        args = {}
        args['error'] = "You've already given that post a rating."
        args['username'] = request.user.username
        args['uid'] = request.user.id
        args['entry_list'] = Entry.objects.all().order_by('-id')[:35]
        # args['entry_list'] = Entry.objects.all().filter(author_id=request.user.id)[:35]

        e_comments = Entry.objects.all()
        args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()
        return render_to_response('coltrane/entry_index.html', args)


def like_entry4(request, entry_id):
    uid = request.user.id

    # verify that the user does not like this entry already
    check = User_Likes.objects.filter(user=uid, liked_entry=entry_id)
    if not check:
        # it's empty, like it
        liked_entry = User_Likes(user=uid, liked_entry=entry_id)
        liked_entry.save()

        # if entry_id:
        e = Entry.objects.get(id=entry_id)
        count = e.likes
        count += 1
        e.likes = count
        e.rating_sum += 4
        e.rating_current = e.rating_sum / e.likes
        e.save()

        # increment the total likes the author recieves
        inc_likes = e.author_id
        count_likes = User_Profile.objects.get(uid_id=inc_likes)
        count_likes.likes += 1
        count_likes.save()

        # prevent the post from getting an additional view since LIKE causes refresh
        e_views = Entry.objects.get(id=entry_id)
        e_views.num_views -= 1
        e_views.save()

        return HttpResponseRedirect('/weblog/%s' % entry_id)

    else:
        args = {}
        args['error'] = "You've already given that post a rating."
        args['username'] = request.user.username
        args['uid'] = request.user.id
        args['entry_list'] = Entry.objects.all().order_by('-id')[:35]
        # args['entry_list'] = Entry.objects.all().filter(author_id=request.user.id)[:35]

        e_comments = Entry.objects.all()
        args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()
        return render_to_response('coltrane/entry_index.html', args)


def like_entry5(request, entry_id):
    uid = request.user.id

    # verify that the user does not like this entry already
    check = User_Likes.objects.filter(user=uid, liked_entry=entry_id)
    if not check:
        # it's empty, like it
        liked_entry = User_Likes(user=uid, liked_entry=entry_id)
        liked_entry.save()

        # if entry_id:
        e = Entry.objects.get(id=entry_id)
        count = e.likes
        count += 1
        e.likes = count
        e.rating_sum += 5
        e.rating_current = e.rating_sum / e.likes
        e.save()

        # increment the total likes the author recieves
        inc_likes = e.author_id
        count_likes = User_Profile.objects.get(uid_id=inc_likes)
        count_likes.likes += 1
        count_likes.save()

        # prevent the post from getting an additional view since LIKE causes refresh
        e_views = Entry.objects.get(id=entry_id)
        e_views.num_views -= 1
        e_views.save()

        return HttpResponseRedirect('/weblog/%s' % entry_id)

    else:
        args = {}
        args['error'] = "You've already given that post a rating."
        args['username'] = request.user.username
        args['uid'] = request.user.id
        args['entry_list'] = Entry.objects.all().order_by('-id')[:35]
        # args['entry_list'] = Entry.objects.all().filter(author_id=request.user.id)[:35]

        e_comments = Entry.objects.all()
        args['count_comments'] = Comments.objects.all().filter(parent_entry_id=e_comments).count()
        return render_to_response('coltrane/entry_index.html', args)


def user_profile_setup(request):
    if request.user.is_authenticated() is False:
        args = {}
        args['entry_list'] = Entry.objects.all()
        args['error'] = 'You cannot change your profile without logging in.'

        return render_to_response('coltrane/entry_index.html', args)

    if request.POST:
        post_values = request.POST.copy()

        form = User_ProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # get the old User Profile object
            old_UP = User_Profile.objects.get(uid_id=request.user.id)
            old_id = old_UP.id

            obj = form.save(commit=False)
            obj.uid_id = old_UP.uid_id
            obj.num_views = old_UP.num_views
            obj.num_posts = old_UP.num_posts
            obj.num_comments = old_UP.num_comments
            obj.likes = old_UP.likes

            delete_me = User_Profile.objects.get(id=old_id)
            delete_me.delete()
            obj.save()

            # up = User_Profile.objects.get(uid_id=request.user.id)
            # count = e.likes
            # count +=1
            # e.likes = count
            # e.save()

            return HttpResponseRedirect('/weblog')



    else:
        form = User_ProfileForm()
        form.author = request.user

    args = {}
    args.update(csrf(request))

    args['form'] = form

    return render_to_response('coltrane/updateprofile.html', args)


# Public profile view
def profile(request):
    args = {}

    uid = request.user.id

    # Basic User Information
    args['username'] = request.user.username
    args['uid'] = request.user.id
    args['firstname'] = request.user.first_name
    args['lastname'] = request.user.last_name

    # Advanced User Information
    advanced = User_Profile.objects.get(uid_id=uid)

    args['num_posts'] = advanced.num_posts
    args['num_views'] = advanced.num_views
    args['num_comments'] = advanced.num_comments
    args['num_likes'] = advanced.likes

    args['bio'] = advanced.bio
    args['website'] = advanced.website
    args['avatar'] = advanced.avatar

    return render_to_response('coltrane/profile.html', args)


def profile_list(request):
    args = {}

    # Basic User Information
    basic = User.objects.all()[1:]
    args['basic'] = basic
    args['username'] = request.user.username
    args['uid'] = request.user.id

    # Advanced User Information
    advanced = User_Profile.objects.all()

    args['advanced'] = advanced

    return render_to_response('coltrane/profile_list.html', args)
