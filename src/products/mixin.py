from django.http import Http404
from sellers.mixin import SellerAccounMixin


class ProductManagerMixin(SellerAccounMixin, object):
    def get_object(self):
        seller = self.get_account()
        obj = super(ProductManagerMixin, self).get_object()
        try:
            obj.seller == seller
        except:
            raise Http404
        if obj.seller == seller:
            return obj
        else:
            raise Http404