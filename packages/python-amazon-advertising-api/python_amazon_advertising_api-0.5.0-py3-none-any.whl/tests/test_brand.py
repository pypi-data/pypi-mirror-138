from ad_api.sp_brands.targeting_recommendations import TargetingRecommendations

access_token = "Atza|IwEBIF2oZKOGdFQGSGFYqqysfprHxdKS1jEG68crTpLqMI1LWfRIDo6H48tTgI35Hlvm57RhcfcqVECy0UP5OKd-FzPoCjNu8d3yXxdYxoyMQ95-sJhW0L96gpfh_yeQpVdmzmmdseFJM2BH7XY-Kj-TZ_mOL7wXXqkTjBcgI4ZevbNkuKIus4_gTz8GIRK7-EO89WHkYMiMc2RAFDC__Y5xIgHMKEe7D4ikETSXU8XDbFxZEX_4RwwM4y7XjhBv89Doi2ZcPSBkMTg3P0wIE-zlUiDflpQJm-W8D_ZRjiYfYipmdlH7mGmNM5kXd8HfOM_mvOmhpXF92WpR1D1K5PSsU8j0FtUzhtBpGDGceZa_g5T2UxgQZh3riak2tkgAGCSrk9Ud0kf5EOVrcLozyB_G1kbB5n_c73FtvtcUUl2sA_pWoKp5lWnJaCd-yYqadKizIy2QnjY_jg7B8Y9z_G1YfFOR"
profile_id = "3049722099969549"
region = "NA"
client_id = "amzn1.application-oa2-client.ded251be82444771be30ce2154f766dd"


target_api = TargetingRecommendations(access_token, profile_id, region, client_id)

response = target_api.get_recommendations_targets_brand(keyword="usb c cable")
print(response.json())
