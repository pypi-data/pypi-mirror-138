"""
Python package for cowsay.
"""

__version__ = "0.1.1"
__author__ = 'Ovlic'

from .cows import cows
from .lib import balloon
from .lib.faces import getFace
DEFAULT_COLUMNS = 40

def doIt(text, action, **options):
    nowrap = options.get('nowrap')
    wrapWidth = DEFAULT_COLUMNS if not nowrap else (options.get('wrapWidth') if options.get('wrapWidth') else None)
    filledBalloon = balloon.say(text, wrapWidth) if action == "say" else balloon.think(text, wrapWidth)
    cow = options.get('cow') if options.get('cow') else cows.defaultCow
    eyes, tongue = getFace(e=options.get('eyes'), T=options.get('tongue'), cow=cow)
    filledCow = cow(thoughts=('\\' if action == 'say' else 'o'), eyes=eyes, tongue=tongue, eye=eyes[0],)
    return filledBalloon + filledCow


def say(text, **options):
  """
        Make the cow say something.

        Parameters
        ----------
        text: :class:`str`
            Text the cow says.
        eyes: :class:`str`
            Eyes for the cow. Defaults to ``'oo'``.
        tongue: :class:`str`
            Tongue for the cow. Defaults to ``'  '``.
        nowrap: :class:`bool`
            Doesn't wrap text. Defaults to ``False``.
        wrapWidth: :class:`int`
            Wrap text. Defaults to ``40``.
        cow: :class:`cows.Cow`
            Cow to use. Defaults to :class:`cows.defaultCow`.

        Returns
        --------
        :class:`str`
            Cow string."""
  return doIt(text, 'say', **options)


def think(text, **options):
  """
        Make the cow think something.

        Parameters
        ----------
        text: :class:`str`
            Text the cow thinks.
        eyes: :class:`str`
            Eyes for the cow.
        tongue: :class:`str`
            Tongue for the cow.
        nowrap: :class:`bool`
            Doesn't wrap text. Defaults to ``False``.
        wrapWidth: :class:`int`
            Wrap text. Defaults to ``40``.
        cow: :class:`cows.Cow`
            Cow to use. Defaults to :class:`cows.defaultCow`.

        Returns
        --------
        :class:`str`
            Cow string."""
  return doIt(text, 'think', **options)

