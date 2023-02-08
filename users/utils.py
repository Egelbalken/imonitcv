from .models import Profile,Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage


def searchProfiles(request):
    search_query = ''

    if request.GET.get("search"):
        search_query = request.GET.get("search")
    
    skills = Skill.objects.filter(name__icontains=search_query)
    # add distinct() to the filter and we do not get any dubblicates
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills))
    
    return profiles, search_query


def paginateProfiles(request, profiles, results):
     # pgainator will show pages with six at eacth page
    page = request.GET.get('page')
    paginator = Paginator(profiles,results)

    # if we dont have a paginator numer use pagenotinteger and set it to page 1
    # and if we try to paginate more then we have try and catch the exepts.
    try:
        profiles = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page= paginator.num_pages
        profiles = paginator.page(page)
    
    # We dont want to show many paginatios if we have, thats whay we need to eleminate it.
    # show minus 4 from current position if there is one or set to first one.
    left_Index = (int(page) - 4)
    if left_Index < 1:
        left_Index = 1

    # show minus 5 from current position if there is one or set to last page.
    right_Index = (int(page) + 5)
    if right_Index > paginator.num_pages:
        right_Index = paginator.num_pages + 1

    # Custom pagination results left right.
    custom_range = range(left_Index, right_Index)
    return custom_range, profiles
