import instaloader

L = instaloader.Instaloader()

profile = instaloader.Profile.from_username(L.context, 'furiagg')

cont = 0

for post in profile.get_posts():
    L.download_post(post, target=profile.username)
    cont+=1
    if cont == 3:
        break