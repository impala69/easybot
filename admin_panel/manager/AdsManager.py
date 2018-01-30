from easybot import models
from admin_panel import FormsHandler


class AdsManager:
    def __init__(self, ad_data=None, ad_files=None, deleted_ad_id=None , edited_ad_id = None):
        self.ad_data = ad_data
        self.deleted_ad_id = deleted_ad_id
        self.ad_files = ad_files
        self.edited_ad_id = edited_ad_id

    def get_all_ads(self):
        result = models.Advertise.objects.filter()
        ad_data = {}
        all_ads = []
        for one_advertise in result:
            ad_data['ad_id'] = one_advertise.pk
            ad_data['ad_title'] = one_advertise.title
            ad_data['ad_text'] = one_advertise.text
            ad_data['ad_image'] = one_advertise.image
            all_ads.append(ad_data)
            ad_data = {}
        return all_ads

    def add_ad(self):
        add_ads_form = FormsHandler.AddAdvertiseForm(self.ad_data, self.ad_files)
        if add_ads_form.is_valid():
            ad_title = add_ads_form.cleaned_data['advertise_title']
            ad_text = add_ads_form.cleaned_data['advertise_text']
            ad_image = add_ads_form.cleaned_data['advertise_image']
            try:
                new_ad = models.Advertise(title=ad_title, text=ad_text, image=ad_image)
                new_ad.save()
                return 1
            except Exception as e:
                print e
                return 0
        else:
            return 0

    def delete_ad(self):
        try:
            models.Advertise.objects.get(pk=self.deleted_ad_id).delete()
            return 1
        except Exception as e:
            print e
            return 0
    def edit_ad(self):
        try:
            return models.Advertise.objects.get(pk=self.edited_ad_id)
        except Exception as e:
            print(e)
            return 0