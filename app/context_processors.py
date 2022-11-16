# This python script is used to pass values like top tags, top profile directly to .html files that are extended.

from app.models import Profile, Tag
from faker import Faker


def tags_processor(request):
    tags = Tag.objects.get_top_tags()
    tags_values = []
    for i in range(1, 7):
        tags_values.append(Faker().random_int(1, 6))
    return {'tags': tags, 'tags_values': tags_values}


def profiles_processor(request):
    account = Profile.objects.get(nickname='root')
    profiles = Profile.objects.get_top_profiles()
    return {'profiles': profiles, 'account': account}
