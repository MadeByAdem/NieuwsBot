import feedparser


def get_recent_articles(rss_url, num_articles=10):
    feed = feedparser.parse(rss_url)
    articles = []

    for entry in feed.entries[:num_articles]:
        title = entry.title
        url = entry.link
        articles.append({'title': title, 'url': url})

    return articles


def extract_first_paragraph(html_content):
    # Simple function to extract the first paragraph from HTML content
    # You can use a more robust HTML parsing library for more complex scenarios
    # For this example, we will use a simple regex-based approach
    import re
    match = re.search(r'<p>(.*?)</p>', html_content)
    if match:
        return match.group(1)
    else:
        return ""


def format_output_articles(rss_url, platform, num_of_articles):
    articles = get_recent_articles(rss_url, num_of_articles)
    # With first paragraph
    # message = ""
    # for idx, article in enumerate(articles, start=1):
    #     item = f"""{idx}. {article['title']} - {article['url']}
    # {article['first_paragraph']}"""
    #     message += item + "\n"  # Add a new line after each article

    # Only with link
    # Initialize an empty string to store the concatenated message
    message = f"{platform}:\n"
    for idx, article in enumerate(articles, start=1):
        item = f"{idx}. {article['title']} - {article['url']}"
        message += item + "\n"  # Add a new line after each article

    return message


# --------------NOS---------------
def nos_algemeen_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nosnieuwsalgemeen"
    platform = "NOS.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


def nos_nieuws_binnenland_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nosnieuwsbinnenland"
    platform = "NOS.nl - Binnenland"
    return format_output_articles(url, platform, num_of_articles)


def nos_nieuws_buitenland_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nosnieuwsbuitenland"
    platform = "NOS.nl - Buitenland"
    return format_output_articles(url, platform, num_of_articles)


def nos_politiek_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nosnieuwspolitiek"
    platform = "NOS.nl - Politiek"
    return format_output_articles(url, platform, num_of_articles)


def nos_sport_algemeen_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nossportalgemeen"
    platform = "NOS.nl - Sport"
    return format_output_articles(url, platform, num_of_articles)


def nos_sport_formule1_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nossportformule1"
    platform = "NOS.nl - Formule1"
    return format_output_articles(url, platform, num_of_articles)


def nos_nieuwsuur_algemeen_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nieuwsuuralgemeen"
    platform = "NOS.nl - Nieuwsuur"
    return format_output_articles(url, platform, num_of_articles)


def nos_nieuws_opmerkelijk_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nosnieuwsopmerkelijk"
    platform = "NOS.nl - Opmerkelijk"
    return format_output_articles(url, platform, num_of_articles)


def nos_nieuws_tech_recent_articles(num_of_articles):
    url = "https://feeds.nos.nl/nosnieuwstech"
    platform = "NOS.nl - Tech"
    return format_output_articles(url, platform, num_of_articles)


# --------------RTL Nieuws---------------
def rtl_algemeen_recent_articles(num_of_articles):
    url = "https://www.rtlnieuws.nl/rss.xml"
    platform = "RTL Nieuws.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


def rtl_tech_recent_articles(num_of_articles):
    url = "https://www.rtlnieuws.nl/tech?_format=rss"
    platform = "RTL Nieuws.nl - Tech"
    return format_output_articles(url, platform, num_of_articles)

# --------------AD.nl---------------
def ad_algemeen_recent_articles(num_of_articles):
    url = "https://www.ad.nl/home/rss.xml"
    platform = "AD.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


def ad_binnenland_recent_articles(num_of_articles):
    url = "https://www.ad.nl/binnenland/rss.xml"
    platform = "AD.nl - Binnenland"
    return format_output_articles(url, platform, num_of_articles)


def ad_buitenland_recent_articles(num_of_articles):
    url = "https://www.ad.nl/buitenland/rss.xml"
    platform = "AD.nl - Buitenland"
    return format_output_articles(url, platform, num_of_articles)


def ad_politiek_recent_articles(num_of_articles):
    url = "https://www.ad.nl/politiek/rss.xml"
    platform = "AD.nl - Politiek"
    return format_output_articles(url, platform, num_of_articles)


def ad_sport_recent_articles(num_of_articles):
    url = "https://www.ad.nl/sport/rss.xml"
    platform = "AD.nl - Sport"
    return format_output_articles(url, platform, num_of_articles)


def ad_formule1_recent_articles(num_of_articles):
    url = "https://www.ad.nl/formule-1/rss.xml"
    platform = "AD.nl - Formule 1"
    return format_output_articles(url, platform, num_of_articles)


def ad_bizar_recent_articles(num_of_articles):
    url = "https://www.ad.nl/bizar/rss.xml"
    platform = "AD.nl - Bizar"
    return format_output_articles(url, platform, num_of_articles)


def ad_wetenschap_recent_articles(num_of_articles):
    url = "https://www.ad.nl/wetenschap/rss.xml"
    platform = "AD.nl - Wetenschap"
    return format_output_articles(url, platform, num_of_articles)

# --------------Volkskrant---------------
def volkskrant_algemeen_recent_articles(num_of_articles):
    url = "https://www.volkskrant.nl/voorpagina/rss.xml"
    platform = "Volkskrant.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


# def volkskrant_politiek_recent_articles(num_of_articles):
#     url = "https://www.volkskrant.nl/politiek"
#     platform = "Volkskrant.nl - Politiek"
#     return format_output_articles(url, platform, num_of_articles)


def volkskrant_sport_recent_articles(num_of_articles):
    url = "https://www.volkskrant.nl/sport/rss.xml"
    platform = "Volkskrant.nl - Sport"
    return format_output_articles(url, platform, num_of_articles)


def volkskrant_wetenschap_recent_articles(num_of_articles):
    url = "https://www.volkskrant.nl/wetenschap/rss.xml"
    platform = "Volkskrant.nl - Wetenschap"
    return format_output_articles(url, platform, num_of_articles)


def volkskrant_bestgelezen_recent_articles(num_of_articles):
    url = "https://www.volkskrant.nl/popular/rss.xml"
    platform = "Volkskrant.nl - Best gelezen"
    return format_output_articles(url, platform, num_of_articles)


def volkskrant_top_recent_articles(num_of_articles):
    url = "https://www.volkskrant.nl/nieuws-achtergrond/rss.xml"
    platform = "Volkskrant.nl - Top verhalen"
    return format_output_articles(url, platform, num_of_articles)

# --------------NRC---------------
def nrc_algemeen_recent_articles(num_of_articles):
    url = "https://www.nrc.nl/rss/"
    platform = "NRC.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


def nrc_binnenland_recent_articles(num_of_articles):
    url = "https://www.nrc.nl/index/binnenland/rss/"
    platform = "NRC.nl - Binnenland"
    return format_output_articles(url, platform, num_of_articles)


def nrc_buitenland_recent_articles(num_of_articles):
    url = "https://www.nrc.nl/index/buitenland/rss/"
    platform = "NRC.nl - Buitenland"
    return format_output_articles(url, platform, num_of_articles)


def nrc_politiek_recent_articles(num_of_articles):
    url = "https://www.nrc.nl/index/den-haag/rss/"
    platform = "NRC.nl - Den Haag"
    return format_output_articles(url, platform, num_of_articles)


def nrc_sport_recent_articles(num_of_articles):
    url = "https://www.nrc.nl/index/sport/rss/"
    platform = "NRC.nl - Sport"
    return format_output_articles(url, platform, num_of_articles)


def nrc_wetenschap_recent_articles(num_of_articles):
    url = "https://www.nrc.nl/index/wetenschap/rss/"
    platform = "NRC.nl - Wetenschap"
    return format_output_articles(url, platform, num_of_articles)


# --------------Telegraaf---------------
def telegraaf_voorpagina_recent_articles(num_of_articles):
    url = "https://www.telegraaf.nl/rss"
    platform = "Telegraaf.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


def telegraaf_nieuws_recent_articles(num_of_articles):
    url = "https://www.telegraaf.nl/nieuws/rss"
    platform = "Telegraaf.nl - Nieuws"
    return format_output_articles(url, platform, num_of_articles)


def telegraaf_sport_recent_articles(num_of_articles):
    url = "https://www.telegraaf.nl/sport/rss"
    platform = "Telegraaf.nl - Sport"
    return format_output_articles(url, platform, num_of_articles)

# --------------Nu.nl---------------
def nu_algemeen_recent_articles(num_of_articles):
    url = "https://www.nu.nl/rss/Algemeen"
    platform = "NU.nl - Voorpagina"
    return format_output_articles(url, platform, num_of_articles)


def nu_sport_recent_articles(num_of_articles):
    url = "https://www.nu.nl/rss/Sport"
    platform = "NU.nl - Sport"
    return format_output_articles(url, platform, num_of_articles)


def nu_tech_recent_articles(num_of_articles):
    url = "https://www.nu.nl/rss/Tech"
    platform = "NU.nl - Tech"
    return format_output_articles(url, platform, num_of_articles)


def nu_wetenschap_recent_articles(num_of_articles):
    url = "https://www.nu.nl/rss/Wetenschap"
    platform = "NU.nl - Wetenschap"
    return format_output_articles(url, platform, num_of_articles)


def nu_opmerkelijk_recent_articles(num_of_articles):
    url = "https://www.nu.nl/rss/Opmerkelijk"
    platform = "NU.nl - Opmerkelijk"
    return format_output_articles(url, platform, num_of_articles)

# --------------Bright---------------
def bright_algemeen_recent_articles(num_of_articles):
    url = "https://www.bright.nl/rss"
    platform = "Bright.nl"
    return format_output_articles(url, platform, num_of_articles)



# --------------Formule1.nl--------------
def formule1nl_recent_articles(num_of_articles):
    url = "https://www.formule1.nl/feed/"
    platform = "Formule1.nl"
    return format_output_articles(url, platform, num_of_articles)

