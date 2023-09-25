from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



def pagination(request,page,p):
    result = 6
    paginator = Paginator(p,result)
    
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        p = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  
        p = paginator.page(page)
    
    left = (int(page) - 1)
    if left < 1:
        left = 1

    right = (int(page) + 2)
    if right > paginator.num_pages :
        right = paginator.num_pages + 1

    custom_range = range(left,right)

    return p,custom_range