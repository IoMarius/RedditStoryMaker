import requests
from core import logger
from models.reddit import Subreddit
from ..listings import (
    append_listings_to_csv,
    parse_listing,
    save_scrape_state,
    load_scrape_state,
)
import random
import time


def run_fetch_stories_pipeline(sub: Subreddit):
    logger.info(f"Running listings pipeline for r/{sub.name}.")
    last_state = load_scrape_state(sub.name)

    if last_state:
        sub.url = f"{sub.url}?after={last_state}"

    response = requests.get(url=sub.url, headers=_get_headers())

    fail_count = 0
    if not response.ok:
        if fail_count == 3:
            raise Exception(f"Cannot fetch data for r/{sub.name}.")
        logger.error(
            f"Failed to fetch from r/{sub.name}. \nStatus code {response.status_code} Url: {sub.url}."
        )
        fail_count += 1
        time.sleep(round(random.uniform(2, 6), 2))
        return run_fetch_stories_pipeline(sub)

    # time.sleep(100000)
    json_data = response.json()

    stories, after = parse_listing(json_data)

    if stories:
        append_listings_to_csv(stories, subreddit=sub.name)

    if after:
        save_scrape_state(subreddit=sub.name, after=after)

    logger.info(f"Listings pipeline ran successfully for r/{sub.name}")


async def run_fetch_stories_pipeline_async(sub: Subreddit):
    logger.info(f"Running listings pipeline for r/{sub.name}.")
    last_state = load_scrape_state(sub.name)

    if last_state:
        sub.url = f"{sub.url}?after={last_state}"

    response = requests.get(url=sub.url, headers=_get_headers())

    fail_count = 0
    if not response.ok:
        if fail_count == 3:
            raise Exception(f"Cannot fetch data for r/{sub.name}.")
        logger.error(
            f"Failed to fetch from r/{sub.name}. \nStatus code {response.status_code} Url: {sub.url}."
        )
        fail_count += 1
        time.sleep(round(random.uniform(2, 6), 2))
        return run_fetch_stories_pipeline(sub)

    # time.sleep(100000)
    json_data = response.json()

    stories, after = parse_listing(json_data)

    if stories:
        append_listings_to_csv(stories, subreddit=sub.name)

    if after:
        save_scrape_state(subreddit=sub.name, after=after)

    logger.info(f"Listings pipeline ran successfully for r/{sub.name}")


def _get_headers():
    return {
        "Host": "www.reddit.com",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Connection": "keep-alive",
        "Cookie": "loid=0000000000hb6i891b.2.1638871744000.Z0FBQUFBQnBWRGZzVlVXeUhsTXdxZUs3YTBMWDduaUdheElTN0h0MUd5VE5wSS1ZNzdnN01aRllwSWVUd2RKNXBkT2NsUWFOTHVKOXhXZVJ0a19mMGdRNFdySVpwNUpQeTZkRTRrckJ6SWZGMHlaVVdkUTVjQ0JMWTF1SVJHQjc4dHJlcFJpNHl3b0w; csv=2; edgebucket=IUQwHRPzMjnV3cb0AD; g_state={'i_l':0,'i_ll':1767382820514,'i_b':'Vq3K5vzplduiC1CxZsLbPpL2rRpP2exzcbutINQHE0w','i_e':{'enable_itp_optimization':0}}; reddit_supported_media_codecs=video/avc,video/vp9; reddit_session=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpsVFdYNlFVUEloWktaRG1rR0pVd1gvdWNFK01BSjBYRE12RU1kNzVxTXQ4IiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0Ml9oYjZpODkxYiIsImV4cCI6MTc4Mjc2NTQxOS45Mzc4NTIsImlhdCI6MTc2NzEyNzAxOS45Mzc4NTIsImp0aSI6IkRCTXZFMDZtTl9MME9zSkdadEprNk5xTUFxQmc2ZyIsImF0IjoxLCJjaWQiOiJjb29raWUiLCJsY2EiOjE2Mzg4NzE3NDQwMDAsInNjcCI6ImVKeUtqZ1VFQUFEX193RVZBTGsiLCJmbG8iOjMsImFtciI6WyJzc28iXX0.t_zFKvHvjOYHYCq1l42T2dlEUopVpsb3ee1Eex5MfJdLCO3qeLByaEjPVcLSWCMaMcBtOgfDLzSAKYBf7iTx-RUpWGjfin9-kp62jgw6VgxavPzpvQoAodM8AmmGh5M5ZD2pzIcN_YuUllCmcHzUBtzdcSSG572Wy8u0eyFaDG7DwFLNCaBElFHkD5ycwAL_HhxjiqZNYB_nf3so7LUV56zyLpGg3lN8tCXIUxdUlAZbD6yV6PJm3e2b6HoAo-AE6JfquGayuTjViD8To9D3UAWa_v8oQzeLgqg_8cmjyJ27V5DC73JyrFWYIN0gqf22hjWF6Nq1bcxNd2rL62BLcg; eu_cookie={'opted':true,'nonessential':true}; theme=1; __stripe_mid=9690c1d8-57ab-4f8d-a17a-6da2ad4c6bba0dca43; prefers_reduced_motion=false; prefers_reduced_motion_sync=true; is_video_autoplay_disabled=false; pc=a2; t2_hb6i891b_recentclicks3=t3_1n3jimg,t3_1lgsekz,t3_1i9e7k2,t3_1keu46x,t3_m6m6x8; token_v2=eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzY3NDQ0Mzg3Ljc2ODA5MiwiaWF0IjoxNzY3MzU3OTg3Ljc2ODA5MiwianRpIjoiNm9JRWJrZWtGeXNMZTNNdEdTR0RDdFhPUXNjUy13IiwiY2lkIjoiMFItV0FNaHVvby1NeVEiLCJsaWQiOiJ0Ml9oYjZpODkxYiIsImFpZCI6InQyX2hiNmk4OTFiIiwiYXQiOjEsImxjYSI6MTYzODg3MTc0NDAwMCwic2NwIjoiZUp4a2tkR090REFJaGQtRmE1X2dmNVVfbTAxdGNZYXNMUWFvazNuN0RWb2NrNzA3Y0Q0cEhQOURLb3FGRENaWGdxbkFCRmdUclREQlJ1VDluTG0zZzJpTmU4dFlzWm5DQkZtd0ZEcmttTEdzaVFRbWVKSWF5eHNtb0lMTnlGeXV0R05OTFQwUUpxaGNNcmVGSHBjMm9ia2JpNTZkR0ZXNXJEeW9zVmZsMHRqR0ZMWW54amNicXcycHVDNm5Na25MUXZrc1h2VGpOOVczOXZtel9TYTBKOE9LcXVtQjNobEpDRzRzZnBpbTNkOVRrNTZ0Q3hhMTkzcVEydWQ2M0s1OTFpdzBPN2VmNl9sckl4bVhZMmgtSnZ0MzF5LWhBNDg4THpQcUFFYXM0VWNaZG1RZF9sVUhVTG1nSkdNSjR0TUk1TXJsMjM4SnRtdlR2OGJ0RXo5OE0tS21OX3pXRE5SekNlTFFwX0gxR3dBQV9fOFExZVRSIiwicmNpZCI6ImlQcnZtYzBxbXZRcWVmNmMyWTBocGVaaXZLNkR3YkVTRjBETldEVUcyWlEiLCJmbG8iOjJ9.duIiGnXngSfWCP6jweLyOiHDUpDQcM-hga-o9KCWamN0mLI9Ca_QLwLzGOFcI9fIo60pBLaMt0E9Ez3M4AntH4SEo6Az-UWPhY99UZ9J60MUym7n3T3coFcwcstRtisqufaSAXj-qJNeI4ajJ4xEp1ebMMJtKC2hhtdJLNeD2atgvzy_CwlA7_zbZ4S-qVTUUgbvddmja-YhWC_hgfeqxOivhSKtebxNE9wk5JvefVPeIcEX5KXYoTpbmSuGBFCwpzK6QVC5gGCrjIP61VDmMLsJPr4uXheoRlPtQSRgV6-NX1fgyd9FlGklFaukyxk0zDjCvJr2bBKdtdmeLyZ6fQ; csrf_token=84c5a28c75bf16225fd594459432d6ef; reddit_chat_view=closed; devvit_games_drawer_expanded_state=0; session_tracker=qlfmjkqmcdfdnferhr.0.1767383191467.Z0FBQUFBQnBXQ0NYNjUxNUlxNjFhdHVsd0tST3ZzNGVIVUk0azM5bnE1bE5NZEtKdi1HMTlwTW9vV3VEcFpaN0pVMUtmUjVMbHVTblhEMzlkQXFZZHJRTEVtOWx6akRQa3liN2NDcnVnVWhsQkZMMGVoRURGU3VZZUpNYXVWa004ZzlZOEI1Z0x5LUM",
        "Priority": "u=0, i",
        "TE": "trailers",
    }
