import json
import re

from json.decoder import JSONDecodeError
from decimal      import Decimal

from django.views import View
from django.http  import JsonResponse

from user.models     import User, MakerInfo
from product.models  import Product, Reward
from purchase.models import Address, Order, RewardOrder
from user.utils      import login_decorator

class RewardListView(View):  
    @login_decorator  
    def get(self, request, product_id): 
        try:

            """
            Created: 2021-02-25
            Updated: 2021-05-03

            [리워드 페이지]
            - 회원 상품 세부 리워드 리스트 - product 상세 reward options 

            [수량 반영]
            - 사용자가 주문한 상품 개수, 상품 재고 수량 반영
            """

            user  = request.user

            product = Product.objects.get(id=product_id) 
            rewards = Reward.objects.filter(product=product)
            
            product_info = {
                'id'         : product.id,
                'title'      : product.title,
                'maker_image': product.maker_info.user_set.all()[0].image,
                'maker_name' : product.maker_info.name
            }

            reward_list = [
                {
                'id'              : reward.id,
                'name'            : reward.name + product.title,
                'combination'     : reward.combination,
                'price'           : reward.price, 
                'remaining_stock' : reward.stock - reward.quantity_sold
                }
            for reward in rewards]

            data = {"product_info" : product_info, "reward_list" : reward_list}

            return JsonResponse({"data" : data}, status=200)

        except:
            raise Http404

class RewardOrderView(View):  
    @login_decorator
    def post(self, request, product_id): 
        try:

            """
            Created: 2021-02-26
            Updated: 2021-05-03

            rewards에 id, quantity 넘어옴

            [주문 페이지]
            - 사용자 입력 배송지 주소 None, 이전 배송지도 없으면 400
            - 사용자 입력 배송지 주소 None, 이전 배송지가 있으면 첫번쨰 주소 선택
            - 사용자 배송지 주소 입력 시 get 또는 create

            [수량 반영]
            - 사용자가 주문한 상품, 리워드 상품 판매 수량 반영
            - 사용자가 주문한 상품, 상품 총 달성 금액 반영
            """

            data = json.loads(request.body)
            user = request.user

            rewards        = data['id_quantity']
            fullname       = data['fullname']
            contact_number = data['contact_number']
            delivery_note  = data.get('delivery_note')
            address        = data.get('address')
            total_amount   = data['total_price']

            if not address and not contact_number:
                return JsonResponse({"message" : "REQUIRED_FIELD"}, status=400)
                
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message' : 'PRODUCT_NOT_FOUND'}, status=404)

            product      = Product.objects.get(id=product_id)
            address_list = Address.objects.filter(user_id=user.id)

            if address is None and not address_list.exists():
                return JsonResponse({'message': "ADDRESS_NEEDED"}, status=400)
            elif address is None and address_list.exists():
                address = address_list[0]
            else: 
                address = Address.objects.get_or_create(address=address, user=user)[0]

            order = Order.objects.create(
                fullname       = fullname,
                contact_number = contact_number,
                delivery_note  = delivery_note,
                address        = address,
                user           = user,
                total_amount   = total_amount
            )

            for reward in rewards:
                quantity   = reward['quantity']
                reward_obj = Reward.objects.get(id=reward['id'])

                reward_order = RewardOrder.objects.create(
                    reward   = reward_obj,
                    order    = order,
                    quantity = quantity
                )
                reward_obj.quantity_sold += reward_order.quantity
                reward_obj.save()

            product.total_amount += Decimal(order.total_amount)
            product.save()

            return JsonResponse({'message': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status=400) 
