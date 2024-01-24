from urllib.parse import urljoin
from bs4 import BeautifulSoup
from django.urls import reverse


def modify_html(original_html, user_site_name, routes_on_original_site):
    soup = BeautifulSoup(original_html, "html.parser")
    for a_tag in soup.find_all("a", href=True):
        original_href = a_tag["href"]
        if not original_href.startswith(("http://", "https://")):
            new_url = urljoin(routes_on_original_site, a_tag["href"])
            a_tag["href"] = reverse("service:router",
                                    args=[user_site_name, new_url])

    modified_html = str(soup)
    return modified_html
