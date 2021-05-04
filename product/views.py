import json
from datetime         import date, datetime 

from django.views     import View
from django.conf      import settings
from django.http      import (
    JsonResponse, HttpResponse, Http404
)
from django.db.models  import Q

from my_settings      import SECRET_KEY, ALGORITHM
from user.utils       import login_decorator
from user.models      import User, MakerInfo
from .models          import  (
    Category, Product, Reward,
    LikeUser, ProductContent, Collection
)


class ProductDetailView(View):
    
    def get(self, request, product_id):

        try:

            """
            Created: 2021-02-25
            Updated: 2021-05-03

            [비회원 스토리 - product 상세 정보페이지]
            - 상품 상세 정보 확인 가능
            - 상품 좋아요 반영 불가능
            """

            tab          = request.GET.get('tab', '스토리')
            product      = Product.objects.get(id=product_id)    
            today        = datetime.today()
            closing_date = product.closing_date

            data         = {
                "id"            : product.id,
                "category"      : product.category_set.first().name,
                "title"         : product.title,
                "tab_names"     : [content.name for content in product.productcontent_set.all()],
                "thumbnail_url" : product.thumbnail_url,
                "description"   : product.description,
                "goal_amount"   : product.goal_amount,
                "opening_date"  : product.opening_date,
                "closing_date"  : closing_date,
                "days_left"     : str((closing_date - today).days),
                "info_box"      : {
                        "achieved_rate"    : product.achieved_rate,
                        "total_amount"     : product.total_amount,
                        "total_supporters" : product.total_supporters
                    },
                "total_likes"   : product.total_likes,
                "tab"           : product.productcontent_set.get(name=tab).content,
                "maker_name"    : product.maker_info.name,
                "maker_image"   : product.maker_info.user_set.first().image,
                "levels"        : [
                    { 
                        "name"  : "평판",
                        "level" : product.maker_info.reputation_level
                    },
                    { 
                        "name"  : "소통",
                        "level" : product.maker_info.communication_level
                    },
                    { 
                        "name"  : "인기",
                        "level" : product.maker_info.popularity_level
                    }
                ]
            }
            return JsonResponse( {"data" : data}, status = 200 )

        except:
            raise Http404


class UserProductDetailView(View):
    
    @login_decorator
    def get(self, request, product_id):
        
        try:
            
            """
            Created: 2021-02-24
            Updated: 2021-05-03

            [회원 스토리 - product 상세 정보페이지]
            - 상품 상세 정보 확인 가능
            - 상품 좋아요 반영 가능
            """

            tab          = request.GET.get('tab', '스토리')
            product      = Product.objects.get(id=product_id)
            total_likes  = product.total_likes
            closing_date = product.closing_date
            user_id      = request.user.id   
            today        = datetime.today()
            liked        = True

            if LikeUser.objects.prefetch_related('product', 'user').filter(product_id=product_id, user_id=user_id).exists():
                liked = False
            
            data      = {
                "id"            : product.id,
                "category"      : product.category_set.first().name,
                "title"         : product.title,
                "tab_names"     : [content.name for content in product.productcontent_set.all()],
                "thumbnail_url" : product.thumbnail_url,
                "description"   : product.description,
                "goal_amount"   : product.goal_amount,
                "opening_date"  : product.opening_date,
                "closing_date"  : closing_date,
                "days_left"     : str((closing_date - today).days),
                "info_box"      : {
                        "achieved_rate"    : product.achieved_rate,
                        "total_amount"     : product.total_amount,
                        "total_supporters" : product.total_supporters
                    },
                "total_likes"   : product.total_likes,
                "tab"           : product.productcontent_set.get(name=tab).content,
                "maker_name"    : product.maker_info.name,
                "maker_image"   : product.maker_info.user_set.first().image,
                "levels"        : [
                    { 
                        "name"  : "평판",
                        "level" : product.maker_info.reputation_level
                    },
                    { 
                        "name"  : "소통",
                        "level" : product.maker_info.communication_level
                    },
                    { 
                        "name"  : "인기",
                        "level" : product.maker_info.popularity_level
                    }
                ],
                "liked"         : liked
            }
            return JsonResponse( {'data' : data}, status = 200 )

        except:
            raise Http404 


class LikeView(View):

    @login_decorator
    def post(self, request, product_id):

        try:

            """
            Created: 2021-02-26
            Updated: 2021-05-03

            [회원 전용 좋아요]
            - 로그인 회원만 product 좋아요 기능 반영
            - 총 좋아요수 집계 반영
            """

            user_id     = request.user.id
            product     = Product.objects.get(id=product_id)
            total_likes = product.total_likes

            if LikeUser.objects.prefetch_related('product', 'user').filter(product_id=product_id, user_id=user_id).exists():
                LikeUser.objects.get(product_id=product_id, user_id=user_id).delete()
                Product.objects.filter(id=product_id).update(total_likes = total_likes - 1)

                return JsonResponse({'message':'SUCCESS', 'total_likes': total_likes}, status=200)

            LikeUser.objects.create(product_id=product_id, user_id=user_id)
            Product.objects.filter(id=product_id).update(total_likes = total_likes + 1)
            
            return JsonResponse( {'message':'SUCCESS', 'total_likes': total_likes}, status=201 )

        except KeyError: 
            return JsonResponse( {'message':'KEY_ERROR'}, status=400)


class MainView(View):

    def get(self, request, category_id=0):
    
        try:

            """
            Created: 2021-02-18
            Updated: 2021-05-03

            [매인패이지] 
            - 카테고리, 날짜 필터 기능
            - 정렬 기능

            ~ 카테고리(Category)
            - 1~12가지
            
            ~ 날짜(endYN)
            - 1(default - 전체)
            - 2(진행된)
            - 3(종료된)

            ~ 정렬(ordering)
            - recommend(default - 추천순)
            - date(마감임박순)
            - support(응원참여자순)
            - price(펀딩액순)

            [collection - 기획전]
            - product가 해당되는 기획전 등록
            - 메인페이지에 기획전 상품 배치
            """

            ordering = request.GET.get('order', 'recommend')
            endYN    = request.GET.get('endYN',1)

            ordering_options = {
                'recommend' : '-achieved_rate',
                'date' : 'closing_date',
                'support' : '-total_supporters',
                'price' : '-total_amount'
            }

            '''
            ~ endYN Q객체 + 딕셔너리
            q = Q()
            endYN_options = {
                '1' : Q(),
                '2' : Q(closing_date__gt=datetime.today()),
                '3' : Q(closing_date__lte=datetime.today())
            }

            q &= endYN_options[endYN]
            '''
            q = Q()

            if endYN == '2':
                q &= Q(closing_date__gt=datetime.today())

            if endYN == '3':
                q &= Q(closing_date__lte=datetime.today())

            products = Product.objects.filter(q)

            products = products if category_id == 0 else products.prefetch_related('category_set').filter(category__id=category_id)

            today       = datetime.today()
            collections = Collection.objects.all()

            product_list = [{
                'category_image'   : [product.category_set.first().image], 
                'title'            : product.title,
                'goal_amount'      : product.goal_amount,
                'toal_amount'      : product.total_amount,
                'achieved_rate'    : product.achieved_rate,
                'total_supporters' : product.total_supporters,
                'closing_date'     : str((product.closing_date - today).days),
                'thumbnail_url'        : product.thumbnail_url,
                'category'         : [product.category_set.first().name],
                'category_id'      : [product.category_set.first().id],
                'id'               : product.id,
                'maker_info_name'  : product.maker_info.name,
                } for product in products.order_by(ordering_options[ordering])
            ]

            for collection in collections:
                projects = collection.product.all()
                planevent_data = [
                    {
                        "planId"   : collection.id,
                        "planTitle": collection.name,
                        "planImage": collection.image_url,
                        "products" : [
                            {
                                "id"       : project.id,
                                "text"     : project.title,
                                "percent"  : project.achieved_rate,
                                "category" : project.category_set.first().name,
                                "img"      : project.thumbnail_url
                            } 
                            for project in projects
                        ]
                    }
                ]

            return JsonResponse( {'data' :  product_list, 'collection' : planevent_data}, status = 200 )
            
        except:
            raise Http404
