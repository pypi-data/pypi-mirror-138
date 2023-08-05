from ad_api.sp_products.campaigns import Campaigns
from ad_api.sp_products.adgroups import AdGroup
from ad_api.sp_products.bidrecommendations import BidRecommendations
from ad_api.sp_products.keywords import Keywords
from ad_api.sp_products.negative_keywords import NegativeKeywords
from ad_api.sp_products.suggested_keywords import SuggestedKeywords
from ad_api.sp_products.product_targeting import ProductTargeting
from ad_api.sp_brands.campaigns import Campaigns
from ad_api.sp_brands.keywords import Keywords
from ad_api.sp_brands.product_targeting import ProductTargeting

access_token = "Atza|IwEBIJRiB_om-n7X5tvRJM5PN6StwsTqeV6GjV65T2X0NcWAWgfempLQDrk04-Ebm0tWolVA27PIdDNrLv69zp0EBKPpwAMLTfOyZN4zV7zp8Ayr5s-gm0karhFjuVEVs9rVgzG0RN3w80sYwzhCK70D6EpJrJptTe6-BeNgIPXen5QSrUag1g_WxKZUvf-UdYDM5n3i_rgw4vBYo35Otc5cWMEP4SF7ygfxthcnPFa5QjBJg0HrR7JxPdtsSBr-lhzzz-lOBrUd1t9ePDby8CtvejR-QVT9-OQArzLiXAYUsVkgRhNEQorFTnhQlTKylzxGltW_SRkZj_pufj-4pqMr9hmzxa_6dd6bmE_IDNTjm8nPXujwYRbVrGD0V7yZEiks7LxVLjA9mR0dda-G39VYdM05N9xTKdUwStC7nOocz6DTvIBC9FRBXzHIOYoS5WdmP22BnMJ4lsaJw2fw0n26CaiF"
profile_id = "3049722099969549"
region = "NA"
client_id = "amzn1.application-oa2-client.ded251be82444771be30ce2154f766dd"

campaign_api = Campaigns(access_token, profile_id, region, client_id)
ad_group_api = AdGroup(access_token, profile_id, region, client_id)
bid_re_api = BidRecommendations(access_token, profile_id, region, client_id)
keyword_api = Keywords(access_token, profile_id, region, client_id)
negative_keyword_api = NegativeKeywords(access_token, profile_id, region, client_id)
suggested_keywords_api = SuggestedKeywords(access_token, profile_id, region, client_id)
# response = suggested_keywords_api.get_suggest_keywords_by_asins(asins=["B076FPGWNZ"], max_num_suggestions=10)
target_api = ProductTargeting(access_token, profile_id, region, client_id)
response = target_api.get_targets(next_token="/u0NEl5BpwIAAAAAAAAAAQNHYugRvAS96IfAZFRDFTb120Pbc5lS/4mv77blh7kPMFXkngwmd9RMYopDrrAaVspAeWYkh+mukxioJA+1DhLSmJMpXXSuGsfJfVM2Ke39SI0RiWe6ZCzDAPjjKm7lUtQkSUwBFA0Y57dIpBmypgIHiPrsAqo7cLIN5nFxTPsf5Jn+0t/aXGeGyIndLY1hlcmKKC4fgD7+CasNbncoRuFVPpSOdkWDR2I2wnUoIRgJmYjz0K/rgoKqhoAgDFeDUhhoxvBJh6RV5v31N6f0a35xK9T4gYNrRQ+JrYTBDIEXJN3DXMFtkB738PN2QhUya3H9puCpYHD0YII1FHMJhlKY0tzm+wc0bqTz1gv6D6ZL")
# response = campaign_api.get_campaign_extended(count=10)
# response = ad_group_api.get_ad_group_extended(count=10)
# response = bid_re_api.get_bid_by_keyword_id("269110793758638")
print(response.json())
