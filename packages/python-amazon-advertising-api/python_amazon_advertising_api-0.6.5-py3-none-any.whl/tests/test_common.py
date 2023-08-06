
from ad_api.common import Portfolios
from ad_api.auth import Auth


def test():
    profile_id = "3049722099969549"
    region = "NA"
    client_id = "amzn1.application-oa2-client.ded251be82444771be30ce2154f766dd"
    client_secret = "50df60a7fe537f1a4fd4a43db938dcb7596a1e6bde43e5ee191fc8d5de0ce9c0"
    redirect_uri = "https://www.seekland.cn/home/store/authorization/ad"
    refresh_token = "Atzr|IwEBIN5FPXVh04EXt1K6s9czZ3s3YWC16hdZEbwx7zGibjxDWIbBegOzNRWiwSSKs822wRldH8LaH4yjQGlIowluOrnw79AZeKHfCaAA8NCsitEL3yI4HOFg9MGNYhuSjjVm7IYGfVTOk065qGzToKOVAm76IXKAlaUfcj9_rTmGT7iEP0l7LL0GaEQ45DLJ6jORNO5-3DC-bjKc4G-e3pIeXW6QB6jUpaa8VchZpkENIIRXMT9ArtUCoWDAxuK3fUmIThbatliuTtrUgvYr73yDgiz2S-YmI36LkP8JfkxW5J7b7OJcHp-r4bYu6iCKmgF27PzLRUnZKkcoFXaqxvj4pqalti4Dtax3lE8mhCoSuMQF53R8MOJxex375hikREAPnMCuSu4p2jmwBNuf6Dd-6UF2OPHDHdEd3S4RcMFs-WmxKLuRRx_z_9lLbGNNwecaL0U"
    auth_api = Auth(client_id, client_secret, redirect_uri, region)
    response = auth_api.get_new_access_token(refresh_token)
    access_token = response.json()["access_token"]
    portfolios_api = Portfolios(access_token, profile_id, region, client_id)
    res = portfolios_api.get_portfolios()
    print(res.json())


test()
