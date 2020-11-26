from django import template

register = template.Library()


@register.simple_tag
def is_liked(vine, profile):
    return profile in vine.likes


@register.simple_tag
def is_disliked(vine, profile):
    return profile in vine.dislikes


@register.simple_tag
def add_like(vine, profile):
    if (vine.is_liked(profile)):

        vine.likes.remove(profile)
    else:

        vine.likes.append(profile)
        if (vine.is_disliked(profile)):

            vine.dislikes.remove(profile)


@register.simple_tag
def add_dislike(vine, profile):
    if (vine.is_disliked(profile)):

        vine.dislikes.remove(profile)
    else:

        vine.dislikes.append(profile)
        if (vine.is_liked(profile)):

            vine.likes.remove(profile)

