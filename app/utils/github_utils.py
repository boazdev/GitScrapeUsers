def create_github_url(user_str:str, min_repos:int = 5,page:int = 1):
    url = f"https://github.com/search?q={user_str}+in%3Auser+repos%3A%3E{min_repos}&type=users&ref=advsearch&s=repositories&o=desc&p={page}"
    return url

def create_github_headers() -> dict:
    headers = {
  'authority': 'github.com',
  'accept': 'application/json',
  'accept-language': 'en-US,en;q=0.9,he;q=0.8',
  'cookie': '_octo=GH1.1.635886773.1666110862; _device_id=28918aa01edf99a154d0ea5d3dd6fa63; user_session=CtFg7O6mfA8MpLPkeE-sZTg0R6jwaKKaEb-pOo63hqu3-C8p; __Host-user_session_same_site=CtFg7O6mfA8MpLPkeE-sZTg0R6jwaKKaEb-pOo63hqu3-C8p; logged_in=yes; dotcom_user=UserMain; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=light; tz=Asia%2FJerusalem; has_recent_activity=1; _gh_sess=C3J4poaISxeCGyQTgg6eH%2B3yUophW4pNbhSeXiz1k1BM5drizK1Rk7iL9R6zck7njTzXbPKfytgMVgnojtB57d5kCbLJccOWdGUuLXRLevmCdgMEsZvyhJzOcxm7nwW3iXb04p5XJN7YGYC9%2BfwubGuvJkBPfgHC%2B0UA8VThm%2Fpd8NyfNf%2Bh29WYzvSBbqdbmghMuOOogae0jBre8Ra20P%2FIKDXb3kmfMlesMy3z7N9l7A61GlqNh%2FqhTdPNa0guwgQ17zwUNyDkGHDBAqatVzQJsFUT3d30Gn%2FftDZpsQeNpQZNMlkXFb9UCaI6VK33KLP2WERE%2B1m2gVlZDQ%3D%3D--fv0kAxxGK0zsBm3L--Uxfgj51Gg9ZARfbOICvlww%3D%3D; _gh_sess=wHKiO6qTETme7BkMMha2KAyD7CWVXYtUTKdn6XgzHFPz%2BZ28NRGukcJV4Y4vNuKnmPiRz5D1%2Fmmv1wAI%2BOki81h%2BQzRCGK5fvZc9tyX%2BXCWhrDLiv2%2F4rj6gPecSvtyCm3pHYU%2BnR%2F%2BcN%2BFAoWOnwgQwM3r23MWApOtNcOF%2F5VM68hz4ypbMPygJ0b%2Bxxv2s5XJrqcnNg248eM6rUUIeRe%2FClMJ1LaCvIBRurziPsmFOYrqGmz9kPGKQB6LX3efubXeNUt%2FDKZJnoOha7VdMfdeEBXnab6V8grOm218Fu7P6lbfmCDITqBL%2B%2F5loBvk9MBC1FSfzNRFcmDGg6g%3D%3D--Zt0D2GGkBZxEvDFw--Q3z1iixC4%2BYCo%2FVhsjqIdg%3D%3D; _octo=GH1.1.1338388705.1682315579; has_recent_activity=1; logged_in=no; _gh_sess=AOvwu4v3vZ0sM4pzjc3LB5RgZlf%2BLkJceeaEBL0EIjen5QEvnOszS3mPzZzDQOl0IjDTzKz9VJkPxmu%2BCx5avxGbG461Wnqmc8B5gFoeQBYb2oPfR%2F3pm77ZPblNGuaNtskhjxuUM1hvPNPgDcQQwqLvY%2B73wpGZuK9MSLcQbaEaNSnSolJlhVU93AictgC%2BDJZObmpwH4bdzLuHoE77wrPe4abjE8nRAHj4iXiYXz9gcpt9JzwAGgaHKSQOPHFBgbzqkZ03ftT9nOKJ%2Fu%2BxPvtScB3NXQ1pKDnxyONqm36fWtjnkqlLJlFfvgW77SQhKtmGhkC0Sx7i0mT2v2HJVy9%2BuXzGfmxcXaZQbZhWvTOGFXCEK2Zrf1B8ZYZavW7abcFWRhImUr%2FpnWex6BOST%2BlfJmGYaRN1kyuYKjHoO%2FbsG7%2Bl3RJDyST890V%2BqKsFRBjOFViuqHk%3D--x%2FR4Myvzyjgzkh25--UjpqPNrwKzgrVJ9zV0hUTw%3D%3D; has_recent_activity=1; logged_in=no',
  'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  'x-github-target': 'dotcom',
  'x-requested-with': 'XMLHttpRequest'
}
    return headers

def users_from_json(users_obj:dict)->list[str]:
    return list(map(lambda user_item: user_item["login"],users_obj["payload"]["results"]))
