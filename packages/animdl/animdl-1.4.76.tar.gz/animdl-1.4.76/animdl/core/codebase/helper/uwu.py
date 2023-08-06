import regex
import base64
import yarl

RECAPTCHA_API_JS = "https://www.google.com/recaptcha/api.js"


def bypass_ddos_guard(session, base_uri):
    js_bypass_uri = regex.search(
        r"'(.*?)'", session.get("https://check.ddos-guard.net/check.js").text
    ).group(1)

    session.get(base_uri + js_bypass_uri)


def bypass_recaptcha(session, url, headers):

    response = {}

    initial_page = session.get(url, headers=headers)

    domain = (
        base64.b64encode("{0.scheme}://{0.host}:443".format(yarl.URL(url)).encode())
        .decode()
        .strip("=")
        + "."
    )

    site_key_match = regex.search(r"recaptchaSiteKey = '(.+?)'", initial_page.text)

    number_match = regex.search(r"recaptchaNumber = '(\d+?)'", initial_page.text)

    if number_match:
        response.update(number=number_match.group(1))

    if site_key_match is None:
        return response

    recaptcha_site_key = site_key_match.group(1)

    recaptcha_out = session.get(
        RECAPTCHA_API_JS,
        params={"render": recaptcha_site_key},
        headers={"referer": url},
    ).text

    v_token_match = regex.search(r"releases/([^/&?#]+)", recaptcha_out)

    if v_token_match is None:
        return response

    v_token = v_token_match.group(1)
    anchor_out = session.get(
        "https://www.google.com/recaptcha/api2/anchor",
        params={
            "ar": 1,
            "k": recaptcha_site_key,
            "co": domain,
            "hl": "en",
            "v": v_token,
            "size": "invisible",
            "cb": "kr42069kr",
        },
    ).text

    recaptcha_token_match = regex.search(r'recaptcha-token.+?="(.+?)"', anchor_out)

    if recaptcha_token_match is None:
        return response

    recaptcha_token = recaptcha_token_match.group(1)

    token_response_out = session.post(
        "https://www.google.com/recaptcha/api2/reload",
        params={"k": recaptcha_site_key},
        data={
            "v": v_token,
            "reason": "q",
            "k": recaptcha_site_key,
            "c": recaptcha_token,
            "sa": "",
            "co": domain,
        },
        headers={"referer": "https://www.google.com/recaptcha/api2"},
    ).text

    token_match = regex.search(r'rresp","(.+?)"', token_response_out)
    if token_match is None:
        return response

    response.update(token=token_match.group(1))

    return response
