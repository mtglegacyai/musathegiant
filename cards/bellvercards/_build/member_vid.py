# -*- coding: utf-8 -*-
"""A team member's own copy of one of MTG's videos (team.json "videos"), for example narrated in their own voice:
their file, thumbnail, length, key moments and transcript replace MTG's on their pages only.
Files live in _build/team_media/<slug>/. On MTG's own pages (no PARTNER) every video stays exactly as it is."""
import bv as _bv

MTG_PERSON = {"@type": "Person", "name": "MTG", "jobTitle": "Your Digital Architect", "url": "https://www.musathegiant.com/"}


def member_video(key, v, moments, transcript, date):
    """(v, moments, transcript, date, own): own is the team.json entry, or None when MTG's video is used."""
    P = _bv.PARTNER
    o = P.get('videos', {}).get(key) if P else None
    if not o:
        return v, moments, transcript, date, None
    url = lambda f: _bv.SITE + _bv.BASE + f
    v = (v[0], v[1], o.get('kind', v[2]), o['duration'], 'mp4', url(o['file']), url(o['poster']), o.get('desc', v[7]), o['iso'])
    return v, [tuple(m) for m in o['moments']], o['transcript'], o.get('date', date), o


def narrator(own):
    return own['narrator'] if own else 'Narrated by MTG with his AI voice.'


def author(own, mtg=None):
    """structured-data author: the member for their own copy, otherwise MTG (or the given MTG reference)"""
    if own:
        return {"@id": _bv.SITE + _bv.BASE + "#partner"}
    return mtg if mtg is not None else dict(MTG_PERSON)


def under(dur):
    """'4:45' -> 5: for captions like "Watch it explained in under 5 minutes" (stays true for a longer own copy)"""
    return int(dur.split(':')[0]) + 1
