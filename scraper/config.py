# URL del perfil de TikTok que deseas scrapear 

TIKTOK_URL = "https://www.tiktok.com/@andrescaluguillin"


# Selectores basados en atributos data-e2e estables de TikTok
SELECTORS = {
    "profile_username": '[data-e2e="user-title"]',
    "profile_followers": '[data-e2e="followers-count"]',
    "profile_likes": '[data-e2e="likes-count"]',
    "video_item": '[data-e2e="user-post-item"]',
    # Selectores alternativos y robustos para el modal/reproductor
    "video_likes": '[data-e2e="like-count"], [data-e2e="browse-like-count"]',
    "video_comments_count": '[data-e2e="comment-count"], [data-e2e="browse-comment-count"]',
    "comment_item": '[data-e2e="comment-level-1"], [data-e2e="comment-item"]',
}